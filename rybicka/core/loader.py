import os
import importlib
from rybicka.core.blade_base import BaseBlade

def load_blades():
    blades = {}
    blades_dir = os.path.join(os.path.dirname(__file__), "..", "blades")

    for entry in os.listdir(blades_dir):
        blade_path = os.path.join(blades_dir, entry)
        if not os.path.isdir(blade_path):
            continue

        try:
            module_path = f"rybicka.blades.{entry}.blade"
            module = importlib.import_module(module_path)
            blade_instance = module.Blade()

            if not isinstance(blade_instance, BaseBlade):
                print(f"[!] Blade '{entry}' does not inherit from BaseBlade – skipped")
                continue

            blades[blade_instance.name] = blade_instance

        except Exception as e:
            print(f"[!] Failed to load blade '{entry}': {e}")

    return blades
