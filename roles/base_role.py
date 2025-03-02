from config import Config
from tools.base_tool import BaseTool
from skills.base_skill import BaseSkill

class BaseRole:
    def __init__(self, name, tools=None, skills=None):
        self.name = name
        self.tools = {tool.__class__.__name__: tool for tool in (tools or []) if isinstance(tool, BaseTool)}
        self.skills = {skill.__class__.__name__: skill for skill in (skills or []) if isinstance(skill, BaseSkill)}

    def use_tool(self, tool_name, *args, **kwargs):
        if tool_name in self.tools:
            Config.debug_log(f"[{self.name}] 🛠️ Utilisation de l'outil {tool_name}.")
            return self.tools[tool_name].run(*args, **kwargs)
        
        Config.debug_log(f"[{self.name}] ❌ Outil {tool_name} non disponible.")
        return None

    def perform_skill(self, skill_name, *args, **kwargs):
        if skill_name in self.skills:
            Config.debug_log(f"[{self.name}] 🎭 Exécution de la compétence {skill_name}.")
            return self.skills[skill_name].perform(*args, **kwargs)
        
        Config.debug_log(f"[{self.name}] ❌ Compétence {skill_name} non disponible.")
        return None
