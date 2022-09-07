import lex

keywords = {
  'class':'class',
  'else': 'else',
  'false': 'false',
  'fi': 'fi',
  'if': 'if',
  'in': 'in',
  'inherits': 'inherits',
  'isvoid': 'isvoid',
  'let': 'let',
  'loop':'loop',
  'pool':'poll',
  'then':'then',
  'while':'while',
  'case':'case',
  'esac':'esac',
  'new':'new',
  'of':'of',
  'not':'not',
  'true':'true'
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
  'FECHACHAVES'
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
    r'\"[\w_\W]*\"'
    return t

def t_NOVALINHA(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
    print(f'Caractere ilegal {t.value[0]!r}')
    t.lexer.skip(1)

###################################################

data = '''
class Main inherits IO {
    main(): Object {
        let hello:String <- "Hello, ",
            name: String <- "",
            ending: String <- "!\n"
        in {
            out_string("Please enter your name:\n");
            name <- in_string();
            out_string(hello.concat(name.concat(ending)));
        }
    };
};'''

lexer = lex.lex()
lexer.input(data)
while True:
  tok = lexer.token()
  if not tok:
    break
  print(tok)
