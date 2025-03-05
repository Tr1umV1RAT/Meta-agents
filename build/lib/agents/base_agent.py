from skills.communication import CommunicationSkill
from skills.memory_access import MemorySkill
from skills.llm_skill import LLMSkill  # 🔥 Nouveau skill !
from config import Config
class BaseAgent:
    def __init__(self, name, role, skills=None):
        self.name = name
        self.role = role
        self.skills = skills if skills is not None else {} 
        

        # Ajout des skills fournis (optionnels)
        if skills:
            for skill_class in skills:
                self.add_skill(skill_class)
    def add_skill(self, skill_class):
              """Ajoute une nouvelle compétence à l’agent."""
              skill = skill_class(self)
              self.skills[skill.__class__.__name__] = skill  # Stockage standardisé
              Config.debug_log(f"✅ {self.name} a reçu la compétence {skill.__class__.__name__}")

    def __str__(self):
        return f"Agent: {self.name}"

    def __repr__(self):
        return f"BaseAgent(name={self.name})"



    def execute_skill(self, skill_name, *args, **kwargs):
          """Exécute une compétence de l’agent."""
          Config.debug_log(f"🔍 {self.name} essaie d'exécuter le skill: {skill_name}")

          if skill_name in self.skills:
                 Config.debug_log(f"✅ {self.name} exécute {skill_name} avec {args}, {kwargs}")
                 return self.skills[skill_name].perform(*args, **kwargs)

          Config.debug_log(f"⚠️ {self.name} ne possède pas la compétence {skill_name}! (Compétences disponibles: {list(self.skills.keys())})")

    
                     
    def act(self, action_name, *args, **kwargs):
        """Exécute une action définie par le rôle, sinon cherche un skill équivalent."""
        if self.role:
            return self.role.perform_action(action_name, *args, **kwargs)

        # Si l'action correspond à un skill, on l'exécute
        if action_name in self.skills:
            return self.skills[action_name].perform(*args, **kwargs)  # 🔥 Correction ici aussi !

        Config.debug_log(f"⚠️ {self.name} n’a pas de rôle défini et ne peut pas effectuer {action_name}!")
