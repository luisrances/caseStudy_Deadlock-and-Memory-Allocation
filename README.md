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

## Sample Visualizations

### Deadlock Detection and Prevention

#### Banker's Algorithm Visualization
![Banker's Algorithm](images/Banker's%20Algorithm.png)
*Visualization of system state matrices (Allocation, Max Claim, and Need) in Banker's Algorithm. The heatmap shows resource distribution across processes.*

#### Resource Allocation Graph
![Resource Allocation Graph](images/Resource%20Allocation%20Graph.png)
*Resource Allocation Graph showing processes (circles), resources (squares), request edges (dashed red), and allocation edges (solid blue).*

![Resource Allocation Graph - 2](images/Resource%20Allocation%20Graph%20-%202.png)
*Another state of the RAG demonstrating a potential deadlock scenario with circular wait condition.*

### Memory Allocation Strategies

#### First Fit Algorithm
![First Fit](images/memory%20allocation%20-%20first%20fit.png)
*First Fit memory allocation showing memory blocks with allocated (blue) and free (grey) segments.*

![First Fit - 2](images/memory%20allocation%20-%20first%20fit%20-%202.png)
*First Fit algorithm after several allocations and deallocations, showing potential fragmentation.*

#### Best Fit Algorithm
![Best Fit](images/memory%20allocation%20-%20best%20fit.png)
*Best Fit allocation strategy minimizing internal fragmentation by choosing the closest matching free block.*

![Best Fit - 2](images/memory%20allocation%20-%20best%20fit%20-%202.png)
*Best Fit algorithm demonstrating efficient space utilization with multiple processes.*

#### Worst Fit Algorithm
![Worst Fit](images/memory%20allocation%20-%20worst%20fit.png)
*Worst Fit allocation strategy choosing the largest available blocks for allocation.*

![Worst Fit - 2](images/memory%20allocation%20-%20worst%20fit%20-%202.png)
*Worst Fit algorithm showing memory state after multiple allocations.*

### Performance Comparison
![Memory Allocation Comparison](images/memory%20allocation%20-%20comparison%20-%202.png)
*Comparative analysis of all three allocation strategies showing successful allocations, fragmentation percentage, and search times.*

![Memory Allocation Comparison - 2](images/memory%20allocation%20-%20comparisonpng.png)
*Performance metrics comparison under different memory pressure scenarios.*
