from roles.doctor import Doctor
from tools.ocr_tool import OCRTool

# Création des outils
ocr_tool = OCRTool()

# Création du médecin avec accès à l’OCR
doctor = Doctor(name="Dr. House", tools=[ocr_tool])

# Test du rôle et de l'outil OCR
image_path = "data/rapport_medical.jpg"
extracted_text = doctor.use_tool("OCRTool", image_path)
print(f"Texte extrait : {extracted_text}")

# Analyse du texte par le médecin
if extracted_text:
    response = doctor.act(extracted_text)
    print(f"🔎 Réponse du médecin : {response}")
