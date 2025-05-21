#!/usr/bin/env python3
"""
Memory Allocation Algorithms: First Fit, Best Fit, Worst Fit

This module implements memory allocation algorithms commonly used in operating systems.
"""

import random
import time
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict, Optional, Any


class MemoryBlock:
    """Represents a block of memory"""
    
    def __init__(self, start: int, size: int, process_id: Optional[str] = None):
        """
        Initialize a memory block
        
        Args:
            start: Starting address of the block
            size: Size of the block in memory units
            process_id: ID of the process occupying the block (None if free)
        """
        self.start = start
        self.size = size
        self.process_id = process_id
        
    @property
    def end(self) -> int:
        """Get the end address of the block"""
        return self.start + self.size - 1
        
    @property
    def is_free(self) -> bool:
        """Check if the block is free"""
        return self.process_id is None
    
    def __str__(self) -> str:
        """String representation of memory block"""
        status = "Free" if self.is_free else f"Allocated to {self.process_id}"
        return f"Block[{self.start}-{self.end}] Size: {self.size} - {status}"


class MemoryAllocator:
    """Base class for memory allocation algorithms"""
    
    def __init__(self, memory_size: int):
        """
        Initialize memory allocator
        
        Args:
            memory_size: Total size of memory
        """
        self.memory_size = memory_size
        self.blocks: List[MemoryBlock] = [MemoryBlock(0, memory_size)]
        self.algorithm_name = "Base Allocator"
        self.stats = {
            "allocations": 0,
            "allocation_failures": 0,
            "deallocations": 0,
            "fragmentation_history": [],
            "search_time_history": [],
            "allocation_history": []
        }
    
    def allocate(self, process_id: str, size: int) -> bool:
        """
        Allocate memory for a process (to be implemented by subclasses)
        
        Args:
            process_id: ID of process requesting memory
            size: Amount of memory requested
            
        Returns:
            bool: True if allocation successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement allocate()")
    
    def deallocate(self, process_id: str) -> bool:
        """
        Deallocate memory for a process
        
        Args:
            process_id: ID of process to deallocate
            
        Returns:
            bool: True if deallocation successful, False otherwise
        """
        deallocated = False
        blocks_to_merge = []
        
        # Find blocks allocated to the process
        for i, block in enumerate(self.blocks):
            if block.process_id == process_id:
                block.process_id = None
                blocks_to_merge.append(i)
                deallocated = True
        
        if deallocated:
            self.stats["deallocations"] += 1
            self._merge_adjacent_free_blocks()
            
            # Record fragmentation after deallocation
            self.stats["fragmentation_history"].append(self.calculate_fragmentation())
        
        return deallocated
    
    def _merge_adjacent_free_blocks(self) -> None:
        """Merge adjacent free blocks to reduce fragmentation"""
        i = 0
        while i < len(self.blocks) - 1:
            current_block = self.blocks[i]
            next_block = self.blocks[i + 1]
            
            if current_block.is_free and next_block.is_free:
                # Merge blocks
                current_block.size += next_block.size
                self.blocks.pop(i + 1)
            else:
                i += 1
    
    def memory_state(self) -> List[Dict[str, Any]]:
        """
        Get current memory state as a list of dictionaries
        
        Returns:
            List of dictionaries with block information
        """
        return [
            {
                "start": block.start,
                "end": block.end,
                "size": block.size,
                "process_id": block.process_id,
                "is_free": block.is_free
            }
            for block in self.blocks
        ]
    
    def visualize_memory(self) -> None:
        """Visualize current memory state with improved text fitting"""
        plt.figure(figsize=(15, 4))  # Wider figure for better text spacing
        
        # Create bar chart
        y_pos = np.arange(1)
        
        # Process each memory block
        for block in self.blocks:
            # Add the block as a bar
            color = 'lightgrey' if block.is_free else 'skyblue'
            plt.barh(y_pos, block.size, left=block.start, height=0.8, color=color)
            
            # Calculate text size and position
            block_center = block.start + block.size / 2
            text_size = min(10, max(6, block.size / 50))  # Dynamic text size
            
            # Format size with K or M suffix for better readability
            if block.size >= 1000000:
                size_text = f"{block.size/1000000:.1f}M"
            elif block.size >= 1000:
                size_text = f"{block.size/1000:.1f}K"
            else:
                size_text = str(block.size)
            
            # Add text label with rotation for narrow blocks
            if block.size < self.memory_size * 0.05:  # If block is narrow
                rotation = 90
                va = 'bottom'
                if block.is_free:
                    text = f"Free\n{size_text}"
                else:
                    text = f"{block.process_id}\n{size_text}"
            else:
                rotation = 0
                va = 'center'
                if block.is_free:
                    text = f"Free\n{size_text}"
                else:
                    text = f"{block.process_id}\n{size_text}"
            
            plt.text(block_center, 0, text,
                    ha='center', va=va,
                    rotation=rotation,
                    fontsize=text_size,
                    color='black')
        
        # Set plot parameters
        plt.yticks([])
        plt.xlabel('Memory Address')
        plt.title(f'Memory State - {self.algorithm_name}')
        plt.xlim(-10, self.memory_size + 10)  # Add padding
        
        # Create legend
        import matplotlib.patches as mpatches
        free_patch = mpatches.Patch(color='lightgrey', label='Free Memory')
        allocated_patch = mpatches.Patch(color='skyblue', label='Allocated Memory')
        plt.legend(handles=[free_patch, allocated_patch], 
                loc='upper center', 
                bbox_to_anchor=(0.5, -0.15),
                ncol=2)
        
        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.2)  # Make room for legend
        plt.show()
    
    def calculate_fragmentation(self) -> float:
        """
        Calculate external fragmentation
        
        Returns:
            External fragmentation as a percentage
        """
        total_free_memory = sum(block.size for block in self.blocks if block.is_free)
        largest_free_block = max((block.size for block in self.blocks if block.is_free), default=0)
        
        if total_free_memory == 0:
            return 0.0
        
        # External fragmentation percentage
        fragmentation = (1 - largest_free_block / total_free_memory) * 100
        return fragmentation
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get memory allocation statistics
        
        Returns:
            Dictionary of statistics
        """
        stats = self.stats.copy()
        stats["current_fragmentation"] = self.calculate_fragmentation()
        stats["free_memory"] = sum(block.size for block in self.blocks if block.is_free)
        stats["used_memory"] = self.memory_size - stats["free_memory"]
        stats["total_memory"] = self.memory_size
        stats["free_blocks"] = sum(1 for block in self.blocks if block.is_free)
        stats["used_blocks"] = sum(1 for block in self.blocks if not block.is_free)
        stats["total_blocks"] = len(self.blocks)
        
        return stats


class FirstFitAllocator(MemoryAllocator):
    """First Fit memory allocation algorithm"""
    
    def __init__(self, memory_size: int):
        """Initialize First Fit allocator"""
        super().__init__(memory_size)
        self.algorithm_name = "First Fit"
    
    def allocate(self, process_id: str, size: int) -> bool:
        """
        Allocate memory using First Fit algorithm
        
        Args:
            process_id: ID of process requesting memory
            size: Amount of memory requested
            
        Returns:
            bool: True if allocation successful, False otherwise
        """
        start_time = time.time()
        
        # Search for the first free block with sufficient size
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size:
                # Found a suitable block
                if block.size == size:
                    # Perfect fit - use the entire block
                    block.process_id = process_id
                else:
                    # Split the block
                    new_free_block = MemoryBlock(block.start + size, block.size - size)
                    block.size = size
                    block.process_id = process_id
                    self.blocks.insert(i + 1, new_free_block)
                
                self.stats["allocations"] += 1
                end_time = time.time()
                self.stats["search_time_history"].append(end_time - start_time)
                self.stats["fragmentation_history"].append(self.calculate_fragmentation())
                self.stats["allocation_history"].append(size)
                return True
        
        # No suitable block found
        self.stats["allocation_failures"] += 1
        end_time = time.time()
        self.stats["search_time_history"].append(end_time - start_time)
        return False


class BestFitAllocator(MemoryAllocator):
    """Best Fit memory allocation algorithm"""
    
    def __init__(self, memory_size: int):
        """Initialize Best Fit allocator"""
        super().__init__(memory_size)
        self.algorithm_name = "Best Fit"
    
    def allocate(self, process_id: str, size: int) -> bool:
        """
        Allocate memory using Best Fit algorithm
        
        Args:
            process_id: ID of process requesting memory
            size: Amount of memory requested
            
        Returns:
            bool: True if allocation successful, False otherwise
        """
        start_time = time.time()
        
        best_fit_idx = -1
        best_fit_size = float('inf')
        
        # Find the smallest free block that is large enough
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size:
                if block.size < best_fit_size:
                    best_fit_idx = i
                    best_fit_size = block.size
        
        # If a suitable block was found
        if best_fit_idx != -1:
            block = self.blocks[best_fit_idx]
            
            if block.size == size:
                # Perfect fit - use the entire block
                block.process_id = process_id
            else:
                # Split the block
                new_free_block = MemoryBlock(block.start + size, block.size - size)
                block.size = size
                block.process_id = process_id
                self.blocks.insert(best_fit_idx + 1, new_free_block)
            
            self.stats["allocations"] += 1
            end_time = time.time()
            self.stats["search_time_history"].append(end_time - start_time)
            self.stats["fragmentation_history"].append(self.calculate_fragmentation())
            self.stats["allocation_history"].append(size)
            return True
        
        # No suitable block found
        self.stats["allocation_failures"] += 1
        end_time = time.time()
        self.stats["search_time_history"].append(end_time - start_time)
        return False


class WorstFitAllocator(MemoryAllocator):
    """Worst Fit memory allocation algorithm"""
    
    def __init__(self, memory_size: int):
        """Initialize Worst Fit allocator"""
        super().__init__(memory_size)
        self.algorithm_name = "Worst Fit"
    
    def allocate(self, process_id: str, size: int) -> bool:
        """
        Allocate memory using Worst Fit algorithm
        
        Args:
            process_id: ID of process requesting memory
            size: Amount of memory requested
            
        Returns:
            bool: True if allocation successful, False otherwise
        """
        start_time = time.time()
        
        worst_fit_idx = -1
        worst_fit_size = -1
        
        # Find the largest free block
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size:
                if block.size > worst_fit_size:
                    worst_fit_idx = i
                    worst_fit_size = block.size
        
        # If a suitable block was found
        if worst_fit_idx != -1:
            block = self.blocks[worst_fit_idx]
            
            if block.size == size:
                # Perfect fit - use the entire block
                block.process_id = process_id
            else:
                # Split the block
                new_free_block = MemoryBlock(block.start + size, block.size - size)
                block.size = size
                block.process_id = process_id
                self.blocks.insert(worst_fit_idx + 1, new_free_block)
            
            self.stats["allocations"] += 1
            end_time = time.time()
            self.stats["search_time_history"].append(end_time - start_time)
            self.stats["fragmentation_history"].append(self.calculate_fragmentation())
            self.stats["allocation_history"].append(size)
            return True
        
        # No suitable block found
        self.stats["allocation_failures"] += 1
        end_time = time.time()
        self.stats["search_time_history"].append(end_time - start_time)
        return False