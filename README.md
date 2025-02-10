# Cache Simulation Project

This project simulates a set-associative write-through cache for both instruction and data caches. The simulation processes memory trace files and calculates the average memory access time (AMAT) for different cache configurations.

## Project Structure

- `cache.py`: Contains the implementation of the `Cache` class and the `WriteThroughCache` class.
- `main.py`: Contains the driver code to run the cache simulation using different trace files and cache configurations.
- `traces/`: Directory containing the memory trace files (`cc.trace`, `spice.trace`, `tex.trace`).

## Cache Implementation

### Cache Class

The `Cache` class is a parent class that defines the basic structure and functionality of a cache. It includes methods for initializing the cache, calculating set indices and tags, and handling memory access. This class is designed to be extended by specific types of caches.

### WriteThroughCache Class

The `WriteThroughCache` class extends the `Cache` class and implements the specific behavior for a write-through cache. It overrides the `access` and `_write_to_memory` methods.

### Initialization

The cache is initialized with the following parameters:
- `total_size`: The total size of the cache in bytes.
- `block_size`: The size of each cache block in bytes.
- `associativity`: The number of blocks per set (i.e., the degree of set associativity).

### Address Translation

The `_get_set_index_and_tag` method is used to translate a memory address into a set index and a tag.

### Memory Access

The `access` method handles memory accesses. It checks if the address is in the cache (hit) or not (miss). If it's a write access, it writes to memory. It uses the LRU policy to replace blocks on a miss.

## Simulation

The `main.py` script simulates the cache using different trace files and cache configurations. It calculates the number of cache hits, misses, and the average memory access time (AMAT) for both the instruction cache (L1I) and the data cache (L1D).

### Running the Simulation

1. Ensure all files are in the correct directory:
   - `cache.py`
   - `main.py`
   - `traces/cc.trace`
   - `traces/spice.trace`
   - `traces/tex.trace`

2. Open a terminal in Visual Studio Code or use the command prompt.

3. Navigate to the project directory:
   ```sh
   cd "c:/Users/nater/OneDrive/Desktop/comp sci/CS 429/cs429-project1"