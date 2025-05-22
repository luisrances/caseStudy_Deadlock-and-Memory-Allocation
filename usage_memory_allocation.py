from memory_allocation import FirstFitAllocator, BestFitAllocator, WorstFitAllocator
import matplotlib.pyplot as plt
import numpy as np

def compare_algorithms(memory_size: int, processes: list):
    """Compare all three memory allocation algorithms"""
    # Initialize allocators
    allocators = {
        'First Fit': FirstFitAllocator(memory_size),
        'Best Fit': BestFitAllocator(memory_size),
        'Worst Fit': WorstFitAllocator(memory_size)
    }
    
    results = {}
    
    # Test each algorithm
    for name, allocator in allocators.items():
        print(f"\n=== Testing {name} Algorithm ===")
        successful_allocations = 0
        
        # Allocate each process
        for pid, size in processes:
            if allocator.allocate(pid, size):
                successful_allocations += 1
                print(f"Successfully allocated {size} units to process {pid}")
            else:
                print(f"Failed to allocate {size} units to process {pid}")
        
        # Get statistics
        stats = allocator.get_statistics()
        results[name] = {
            'successful_allocations': successful_allocations,
            'fragmentation': stats['current_fragmentation'],
            'search_times': np.mean(stats['search_time_history'])
        }
        
        # Visualize current state
        print(f"\nMemory state after {name} allocation:")
        allocator.visualize_memory()

    return results

def plot_comparison(results: dict):
    """Plot comparison of algorithm performance with enhanced visualization"""
    metrics = {
        'successful_allocations': {
            'title': 'Successful Process Allocations',
            'ylabel': 'Number of Processes',
            'color': 'green',
            'fmt': 'd'  # Format as integer
        },
        'fragmentation': {
            'title': 'Memory Fragmentation',
            'ylabel': 'Fragmentation (%)',
            'color': 'orange',
            'fmt': '.1f'  # Format with 1 decimal place
        },
        'search_times': {
            'title': 'Average Search Time',
            'ylabel': 'Time (milliseconds)',
            'color': 'blue',
            'fmt': '.2f'  # Format with 2 decimal places
        }
    }
    
    algorithms = list(results.keys())
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Memory Allocation Algorithm Comparison', fontsize=16, y=1.05)
    
    # Plot each metric
    for i, (metric, config) in enumerate(metrics.items()):
        ax = axes[i]
        values = [results[algo][metric] for algo in algorithms]
        
        # Convert search times to milliseconds
        if metric == 'search_times':
            values = [v * 1000 for v in values]
        
        # Create bars
        bars = ax.bar(algorithms, values, color=config['color'], alpha=0.7)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:{config["fmt"]}}',
                   ha='center', va='bottom')
        
        # Customize subplot
        ax.set_title(config['title'], pad=20)
        ax.set_ylabel(config['ylabel'])
        ax.tick_params(axis='x', rotation=30)
        ax.grid(True, linestyle='--', alpha=0.7, axis='y')
        
        # Add border to subplot
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(0.5)
    
    # Adjust layout
    plt.tight_layout()
    
    # Add explanatory text
    fig.text(0.05, -0.05, 
             'Notes:\n'
             '• Successful Allocations: Higher is better\n'
             '• Fragmentation: Lower percentage is better\n'
             '• Search Time: Lower is better\n',
             ha='left', va='top', fontsize=10)
    
    plt.show()

# Rest of the code remains the same...
def simulate_realistic_workload(time_steps: int, base_memory_size: int):
    """Simulate a realistic workload with varying process sizes and lifetimes"""
    import random
    
    processes = []
    active_processes = set()
    current_pid = 1
    
    for step in range(time_steps):
        # Simulate process termination
        if active_processes and random.random() < 0.3:  # 30% chance to terminate a process
            processes_to_remove = random.sample(list(active_processes), 
                                             k=min(2, len(active_processes)))
            for pid in processes_to_remove:
                processes.append((f'D{pid}', 0))  # Deallocation marker
                active_processes.remove(pid)
        
        # Simulate new process creation with varying patterns
        if random.random() < 0.4:  # 40% chance to create new processes
            num_new_processes = random.randint(1, 3)
            for _ in range(num_new_processes):
                # Simulate different types of processes
                process_type = random.choice(['S', 'M', 'L', 'XL'])
                if process_type == 'S':
                    size = random.randint(10, 50)
                elif process_type == 'M':
                    size = random.randint(51, 150)
                elif process_type == 'L':
                    size = random.randint(151, 300)
                else:
                    size = random.randint(301, 400)
                
                processes.append((f'P{current_pid}', size))
                active_processes.add(current_pid)
                current_pid += 1
    
    return processes

def main():
    # Larger memory size with more complex scenarios
    MEMORY_SIZE = 2000
    TIME_STEPS = 30
    
    # Generate realistic workload
    processes = simulate_realistic_workload(TIME_STEPS, MEMORY_SIZE)
    
    print(f"Memory size: {MEMORY_SIZE} units")
    print(f"Total time steps: {TIME_STEPS}")
    print(f"Total process operations: {len(processes)}")
    
    # Group processes by type (allocation vs deallocation)
    allocations = [(pid, size) for pid, size in processes if not pid.startswith('D')]
    deallocations = [pid[1:] for pid, _ in processes if pid.startswith('D')]
    
    print("\nWorkload Statistics:")
    print(f"Total allocations: {len(allocations)}")
    print(f"Total deallocations: {len(deallocations)}")
    print(f"Average process size: {sum(size for _, size in allocations) / len(allocations):.2f}")
    
    # Create memory pressure scenarios
    high_pressure_processes = [(pid, size * 1.2) for pid, size in allocations]
    results_normal = compare_algorithms(MEMORY_SIZE, processes)
    results_pressure = compare_algorithms(MEMORY_SIZE, high_pressure_processes)
    
    # Plot comparisons
    print("\n=== Normal Workload ===")
    plot_comparison(results_normal)
    
    print("\n=== High Pressure Workload ===")
    plot_comparison(results_pressure)
    
    # Detailed analysis
    print("\n=== Comparative Analysis ===")
    for algorithm in results_normal.keys():
        print(f"\n{algorithm} Performance Impact:")
        for metric in results_normal[algorithm].keys():
            normal_value = results_normal[algorithm][metric]
            pressure_value = results_pressure[algorithm][metric]
            
            # Handle division by zero case
            if normal_value != 0:
                percentage_change = ((pressure_value - normal_value) / normal_value) * 100
                change_str = f"Change: {percentage_change:+.2f}%"
            else:
                change_str = "Change: N/A (baseline was 0)"
            
            if metric == 'search_times':
                print(f"  {metric}: {normal_value*1000:.2f}ms → {pressure_value*1000:.2f}ms")
                print(f"    {change_str}")
            else:
                print(f"  {metric}: {normal_value:.2f} → {pressure_value:.2f}")
                print(f"    {change_str}")

if __name__ == "__main__":
    main()