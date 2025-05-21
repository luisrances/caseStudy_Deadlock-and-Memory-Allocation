#!/usr/bin/env python3
"""
Deadlock Simulation: Banker's Algorithm and Resource Allocation Graph
"""
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Tuple, Dict, Set

class BankersAlgorithm:
    """Implementation of Banker's Algorithm for deadlock avoidance"""
    
    def __init__(self, processes: int, resources: int):
        """
        Initialize Banker's Algorithm with number of processes and resources
        
        Args:
            processes: Number of processes
            resources: Number of resource types
        """
        self.n_processes = processes
        self.n_resources = resources
        
        # Initialize matrices
        self.available = np.zeros(resources, dtype=int)  # Available resources
        self.max_claim = np.zeros((processes, resources), dtype=int)  # Maximum resources each process may request
        self.allocation = np.zeros((processes, resources), dtype=int)  # Currently allocated resources
        self.need = np.zeros((processes, resources), dtype=int)  # Need = Max - Allocation
    
    def set_available(self, available: List[int]) -> None:
        """Set available resources"""
        self.available = np.array(available)
    
    def set_max_claim(self, max_claim: List[List[int]]) -> None:
        """Set maximum resource claims for each process"""
        self.max_claim = np.array(max_claim)
        self._update_need()
    
    def set_allocation(self, allocation: List[List[int]]) -> None:
        """Set current resource allocation for each process"""
        self.allocation = np.array(allocation)
        self._update_need()
    
    def _update_need(self) -> None:
        """Update need matrix based on max claim and allocation"""
        self.need = self.max_claim - self.allocation
    
    def request_resources(self, process_id: int, request: List[int]) -> bool:
        """
        Process resource request using Banker's Algorithm
        
        Args:
            process_id: ID of process making the request
            request: List of resources being requested
            
        Returns:
            bool: True if request can be granted safely, False otherwise
        """
        request = np.array(request)
        
        # Check if request exceeds need
        if np.any(request > self.need[process_id]):
            print(f"Error: Process {process_id} is requesting more than its need")
            return False
        
        # Check if request exceeds available
        if np.any(request > self.available):
            print(f"Process {process_id} must wait, resources not available")
            return False
        
        # Try to allocate resources and check if system remains in safe state
        self._temporarily_allocate(process_id, request)
        
        if self.is_safe():
            # Allocation is safe, commit changes
            return True
        else:
            # Allocation is not safe, rollback changes
            self._rollback_allocation(process_id, request)
            print(f"Request denied: granting would lead to unsafe state")
            return False
    
    def _temporarily_allocate(self, process_id: int, request: List[int]) -> None:
        """Temporarily allocate resources to check safety"""
        self.available -= request
        self.allocation[process_id] += request
        self.need[process_id] -= request
    
    def _rollback_allocation(self, process_id: int, request: List[int]) -> None:
        """Rollback temporary allocation"""
        self.available += request
        self.allocation[process_id] -= request
        self.need[process_id] += request
    
    def is_safe(self) -> bool:
        """
        Check if system is in safe state using Banker's Algorithm
        
        Returns:
            bool: True if system is in safe state, False if deadlock may occur
        """
        # Create working copies
        work = self.available.copy()
        finish = np.zeros(self.n_processes, dtype=bool)
        
        # Find an unfinished process that can be allocated all needed resources
        found = True
        safe_sequence = []
        
        while found:
            found = False
            for i in range(self.n_processes):
                if not finish[i] and np.all(self.need[i] <= work):
                    # Process i can finish
                    work += self.allocation[i]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
        
        # System is safe if all processes can finish
        is_safe = np.all(finish)
        
        if is_safe:
            print(f"System is in a safe state. Safe sequence: {safe_sequence}")
        else:
            print("System is not in a safe state. Deadlock may occur.")
        
        return is_safe
    
    def system_state_summary(self) -> str:
        """Generate a summary of the current system state"""
        summary = "System State Summary:\n"
        summary += f"Available Resources: {self.available}\n\n"
        summary += "Process Information:\n"
        
        for i in range(self.n_processes):
            summary += f"Process {i}:\n"
            summary += f"  Allocation: {self.allocation[i]}\n"
            summary += f"  Max Claim:  {self.max_claim[i]}\n"
            summary += f"  Need:       {self.need[i]}\n\n"
        
        return summary
    
    def visualize_state(self) -> None:
        """Visualize current system state"""
        # Create figure with subplots
        fig, ax = plt.subplots(1, 3, figsize=(24, 8))
        
        # Display matrices as heatmaps
        im0 = ax[0].imshow(self.allocation, cmap='YlOrRd')
        ax[0].set_title('Allocation Matrix')
        ax[0].set_xlabel('Resources')
        ax[0].set_ylabel('Processes')
        plt.colorbar(im0, ax=ax[0])
        
        im1 = ax[1].imshow(self.max_claim, cmap='YlOrRd')
        ax[1].set_title('Max Claim Matrix')
        ax[1].set_xlabel('Resources')
        plt.colorbar(im1, ax=ax[1])
        
        im2 = ax[2].imshow(self.need, cmap='YlOrRd')
        ax[2].set_title('Need Matrix')
        ax[2].set_xlabel('Resources')
        plt.colorbar(im2, ax=ax[2])
        
        # Add text annotations
        for i in range(self.n_processes):
            for j in range(self.n_resources):
                ax[0].text(j, i, self.allocation[i, j], ha='center', va='center', color='black')
                ax[1].text(j, i, self.max_claim[i, j], ha='center', va='center', color='black')
                ax[2].text(j, i, self.need[i, j], ha='center', va='center', color='black')
        
        plt.tight_layout()
        plt.show()


class ResourceAllocationGraph:
    """Implementation of Resource Allocation Graph for deadlock detection"""
    
    def __init__(self):
        """Initialize an empty Resource Allocation Graph"""
        self.graph = nx.DiGraph()
        self.processes: Set[str] = set()
        self.resources: Set[str] = set()
        self.resource_instances: Dict[str, int] = {}  # Maps resource to number of instances
        self.resource_allocations: Dict[str, List[str]] = {}  # Maps resource to list of processes
        
    def add_process(self, process: str) -> None:
        """Add a process to the graph"""
        self.processes.add(process)
        self.graph.add_node(process, type='process')
    
    def add_resource(self, resource: str, instances: int = 1) -> None:
        """Add a resource with specified number of instances to the graph"""
        self.resources.add(resource)
        self.resource_instances[resource] = instances
        self.resource_allocations[resource] = []
        self.graph.add_node(resource, type='resource', instances=instances)
    
    def request_edge(self, process: str, resource: str) -> None:
        """Add a request edge from process to resource"""
        if process not in self.processes:
            self.add_process(process)
        if resource not in self.resources:
            self.add_resource(resource)
        
        self.graph.add_edge(process, resource, type='request')
    
    def allocation_edge(self, resource: str, process: str) -> None:
        """Add an allocation edge from resource to process"""
        if process not in self.processes:
            self.add_process(process)
        if resource not in self.resources:
            self.add_resource(resource)
        
        self.graph.add_edge(resource, process, type='allocation')
        self.resource_allocations[resource].append(process)
    
    def remove_request_edge(self, process: str, resource: str) -> None:
        """Remove a request edge from process to resource"""
        if self.graph.has_edge(process, resource):
            self.graph.remove_edge(process, resource)
    
    def remove_allocation_edge(self, resource: str, process: str) -> None:
        """Remove an allocation edge from resource to process"""
        if self.graph.has_edge(resource, process):
            self.graph.remove_edge(resource, process)
            self.resource_allocations[resource].remove(process)
    
    def detect_deadlock(self) -> Tuple[bool, List[List[str]]]:
        """
        Detect if there's a deadlock in the graph
        
        Returns:
            Tuple of (has_deadlock, deadlock_cycles)
        """
        # For RAG with single instance resources, we simply need to find cycles
        cycles = list(nx.simple_cycles(self.graph))
        
        # Filter cycles that represent deadlocks (process → resource → process → ...)
        deadlock_cycles = []
        for cycle in cycles:
            # Check if cycle alternates between processes and resources
            is_alternating = True
            for i in range(len(cycle)):
                curr = cycle[i]
                next_node = cycle[(i + 1) % len(cycle)]
                
                if curr in self.processes and next_node not in self.resources:
                    is_alternating = False
                    break
                if curr in self.resources and next_node not in self.processes:
                    is_alternating = False
                    break
            
            if is_alternating:
                deadlock_cycles.append(cycle)
        
        return len(deadlock_cycles) > 0, deadlock_cycles
    
    def visualize(self) -> None:
        """Visualize the Resource Allocation Graph"""
        plt.figure(figsize=(10, 8))
        
        # Create position layout
        pos = nx.spring_layout(self.graph, seed=42)
        
        # Draw processes (circular nodes)
        process_nodes = [node for node in self.graph.nodes if node in self.processes]
        nx.draw_networkx_nodes(self.graph, pos, nodelist=process_nodes, 
                               node_shape='o', node_color='skyblue', node_size=700)
        
        # Draw resources (square nodes)
        resource_nodes = [node for node in self.graph.nodes if node in self.resources]
        nx.draw_networkx_nodes(self.graph, pos, nodelist=resource_nodes, 
                               node_shape='s', node_color='lightgreen', node_size=700)
        
        # Draw request edges (process -> resource) as dashed lines
        request_edges = [(u, v) for u, v, d in self.graph.edges(data=True) if d['type'] == 'request']
        nx.draw_networkx_edges(self.graph, pos, edgelist=request_edges, 
                               arrowstyle='->', arrowsize=15, style='dashed', 
                               edge_color='red', width=1.5)
        
        # Draw allocation edges (resource -> process) as solid lines
        allocation_edges = [(u, v) for u, v, d in self.graph.edges(data=True) if d['type'] == 'allocation']
        nx.draw_networkx_edges(self.graph, pos, edgelist=allocation_edges, 
                               arrowstyle='->', arrowsize=15, style='solid', 
                               edge_color='blue', width=1.5)
        
        # Add labels
        labels = {node: node for node in self.graph.nodes}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=12)
        
        # Create legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='skyblue', markersize=15, label='Process'),
            Line2D([0], [0], marker='s', color='w', markerfacecolor='lightgreen', markersize=15, label='Resource'),
            Line2D([0], [0], linestyle='dashed', color='red', label='Request'),
            Line2D([0], [0], linestyle='solid', color='blue', label='Allocation')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.title("Resource Allocation Graph")
        plt.axis('off')
        plt.tight_layout()
        plt.show()


def demo_bankers_algorithm() -> None:
    """Demonstrate Banker's Algorithm with a simple example"""
    print("\n=== Banker's Algorithm Demonstration ===\n")
    
    # Create a system with 5 processes and 3 resource types
    ba = BankersAlgorithm(5, 3)
    
    # Set available resources (A, B, C)
    ba.set_available([10, 5, 7])
    
    # Set maximum resource claims for each process
    ba.set_max_claim([
        [7, 5, 3],  # Process 0
        [3, 2, 2],  # Process 1
        [9, 0, 2],  # Process 2
        [2, 2, 2],  # Process 3
        [4, 3, 3]   # Process 4
    ])
    
    # Set current resource allocation for each process
    ba.set_allocation([
        [0, 1, 0],  # Process 0
        [2, 0, 0],  # Process 1
        [3, 0, 2],  # Process 2
        [2, 1, 1],  # Process 3
        [0, 0, 2]   # Process 4
    ])
    
    # Display system state
    print(ba.system_state_summary())
    
    # Check if system is in safe state
    ba.is_safe()
    
    # Try a few resource requests
    print("\nTrying resource requests:")
    ba.request_resources(1, [1, 0, 2])  # Process 1 requests (1,0,2)
    ba.request_resources(4, [3, 3, 0])  # Process 4 requests (3,3,0)
    
    # Display updated system state
    print("\nUpdated system state:")
    print(ba.system_state_summary())
    
    # Visualize system state
    ba.visualize_state()


def demo_rag() -> None:
    """Demonstrate Resource Allocation Graph with a simple example"""
    print("\n=== Resource Allocation Graph Demonstration ===\n")
    
    # Create a Resource Allocation Graph
    rag = ResourceAllocationGraph()
    
    # Add processes and resources
    for i in range(1, 5):
        rag.add_process(f"P{i}")
    
    for i in range(1, 4):
        rag.add_resource(f"R{i}")
    
    # Add allocation edges (resource allocated to process)
    rag.allocation_edge("R1", "P1")
    rag.allocation_edge("R2", "P3")
    rag.allocation_edge("R3", "P4")
    
    # Add request edges (process requesting resource)
    rag.request_edge("P1", "R2")
    rag.request_edge("P2", "R1")
    rag.request_edge("P3", "R3")
    rag.request_edge("P4", "R1")
    
    # Detect deadlock
    has_deadlock, cycles = rag.detect_deadlock()
    
    print(f"Deadlock detected: {has_deadlock}")
    if has_deadlock:
        print("Deadlock cycles:")
        for cycle in cycles:
            print(" → ".join(cycle + [cycle[0]]))
    
    # Visualize the graph
    rag.visualize()
    
    # Create a deadlock situation
    print("\nCreating a deadlock situation...")
    rag.remove_request_edge("P2", "R1")
    rag.request_edge("P3", "R1")
    
    # Detect deadlock again
    has_deadlock, cycles = rag.detect_deadlock()
    
    print(f"Deadlock detected: {has_deadlock}")
    if has_deadlock:
        print("Deadlock cycles:")
        for cycle in cycles:
            print(" → ".join(cycle + [cycle[0]]))
    
    # Visualize the new graph
    rag.visualize()


if __name__ == "__main__":
    print("Operating Systems Deadlock Simulation")
    print("====================================")
    
    demo_bankers_algorithm()
    demo_rag()