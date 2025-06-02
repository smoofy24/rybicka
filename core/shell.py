import cmd2
from core.loader import load_blades
from core.blade_base import BaseBlade

class RybickaShell(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = "rybicka> "
        self.intro = "Welcome to Rybicka – type 'help' for commands"
        self.blades = load_blades()
        self.current_blade: BaseBlade | None = None

    def do_list(self, args):
        """List all available blades"""
        if not self.blades:
            self.poutput("No blades loaded.")
            return
        for name, blade in self.blades.items():
            self.poutput(f"{name} - {blade.description}")

    def do_use(self, args):
        """Use a blade: use <blade_name>"""
        blade_name = args.strip()
        blade = self.blades.get(blade_name)
        if not blade:
            self.poutput(f"Blade '{blade_name}' not found.")
            return
        self.current_blade = blade
        self.poutput(f"[+] Loaded blade: {blade_name}")

    def do_set(self, args):
        """Set argument for the selected blade: set <key> <value>"""
        if self.current_blade is None:
            self.poutput("No blade selected. Use 'use <blade>' first.")
            return

        parts = args.strip().split(maxsplit=1)
        if len(parts) != 2:
            self.poutput("Usage: set <key> <value>")
            return

        key, value = parts
        self.current_blade.set_arg(key, value)
        self.poutput(f"[+] Set {key} = {value}")

    def do_show(self, args):
        """Show options for current blade: show options"""
        if args.strip() != "options":
            self.poutput("Usage: show options")
            return

        if self.current_blade is None:
            self.poutput("No blade selected.")
            return

        if not self.current_blade.arg_spec:
            self.poutput("This blade has no configurable options.")
            return

        self.poutput("Current options:")
        for key, desc in self.current_blade.arg_spec.items():
            value = self.current_blade.args.get(key, "<unset>")
            self.poutput(f"  {key:10} = {value:20} # {desc}")

    def do_run(self, args):
        """Run the selected blade with its arguments"""
        if self.current_blade is None:
            self.poutput("No blade selected. Use 'use <blade>' first.")
            return

        try:
            result = self.current_blade.run()
            self.poutput(f"[{self.current_blade.name}] Result:\n{result}")
        except Exception as e:
            self.poutput(f"Error while executing blade '{self.current_blade.name}': {e}")
