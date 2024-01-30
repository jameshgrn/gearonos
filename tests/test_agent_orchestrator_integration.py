import unittest
from gearonos.orchestrator import Orchestrator
from gearonos.memory import MemoryAgent, MemoryDocument
from gearonos.tasks.task import Task

class TestAgentOrchestratorIntegration(unittest.TestCase):
    def test_task_distribution(self):
        orchestrator = Orchestrator(None)
        memory_agent = MemoryAgent("memory_agent", db_interface=None)
        orchestrator.register_agent(memory_agent)
        
        task = Task("index_memory", MemoryDocument("content", "context", "2023-04-01", ["keyword1"]))
        orchestrator.enqueue_task(task)
        orchestrator.distribute_tasks()
        
        # Verify the task was removed from the queue, indicating it was distributed
        self.assertEqual(len(orchestrator.task_queue), 0)


