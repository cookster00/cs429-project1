from cache import WriteThroughCache, WriteBackCache

def read_trace_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            access_type, address = line.split()
            yield int(access_type), int(address, 16)

def simulate_write_through(trace_file, associativity, cache_type):
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
        elif access_type == 0:  # Data read
            if data_cache.access(address, access_type):
                data_hits += 1
            else:
                data_misses += 1
        else: # Data write
            data_cache.access(address, access_type)
            data_misses += 1


    # Calculate miss rate and AMAT for instruction cache
    total_instruction_accesses = instruction_hits + instruction_misses
    instruction_miss_rate = instruction_misses / total_instruction_accesses
    instruction_hit_rate = instruction_hits / total_instruction_accesses

    # Calculate miss rate and AMAT for data cache
    total_data_accesses = data_hits + data_misses
    data_miss_rate = data_misses / total_data_accesses
    data_hit_rate = data_hits / total_data_accesses

    # Calculate AMAT for instruction and data caches
    instruction_amat = hit_time + instruction_miss_rate * miss_penalty
    data_amat = hit_time + data_miss_rate * miss_penalty

    # Calculate combined AMAT
    total_accesses = total_instruction_accesses + total_data_accesses
    total_time = (instruction_hits + instruction_misses) * instruction_amat + (data_hits + data_misses) * data_amat
    combined_amat = total_time / total_accesses

    return (total_instruction_accesses, instruction_misses, instruction_hit_rate), (total_data_accesses, data_misses, data_hit_rate), combined_amat

def simulate_write_back(trace_file, associativity, cache_type):
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
            access, write_back = instruction_cache.access(address, access_type)
            if access:
                instruction_hits += 1
            else:
                instruction_misses += 1
        else:  # Data read or write
            access, write_back = data_cache.access(address, access_type)
            if access and not write_back:
                data_hits += 1
            else:
                data_misses += 1

    # Calculate miss rate and AMAT for instruction cache
    total_instruction_accesses = instruction_hits + instruction_misses
    instruction_miss_rate = instruction_misses / total_instruction_accesses
    instruction_hit_rate = instruction_hits / total_instruction_accesses

    # Calculate miss rate and AMAT for data cache
    total_data_accesses = data_hits + data_misses
    data_miss_rate = data_misses / total_data_accesses
    data_hit_rate = data_hits / total_data_accesses

    # Calculate AMAT for instruction and data caches
    instruction_amat = hit_time + instruction_miss_rate * miss_penalty
    data_amat = hit_time + data_miss_rate * miss_penalty

    # Calculate combined AMAT
    total_accesses = total_instruction_accesses + total_data_accesses
    total_time = (instruction_hits + instruction_misses) * instruction_amat + (data_hits + data_misses) * data_amat
    combined_amat = total_time / total_accesses

    return (total_instruction_accesses, instruction_misses, instruction_hit_rate), (total_data_accesses, data_misses, data_hit_rate), combined_amat

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
            access, memory_write = instruction_cache.access(address, access_type)
            if access and not memory_write:
                instruction_hits += 1
            else:
                instruction_misses += 1
                L2_access, L2_memory_write = L2_cache.access(address, access_type)
                if L2_access and not L2_memory_write:
                    L2_hits += 1
                else:
                    L2_misses += 1
        else:  # Data read or write
            access, write_back = data_cache.access(address, access_type)
            if access and not write_back:
                data_hits += 1
            else:
                data_misses += 1
                L2_access, L2_write_back = L2_cache.access(address, access_type)
                if L2_access and not L2_write_back:
                    L2_hits += 1
                else:
                    L2_misses += 1

    # Calculate miss rate and hit rate for instruction cache
    total_instruction_accesses = instruction_hits + instruction_misses
    instruction_miss_rate = instruction_misses / total_instruction_accesses
    instruction_hit_rate = instruction_hits / total_instruction_accesses

    # Calculate miss rate and hit rate for data cache
    total_data_accesses = data_hits + data_misses
    data_miss_rate = data_misses / total_data_accesses
    data_hit_rate = data_hits / total_data_accesses


    # Calculate miss rate and hit rate for L2 cache
    total_L2_accesses = L2_hits + L2_misses
    L2_miss_rate = L2_misses / total_L2_accesses
    L2_hit_rate = L2_hits / total_L2_accesses

    # Calculate AMAT for L1 instruction and data caches
    L1_instruction_amat = L1_hit_time + instruction_miss_rate * (L2_hit_time + L2_miss_rate * L2_miss_penalty)
    L1_data_amat = L1_hit_time + data_miss_rate * (L2_hit_time + L2_miss_rate * L2_miss_penalty)

    # Calculate combined AMAT
    total_accesses = total_instruction_accesses + total_data_accesses
    total_amat = (total_instruction_accesses * L1_instruction_amat + total_data_accesses * L1_data_amat) / total_accesses


    return (instruction_hit_rate, instruction_misses, total_instruction_accesses), (data_hit_rate, data_misses, total_data_accesses), (L2_hit_rate, L2_misses, total_L2_accesses), total_amat

def main():
    trace_files = ['traces/cc.trace'] # Optional traces: , 'traces/spice.trace', 'traces/tex.trace']
    associativities = [1, 4, 8, 16, 32, 64, 128]
    '''
    for trace_file in trace_files:
        print(f"Processing {trace_file} with Write-Through Cache...")
        for associativity in associativities:
            (total_instruction_accesses, instruction_misses, instruction_hit_rate), (total_data_accesses, data_misses, data_hit_rate), combined_amat = simulate_write_through(trace_file, associativity, WriteThroughCache)
            print(f"Associativity: {associativity}")
            print(f"  Instruction Cache - Hit rate: {instruction_hit_rate:.3f}, Misses: {instruction_misses}, Total Accesses: {total_instruction_accesses} cycles")
            print(f"  Data Cache - Hit rate: {data_hit_rate:.3f}, Misses: {data_misses}, Total accesses: {total_data_accesses}")
            print(f"  Combined AMAT: {combined_amat:.2f} cycles")
    
    for trace_file in trace_files:
        print(f"Processing {trace_file} with Write-Back Cache...")
        for associativity in associativities:
            (total_instruction_accesses, instruction_misses, instruction_hit_rate), (total_data_accesses, data_misses, data_hit_rate), combined_amat = simulate_write_back(trace_file, associativity, WriteBackCache)
            print(f"Associativity: {associativity}")
            print(f"  Instruction Cache - Hit rate: {instruction_hit_rate:.3f}, Misses: {instruction_misses}, Total Accesses: {total_instruction_accesses} cycles")
            print(f"  Data Cache - Hit rate: {data_hit_rate:.3f}, Misses: {data_misses}, Total accesses: {total_data_accesses}")
            print(f"  Combined AMAT: {combined_amat:.2f} cycles")
    
    '''
    for trace_file in trace_files:
        print(f"Processing {trace_file} with Write-Back & L2 Cache...")
        for associativity in associativities:
            (instruction_hit_rate, instruction_misses, total_instruction_accesses), (data_hit_rate, data_misses, total_data_accesses), (L2_hit_rate, L2_misses, total_L2_accesses), total_amat = simulate_L1_L2_cache(trace_file, 2, associativity, WriteBackCache)
            print(f"L2 Associativity: {associativity}")
            print(f"  Instruction Cache - Hit rate: {instruction_hit_rate:.3f}, Misses: {instruction_misses}, Total Accesses: {total_instruction_accesses} ")
            print(f"  Data Cache - Hit rate: {data_hit_rate:.3f}, Misses: {data_misses}, Total accesses: {total_data_accesses}")
            print(f"  L2 Cache - Hits: {L2_hit_rate:.3f}, Misses: {L2_misses}, Total accesses: {total_L2_accesses} ")
            print(f"  Combined AMAT: {total_amat:.2f} cycles")
    

if __name__ == "__main__":
    main()