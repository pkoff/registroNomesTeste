import pandas as pd
import os
from unidecode import unidecode
from colorama import Fore, Style, init

RAINBOW = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

sobrenomes_suporte = {"de", "da", "do", "dos", "das"}

ARQUIVO_REGISTRO = 'registroDeNomes.txt'

init(autoreset=True)

df1 = pd.read_csv(
    'https://raw.githubusercontent.com/datasets-br/prenomes/refs/heads/master/data/nomes-censos-ibge.csv'
)

dfPrenomes = (
    df1['Nome']
    .dropna()
    .astype(str)
    .str.lower()
    .apply(unidecode)
    .tolist()
)

df2 = pd.read_csv('https://raw.githubusercontent.com/pkoff/registroNomesTeste/refs/heads/main/sobrenomes.txt',
                    sep="\t",
                    header=None,
                    names=["freq", "sobrenome"]
                    )

dfSobrenomes = (
    df2['sobrenome']
    .dropna()
    .astype(str)
    .str.lower()
    .apply(unidecode)
    .str.split()
    .explode()
    .drop_duplicates()
    .tolist()
)

dfNomes = list(set(dfPrenomes + dfSobrenomes))

dfNomes = [unidecode(n).lower().strip() for n in dfNomes]

def print_rainbow(text: str, start: int = 0):

    out = []
    color_index = start % len(RAINBOW)
    for ch in text:
        if ch.isspace():
            out.append(ch)
        else:
            out.append(RAINBOW[color_index] + ch)
            color_index = (color_index + 1) % len(RAINBOW)
    print(''.join(out) + Style.RESET_ALL)

def limpar_registro(nome_arquivo):

    open(nome_arquivo, "w").close()
    print("o registro foi apagado completamente")

def ler_registro_csv(nome_arquivo):

    if not os.path.exists(nome_arquivo) or os.stat(nome_arquivo).st_size == 0:
        return pd.DataFrame(columns=['Contagem']).rename_axis('Nome')
    
    df = pd.read_csv(
        nome_arquivo, 
        header=None, 
        names=['Nome', 'Contagem'],
        index_col='Nome',
        skipinitialspace=True 
    )
    
    return df

def salvar_registro(df, nome_arquivo):

    df.to_csv(
        nome_arquivo, 
        header=False, 
        sep=',', 
        encoding='utf-8'
    )


def registrar_nomes_do_usuario(nome_completo):

    registro_df = ler_registro_csv(ARQUIVO_REGISTRO)
    
    for nome in nomes_individuais:
        nome_limpo = unidecode(nome).lower()
        
        if nome_limpo in registro_df.index:
            registro_df.loc[nome_limpo, 'Contagem'] += 1
        else:
            registro_df.loc[nome_limpo] = {'Contagem': 1}

    salvar_registro(registro_df, ARQUIVO_REGISTRO)
    
    return registro_df

while True:
    print('----=======----')
    nome_do_usuario = unidecode(input('digite seu nome completo separado por espaços(flush para apagar registro):')).lower()

    if nome_do_usuario == 'flush':
        limpar_registro(ARQUIVO_REGISTRO)
        continue

    elif nome_do_usuario == 'registro' or nome_do_usuario == 'ler':
        print(ler_registro_csv(ARQUIVO_REGISTRO).sort_values(by='Contagem', ascending=False).rename(index=str.capitalize))
        continue

    elif 'augusto' in nome_do_usuario:
        print_rainbow('oi ru!', start=3)
        print_rainbow('oi ru?', start=1)
        print_rainbow('oi ru.', start=5)
        continue

    nomes_individuais = [
        n for n in nome_do_usuario.split()
        if n.strip() and n not in sobrenomes_suporte
    ]

    nome_invalido = False

    for nome in nomes_individuais:
        if nome not in dfNomes:
            print('digite apenas nomes reais')
            nome_invalido = True
            break

    if nome_invalido:
        continue

    registro_final = registrar_nomes_do_usuario(nome_do_usuario)

    registro_final = registro_final.sort_values(by='Contagem', ascending=False)
    registro_final.index = registro_final.index.str.capitalize()

    print("\n---=== tabela de nomes do registro ===---")
    print(registro_final)