class Cache:
    def __init__(self, total_size, block_size, associativity):
        self.total_size = total_size
        self.block_size = block_size
        self.associativity = associativity
        self.num_sets = total_size // (block_size * associativity)
        self.cache = [[{'valid': False, 'tag': None, 'data': None, 'lru': 0, 'dirty': False} for _ in range(associativity)] for _ in range(self.num_sets)]
        self.lru_counter = 0

    def _get_set_index_and_tag(self, address):
        block_offset_bits = self.block_size.bit_length() - 1
        index_bits = self.num_sets.bit_length() - 1
        set_index = (address >> block_offset_bits) & ((1 << index_bits) - 1)
        tag = address >> (block_offset_bits + index_bits)
        return set_index, tag

    def access(self, address, access_type):
        raise NotImplementedError("This method should be overridden by subclasses")

    def _write_to_memory(self, address):
        raise NotImplementedError("This method should be overridden by subclasses")


class WriteThroughCache(Cache):
    def __init__(self, total_size, block_size, associativity):
        super().__init__(total_size, block_size, associativity)

    def access(self, address, access_type):
        set_index, tag = self._get_set_index_and_tag(address)
        cache_set = self.cache[set_index]

        # Check for hit
        for block in cache_set:
            if block['valid'] and block['tag'] == tag:
                if access_type == 1:  # Write access
                    self._write_to_memory(address)
                block['lru'] = self.lru_counter
                self.lru_counter += 1
                return True  # Cache hit

        # Cache miss
        if access_type == 1:  # Write access
            self._write_to_memory(address)

        # Find LRU block to replace
        lru_block = min(cache_set, key=lambda block: block['lru'])
        lru_block['valid'] = True
        lru_block['tag'] = tag
        lru_block['data'] = None  # Assuming data is not needed for this simulation
        lru_block['lru'] = self.lru_counter
        self.lru_counter += 1
        return False  # Cache miss

    def _write_to_memory(self, address):
        # Simulate writing to main memory
        pass


class WriteBackCache(Cache):
    def __init__(self, total_size, block_size, associativity):
        super().__init__(total_size, block_size, associativity)

    def access(self, address, access_type):
        set_index, tag = self._get_set_index_and_tag(address)
        cache_set = self.cache[set_index]

        memory_write = False

        # Check for hit
        for block in cache_set:
            if block['valid'] and block['tag'] == tag:
                if access_type == 1:  # Write access
                    block['dirty'] = True
                block['lru'] = self.lru_counter
                self.lru_counter += 1
                return True, memory_write  # Cache hit

        # Cache miss
        # Find LRU block to replace
        lru_block = min(cache_set, key=lambda block: block['lru'])
        if lru_block['valid'] and lru_block['dirty']:
            memory_write = True

        lru_block['valid'] = True
        lru_block['tag'] = tag
        lru_block['data'] = None  # Assuming data is not needed for this simulation
        lru_block['lru'] = self.lru_counter
        lru_block['dirty'] = (access_type == 1)  # Set dirty bit if it's a write access
        self.lru_counter += 1
        return False, memory_write # Cache miss

    def _write_to_memory(self, address):
        # Simulate writing to main memory
        pass