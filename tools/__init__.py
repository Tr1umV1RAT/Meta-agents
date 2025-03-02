import os
import importlib

import importlib.util

def import_module_safely(module_name):
    try:
        module_spec = importlib.util.find_spec(module_name)
        if module_spec:
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            globals()[module_name.split(".")[-1]] = module
    except Exception as e:
        print(f"⚠️ Erreur lors de l'import de {module_name}: {e}")

# Liste des modules à importer
modules = ["tools.web_cleaner_tool", "tools.base_tool","tools.extractor_key_info"]

for module in modules:
    import_module_safely(module)

