import sys
import operator

# Python 3 gives us more fine grained division operators
if sys.version_info[0] > 2:
    division_function = operator.truediv
else:
    division_function = operator.div
    

SPECIAL_FORMS = {
    '+':operator.add,
    '-':operator.sub,
    '*':operator.mul,
    '/':division_function,
    'not':operator.not_,
    '>':operator.gt,
    '<':operator.lt,
    '>=':operator.ge,
    '<=':operator.le,
    '=':operator.eq, 
    'equal?':operator.eq,
    'eq?':operator.is_,
    'length':len,
    'cons':lambda x,y:[x]+y,
    'car':lambda x:x[0],
    'cdr':lambda x:x[1:],
    'append':operator.add,  
    'list':lambda *x:list(x),
    'list?': lambda x:isa(x,list), 
    'null?':lambda x:x==[],
    'symbol?':lambda x: isa(x, Symbol),
    'pyeval': lambda x: eval(x),
    'true': True,
    'false': False
}
