# -*- coding: utf-8 -*-
from random import randint, choice
from itertools import product

### Funcoes auxiliares
def sortear(lista):
    return lista[randint(0,len(lista)-1)]

def gerar_cpf_cnpj(lista):
    cnpj = randint(10000000000, 99999999999)
    while cnpj in lista:
        cnpj = randint(10000000000, 99999999999)
    return cnpj

def gerar_nome_novo(listas_formacao, lista_nomes_existentes):
    nome = []
    for lista in listas_formacao:
        nome.append(sortear(lista))
    while ' '.join(nome) in lista_nomes_existentes:
        nome = []
        for lista in listas_formacao:
            nome.append(sortear(lista))
    return ' '.join(nome)

def gerar_numero_novo(min,max,lista):
    num = randint(min,max)
    while num in lista:
        num = randint(min,max)
    return num

def gerar_combinacoes_questoes(listas,materia,pessoas):
    for i in range(len(listas[-1])):
        listas[-1][i] += '?'
    return [(' '.join(l),choice("ABCDEF"), materia, choice(pessoas)[0]) for l in list(product(*listas))]

### Geradores
PEOPLE_NAMES = ['José','Joselito','Joana','Josefina','Raimundo','Raimunda'] # precisamos de 20 nomes
PEOPLE_SURNAMES = ['da Silva','Silva','Souza','Couto','do Nascimento']  # e de 20 sobrenomes
EMAIL_PROVIDERS = ['gmail','hotmail','yahoo','outlook']
EMAIL_CONNECTORS = ['','.','-','_']

'''
Retorna lista de pessoas = (cpf,nome,email,cnpj)
'''
def gerar_pessoas(quantidade,cnpjs):
    pessoas = []
    cpfs = []
    nomes = []
    emails = []
    for _ in range(quantidade):
        cpfs.append(gerar_cpf_cnpj(cpfs))

        nome = gerar_nome_novo([PEOPLE_NAMES,PEOPLE_SURNAMES], nomes)
        nomes.append(nome)

        partes_nome = nome.split(' ')

        email = partes_nome[0].lower() + sortear(EMAIL_CONNECTORS) + partes_nome[-1].lower() + sortear(['',str(randint(0,999999))]) +'@'+sortear(EMAIL_PROVIDERS)+'.com'
        emails.append(email)

        cnpj = sortear(cnpjs)[0]

        pessoas.append((cpfs[-1],nomes[-1],emails[-1],cnpj))
    return pessoas
    

TIPO_INSTITUICAO_SUPERIOR = ['Faculdade','Universidade']
TIPO_INSTITUICAO_ESCOLA = ['Escola','Colégio']
TIPO_INSTITUICAO = ['Estadual','Federal']
LOCAIS_INSTITUICAO = ['de São Paulo','da Bahia','de Brasilia','do Mato Grosso']

'''
Retorna lista de instituicoes = (cnpj,nome,rank)
'''
def gerar_instituicao_academica(number,escola=True):
    instituicoes = []
    cnpjs = []
    nomes = []
    ranks = []
    for _ in range(number):
        if escola:
            nomes.append(gerar_nome_novo([TIPO_INSTITUICAO_ESCOLA,TIPO_INSTITUICAO,LOCAIS_INSTITUICAO], nomes))
        else:
            nomes.append(gerar_nome_novo([TIPO_INSTITUICAO_SUPERIOR,TIPO_INSTITUICAO,LOCAIS_INSTITUICAO], nomes))

        cnpjs.append(gerar_cpf_cnpj(cnpjs))

        ranks.append(gerar_numero_novo(1,200,ranks))
        instituicoes.append((cnpjs[-1],nomes[-1],ranks[-1]))
    return instituicoes



MATERIAS = ['História','Cálculo','Geografia','Arte','Matemática','Informática']

# Historia - 3
P_HISTORIA1 = ['Como começou']
P_HISTORIA2 = ['a segunda guerra mundial','o Iluminismo','a primeira guerra mundial']
# Calculo - 6
P_CALCULO1 = ['Qual é a']
P_CALCULO2 = ['integral','derivada']
P_CALCULO3 = ['de x','de 1/x','de 12e^6']

# 'Geografia' - 6
P_GEOGRAFIA1 = ['Qual é a capital do/da','Em qual continente fica o/a']
P_GEOGRAFIA2 = ['Itália','estado do Rio Grande do Sul','China']
# Arte - 6
P_ARTE1 = ['Cite uma obra do famosa movimento','Aonde começou o movimento']
P_ARTE2 = ['Renascentista','Barroco','da Arte Moderna']

# Matematica - 5
P_MATEMATICA1 = ['Quanto é']
P_MATEMATICA2 = ['+','-','/','*','^']

# Informatica - 9
P_INFORMATICA1 = ['O que é','Como implementar','Como fazer uma busca em']
P_INFORMATICA2 = ['um grafo','uma hashtable','uma lista ligada']

# Temos atualmente 35 perguntas

'''
Retorna tupla (materias, questoes)
    materias = lista de tuplas (id,nome)
    questoes = lista de tuplas (pergunta,resposta,id_materia,cpf_criador)
    O id da questão deve ser considerado como o indice dela na lista
'''
def gerar_questoes_materia(pessoas):
    areas = ["Humanas","Exatas","Humanas","Humanas","Exatas","Exatas"]
    materias = [(i,MATERIAS[i],areas[i]) for i in range(len(MATERIAS))]
    questoes = []

    questoes.extend(gerar_combinacoes_questoes([P_HISTORIA1,P_HISTORIA2],0,pessoas))
    questoes.extend(gerar_combinacoes_questoes([P_CALCULO1,P_CALCULO2,P_CALCULO3],1,pessoas))
    questoes.extend(gerar_combinacoes_questoes([P_GEOGRAFIA1,P_GEOGRAFIA2],2,pessoas))
    questoes.extend(gerar_combinacoes_questoes([P_ARTE1,P_ARTE2],3,pessoas))
    questoes.extend(gerar_combinacoes_questoes([P_INFORMATICA1,P_INFORMATICA2],5,pessoas))

    for i in range(len(P_MATEMATICA2)):
        a = randint(0,1000)
        b = randint(0,730)
        P_MATEMATICA2[i] = str(a)+P_MATEMATICA2[i]+str(b)+'?'
    questoes.extend(gerar_combinacoes_questoes([P_MATEMATICA1,P_MATEMATICA2],4,pessoas))
    return (materias,questoes)


TIPOS = ['Olimpíada','Competição']
ESCOPO = ['Brasileira de', 'Internacional de']
TEMAS = ['Matemática','Conhecimentos Gerais','Informática']
TEMAS_TO_MATERIA = [[1,4],[0,2,3],[5]] # id das materias que caem na prova
NIVEIS = ['Básica','Avançada']


# temos 24 possiveis provas

def repetido(cpf,lista,id_prova):
    for elem in lista:
        if elem[0] == id_prova and elem[1] == cpf:
            return True
    return False

def resposta_repetida(responde,realizador,id_questao):
    for elem in responde:
        if elem[0] == realizador and elem[1] == id_questao:
            return True
    return False

'''
Retorna tupla (provas,composta,realiza,responde)
    provas é uma lista de (id, nome, nivel)
    composta é uma lista de (id_prova,id_questão) - numero da questao é o index na lista
    realiza é uma lista de (id_prova,cpf_realizador,inscricao)
    responde é uma lista de (cpf_realizador,id_questao,resposta)
'''
def gerar_provas(questoes,pessoas,pessoas_por_prova=3):
    provas = []
    composta = []
    realiza = []
    responde = []
    
    listas = [TIPOS,ESCOPO,TEMAS,NIVEIS]
    todos_nomes = [' '.join(elem) for elem in list(product(*listas))]

    for id_prova in range(len(todos_nomes)):
        nome = todos_nomes[id_prova]
        nivel = 'Básica' if 'Básica' in nome else 'Avançada'
        provas.append((id_prova,nome,nivel))

        tema = 0
        while tema < len(TEMAS)-1 and TEMAS[tema] not in nome:
            tema += 1
        questoes_escolhidas = []
        for _ in range(5):
            id_questao = randint(0,len(questoes)-1)
            while (id_prova,id_questao) in questoes_escolhidas or \
                 questoes[id_questao][2] not in TEMAS_TO_MATERIA[tema]:
                id_questao = randint(0,len(questoes)-1)
            questoes_escolhidas.append((id_prova,id_questao))
        composta.extend(questoes_escolhidas)

        for _ in range(pessoas_por_prova):
            realizador = choice(pessoas)[0]
            inscricao = randint(100,99999)
            while repetido(realizador,realiza,id_prova):
                realizador = choice(pessoas)[0]
            realiza.append((id_prova,realizador,inscricao))

            for questao_ in questoes_escolhidas:
                if not resposta_repetida(responde,realizador,questao_[1]):
                    responde.append((realizador,questao_[1],choice("ABCDEF")))


    return (provas,composta,realiza,responde)


escolas = gerar_instituicao_academica(10,True)
faculdades = gerar_instituicao_academica(10,False)
escolas_cpy = escolas[:]

escolas.extend(faculdades)
# print(escolas)

pessoas = gerar_pessoas(4,faculdades)
# print(pessoas)

materias,questoes = gerar_questoes_materia(pessoas)
# print(materias)
# print(questoes)

provas,compoe,realiza,responde = gerar_provas(questoes,pessoas)
# print(provas)
# print(compoe)
# print(realiza)
# print(responde)

#### POPULANDO BANCO DE DADOS ###############
# InstituicaoAcademica
print()
for (cnpj,nome,rank) in escolas:
    print(f"INSERT INTO InstituicaoAcademica VALUES ({cnpj},'{nome}')")

# Escola
print()
for (cnpj,nome,rank) in escolas_cpy:
    print(f"INSERT INTO Escola VALUES ({cnpj},'{nome}',{rank})")

# Universidade
print()
for (cnpj,nome,rank) in faculdades:
    print(f"INSERT INTO Universidade VALUES ({cnpj},'{nome}',{rank})")

# Pessoa
print()
for (cpf,nome,email,cnpj) in pessoas:
    print(f"INSERT INTO Pessoa VALUES ({cpf},'{nome}','{email}',{cnpj})")

# Questao
print()
for (id,x) in enumerate(questoes):
    (pergunta,resposta,_,cpf_criador) = x
    print(f"INSERT INTO Questao VALUES ({id},'{pergunta}','{resposta}',{cpf_criador})")

# Materia
# TODO Tem id e nome, mas falta a area de conhecimento
print()
for (id,nome,area) in materias:
    print(f"INSERT INTO Materia VALUES ({id},'{nome}','{area}')")

# Prova
print()
for (id, nome, nivel) in provas:
    print(f"INSERT INTO Prova VALUES ({id},'{nome}','{nivel}')")

# Realiza
print()
for (id_prova,cpf_realizador,inscricao) in realiza:
    print(f"INSERT INTO Realiza VALUES ({id_prova},{cpf_realizador},{inscricao})")

# Responde
print()
for (cpf_realizador,id_questao,resposta) in responde:
    print(f"INSERT INTO Responde VALUES ({cpf_realizador},{id_questao},'{resposta}')")

# Compoe
print()
for (n_questao, x) in enumerate(compoe):
    (id_prova,id_questão) = x
    print(f"INSERT INTO Compoe VALUES ('{id_prova}','{id_questão}',{n_questao})")

# Aborda
print()
for (id_questao,x) in enumerate(questoes):
    (_,_,id_materia,_) = x
    print(f"INSERT INTO Aborda VALUES ({id_questao},{id_materia})")

print("\nexit")

'''
Pessoa - OK
InstituicaoAcademica - OK
Escola - OK
Universidade - OK
Questao - OK
Materia - OK
Aborda - OK
Prova - OK
Compoe - OK
Realiza - OK
Responde - OK
'''