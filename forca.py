import requests as r
import random
import types
from textwrap import wrap
#from IPython.display import clear_output

def normalizaPalavra(word):
    '''
    Cria uma versão 'normalizada' da palavra escolhida, sem acentos ou cedilhas
    '''
    wordNormalizada = word
    acentos = (('Ã', 'A'), ('Á', 'A'), ('À', 'A'), ('Â', 'A'),('Ê', 'E'), ('É', 'E'), ('È', 'E'), ('Í', 'I'),
               ('Ô', 'O'), ('Ó', 'O'), ('Ú', 'U'), ('Ü', 'U') , ('Ç', 'C') )  
    
    for c in word:
        for i in range(len(acentos)):
            if c == acentos[i][0]:
                wordNormalizada = wordNormalizada.replace(c, acentos[i][1])
    return wordNormalizada


def camposPalavra(word:str, letra:str = None, campoAnterior:list = None): 
    '''
    Lista de '_' e letras que representam os acertos do usuário
    '''
    wordNormalizada = normalizaPalavra(word)
    output = []
    
    if campoAnterior == None:
        output = ["-" if k == "-" else "_" for k in palavraNome]
    else:   
        for k in range(len(wordNormalizada)):
            if campoAnterior[k] != "_": #Refatorar
                output.append(campoAnterior[k])
            elif letra != None and (wordNormalizada[k] == letra.upper() or palavraNome[k] == letra.upper()):
                output.append(word[k])
            else:
                output.append("_")
    return output


def mensagemTopo(palavraNormalizada, campos:list, vidas:int, tentativa:str):
    '''
    Mensagem no topo do jogo.
    '''
    if vidas != 0 and "_" in campos:
        if tentativa != "":
            if tentativa.upper() == "DICA":
                mensagem = '\nVocê recebeu uma dica!\n'
            else:
                if tentativa.upper() in palavraNormalizada or tentativa.upper() in palavraNome:
                    mensagem = '\nAcertou!\n'
                else:
                    mensagem = '\nErrou :( \n'
        else:
            mensagem = '\nBem vindo ao jogo da Forca!\n'
    elif vidas == 0:    
        mensagem = f"\nGAME OVER!!!! :(   a resposta certa era {palavraNome}. \n"
    elif "_" not in campos:
        mensagem = f"\nParabéns! Você VENCEU!!! \n"
    else:
        mensagem = '\n\n'
    return mensagem


def vidasRestantes(listTentativas:list, pediuDica:bool):
    return (6 - len(listTentativas) if pediuDica == False else 5 - len(listTentativas))

    
def desenho(camposForca:list, listTentativas:list, pediuDica:bool, dica):
    '''
    Mecanismo de 'impressão' da forca, fixado em no máximo 6 erros.
    '''
    vidas = vidasRestantes(listTentativas, pediuDica)

 
    # elementos do desenho
    cabeca = ("O" if vidas <= 5 else " ")        # 1 erro
    tronco = ("|" if vidas <= 4 else " ")        # 2 erros
    bracoEsq = ("/" if vidas <= 3 else " ")      # 3 erros
    bracoDir = ("\\" if vidas <= 2 else " ")     # 4 erros
    pernaEsq = ("/" if vidas <= 1 else " ")      # 5 erros
    pernaDir = ("\\" if vidas <= 0 else " ")     # 6 erros
    
    dicas = list()
    
    #dicas =  wrap(dica, width=30)
    dicas = ([''] if pediuDica == False else wrap(dica, width=60))

    if len(dicas) == 1:
        dicas.append("")
        dicas.append("")
    elif len(dicas) == 2:
        dicas.append("")

    mensagemDica = ('Digite "DICA" para trocar uma vida por uma dica.' if pediuDica == False else 'A dica é :')
    #mensagemStatus = mensagemTopo(pediuDica, camposForca, vidas)
    
    #print(mensagemStatus)
    print(f"  ___")
    print(f" |   {cabeca}       Você tem {vidas} vidas disponíveis.")
    print(f' |  {bracoEsq}{tronco}{bracoDir}      Você já chutou errado as letras:', *listTentativas)
    print(f' |   {tronco}       {mensagemDica} {dicas[0]}')
    print(f" |  {pernaEsq} {pernaDir}      {dicas[1]}")
    print(f" |           {dicas[2]}")
    print(f" |       ")
    print(f"_|______     ", *camposForca)
    print()

def encontrarDica(palavra):
    '''
    Encontra o significado da palavra
    '''
    palavraDica = ''
    #Faz a requisição do significado na API
    url = f'https://significado.herokuapp.com/{palavra}'
    resp = r.get(url)
    resp.status_code # é necessario?
    raw_data = resp.json()

    #Verifica se a palavra está presente no dicionário 
    try:
        palavraDica = raw_data[0]['meanings'][0]
        if 'error' in raw_data:
            return 'error'
        return palavraDica
    except (IndexError, KeyError) as e:
        return "error"

def encontrarPalavra(listaPalavras):      
    ''' 
    Função para encontrar palavra
    '''
    palavra = {'nome': '', 'dica': ''}
    palavraDica = ''
    index = random.randint(0, len(listaPalavras))
    
    palavraDica = encontrarDica(listaPalavras[index])

    if palavraDica == 'error':
      palavra = encontrarPalavra(listaPalavras)
    else:    
      palavra['nome'] = listaPalavras[index]
      palavra['dica'] = palavraDica
    
    return palavra

#Lê o arquivo com a lista de palavras                                       
with open("novas_palavras.txt", "r", encoding="utf-8") as f:                  
    palavrasDificeis = f.readlines()                                                     


palavrasFaceis = ['Imagem', 'Alicate', 'Azedo', 'Orgulho', 'Beleza', 'sacola', 'árvore']
palavrasIntermediarias = ['quinquilharia', 'obsessão', 'bambolê', 'dobradiça', 'espátula', 'hóstia', 'joystick']

# Teste para escolher nível de dificuldade

nomeJogo = '''
---------------------> JOGO DA FORCA <---------------------

Instruções:

- O objetivo deste jogo é descobrir a palavra adivinhando as letras que ela possui.
- A cada tentativa errada, uma parte do corpo do boneco aparecerá.
- Você terá 6 tentativas.
- O jogo termina quando você acerta todas as letras da palavra ou quando o desenho do boneco de completar (após a 6ª tentativa).

Bom jogo!

'''
print(nomeJogo)


# Instruções de jogo e nível de dificuldade

nivel = input("Em qual nível de dificuldade pretende jogar?\nF - Fácil, I - Intermediário, D - Difícil\n").upper()

while nivel != 'F' and nivel != 'I' and nivel != 'D':
    #clear_output(wait=False)
    print(nomeJogo)
    nivel = input("Em qual nível de dificuldade pretende jogar?\nDigite uma das letras abaixo\nF - Fácil, I - Intermediário, D - Difícil\n").upper()

if nivel == 'F':
    palav = encontrarPalavra(palavrasFaceis)
elif nivel == 'I':  
    palav = encontrarPalavra(palavrasIntermediarias)
else:
    palav = encontrarPalavra(palavrasDificeis)


# palav = encontrarPalavra(palavrasDificeis)   # ESSA PARTE PODE FICAR ONDE A PESSSOA SELECIONA A DIFICULDADE. 


palavraNome = (palav['nome'].upper() if palav['nome'].upper()[-1] != '\n' else palav['nome'].upper()[:-1])
palavraNormalizada = normalizaPalavra(palavraNome)
palavraDica = palav['dica']

# -----------------------------------------------


# Variáveis para teste até resolver o erro acima

# palavraNome = "araçuaí".upper()
# palavraNormalizada = normalizaPalavra(palavraNome)
# palavraDica = "Dica de Teste."

# -----------------------------------------------

campos = camposPalavra(palavraNome)
usuarioPediuDica = False
tentativaUsuario = ""
tentativas = []


#clear_output(wait=False)
print(mensagemTopo(palavraNormalizada, campos, vidasRestantes(tentativas, usuarioPediuDica), tentativaUsuario))
# print('\nBem vindo ao jogo da Forca!\n')
desenho(campos, tentativas, usuarioPediuDica, palavraDica) # PRIMEIRA IMPRESSÃO, SEM TENTATIVAS

while  tentativaUsuario == "" and vidasRestantes(tentativas, usuarioPediuDica)> 0 and "_" in campos:  
    tentativaUsuario = input("Tente uma letra: ")    # ENTRADA DE TENTATIVAS = LETRAS 
    
    # validação de entrada     
    while (len(tentativaUsuario) != 1 and tentativaUsuario.upper()!= "DICA") or not tentativaUsuario.isalpha() or tentativaUsuario.upper() in tentativas or tentativaUsuario.upper() in campos :  
        if len(tentativaUsuario) != 1 and tentativaUsuario.upper()!= "DICA":
            tentativaUsuario = input("Digite APENAS UMA letra: ").upper()
        elif tentativaUsuario.upper() in campos or tentativaUsuario.upper() in tentativas:
            tentativaUsuario = input("Você já digitou esta letra. Digite outra letra: ").upper()
        else:
            tentativaUsuario = input("Caractere inválido. Digite uma LETRA: ").upper()
    else: #entradas válidas
        if tentativaUsuario.upper() == "DICA":
            usuarioPediuDica = True
            #clear_output(wait=True)
            print(mensagemTopo(palavraNormalizada, campos, vidasRestantes(tentativas, usuarioPediuDica), tentativaUsuario))
            #print('\nVocê recebeu uma dica!\n')
            desenho(campos, tentativas, usuarioPediuDica, palavraDica) 
            tentativaUsuario = ""
        else:             
            # contabiliza erro apenas na primeira vez que uma tentativa errada é feita        
            if tentativaUsuario.upper() not in palavraNormalizada and tentativaUsuario.upper() not in palavraNome and tentativaUsuario.upper() not in tentativas :
                tentativas.append(tentativaUsuario.upper())
            
            #clear_output(wait=True) # limpar tela antes de imprimir novamente
            campos = camposPalavra(palavraNome,  tentativaUsuario, campos)
            print(mensagemTopo(palavraNormalizada, campos, vidasRestantes(tentativas, usuarioPediuDica), tentativaUsuario))
            #print('\nAcertou!\n' if entativa.upper() in palavraNormalizada else '\nErrou :( \n')
            desenho(campos, tentativas, usuarioPediuDica, palavraDica) 
            tentativaUsuario = ""
else:        
    if vidasRestantes(tentativas, usuarioPediuDica) == 0:  # GAME OVER
        #clear_output(wait=True) # limpar tela antes de imprimir novamente
        print(mensagemTopo(palavraNormalizada, campos, vidasRestantes(tentativas, usuarioPediuDica), tentativaUsuario))
        #print(f"\nGAME OVER!!!! :(   a resposta certa era {palavraNome}. \n")
        desenho(campos, tentativas, usuarioPediuDica, palavraDica) 
        
    elif "_" not in campos: # Usuário VENCEU
        #clear_output(wait=True)  
        print(mensagemTopo(palavraNormalizada, campos, vidasRestantes(tentativas, usuarioPediuDica), tentativaUsuario))
        #print('\nParabéns! Você VENCEU!!! \n')
        desenho(campos, tentativas, usuarioPediuDica, palavraDica) 