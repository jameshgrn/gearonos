import unittest
from gearonos.orchestrator import Orchestrator
from gearonos.base_agent import BaseAgent

class TestOrchestrator(unittest.TestCase):
    def test_register_agent(self):
        orchestrator = Orchestrator(None)
        agent_mock = BaseAgent("test_agent", {})
        orchestrator.register_agent(agent_mock)
        
        self.assertIn("test_agent", orchestrator.agent_registry)