import pytest
from deadlock_simulation import ResourceAllocationGraph

@pytest.fixture
def empty_rag():
    """Fixture for an empty RAG"""
    return ResourceAllocationGraph()

@pytest.fixture
def populated_rag():
    """Fixture for a RAG with basic setup"""
    rag = ResourceAllocationGraph()
    # Add processes P1-P3
    for i in range(1, 4):
        rag.add_process(f"P{i}")
    # Add resources R1-R2 with instances
    resources = {"R1": 2, "R2": 1}
    for r, instances in resources.items():
        rag.add_resource(r, instances)
    return rag

class TestRAGComprehensive:
    def test_empty_initialization(self, empty_rag):
        """Test initial empty state"""
        assert len(empty_rag.processes) == 0
        assert len(empty_rag.resources) == 0
        assert len(empty_rag.resource_instances) == 0
    
    def test_process_addition(self, empty_rag):
        """Test process addition functionality"""
        empty_rag.add_process("P1")
        assert "P1" in empty_rag.processes
        assert len(empty_rag.processes) == 1
        
        # Test duplicate process addition
        with pytest.raises(ValueError):
            empty_rag.add_process("P1")
    
    def test_resource_addition(self, empty_rag):
        """Test resource addition functionality"""
        empty_rag.add_resource("R1", 2)
        assert "R1" in empty_rag.resources
        assert empty_rag.resource_instances["R1"] == 2
        
        # Test duplicate resource addition
        with pytest.raises(ValueError):
            empty_rag.add_resource("R1", 1)
    
    def test_resource_instance_validation(self, empty_rag):
        """Test resource instance validation"""
        with pytest.raises(ValueError):
            empty_rag.add_resource("R1", 0)  # Zero instances
        with pytest.raises(ValueError):
            empty_rag.add_resource("R1", -1)  # Negative instances
    
    def test_populated_rag_structure(self, populated_rag):
        """Test populated RAG structure"""
        # Process validation
        assert len(populated_rag.processes) == 3
        assert all(f"P{i}" in populated_rag.processes for i in range(1, 4))
        
        # Resource validation
        assert len(populated_rag.resources) == 2
        assert populated_rag.resource_instances["R1"] == 2
        assert populated_rag.resource_instances["R2"] == 1
    
    def test_invalid_process_operations(self, populated_rag):
        """Test operations with invalid processes"""
        with pytest.raises(ValueError):
            populated_rag.request_edge("P99", "R1")  # Non-existent process
        with pytest.raises(ValueError):
            populated_rag.allocation_edge("R1", "P99")  # Non-existent process
    
    def test_invalid_resource_operations(self, populated_rag):
        """Test operations with invalid resources"""
        with pytest.raises(ValueError):
            populated_rag.request_edge("P1", "R99")  # Non-existent resource
        with pytest.raises(ValueError):
            populated_rag.allocation_edge("R99", "P1")  # Non-existent resource
    
    def test_resource_instance_tracking(self, populated_rag):
        """Test resource instance tracking"""
        # Allocate all instances of R1
        populated_rag.allocation_edge("R1", "P1")
        populated_rag.allocation_edge("R1", "P2")
        
        # Verify we can't allocate more than available instances
        with pytest.raises(ValueError):
            populated_rag.allocation_edge("R1", "P3")

if __name__ == "__main__":
    pytest.main(["-v", __file__])