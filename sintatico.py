from lexico import tokens, lexer
from ply.yacc import yacc

VERBOSE = 1

def p_program(p):
    '''program : classlist 
     | empty'''
    pass
def p_classlist(p):
    '''classlist : classlist cs PONTOEVIRGULA
     | cs PONTOEVIRGULA'''
    pass

def p_cs(p):
    '''cs : CLASS ID ABRECHAVES featurelist FECHACHAVES
     | CLASS ID INHERITS ID ABRECHAVES featurelist FECHACHAVES'''
    pass

def p_featurelist(p):
    '''featurelist : featurelist feature PONTOEVIRGULA
     | empty'''
    pass

def p_feature_1(p):
    'feature : ID ABREPARENTESES formallist FECHAPARENTESES DOISPONTOS ID ABRECHAVES expr FECHACHAVES'
    pass

def p_feature_2(p):
    '''feature : ID DOISPONTOS ID
     | ID DOISPONTOS ID ATRIBUICAO expr
     | empty'''

def p_formallist(p):
    '''formallist : formallist VIRGULA formal
     | empty
     | formal'''
    pass

def p_formal(p):
    'formal : ID DOISPONTOS ID'
    pass

def p_expr(p):
    '''expr : ID ATRIBUICAO expr
     | expr PONTO ID ABREPARENTESES FECHAPARENTESES
     | expr ARROBA ID PONTO ID ABREPARENTESES FECHAPARENTESES
     | expr ARROBA ID PONTO ID ABREPARENTESES exprlist FECHAPARENTESES
     | expr PONTO ID ABREPARENTESES exprlist FECHAPARENTESES
     | ID ABREPARENTESES FECHAPARENTESES
     | ID ABREPARENTESES exprlist FECHAPARENTESES
     | IF expr THEN expr ELSE expr FI
     | WHILE expr LOOP expr POOL
     | ABRECHAVES exprlista FECHACHAVES
     | LET ID DOISPONTOS ID exprlistlet IN expr
     | LET ID DOISPONTOS ID ATRIBUICAO expr exprlistlet IN expr
     | CASE expr OF exprlistcase ESAC
     | NEW ID
     | ISVOID expr
     | expr MAIS expr
     | expr MENOS expr 
     | expr MULTIPLICACAO expr
     | expr DIVISAO expr
     | COMPLEMENTO expr
     | expr MENOR expr
     | expr MENORIGUAL expr
     | expr IGUAL expr
     | NOT expr
     | ABREPARENTESES expr FECHAPARENTESES
     | ID
     | NUMERO
     | STRING
     | TRUE
     | FALSE'''
    pass

# def p_expr_2(p):
#     '''expr : expr PONTO ID ABREPARENTESES FECHAPARENTESES
#      | expr ARROBA ID PONTO ID ABREPARENTESES FECHAPARENTESES
#      | expr ARROBA ID PONTO ID ABREPARENTESES exprlist FECHAPARENTESES
#      | expr PONTO ID ABREPARENTESES exprlist FECHAPARENTESES '''
#     pass
# def p_expr_3(p):
#     '''expr : ID ABREPARENTESES FECHAPARENTESES
#      | ID ABREPARENTESES exprlist FECHAPARENTESES'''
#     pass

# def p_expr_4(p):
#     '''expr : LET ID DOISPONTOS ID exprlistlet IN expr
#      | LET ID DOISPONTOS ID ATRIBUICAO exprlistlet IN expr'''
#     pass

def p_exprlista(p):
    '''exprlista : exprlista expr PONTOEVIRGULA
     | expr PONTOEVIRGULA'''
    pass

def p_exprlist(p):
    '''exprlist : exprlist VIRGULA expr
     | empty
     | expr'''
    pass

def p_exprlistlet(p):
    '''exprlistlet : exprlistlet letexpr  
     | letexpr'''
    pass

def p_letexpr(p):
    '''letexpr : VIRGULA ID DOISPONTOS ID 
     | VIRGULA ID DOISPONTOS ID ATRIBUICAO expr
     | empty'''
    pass


def p_exprlistcase(p):
    '''exprlistcase : exprlistcase exprcase
     | exprcase'''
    pass

def p_exprcase(p):
    'exprcase : ID DOISPONTOS ID SETA expr PONTOEVIRGULA'
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if VERBOSE:
        if p is not None:
            print ("Error no Sintatico linha:" + str(lexer.lineno)+"  Error de Contexto " + str(p.value))
        else:
            print ("Error no Lexico linha: " + str(lexer.lineno))
    else:
        raise Exception('Syntax', 'error')

parser = yacc()

fin = 'programa3.cl'
f = open(fin,'r')
data = f.read()
#"print (data)
#parser.parse(data, tracking=True)
aux = parser.parse(data, lexer=lexer)
print(aux)


