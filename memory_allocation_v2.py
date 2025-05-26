import matplotlib.pyplot as plt
import numpy as np
import time
import random

def generate_realistic_sample(num_blocks=5, num_processes=4):
    # Simulate memory blocks between 128MB to 1024MB
    memory_blocks = sorted([random.randint(128, 1024) for _ in range(num_blocks)], reverse=True)

    # Simulate processes with memory needs between 100MB to 800MB
    processes = sorted([random.randint(100, 800) for _ in range(num_processes)], reverse=True)

    print("# === Randomly Generated Sample ===")
    print("memory_blocks =", memory_blocks)
    print("processes =", processes)

    return memory_blocks, processes

def log_allocation_result(strategy, processes, allocation, block_history):
    print(f"\n=== Testing {strategy} Algorithm ===")
    for i, block_index in enumerate(allocation):
        if block_index == -1:
            print(f"Failed to allocate {processes[i]} units to process P{i + 1}")
        else:
            print(f"Successfully allocated {processes[i]} units to process P{i + 1} -> Block {block_index + 1}")
    print("\nFree blocks per iteration:")
    for i, blocks in enumerate(block_history):
        print(f"Iteration {i+1}: {blocks}")

def allocate_with_tracking(strategy_name, blocks, processes, allocation_func, repetitions=1000000):
    import copy

    total_duration = 0
    for _ in range(repetitions):
        blocks_copy = blocks.copy()
        start_time = time.perf_counter()
        for process in processes:
            _, blocks_copy = allocation_func(blocks_copy, process)
        end_time = time.perf_counter()
        total_duration += (end_time - start_time)

    avg_duration = total_duration / repetitions

    # Perform actual allocation once to get real allocation & tracking data
    allocation = [-1] * len(processes)
    block_states = []
    blocks_copy = blocks.copy()

    for i, process in enumerate(processes):
        result = allocation_func(blocks_copy, process)
        allocation[i] = result[0]
        blocks_copy = result[1]
        block_states.append(blocks_copy.copy())

    log_allocation_result(strategy_name, processes, allocation, block_states)
    return allocation, block_states, avg_duration


def first_fit(blocks, process):
    for j, block in enumerate(blocks):
        if block >= process:
            blocks[j] -= process
            return j, blocks
    return -1, blocks

def best_fit(blocks, process):
    best_index = -1
    for j, block in enumerate(blocks):
        if block >= process:
            if best_index == -1 or blocks[j] < blocks[best_index]:
                best_index = j
    if best_index != -1:
        blocks[best_index] -= process
        return best_index, blocks
    return -1, blocks

def worst_fit(blocks, process):
    worst_index = -1
    for j, block in enumerate(blocks):
        if block >= process:
            if worst_index == -1 or blocks[j] > blocks[worst_index]:
                worst_index = j
    if worst_index != -1:
        blocks[worst_index] -= process
        return worst_index, blocks
    return -1, blocks

def visualize_allocation_chart(title, processes, allocations):
    fig, ax = plt.subplots()
    colors = ['green' if a != -1 else 'red' for a in allocations]
    labels = [f"P{i+1}" for i in range(len(processes))]
    ax.bar(labels, processes, color=colors)
    ax.set_title(title)
    ax.set_ylabel("Memory Requested")
    for i, val in enumerate(processes):
        label = "OK" if allocations[i] != -1 else "Fail"
        ax.text(i, val + 5, label, ha='center')
    plt.show()

def visualize_fragmentation_chart(strategy, memory_blocks, block_states):
    remaining = [sum(state) for state in block_states]
    plt.plot(range(1, len(block_states)+1), remaining, marker='o', label=strategy)
    plt.xlabel("Process Iteration")
    plt.ylabel("Remaining Free Memory")
    plt.title("Memory Fragmentation over Time")
    plt.legend()

def visualize_time_efficiency(times):
    strategies = list(times.keys())
    durations = list(times.values())

    # Prevent division by zero
    efficiencies = [1 / t if t > 0 else 0 for t in durations]

    plt.bar(strategies, efficiencies, color='mediumseagreen')
    plt.ylabel("Time Efficiency (1 / seconds)")
    plt.title("Time Efficiency of Allocation Strategies")
    if any(efficiencies):
        plt.ylim(0, max(efficiencies) * 1.2)
    else:
        plt.ylim(0, 1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def summarize_visualization(processes, allocations_dict, block_states_dict, search_times):
    strategies = list(allocations_dict.keys())
    
    successful_allocations = [sum(1 for a in allocations_dict[s] if a != -1) for s in strategies]
    fragmentation = [
        (sum(block_states_dict[s][-1]) / sum(memory_blocks)) * 100 if block_states_dict[s] else 0
        for s in strategies
    ]
    search_ms = [search_times[s] * 1000 for s in strategies]  # convert seconds to milliseconds

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Subplot 1: Successful Allocations
    axs[0].bar(strategies, successful_allocations, color='green')
    axs[0].set_title("Successful Process Allocations")
    axs[0].set_ylabel("Number of Processes")
    for i, val in enumerate(successful_allocations):
        axs[0].text(i, val + 0.2, str(val), ha='center')

    # Subplot 2: Fragmentation
    axs[1].bar(strategies, fragmentation, color='orange')
    axs[1].set_title("Memory Fragmentation")
    axs[1].set_ylabel("Fragmentation (%)")
    for i, val in enumerate(fragmentation):
        axs[1].text(i, val + 0.2, f"{val:.2f}", ha='center')

    # Subplot 3: Time Efficiency
    axs[2].bar(strategies, search_ms, color='skyblue')
    axs[2].set_title("Average Search Time")
    axs[2].set_ylabel("Time (milliseconds)")
    for i, val in enumerate(search_ms):
        axs[2].text(i, val + 0.1, f"{val:.2f}", ha='center')

    for ax in axs:
        ax.set_xticks(range(len(strategies)))
        ax.set_xticklabels(strategies, rotation=15)

    plt.tight_layout()
    plt.show()


def compare_algorithms(memory_blocks, processes):
    print("Memory Blocks:", memory_blocks)
    print("Processes:", processes)

    search_times = {}

    # First Fit
    allocation1, states1, time1 = allocate_with_tracking("First Fit", memory_blocks.copy(), processes, first_fit)
    visualize_allocation_chart("First Fit Allocation", processes, allocation1)
    visualize_fragmentation_chart("First Fit", memory_blocks, states1)
    search_times["First Fit"] = time1

    # Best Fit
    allocation2, states2, time2 = allocate_with_tracking("Best Fit", memory_blocks.copy(), processes, best_fit)
    visualize_allocation_chart("Best Fit Allocation", processes, allocation2)
    visualize_fragmentation_chart("Best Fit", memory_blocks, states2)
    search_times["Best Fit"] = time2

    # Worst Fit
    allocation3, states3, time3 = allocate_with_tracking("Worst Fit", memory_blocks.copy(), processes, worst_fit)
    visualize_allocation_chart("Worst Fit Allocation", processes, allocation3)
    visualize_fragmentation_chart("Worst Fit", memory_blocks, states3)
    search_times["Worst Fit"] = time3

    # Show fragmentation chart
    plt.tight_layout()
    plt.show()

    # Show time efficiency
    visualize_time_efficiency(search_times)
    print(search_times)

    allocations = {
        "First Fit": allocation1,
        "Best Fit": allocation2,
        "Worst Fit": allocation3
    }

    block_states = {
        "First Fit": states1,
        "Best Fit": states2,
        "Worst Fit": states3
    }

    summarize_visualization(processes, allocations, block_states, search_times)

# Sample usage
# memory_blocks = [100, 500, 200, 300, 600]
# processes = [212, 417, 112, 426]
memory_blocks, processes = generate_realistic_sample() # Generate realistic sample data

compare_algorithms(memory_blocks, processes)
