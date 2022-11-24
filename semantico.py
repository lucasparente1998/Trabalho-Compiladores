from sintatico import analisador

TypeList = [('Object', None, [('abort',[],'Object'),('type_name',[],'String'),('copy',[],'SELF_TYPE')], []),
        ('SELF_TYPE',None,[],[]),
        ('IO', 'Object', [('out_string',[('x','String')],'SELF_TYPE'),('out_int',[('x','Int')],'SELF_TYPE'),('in_string',[],'String'),('in_int',[],'Int')], []),
        ('Int', 'IO', [], []),
        ('String', 'IO', [('length',[],'Int'),('concat',[('s','String')],'String'),('substr',[('i','Int'), ('l','Int')],'String')], []),
        ('Bool', 'IO', [], [])]
MethodsList=[]
IDsList=[]


for Type in TypeList:
    for method in Type[2]:
        MethodsList.append(method)

for Type in TypeList:
    for ID in Type[3]:
        IDsList.append(ID)

def percorrerArv(t):
    if type(t) == list or type(t) == tuple:
        for son in t:
            percorrerArv(son)
        print(t[0])
print(analisador)
