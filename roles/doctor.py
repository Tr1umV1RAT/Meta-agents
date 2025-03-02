from roles.base_role import BaseRole


class DoctorRole(BaseRole):
    def __init__(self):
        super().__init__(
            name="Médecin",
            actions=[self.analyze_case]
        )

    def analyze_case(self, case_description):
        print(f"🩺 Analyse du cas médical...")
        return self.use_tool("LLMTool", f"Analyse médicale du cas : {case_description}")
