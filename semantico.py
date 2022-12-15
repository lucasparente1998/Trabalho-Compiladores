from sintatico import analisador
import copy
from geracao_de_codigo import *

Tipos = [('Object', None, [
                ('abort', [], 'Object'),
                ('type_name', [], 'String'), 
                ('copy', [], 'SELF_TYPE')], 
                [('self', 'Object')]), 
            ('IO', 'Object', [
                ('out_string', [('x', 'String')], 'SELF_TYPE'), 
                ('out_int', [('x', 'Int')], 'SELF_TYPE'),
                ('in_string', [], 'String'), 
                ('in_int', [], 'Int')], []), 
            ('String', 'IO', [
                ('length', [], 'Int'), 
                ('concat', [('s', 'String')], 'String'), 
                ('substr', [('i', 'Int'), ('l', 'Int')], 'String')], []), 
            ('Int', 'IO', [], []), 
            ('Bool', 'IO', [], []),
            ('SELF_TYPE', None, [], [])]

Metodos = []
IDs = []

traducao = ''

scope = 'program'

for tipo in Tipos:
    for metodo in tipo[2]:
        Metodos.append(metodo)

for tipo in Tipos:
    for ID in tipo[3]:
        IDs.append(ID)

def identificar( t, IDs, Metodos, Tipos ):
    if t == None:
        return

    TiposNovo = []
    IDsNovo = []
    MetodosNovo = []
    TiposNovo = Tipos

    global traducao

    if EhClasse(t[0]):
        global scope
        scope = t[1]
        MetodosNovo = copy.deepcopy(Metodos)
        IDsNovo = IDs
    elif EhMetodo(t[0]) or EhLet(t[0]):
        IDsNovo = copy.deepcopy(IDs)
        MetodosNovo = Metodos
    else:
        TiposNovo = Tipos
        IDsNovo = IDs
        MetodosNovo = Metodos

    if t[0] == 'cs':
        for formal in t[2]:
            identificar(formal, IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'csInh':
        tratarCsInh(t, TiposNovo)
        for formal in t[3]:
            if type(formal) == list:
                for i in formal:
                    identificar(i, IDsNovo, MetodosNovo, TiposNovo)
            else:
                identificar(formal, IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'featureParametro':
        traducao = traducao + featureParametro(t)
        tratarFeatureParametro(t, IDsNovo, MetodosNovo, TiposNovo)
        for formal in t[4]:
            identificar(formal, IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'featureReturn':
        tratarFeatureReturn(t, MetodosNovo, TiposNovo)
        identificar(t[3], IDsNovo, MetodosNovo, TiposNovo)
        traducao = traducao + featureClass(t)
    elif t[0] == 'feature':
        tratarfeatureAnonimos(t, IDsNovo, TiposNovo)
        for formal in t[2]:
            identificar(formal, IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'featureDeclaration':
        tratarFeatureDeclaration(t, IDsNovo, TiposNovo)
    elif t[0] == 'formal':
        tratarFormal(t, IDsNovo, TiposNovo)
    elif t[0] == 'exprValor':
        tratarExprValor(t, IDsNovo)
    elif t[0] == 'exprNew':
        tratarExprNew(t, IDsNovo)
    elif t[0] == 'exprIsVoid':
        tratarExprVoid(t, IDsNovo)
    elif t[0] == 'exprNot':
        tratarExprNot(t, IDsNovo)
    elif t[0] == 'comp':
        tratarComp(t, IDsNovo)
    elif t[0] == 'oper':
        tratarOper(t, IDsNovo)
    elif t[0] == 'exprAtri':
        tratarExprAtri(t, IDsNovo)
    elif t[0] == 'exprpar':
        identificar(t[1], IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'exprChamaMetodo':
        tratarExprChamaMetodo(t, MetodosNovo, IDsNovo)
    elif t[0] == 'exprIf':
        tratarExprIf(t, IDsNovo)
        identificar(t[2], IDsNovo, MetodosNovo, TiposNovo)
        identificar(t[3], IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'exprWhile':
        tratarExprWhile(t, IDsNovo)
        identificar(t[3], IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'exprLista':
        identificar(t[1], IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'exprLet':
        tratarExprLet(t, IDsNovo, TiposNovo)
        identificar(t[4], IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'exprType':
        tratarExprType(t, IDsNovo, TiposNovo)
        identificar(t[5], IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'exprcase':
        tratarExprCase(t, IDs, TiposNovo)
    elif t[0] == 'exprArroba':
        tratarExprArroba(t, IDs, Metodos, Tipos)
        identificar(t[1], IDsNovo, MetodosNovo, TiposNovo)
    elif t[0] == 'exprSemArroba':
        tratarExprSemArroba(t, IDs, Metodos, Tipos)
        identificar(t[1], IDsNovo, MetodosNovo, TiposNovo)
    else:
        if type(t) == list:
            for i in t:
                identificar(i, IDsNovo, MetodosNovo, TiposNovo)

def EhClasse(s):
    return s == 'csInh' or s == 'cs'

def EhMetodo( s ):
    return s == 'featureParametro' or s == 'featureReturn'

def EhLet( s ):
    return s == 'exprLet2' or s == 'exprLet'

def tratarCsInh( t, Tipos ):
    inherits = getType(t[2], Tipos)
    classe = getType(t[1], Tipos)
    if inherits == None:
        print("Erro Semântico: Tipo '%s' não declarado" % t[2])
    else:
        for metodo in inherits[2]:
            classe[2].append(metodo)
        for id in inherits[3]:
            classe[3].append(id)

def tratarFeatureParametro( t, IDs, Metodos, Tipos ):
    if isInListMetodo(t[1], Metodos):
        print("Erro Semântico: método %s já declarado" % t[1])
    if not isInListType(t[3], Tipos):
        print("Erro Semântico: tipo %s não foi declarado" % t[3])
    verificaParametro(t[2], Tipos)
    metodo = (t[1], [], t[3])
    tipo = getType(scope, Tipos)
    if tipo != None:
        tipo[2].append(metodo)
    for id in t[2]:
        newId = (id[1], id[2])
        IDs.append(newId)
        metodo[1].append(newId)
    Metodos.append(metodo)

def tratarFeatureReturn( t, Metodos, Tipos ):
    if isInListMetodo(t[1], Metodos):
        print("Erro Semântico: método %s já declarado" % t[1])
    if not isInListType(t[2], Tipos):
        print("Erro Semântico: tipo %s não foi declarado" % t[2])
    metodo = (t[1], [], t[2])
    tipo = getType(scope, Tipos)
    if tipo != None:
        tipo[2].append(metodo)
    Metodos.append(metodo)

def tratarfeatureAnonimos( t, IDs, Tipos ):
    if isInListId(t[1], IDs):
        print("Erro Semântico: variavel %s já declarada" % t[1])
    if not isInListType(t[2], Tipos):
        print("Erro Semântico: tipo %s não foi declarado" % t[2])
    if t[2] == 'String':
        if type(t[3][1]) != str:
            print("Erro Semântico: valor incompativel com a variavel %s" % t[1])
    if t[2] == 'Int':
        if type(t[3][1]) != int:
            print("Erro Semântico: valor incompativel com a variavel %s" % t[1])

    IDs.append((t[1], t[2]))

def tratarFeatureDeclaration( t, IDs, Tipos ):
    if isInListId(t[1], IDs):
        print("Erro Semântico: variavel %s já declarada" % t[1])
    if not isInListType(t[2], Tipos):
        print("Erro Semântico: tipo %s não foi declarado" % t[2])
    IDs.append((t[1], t[2]))

def tratarFormal( t, IDs, Tipos ):
    if isInListId(t[1], IDs):
        print("Erro Semântico: %s já declarado" % t[1])
    if not isInListType(t[2], Tipos):
        print("Erro Semântico: tipo %s não foi declarado" % t[2])
    IDs.append((t[1], t[2]))

def tratarExprValor( t, IDs ):
    if not isInListId(t[1], IDs):
        print("Erro Semântico: %s não foi declarado" % t[1])

def tratarExprNew( t, Tipos ):
    if not isInListType(t[2], Tipos):
        print("Erro Semântico: tipo %s não foi declarado" % t[2])

def tratarExprVoid( t, IDs ):
    if not isInListId(t[2], IDs):
        print("Erro Semântico: %s não foi declarado" % t[2])

def tratarExprNot( t, IDs ):
    if t[2][0] == 'comp':
        tratarComp(t[2], IDs)
        return
    print("Erro Semântico: expressão %s não é booleano" % t[2])

def tratarComp( t, IDs ):
    if t[2][0] == 'exprNotVoidCompNew':
        id1 = getId(t[2][2][1], IDs)
    elif t[2][0] == 'oper':
        tratarOper(t[2], IDs)
        id1 = (0, 'Int')
    else:
        id1 = getId(t[2][1], IDs)
    if t[3][0] == 'exprNotVoidCompNew':
        id2 = getId(t[3][2][1], IDs)
    elif t[3][0] == 'oper':
        tratarOper(t[3], IDs)
        id2 = (0, 'Int')
    else:
        id2 = getId(t[3][1], IDs)

    if id1 == None:
        if type(tryConvertInt(t[2][1])) != int:
            print("Erro Semântico: %s não foi declarado" % t[2][1])
        id1 = (str(tryConvertInt(t[2][1])), 'Int')
    if id2 == None:
        if type(tryConvertInt(t[3][1])) != int:
            print("Erro Semântico: %s não foi declarado" % t[3][1])
        id2 = (str(tryConvertInt(t[3][1])), 'Int')
    if id1[1] != id2[1]:
        print("Erro Semântico: %s %s devem ser do mesmo tipo" % id1[0], id2[0])

def tratarOper( t, IDs ):
    id1 = getId(t[2], IDs)
    id2 = getId(t[3], IDs)

    if id1 == None:
        tryParseInt(t[2][1], IDs)
    elif id1[1] != "Int":
        print("Erro Semântico: %s deve ser do tipo Int" % id1[0])
    if id2 == None:
        tryParseInt(t[3][1], IDs)
    elif id2[1] != "Int":
        print("Erro Semântico: %s deve ser do tipo Int" % id2[0])

def tratarExprAtri( t, IDs ):
    if getId(t[1], IDs) == None:
        print("Erro Semântico: %s não foi declarada" % t[1])
    elif t[3][0] == 'op':
        tratarOper(t[3], IDs)
    elif t[3][0] == 'exprValor':
        id = getId(t[3][1], IDs)
        if id == None:
            print("Erro Semântico: %s não foi declarada" % t[3][1])
    return t[1]

def tratarExprChamaMetodo( t, Metodos, IDs ):
    if not isInListMetodo(t[1], Metodos):
        print("Erro Semântico: metodo %s não declarado" % t[1])
    verificaParametroCall(t[2], getMetodo(t[1], Metodos), IDs)

def tratarExprIf( t, IDs ):
    if t[1][0] == 'comp':
        tratarComp(t[1], IDs)
        return
    if t[1][0] == 'exprNotVoidCompNew':
        tratarExprNot(t[1], IDs)
        return
    print("Erro Semântico: expressão %s não é booleano" % t[1])

def tratarExprWhile( t, IDs ):
    if t[1][0] == 'comp':
        tratarComp(t[1], IDs)
        return
    if t[1][0] == 'exprNotVoidCompNew':
        tratarExprNot(t[1], IDs)
        return
    print('Erro Semântico: expressão {t[1]} não é booleano')

def tratarExprLet( t, IDs, Tipos ):
    aux = ('featureDeclaration', t[1], t[2])
    tratarFeatureDeclaration(aux, IDs, Tipos)
    for f in t[3]:
        if f != None:
            tratarExprCase(f, IDs, Tipos)

def tratarExprType( t, IDs, Tipos ):
    aux = ('feature', t[1], t[2])
    tratarfeatureAnonimos(aux, IDs, Tipos)
    for f in t[3]:
        if f != None:
            tratarExprCase(f, IDs, Tipos)

def tratarExprCase( t, IDs, Tipos ):
    if len(t) == 4:
        aux = ('feature', t[1], t[2], t[3])
        tratarfeatureAnonimos(aux, IDs, Tipos)
    elif len(t) == 3:
        aux = ('featureDeclaration', t[1], t[2])
        tratarFeatureDeclaration(aux, IDs, Tipos)
    pass

def tratarExprArroba(t, IDs, Metodos, Tipos):
    nome = None
    NomeDoMetodo = None
    if t[1][0] == 'exprChamaMetodo':
        nome = getMetodo(t[1][1], Metodos)[2]
        NomeDoMetodo = t[1][1]
    else:
        aux = getId(t[1][1], IDs)
        NomeDoMetodo = t[2][1]
        if aux != None:
            nome = aux[1]
    if nome != None:
        tipo = getType(nome, Tipos)
        if nome == 'SELF_TYPE':
            configSelfType(IDs, Metodos, Tipos)
        if not isInListMetodo(t[2][1], tipo[2]):
            print("Erro Semântico: metodo %s não pertence ao tipo %s" % NomeDoMetodo, nome)

def tratarExprSemArroba(t, IDs, Metodos, Tipos):
    nome = None
    NomeDoMetodo = None
    if t[1][0] == 'exprChamaMetodo':
        nome = getMetodo(t[1][1], Metodos)[2]
        NomeDoMetodo = t[1][1]
    else:
        aux = getId(t[1][1], IDs)
        NomeDoMetodo = t[2][1]
        if aux != None:
            nome = aux[1]
    if nome != None:
        tipo = getType(nome, Tipos)
        if nome == 'SELF_TYPE':
            configSelfType(IDs, Metodos, Tipos)
        if not isInListMetodo(NomeDoMetodo, tipo[2]):
            print("Erro Semântico: metodo %s não pertence ao tipo %s" % NomeDoMetodo, nome)

def isInListType( item, lista ):
    for i in lista:
        if item == i[0]:
            return True
    return False

def isInListId( item, lista ):
    for i in lista:
        if item == i[0]:
            return True
    return False

def isInListMetodo( metodo, lista ):
    for i in lista:
        if metodo == i[0]:
            return True
    return False

def getId( nome, lista ):
    for item in lista:
        if item[0] == nome:
            return item
    return None

def getMetodo( nome, Metodos ):
    for metodo in Metodos:
        if nome == metodo[0]:
            return metodo
    return None

def getType( nome, Tipos ):
    for tipo in Tipos:
        if nome == tipo[0]:
            return tipo
    return None

def tryParseInt( valor, IDs ):
    try:
        valor = int(valor)
    except:
        if isInListId(valor, IDs):
            tipo = getId(valor, IDs)[1]
            if tipo == 'Int':
                return
        print(f'Erro Semântico:: {valor} não é do tipo inteiro')

def tryConvertInt( s ):
    try:
        return int(s)
    except:
        return s

def verificaParametro( parametros, Tipos ):
    idsParametros = []
    for parametro in parametros:
        if not isInListType(parametro[2], Tipos):
            print("Erro Semântico: tipo %s não foi declarado" % parametro[2])
        if parametro[1] in idsParametros:
            print("Erro Semântico: id %s já utilizado por outro parametro" % parametro[1])
        idsParametros.append(parametro[1])

def verificaParametroCall( parametros, metodo, IDs ):
    if parametros[0] == None:
        del (parametros[0])
    if len(parametros) != len(metodo[1]):
        print("Erro Semântico: metodo %s deve conter %d parametros" % metodo[0], len(metodo[1]))
    for i in range(0, len(parametros)):
        if not isInListId(parametros[i][1], IDs):
            if metodo[1][i][1] == 'Int':
                tryParseInt(parametros[i][1], IDs)
            elif metodo[1][i][1] != 'String':
                print(f'Erro Semântico: parametro {parametros[i][1]} de tipo incorreto')
            if parametros[i][0] != 'exprValor':
                print(f'Erro Semântico: id {parametros[i][1]} não foi declarado')
        else:
            parametro = getId(parametros[i][1], IDs)
            if parametro[1] != metodo[1][i][1]:
                print("Erro Semântico: parametro %s de tipo incorreto" % parametros[i][1])

def configSelfType( IDs, Metodos, Tipos ):
    selftype = getType('SELF_TYPE', Tipos)
    selftype[2].clear()
    selftype[3].clear()
    for metodo in Metodos:
        selftype[2].append(metodo)
    for id in IDs:
        selftype[3].append(id)

for filho in analisador[0]:
    if type(filho) == tuple:
        if isInListType(filho[1], Tipos):
            print("Erro Semântico: tipo %s já foi declarado" % filho[1])
        if filho[0] == 'cs':
            Tipos.append((filho[1], None, [], []))
        elif filho[0] == 'csInh':
            Tipos.append((filho[1], filho[2], [], []))

for filho in analisador[0]:
    identificar(filho, IDs, Metodos, Tipos)

print(traducao)
