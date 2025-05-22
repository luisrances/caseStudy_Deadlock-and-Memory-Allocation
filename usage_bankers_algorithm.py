from deadlock_simulation import BankersAlgorithm

def main():
    # Create banker's algorithm instance with 5 processes and 4 resource types
    banker = BankersAlgorithm(5, 4)

    # Set initial available resources (R1=10, R2=7, R3=8, R4=5)
    banker.set_available([10, 7, 8, 5])

    # Set maximum resource claims for each process
    max_claims = [
        [5, 4, 3, 1],  # P0's maximum claims
        [4, 3, 2, 2],  # P1's maximum claims
        [7, 2, 4, 3],  # P2's maximum claims
        [3, 3, 3, 2],  # P3's maximum claims
        [6, 4, 2, 2]   # P4's maximum claims
    ]
    banker.set_max_claim(max_claims)

    # Set initial resource allocations
    allocations = [
        [1, 1, 0, 0],  # P0's current allocation
        [2, 0, 1, 1],  # P1's current allocation
        [0, 1, 2, 0],  # P2's current allocation
        [1, 0, 1, 0],  # P3's current allocation
        [0, 2, 0, 1]   # P4's current allocation
    ]
    banker.set_allocation(allocations)

    # Print initial state
    print("\n=== Initial System State ===")
    print(banker.system_state_summary())

    # Check if initial state is safe
    print("\n=== Safety Check for Initial State ===")
    initial_safety = banker.is_safe()
    print(f"Initial state is {'safe' if initial_safety else 'unsafe'}\n")

    # Try some resource requests
    test_requests = [
        (0, [2, 0, 1, 0]),  # P0 requests additional resources
        (2, [3, 0, 1, 2]),  # P2 requests additional resources
        (4, [4, 1, 0, 0])   # P4 requests additional resources
    ]

    print("=== Testing Resource Requests ===")
    for process_id, request in test_requests:
        print(f"\nProcess {process_id} requesting resources: {request}")
        success = banker.request_resources(process_id, request)
        if success:
            print(f"Request for Process {process_id} was granted")
            print("\nUpdated system state:")
            print(banker.system_state_summary())
        else:
            print(f"Request for Process {process_id} was denied")

    # Visualize final state
    print("\n=== Visualizing Final System State ===")
    banker.visualize_state()

if __name__ == "__main__":
    main()