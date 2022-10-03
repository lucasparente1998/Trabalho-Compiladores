import lex

keywords = {
    'class': 'CLASS',
    'else': 'ELSE',
    'false': 'FALSE',
    'fi': 'FI',
    'if': 'IF',
    'in': 'IN',
    'inherits': 'INHERITS',
    'isvoid': 'ISVOID',
    'let': 'LET',
    'loop': 'LOOP',
    'pool': 'POOL',
    'then': 'THEN',
    'while': 'WHILE',
    'case': 'CASE',
    'esac': 'ESAC',
    'new': 'NEW',
    'of': 'OF',
    'not': 'NOT',
    'true': 'TRUE'
}


tokens = [
    'ID',
    'NUMERO',
    'STRING',
    'MAIS',
    'MENOS',
    'MULTIPLICACAO',
    'DIVISAO',
    'IGUAL',
    'MENORIGUAL',
    'MENOR',
    'PONTO',
    'DOISPONTOS',
    'PONTOEVIRGULA',
    'VIRGULA',
    'ATRIBUICAO',
    'ABREPARENTESES',
    'FECHAPARENTESES',
    'ABRECHAVES',
    'FECHACHAVES',
    'COMPLEMENTO',
    'ARROBA',
    'SETA'
] + list(keywords.values())


t_MAIS = r'\+'
t_MENOS = r'\-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'\/'
t_IGUAL = r'\='
t_MENORIGUAL = r'\<\='
t_MENOR = r'\<'
t_PONTO = r'\.'
t_DOISPONTOS = r'\:'
t_PONTOEVIRGULA = r'\;'
t_VIRGULA = r'\,'
t_ATRIBUICAO = r'\<\-'
t_ABREPARENTESES = r'\('
t_FECHAPARENTESES = r'\)'
t_ABRECHAVES = r'\{'
t_FECHACHAVES = r'\}'
t_COMPLEMENTO = r'\~'
t_ARROBA = r'\@'
t_SETA = r'\=\>'

t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-z_][a-zA-Z_0-9]*'
    if t.value in keywords:
        t.type = t.value.upper()
    else:
        t.type = 'ID'
    return t


def t_NUMERO(t):
    r'\d+'
    return t


def t_STRING(t):
    r'\"[^"]*\"'
    return t


def t_COMMENT_BLOCO(t):
    r'(\(\*(.|\n)*?\*\))'
    t.lexer.lineno += t.value.count('\n')

def t_COMMENT_LINHA(t):
    r'\-\-[^-][^-]*\-\-'
    


def t_NOVALINHA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f'Caractere ilegal {t.value[0]!r}')
    t.lexer.skip(1)

###################################################


lexer = lex.lex()