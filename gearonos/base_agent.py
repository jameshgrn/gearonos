from abc import ABC, abstractmethod
from typing import Any, Dict
from .task import Task  

class BaseAgent(ABC):
    def __init__(self, id: str, capabilities: Dict[str, Any]):
        """
        Initialize the agent with a unique ID and a dictionary of capabilities.
        """
        self.id = id
        self.capabilities = capabilities
        self.status = "idle"  # Possible values: idle, busy, error

    @abstractmethod
    def can_handle_task(self, task: Task) -> bool:
        """
        Determine if the agent can handle the given task based on its capabilities.
        This method should be overridden by subclasses to provide specific logic
        for task handling capabilities.
        """
        pass

    @abstractmethod
    def assign_task(self, task: Task):
        """
        Assign a task to the agent for processing. This method should be overridden
        by subclasses to implement the task processing logic.
        """
        pass

    @abstractmethod
    def report_status(self) -> Dict[str, Any]:
        """
        Report the current status of the agent, including any results or errors.
        This method can be extended by subclasses but provides a basic implementation.
        """
        return {"id": self.id, "status": self.status}

    @abstractmethod
    def communicate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send and receive messages to/from the Orchestrator or other agents.
        This method provides a basic structure for communication and can be
        overridden by subclasses for more complex interactions.
        """
        # Basic implementation: Log the message and return an acknowledgment
        print(f"Agent {self.id} received message: {message}")
        return {"response": "acknowledged"}

    @abstractmethod
    def update_capabilities(self, capabilities: Dict[str, Any]):
        """
        Update the agent's capabilities. This method allows for dynamic changes
        in what the agent can do, supporting a flexible and adaptable system.
        """
        self.capabilities.update(capabilities)

    @abstractmethod
    def set_status(self, status: str):
        """
        Update the agent's status. Useful for managing the agent's state, especially
        in a multi-threaded or asynchronous environment.
        """
        self.status = status