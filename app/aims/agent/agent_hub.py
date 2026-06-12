from app.aims.agent.agent_types import AgentActionType


class AgentHub:
    """
    Class for managing agent actions.
    """

    def __init__(self):
        self.agents = []
        pass

    def add_agent(self, agent):
        self.agents.append(agent)
        pass

    def remove_agent(self, agent):
        self.agents.remove(agent)
        AgentActionType.DELETE
        pass

    def get_agents(self):
        return self.agents
