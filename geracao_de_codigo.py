from sintatico import analisador


def featureClass(t):
    traducao = '@' + str(t[1]) + '()'
    return traducao

def featureParametro(t):
    traducao = '@' + str(t[1]) + '(' 
    for i in t[2]:
        traducao += str(i[1]) + ':' + str(i[2]) + ','
    traducao = traducao[:-2] + ')'
    return traducao


