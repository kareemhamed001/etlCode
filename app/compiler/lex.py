from ply.lex import TOKEN

# To handle reserved words
reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'into': 'INTO',
    'where': 'WHERE',
    'like': 'LIKE',
    'insert': 'INSERT',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'distinct': 'DISTINCT',
    'order': 'ORDER',
    'by': 'BY',
    'asc': 'ASC',
    'desc': 'DESC',
    'limit': 'LIMIT',
    'values': 'VALUES',
    'update': 'UPDATE',
    'set': 'SET',
    'delete': 'DELETE',
    'run': 'RUN',
    'train':'TRAIN',
    'model':'MODEL',
    'using':'USING',
    'framedir':'FRAMEDIR'
}

tokens = [
             'NUMBER',
             'PLUS',
             'MINUS',
             'TIMES',
             'DIVIDE',
             'PERCENT',
             'LPAREN',
             'RPAREN',
             'COLNAME',
             'DATASOURCE',
             'EQUAL',
             'NOTEQUAL',
             'BIGGER_EQUAL',
             'BIGGER',
             'SMALLER_EQUAL',
             'SMALLER',
             'SIMICOLON',
             'COMMA',
             'STRING',
             'PATTERN',
             'COLNUMBER',
             'MODELNAME',
         ] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PERCENT = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUAL = r'='
t_NOTEQUAL = r'<>'
t_BIGGER_EQUAL = r'>='
t_BIGGER = r'>'
t_SMALLER_EQUAL = r'<='
t_SMALLER = r'<'
t_SIMICOLON = r';'
t_COMMA = r','

# ignored characters 
t_ignore = ' \t'  # Spaces and tabs
t_ignore_COMMENT = r'/\*.*\*/'  # Comment

digit = r'([0-9])'
nondigit = r'([_A-Za-z])'
identifier = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'
identifier = identifier + r'|' + r'\[' + digit + r'+\]'


@TOKEN(r'[a-zA-Z][a-zA-Z0-9_]*')
def t_MODELNAME(t):
    t.type = reserved.get(t.value, 'MODELNAME')  # Check for reserved words
    t.value = str(t.value)
    return t

@TOKEN('\[[a-zA-Z][a-zA-Z0-9_,]*\]')
def t_COLNAME(t):
    t.type = reserved.get(t.value, 'COLNAME')  # Check for reserved words
    return t


@TOKEN(r'"([^"\n])*"')
def t_STRING(t):
    t.value = str(t.value.title())[1:-1]
    return t


@TOKEN(r'\[\d+\]')
def t_COLNUMBER(t):
    t.value = int(t.value[1:-1])
    return t


@TOKEN(r'\d+')
def t_NUMBER(t):
    t.value = int(t.value)
    return t


@TOKEN(r'\[[^,\]\[]+\]')
def t_DATASOURCE(t):
    t.value = str(t.value[1:-1])
    return t


@TOKEN(r'\n+')
def t_newline(t):
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print(f"Illegal entity {t.value}")
    t.lexer.skip(1)
