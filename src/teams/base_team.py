from config import Config  # ✅ Import de la configuration
from agents.base_agent import BaseAgent  # ✅ Import de la classe Agent si nécessaire
from environments.base_env import BaseEnvironment  # ✅ Import de l'environnement si nécessaire

class BaseTeam:
    def __init__(self, name, agents=None, environment=None):
        self.name = name
        self.agents = set(agents) if agents else set()
        self.environment = environment

    def add_agent(self, agent: BaseAgent):
        if agent in self.agents:
            Config.debug_log(f"⚠️ {agent.name} est déjà dans l'équipe {self.name}.")
        else:
            self.agents.add(agent)
            Config.debug_log(f"✅ {agent.name} rejoint l'équipe {self.name}.")

    def execute_task(self, action_name, *args, **kwargs):
        Config.debug_log(f"\n🚀 Équipe {self.name} exécute : {action_name}")
        
        if self.environment and not self.environment.enforce_rules(action_name):
            Config.debug_log(f"⚠️ Action {action_name} interdite dans l'environnement {self.environment.name}!")
            return None

        responses = {}
        for agent in self.agents:
            try:
                responses[agent.name] = agent.act(action_name, *args, **kwargs)
            except Exception as e:
                Config.debug_log(f"❌ Erreur lors de l'exécution de {action_name} par {agent.name} : {e}")
        
        return responses
