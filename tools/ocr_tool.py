from paddleocr import PaddleOCR

class OCRTool:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="fr")

    def run(self, image_path):
        results = self.ocr.ocr(image_path, cls=True)
        extracted_text = "\n".join([res[1][0] for res in results[0]])
        return extracted_text
