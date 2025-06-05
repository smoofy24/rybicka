from rybicka.core.blade_base import BaseBlade

class Blade(BaseBlade):
    name = "echo"
    description = "Simple blade that prints a greeting"
    arg_spec = {
            "msg": "Message to display"
            }

    def run(self):
        return self.args.get("msg", "Hello from blade!")
