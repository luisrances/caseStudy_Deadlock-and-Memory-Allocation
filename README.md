# Simulating and Analyzing Deadlock and Memory Allocation Strategies in Operating Systems

  This project attempts the simulation of deadlock scenarios and evaluating allocation strategies, mainly First fit, Best fit, and Worst fit, and analyzing and charting each individual efficiency and impact on fragmentation and system safe.

# Members:
    Bensing, Denmark
    Deocampo, Arden Klyde
    Mellomida, Jhondel
    Ocariza, James Andrew
    Rances, Francis Luis

## Project Structure

- `deadlock_simulation.py`: Core implementation of deadlock-related algorithms
  - Banker's Algorithm for deadlock avoidance
  - Resource Allocation Graph (RAG) for deadlock detection
  - Visualization utilities for both algorithms

- `memory_allocation.py`: Implementation of memory allocation strategies
  - First Fit allocator
  - Best Fit allocator
  - Worst Fit allocator
  - Memory block management and visualization

- `usage_bankers_algorithm.py`: Demonstration of Banker's Algorithm
  - Example setup with 5 processes and 4 resource types
  - Safe state verification
  - Resource request handling

- `usage_memory_allocation.py`: Comprehensive memory allocation comparison
  - Performance comparison of all three allocation strategies
  - Realistic workload simulation
  - Visualization of allocation results
  - Comparative analysis under normal and high-pressure scenarios

- `usage_resource_allocation_graph.py`: RAG demonstration
  - Example with 5 processes and 4 resources
  - Deadlock detection
  - Visualization of resource allocation state
  - Deadlock resolution example

## Getting Started

### Prerequisites
```python
pip install numpy matplotlib networkx pytest
