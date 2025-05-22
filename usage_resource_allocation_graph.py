from deadlock_simulation import ResourceAllocationGraph

def main():
    # Create a new Resource Allocation Graph
    rag = ResourceAllocationGraph()

    # Add processes (P1 through P5)
    processes = [f"P{i}" for i in range(1, 6)]
    for p in processes:
        rag.add_process(p)

    # Add resources with different instances
    resources = {
        "R1": 2,  # Resource 1 with 2 instances
        "R2": 1,  # Resource 2 with 1 instance
        "R3": 3,  # Resource 3 with 3 instances
        "R4": 1   # Resource 4 with 1 instance
    }
    
    for resource, instances in resources.items():
        rag.add_resource(resource, instances)

    print("=== Initial System Setup ===")
    print("Processes:", sorted(list(rag.processes)))
    print("Resources:", {r: rag.resource_instances[r] for r in sorted(rag.resources)})

    # Create initial resource allocations
    print("\n=== Creating Initial Allocations ===")
    allocations = [
        ("R1", "P1"),  # R1 allocated to P1
        ("R2", "P2"),  # R2 allocated to P2
        ("R3", "P3"),  # R3 allocated to P3
        ("R4", "P4"),  # R4 allocated to P4
    ]
    
    for resource, process in allocations:
        print(f"Allocating {resource} to {process}")
        rag.allocation_edge(resource, process)

    # Create resource requests
    print("\n=== Creating Resource Requests ===")
    requests = [
        ("P1", "R2"),  # P1 requests R2
        ("P2", "R3"),  # P2 requests R3
        ("P3", "R4"),  # P3 requests R4
        ("P4", "R1"),  # P4 requests R1
        ("P5", "R1"),  # P5 requests R1
    ]
    
    for process, resource in requests:
        print(f"{process} requesting {resource}")
        rag.request_edge(process, resource)

    # Check for deadlocks
    print("\n=== Checking for Deadlocks ===")
    has_deadlock, cycles = rag.detect_deadlock()
    
    if has_deadlock:
        print("Deadlock detected!")
        print("Deadlock cycles found:")
        for cycle in cycles:
            print(" → ".join(cycle + [cycle[0]]))
    else:
        print("No deadlock detected")

    # Visualize the current state
    print("\n=== Visualizing Current State ===")
    rag.visualize()

    # Demonstrate deadlock resolution
    print("\n=== Demonstrating Deadlock Resolution ===")
    print("Removing P4's request for R1")
    rag.remove_request_edge("P4", "R1")
    
    # Check for deadlocks again
    has_deadlock, cycles = rag.detect_deadlock()
    
    if has_deadlock:
        print("Deadlock still exists!")
        print("Remaining deadlock cycles:")
        for cycle in cycles:
            print(" → ".join(cycle + [cycle[0]]))
    else:
        print("Deadlock resolved!")

    # Visualize the final state
    print("\n=== Visualizing Final State ===")
    rag.visualize()

if __name__ == "__main__":
    main()