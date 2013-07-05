import importlib

from .symbols import Symbol
from .special_forms import SPECIAL_FORMS
from .parse import to_string


class Scope(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        # Bind parm list to corresponding args, or single parm to list of args
        self.outer = outer
        if isinstance(parms, Symbol):
            self.update({parms: list(args)})
        else:
            if len(args) != len(parms):
                raise TypeError('expected %s, given %s, '
                                % (to_string(parms), to_string(args)))
            self.update(zip(parms, args))

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer is None:
            # Check for outside modules in this conditional since we
            #  know it's the top level and we've already not found the
            #  variable
            if ":" in var:
                namespace, attribute = var.split(":")

                if "py" == namespace:
                    return {"py:{}".format(attribute): eval(attribute)}

                else:
                    module = importlib.import_module(namespace)

                module_funcs = {
                    "{}:{}".format(namespace, k): attr
                    for k, attr
                    in vars(module).items()
                }
                self.update(module_funcs)
                return self

            raise LookupError(var)
        else:
            return self.outer.find(var)


def add_globals(self, special_forms=None):
    "Add some Scheme standard procedures."
    if special_forms is None:
        special_forms = SPECIAL_FORMS
    self.update(special_forms)
    return self
