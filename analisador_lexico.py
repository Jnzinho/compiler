import string

LETRAS = string.ascii_letters
DIGITOS = string.digits
ESPACOS = " \t\r"

PALAVRAS_RESERVADAS = {
    'if': 'ESTRUTURA_CONTROLE',
    'else': 'ESTRUTURA_CONTROLE',
    'for': 'ESTRUTURA_CONTROLE',
    'while': 'ESTRUTURA_CONTROLE',
    'do': 'ESTRUTURA_CONTROLE',
    'int': 'TIPO_VARIAVEL',
    'float': 'TIPO_VARIAVEL',
    'bool': 'TIPO_VARIAVEL',
    'string': 'TIPO_VARIAVEL',
}

def categorizar(caractere):
    if caractere in LETRAS:
        return 'LETRA'
    elif caractere in DIGITOS:
        return 'DIGITO'
    elif caractere == '\n':
        return '\\n'
    elif caractere in ESPACOS:
        return 'ESPACO'
    elif caractere in '{}()_+-*/=!<>,.&|':
        return caractere
    elif caractere == '.':
        return '.'
    else:
        return 'QUALQUER'

def tipo_token(char):
    return {
        '+': 'OPERADOR_ARITMETICO',
        '-': 'OPERADOR_ARITMETICO',
        '*': 'OPERADOR_ARITMETICO',
        '/': 'OPERADOR_ARITMETICO',
        '=': 'ATRIBUICAO',
        '!': 'NEGACAO',
        '<': 'OPERADOR_RELACIONAL',
        '>': 'OPERADOR_RELACIONAL',
        '&': 'OPERADOR_LOGICO',
        '|': 'OPERADOR_LOGICO',
        '(': 'PARENTESE_ESQUERDO',
        ')': 'PARENTESE_DIREITO',
        '{': 'CHAVE_ESQUERDA',
        '}': 'CHAVE_DIREITA',
        ',': 'VIRGULA',
        '.': 'PONTO'
    }.get(char, 'DESCONHECIDO')

def analisar_lexico(codigo):
    tokens = []
    erros = []

    lexema = ''
    estado = 'q0'
    i = 0
    linha = 1

    while i < len(codigo):
        char = codigo[i]
        cat = categorizar(char)

        if estado == 'q0' and cat in ['ESPACO', '\\n']:
            if char == '\n':
                linha += 1
            i += 1
            continue

        if cat == 'QUALQUER':
            erros.append((linha, f"Caractere inválido: '{char}'"))
            i += 1
            continue

        lexema += char

        if estado == 'q0':
            if cat == 'LETRA' or cat == '_':
                estado = 'q1'
            elif cat == 'DIGITO':
                estado = 'q2'
            elif char == '/':
                estado = 'q3'
            elif char in '+-*=!<>|&{},().':
                tokens.append((char, tipo_token(char)))
                lexema = ''
            else:
                erros.append((linha, f"Caractere inválido: '{char}'"))
                estado = 'ERRO'
                i += 1
                continue
        elif estado == 'q1':
            if cat in ['LETRA', 'DIGITO', '_']:
                pass
            else:
                token_tipo = PALAVRAS_RESERVADAS.get(lexema.strip(), 'IDENTIFICADOR')
                tokens.append((lexema.strip(), token_tipo))
                lexema = ''
                estado = 'q0'
                continue
        elif estado == 'q2':
            if cat == 'DIGITO':
                pass
            else:
                tokens.append((lexema.strip(), 'NUMERO'))
                lexema = ''
                estado = 'q0'
                continue
        elif estado == 'q3':
            if char == '/':
                estado = 'q10'
            else:
                tokens.append(('/', 'OPERADOR_ARITMETICO'))
                lexema = ''
                estado = 'q0'
                continue
        elif estado == 'q10':
            if char == '\n':
                estado = 'q0'
                lexema = ''
                linha += 1
        i += 1

    if lexema and estado == 'q1':
        token_tipo = PALAVRAS_RESERVADAS.get(lexema.strip(), 'IDENTIFICADOR')
        tokens.append((lexema.strip(), token_tipo))
    elif lexema and estado == 'q2':
        tokens.append((lexema.strip(), 'NUMERO'))

    return tokens, erros

if __name__ == "__main__":
    with open("entrada.txt", "r") as f:
        codigo = f.read()
    tokens, erros = analisar_lexico(codigo)

    print("Tokens:")
    for lex, tipo in tokens:
        print(f"{lex:<15} {tipo}")

    if erros:
        print("\nErros léxicos:")
        for linha, msg in erros:
            print(f"Linha {linha}: {msg}")
