import unittest
from unittest.mock import MagicMock
from gearonos.memory import MemoryAgent, MemoryDocument

class TestMemoryAgent(unittest.TestCase):
    def test_index_memory(self):
        db_interface_mock = MagicMock()
        memory_agent = MemoryAgent("test_agent", db_interface=db_interface_mock)
        memory_doc = MemoryDocument("content", "context", "2023-04-01", ["keyword1", "keyword2"])
        
        memory_agent.index_memory(memory_doc)
        db_interface_mock.store_memory.assert_called_once()