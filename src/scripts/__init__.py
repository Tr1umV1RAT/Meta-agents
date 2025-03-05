import os
import glob

# Récupère tous les fichiers Python du dossier sauf __init__.py
modules = glob.glob(os.path.dirname(__file__) + "/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules if os.path.isfile(f) and not f.endswith("__init__.py")]

# Import dynamique des modules
for module in __all__:
    exec(f"from .{module} import *")

from scripts import test_tool