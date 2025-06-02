import cmd2
from core.loader import load_blades

class RybickaShell(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "rybicka> "
        self.intro = "Welcome to Rybicka – type 'help' for commands"
        self.blades = load_blades()

    def do_list(self, args):
        """List all available blades"""
        if not self.blades:
            self.poutput("No blades loaded.")
            return
        for name, blade in self.blades.items():
            self.poutput(f"{name} - {blade.description}")

    def do_run(self, args):
        """Run a blade: run <blade_name>"""
        parts = args.strip().split()
        if not parts:
            self.poutput("Usage: run <blade_name>")
            return

        blade_name = parts[0]
        blade = self.blades.get(blade_name)
        if not blade:
            self.poutput(f"Blade '{blade_name}' not found.")
            return

        try:
            result = blade.run()
            self.poutput(f"[{blade_name}] Result:\n{result}")
        except Exception as e:
            self.poutput(f"Error while executing blade '{blade_name}': {e}")
