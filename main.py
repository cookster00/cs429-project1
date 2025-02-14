from cache import WriteThroughCache, WriteBackCache

def read_trace_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            access_type, address = line.split()
            yield int(access_type), int(address, 16)

def simulate_cache(trace_file, associativity, cache_type):
    # Cache configuration
    total_size = 1024  # Total cache size in bytes
    block_size = 32    # Block size in bytes
    hit_time = 1       # Hit time in cycles
    miss_penalty = 100 # Miss penalty in cycles

    # Initialize the caches
    instruction_cache = cache_type(total_size, block_size, associativity)
    data_cache = cache_type(total_size, block_size, associativity)

    instruction_hits, instruction_misses = 0, 0
    data_hits, data_misses = 0, 0

    # Process the trace file
    for access_type, address in read_trace_file(trace_file):
        if access_type == 2:  # Instruction read
            if instruction_cache.access(address, access_type):
                instruction_hits += 1
            else:
                instruction_misses += 1
        else:  # Data read or write
            if data_cache.access(address, access_type):
                data_hits += 1
            else:
                data_misses += 1

    # Calculate miss rate and AMAT for instruction cache
    total_instruction_accesses = instruction_hits + instruction_misses
    instruction_miss_rate = instruction_misses / total_instruction_accesses
    instruction_amat = hit_time + instruction_miss_rate * miss_penalty

    # Calculate miss rate and AMAT for data cache
    total_data_accesses = data_hits + data_misses
    data_miss_rate = data_misses / total_data_accesses
    data_amat = hit_time + data_miss_rate * miss_penalty

    return (instruction_hits, instruction_misses, instruction_amat), (data_hits, data_misses, data_amat)


def simulate_L1_L2_cache(trace_file, L1_associativity, L2_associativity, cache_type):
    # Function to run Section 6 of the assignment. Creates L1I, L1D, and L2 cache


    # L1 Cache creation
    L1_total_size = 1024  # Total cache size in bytes
    L1_block_size = 32    # Block size in bytes
    L1_hit_time = 1       # Hit time in cycles
    L1_miss_penalty = 100 # Miss penalty in cycles

    instruction_cache = cache_type(L1_total_size, L1_block_size, L1_associativity)
    data_cache = cache_type(L1_total_size, L1_block_size, L1_associativity)

    instruction_hits, instruction_misses = 0, 0
    data_hits, data_misses = 0, 0




    # L2 Cache creation
    L2_total_size = 16384
    L2_block_size = 128
    L2_hit_time = 10      # Hit time in cycles
    L2_miss_penalty = 100 # Miss penalty in cycles


    L2_cache = cache_type(L2_total_size, L2_block_size, L2_associativity)

    L2_hits, L2_misses = 0, 0

    # Process the trace file
    # If either L1 misses, check L2 for data
    for access_type, address in read_trace_file(trace_file):
        if access_type == 2:  # Instruction read
            if instruction_cache.access(address, access_type):
                instruction_hits += 1
            else:
                instruction_misses += 1
                if L2_cache.access(address, access_type):
                    L2_hits += 1
                else:
                    L2_misses += 1
        else:  # Data read or write
            if data_cache.access(address, access_type):
                data_hits += 1
            else:
                data_misses += 1
                if L2_cache.access(address, access_type):
                    L2_hits += 1
                else:
                    L2_misses += 1

    # Calculate miss rate and AMAT for instruction cache
    total_instruction_accesses = instruction_hits + instruction_misses
    instruction_miss_rate = instruction_misses / total_instruction_accesses
    instruction_amat = L1_hit_time + instruction_miss_rate * L1_miss_penalty

    # Calculate miss rate and AMAT for data cache
    total_data_accesses = data_hits + data_misses
    data_miss_rate = data_misses / total_data_accesses
    data_amat = L1_hit_time + data_miss_rate * L1_miss_penalty

    # Calculate miss rate and AMAT for L2 cache
    total_L2_accesses = L2_hits + L2_misses
    L2_miss_rate = L2_misses / total_L2_accesses
    L2_amat = L2_hit_time + L2_miss_rate * L2_miss_penalty

    return (instruction_hits, instruction_misses, instruction_amat), (data_hits, data_misses, data_amat), (L2_hits, L2_misses, L2_amat)

def main():
    trace_files = ['traces/cc.trace', 'traces/spice.trace', 'traces/tex.trace']
    associativities = [1, 2, 4, 8, 16, 32]

    for trace_file in trace_files:
        print(f"Processing {trace_file} with Write-Through Cache...")
        for associativity in associativities:
            (instruction_hits, instruction_misses, instruction_amat), (data_hits, data_misses, data_amat) = simulate_cache(trace_file, associativity, WriteThroughCache)
            print(f"Associativity: {associativity}")
            print(f"  Instruction Cache - Hits: {instruction_hits}, Misses: {instruction_misses}, AMAT: {instruction_amat:.2f} cycles")
            print(f"  Data Cache - Hits: {data_hits}, Misses: {data_misses}, AMAT: {data_amat:.2f} cycles")
    '''
    for trace_file in trace_files:
        print(f"Processing {trace_file} with Write-Back Cache...")
        for associativity in associativities:
            (instruction_hits, instruction_misses, instruction_amat), (data_hits, data_misses, data_amat) = simulate_cache(trace_file, associativity, WriteBackCache)
            print(f"Associativity: {associativity}")
            print(f"  Instruction Cache - Hits: {instruction_hits}, Misses: {instruction_misses}, AMAT: {instruction_amat:.2f} cycles")
            print(f"  Data Cache - Hits: {data_hits}, Misses: {data_misses}, AMAT: {data_amat:.2f} cycles")

    for trace_file in trace_files:
        print(f"Processing {trace_file} with Write-Back & L2 Cache...")
        for associativity in associativities:
            (instruction_hits, instruction_misses, instruction_amat), (data_hits, data_misses, data_amat), (L2_hits, L2_misses, L2_amat) = simulate_L1_L2_cache(trace_file, 2, associativity, WriteBackCache)
            print(f"L2 Associativity: {associativity}")
            print(f"  Instruction Cache - Hits: {instruction_hits}, Misses: {instruction_misses}, AMAT: {instruction_amat:.2f} cycles")
            print(f"  Data Cache - Hits: {data_hits}, Misses: {data_misses}, AMAT: {data_amat:.2f} cycles")
            print(f"  L2 Cache - Hits: {L2_hits}, Misses: {L2_misses}, AMAT: {L2_amat:.2f} cycles")
    '''
if __name__ == "__main__":
    main()