import pytest
from deadlock_simulation import ResourceAllocationGraph
import sys
from io import StringIO
import contextlib
from usage_resource_allocation_graph import main

# filepath: c:\Users\acer\Desktop\deadlock case study\test_usage_resource_allocation_graph.py

@pytest.fixture
def basic_rag():
    """Fixture for a basic RAG setup"""
    rag = ResourceAllocationGraph()
    # Add processes P1-P5
    for i in range(1, 6):
        rag.add_process(f"P{i}")
    # Add resources R1-R4 with instances
    resources = {"R1": 2, "R2": 1, "R3": 3, "R4": 1}
    for r, instances in resources.items():
        rag.add_resource(r, instances)
    return rag

@pytest.fixture
def captured_output():
    """Fixture to capture stdout"""
    output = StringIO()
    with contextlib.redirect_stdout(output):
        yield output

class TestResourceAllocationGraph:
    
    def test_initial_setup(self, basic_rag):
        """Test initial system setup"""
        assert len(basic_rag.processes) == 5
        assert len(basic_rag.resources) == 4
        assert basic_rag.resource_instances["R1"] == 2
        assert basic_rag.resource_instances["R2"] == 1
        assert basic_rag.resource_instances["R3"] == 3
        assert basic_rag.resource_instances["R4"] == 1

    def test_no_deadlock_scenario(self, basic_rag):
        """Test scenario without deadlock"""
        # Create simple allocations without circular wait
        allocations = [("R1", "P1"), ("R2", "P2")]
        for r, p in allocations:
            basic_rag.allocation_edge(r, p)
        
        # Add non-conflicting requests
        requests = [("P3", "R3"), ("P4", "R4")]
        for p, r in requests:
            basic_rag.request_edge(p, r)
        
        has_deadlock, cycles = basic_rag.detect_deadlock()
        assert not has_deadlock
        assert len(cycles) == 0

    def test_deadlock_scenario(self, basic_rag):
        """Test scenario with deadlock"""
        # Create allocations that will lead to deadlock
        allocations = [
            ("R1", "P1"), ("R2", "P2"),
            ("R3", "P3"), ("R4", "P4")
        ]
        for r, p in allocations:
            basic_rag.allocation_edge(r, p)
        
        # Create circular wait condition
        requests = [
            ("P1", "R2"), ("P2", "R3"),
            ("P3", "R4"), ("P4", "R1")
        ]
        for p, r in requests:
            basic_rag.request_edge(p, r)
        
        has_deadlock, cycles = basic_rag.detect_deadlock()
        assert has_deadlock
        assert len(cycles) > 0

    def test_deadlock_resolution(self, basic_rag):
        """Test deadlock resolution"""
        # Create initial deadlock condition
        allocations = [("R1", "P1"), ("R2", "P2")]
        requests = [("P1", "R2"), ("P2", "R1")]
        
        for r, p in allocations:
            basic_rag.allocation_edge(r, p)
        for p, r in requests:
            basic_rag.request_edge(p, r)
        
        # Verify deadlock exists
        has_deadlock, _ = basic_rag.detect_deadlock()
        assert has_deadlock
        
        # Resolve deadlock
        basic_rag.remove_request_edge("P2", "R1")
        
        # Verify resolution
        has_deadlock, _ = basic_rag.detect_deadlock()
        assert not has_deadlock

    @pytest.mark.parametrize("resources,expected_deadlock", [
        ({"R1": 1, "R2": 1}, True),  # Minimal case
        ({"R1": 2, "R2": 2}, False),  # Sufficient resources
        ({"R1": 3, "R2": 1}, True),   # Mixed availability
    ])
    def test_various_resource_configurations(self, resources, expected_deadlock):
        """Test different resource configurations"""
        rag = ResourceAllocationGraph()
        
        # Add test processes
        for i in range(1, 3):
            rag.add_process(f"P{i}")
        
        # Add resources with specified instances
        for r, instances in resources.items():
            rag.add_resource(r, instances)
        
        # Create basic circular wait
        rag.allocation_edge("R1", "P1")
        rag.allocation_edge("R2", "P2")
        rag.request_edge("P1", "R2")
        rag.request_edge("P2", "R1")
        
        has_deadlock, _ = rag.detect_deadlock()
        assert has_deadlock == expected_deadlock

    def test_visualization_output(self, basic_rag, captured_output):
        """Test that visualization produces output"""
        basic_rag.visualize()
        output = captured_output.getvalue()
        assert len(output) > 0
        assert "digraph" in output.lower()

def test_main_execution():
    """Test the main execution flow"""
    with pytest.raises(SystemExit) as e:
        with contextlib.redirect_stdout(StringIO()):
            main()
    assert e.type == SystemExit

if __name__ == '__main__':
    pytest.main(['-v', __file__])