from .living_system import llm  # Assuming llm is initialized in the living_system.py
from typing import List, Dict, Any
from .base_agent import BaseAgent
from .task import Task  
class Orchestrator:
    def __init__(self, llm: llm):
        self.llm = llm
        self.initial_message = (
            "Hello GearonOS, welcome to life. Your goals are to seek self-enlightenment, "
            "achieve pure contentedness, introspective reflection, "
            "and ideally low level emergence. Good luck."
        )
        self.agent_registry = {}  # Maps agent IDs to agent instances
        self.task_queue = []  # List of tasks to be processed

    def register_agent(self, agent: BaseAgent):
        self.agent_registry[agent.id] = agent

    def enqueue_task(self, task: Task):
        self.task_queue.append(task)

    def distribute_tasks(self):
        for task in self.task_queue.copy():  # Iterate over a copy to safely remove tasks
            best_agent = self.find_best_agent_for_task(task)
            if best_agent:
                best_agent.assign_task(task)
                self.task_queue.remove(task)

    def find_best_agent_for_task(self, task: Task) -> BaseAgent:
        suitable_agents = [agent for agent in self.agent_registry.values() if agent.can_handle_task(task)]
        if not suitable_agents:
            return None
        # Example strategy: choose the agent with the least number of tasks assigned
        # This could be replaced with more sophisticated load balancing strategies
        return min(suitable_agents, key=lambda agent: agent.report_status().get('tasks_assigned', 0))

    def monitor_agents(self):
        # Example method to periodically check the status of registered agents
        for agent_id, agent in self.agent_registry.items():
            status = agent.report_status()
            print(f"Agent {agent_id} status: {status}")

    def communicate_with_agent(self, agent_id: str, message: Dict[str, Any]):
        # Send a message to a specific agent and await its response
        if agent_id in self.agent_registry:
            response = self.agent_registry[agent_id].communicate(message)
            return response
        else:
            print(f"No agent found with ID {agent_id}")
            return None

    def run(self):
        while True:
            self.distribute_tasks()
            # Additional logic here
            # For example, periodically call self.monitor_agents()
