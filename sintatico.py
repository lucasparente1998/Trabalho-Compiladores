from lexico import tokens, lexer
from ply.yacc import yacc



VERBOSE = 1

def p_program(p):
    'program : classlist'
    p[0] = [p[1]]
    pass

def p_classlist(p):
    '''classlist : classlist cs PONTOEVIRGULA
     | cs PONTOEVIRGULA'''
    if len(p) == 3:
        p[0] = [p[1]]
    else: 
        p[0] = p[1]
        p[0].append(p[2])
    pass

def p_cs(p):
    '''cs : CLASS ID ABRECHAVES featurelist FECHACHAVES
     | CLASS ID INHERITS ID ABRECHAVES featurelist FECHACHAVES'''
    if len(p) == 6:
        p[0] = ('cs', p[2], p[4])
    else:
        p[0] = ('csInh', p[2], p[4], p[6])
    pass

def p_featurelist(p):
    '''featurelist : featurelist feature PONTOEVIRGULA
     | empty'''
    
    if len(p) == 2:
        p[0] = None
    else:
        p[0] = [p[1]]
        p[0].append(p[2])
    pass

def p_feature(p):
    '''feature : ID ABREPARENTESES formallist FECHAPARENTESES DOISPONTOS ID ABRECHAVES expr FECHACHAVES 
                | ID ABREPARENTESES FECHAPARENTESES DOISPONTOS ID ABRECHAVES expr FECHACHAVES
                | ID DOISPONTOS ID ATRIBUICAO expr 
                | ID DOISPONTOS ID 
                | empty'''
    if len(p) == 10:
        p[0] = ('featureParametro',p[1],p[3],p[6],p[8])
    elif len(p) == 9:
        p[0] = ('featureReturn',p[1],p[5],p[7])
    elif len(p) == 6:
        p[0] = ('feature',p[1],p[3],p[5])
    elif len(p) == 4:
        p[0] = ('featureDeclaration',p[1],p[3])
    elif len(p) == 2:
        p[0] = None
    pass

def p_formallist(p):
    '''formallist : formallist VIRGULA formal
     | empty
     | formal'''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = None
    pass

def p_formal(p):
    'formal : ID DOISPONTOS ID'
    p[0] = ('formal', p[1], p[3])
    pass

def p_expr_novo(p):
    'expr : NEW ID'
    p[0] = ('exprNew', p[1], p[2])
    pass

def p_expr_void(p):
    'expr : ISVOID expr'
    p[0] = ('exprIsVoid', p[1], p[2])
    pass

def p_ex_not_comp(p):
    '''expr : NOT expr
            | COMPLEMENTO expr '''
    p[0] = ('exprNot', p[1], p[2])
    pass

def p_ex_1(p):
    '''expr : STRING
            | TRUE
            | FALSE
            '''
    p[0] = ('exprValor', p[1])
    pass

def p_ex_num(p):
    'expr : NUMERO'
    p[0] = ('expValor', tryParseInt(p[1]))
    pass

def p_ex_id(p):
    'expr : ID'
    p[0] = ('exprID', p[1])
    pass
def p_expr_comp(p):
    '''expr : expr MENOR expr
     | expr MENORIGUAL expr
     | expr IGUAL expr'''
    p[0] = ('comp',p[2], p[1], p[3])
    pass

def p_expr_oper(p):
    '''expr : expr MAIS expr
     | expr MENOS expr 
     | expr MULTIPLICACAO expr
     | expr DIVISAO expr'''
    p[0] = ('oper',p[2], p[1], p[3])
    pass

def p_expr_atri(p):
    'expr : ID ATRIBUICAO expr'
    p[0] = ('exprAtri', p[1], p[2], p[3])
    pass

def p_expr_par(p):
    'expr : ABREPARENTESES expr FECHAPARENTESES'
    p[0] = ('exprpar', p[2])
    pass

def p_expr_arroba(p):
    '''expr : expr ARROBA ID PONTO expr
            | expr PONTO expr '''
    if len(p) == 9:
        p[0] = ('exprArroba', p[1], p[3], p[5])
    else:
        p[0] = ('exprSemArroba', p[1], p[3])
    pass

def p_expr_id(p):
    'expr : ID ABREPARENTESES exprlist FECHAPARENTESES'
    p[0] = ('exprChamaMetodo', p[1], p[3])
    pass

def p_expr_if(p):
    'expr : IF expr THEN expr ELSE expr FI'
    p[0] = ('exprIf', p[2], p[4], p[6])
    pass

def p_expr_while(p):
    'expr : WHILE expr LOOP expr POOL'
    p[0] = ('exprWhile', p[2], p[4])
    pass

def p_expr_lista(p):
    'expr : ABRECHAVES exprlista FECHACHAVES'
    p[0] = ('exprLista',p[2])
    pass

def p_expr_let(p):
    '''expr : LET ID DOISPONTOS ID exprlistlet IN expr
     | LET ID DOISPONTOS ID ATRIBUICAO expr exprlistlet IN expr'''

    if len(p) == 8:
        p[0] = ('exprLet', p[2], p[4], p[5], p[7])
    else:
        p[0] = ('exprLet2', p[2], p[4], p[6], p[7], p[9])
    pass

def p_expr_case(p):
    'expr : CASE expr OF exprlistcase ESAC'
    p[0] = ('exprCase', p[2], p[4])
    pass

def p_exprlista(p):
    '''exprlista : exprlista expr PONTOEVIRGULA
     | expr PONTOEVIRGULA'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[2])
    pass

def p_exprlist(p):
    '''exprlist : exprlist VIRGULA expr
     | expr
     | empty'''
    
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = None
    pass

def p_exprlistlet(p):
    '''exprlistlet : exprlistlet letexpr  
     | letexpr'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass

def p_letexpr(p):
    '''letexpr : VIRGULA ID DOISPONTOS ID 
     | VIRGULA ID DOISPONTOS ID ATRIBUICAO expr
     | empty'''
    
    if len(p) == 5:
        p[0] = ('exprType', p[2], p[4])
    elif len(p) == 7:
        p[0] = ('exprType', p[2], p[4],p[6])
    else:
        p[0] = None
    pass


def p_exprlistcase(p):
    '''exprlistcase : exprlistcase exprcase
     | exprcase'''
    if len(p) == 3:
        p[0] = p[1]
        p[0].append(p[2])
    else:
        p[0] = [p[1]]
    pass 

def p_exprcase(p):
    'exprcase : ID DOISPONTOS ID SETA expr PONTOEVIRGULA'
    p[0] = ('exprcase', p[1], p[3], p[5])
    pass

def p_empty(p):
    'empty :'
    pass

def tryParseInt(s):
    try:
        return int(s)
    except:
        return s

def p_error(p):
    if VERBOSE:
        print ("Error no Sintatico linha:" + str(lexer.lineno)+ " .Token " + str(p.value) + " diferente do esperado. ")
      
    else:
        raise Exception('Syntax', 'error')

parser = yacc()

fin = 'testes.cl'
f = open(fin,'r')
data = f.read()
analisador = parser.parse(data, lexer=lexer)



