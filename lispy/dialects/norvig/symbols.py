class Symbol(str):
    pass


def Sym(s, symbol_table={}):
    "Find or create unique Symbol entry for str s in symbol table."
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)
    return symbol_table[s]

EOF_OBJECT = Symbol('#<eof-object>')  # Note: uninterned; can't be read

QUOTE_SYMBOL, IF_SYMBOL, SET_SYMBOL, DEFINE_SYMBOL, LAMBDA_SYMBOL, BEGIN_SYMBOL, DEFINEMACRO_SYMBOL, QUASIQUOTE_SYMBOL, UNQUOTE_SYMBOL, UNQUOTESPLICING_SYMBOL = map(
    Sym,
    "quote   if   set!  define   lambda   begin   define-macro quasiquote   unquote   unquote-splicing".split())

APPEND_SYMBOL, CONS_SYMBOL, LET_SYMBOL = map(Sym, "append cons let".split())

QUOTES = {
    "'": QUOTE_SYMBOL,
    "`": QUASIQUOTE_SYMBOL,
    ",": UNQUOTE_SYMBOL,
    ",@": UNQUOTESPLICING_SYMBOL
}


def atom(token):
    """
    Numbers become numbers; #t and #f are booleans; "..." string;
    otherwise Symbol.
    """
    if token == '#t':
        return True
    elif token == '#f':
        return False
    elif token[0] == '"':
        return token[1:-1].decode('string_escape')
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            try:
                return complex(token.replace('i', 'j', 1))
            except ValueError:
                return Sym(token)
