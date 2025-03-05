import re
from config import Config
from .base_tool import BaseTool
  # Suppose qu'on a un module pour interagir avec l'IA

class WebCleanerTool(BaseTool):
    """Outil permettant de nettoyer et reformater le texte brut issu d'un scraping."""
    name = "cleaner"
    def __init__(self):
        super().__init__("WebCleaner")
        

    def clean_html(self, text):
        """Nettoie les résidus HTML et les espaces inutiles."""
        cleaned_text = re.sub(r'\s+', ' ', text).strip()  # Supprime les espaces multiples
        text = re.sub(r'<[^>]+>', '', text)  # Supprime les balises HTML
        return cleaned_text

    def summarize_with_ai(self, text):
        """Utilise l'IA pour reformuler ou résumer le contenu."""
        prompt = f"""
        Tu es un assistant spécialisé en extraction d'informations web. Reformule ce texte pour qu'il soit clair, structuré et compréhensible :
        
        ---- Texte original ----
        {text}
        
        ---- Instructions ----
        - Supprime les éléments inutiles (pubs, textes répétitifs, mentions légales, etc.).
        - Reformule les phrases pour une meilleure lisibilité.
        - Ne change pas le sens du contenu.
        """

        Config.debug_log("🤖 WebCleaner envoie le texte à l'IA pour reformulation...")
        return self.Config.query_llm(prompt)

    def run(self, result):
        """ Nettoie uniquement le contenu texte pertinent d'un résultat de recherche """
        if isinstance(result, dict):
                text = result.get("content", "")  
        else:
                text = str(result)  

        cleaned_text = self.clean_html(text)
        return {**result, "cleaned_content": cleaned_text}  

        if use_ai:
            return self.summarize_with_ai(cleaned_text)
        
        return cleaned_text
