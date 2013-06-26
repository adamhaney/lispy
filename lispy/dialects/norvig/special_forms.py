import operator

SPECIAL_FORMS = {
    '+':operator.add,
    '-':operator.sub,
    '*':operator.mul,
    '/':operator.div,
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

    'true': True,
    'false': False
}
