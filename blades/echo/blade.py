from core.blade_base import BaseBlade

class Blade(BaseBlade):
    name = "echo"
    description = "Simple blade that prints a greeting"

    def run(self):
        return "Hello from blade!"
