import importlib

class Scope(dict):
    "A scope: a dict of {'var':val} pairs, with an outer Scope."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms,args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Scope where var appears."

        # If ':' in var add module to environment
        if ":" in var:
            namespace, attribute = var.split(":")
            module = importlib.import_module(namespace)

            module_funcs = {
                "{}:{}".format(namespace, k): attr
                for k, attr
                in vars(module).items()
            }
            self.update(module_funcs)
        try:
            return self if var in self else self.outer.find(var)
        except AttributeError:
            raise NameError("name '{}' is not defined".format(var))

def add_globals(env, special_forms=None):
    "Add some Scheme standard procedures to an environment."
    if special_forms is None:
        special_forms = {}

    env.update(special_forms)
    return env
