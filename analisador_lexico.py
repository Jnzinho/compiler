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
    elif caractere == ';':
        return 'PONTO_VIRGULA'
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
        '.': 'PONTO',
        ';': 'PONTO_VIRGULA'  
    }.get(char, 'DESCONHECIDO')

def AnalisadorLexico(codigo):
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

        if estado == 'q0':
            if cat == 'LETRA' or cat == '_':
                lexema += char
                estado = 'q1'
                i += 1
            elif cat == 'DIGITO':                                                                 
                lexema += char
                estado = 'q2'
                i += 1
            elif char == '/':
                lexema += char
                estado = 'q3'
                i += 1
            elif char in '+-*=!<>|&{},().;':
                tokens.append((char, tipo_token(char)))
                i += 1
            else:
                erros.append((linha, f"Caractere inválido: '{char}'"))
                estado = 'ERRO'
                i += 1
                continue
        elif estado == 'q1':
            if cat in ['LETRA', 'DIGITO', '_']:
                lexema += char
                i += 1
            else:
                token_tipo = PALAVRAS_RESERVADAS.get(lexema.strip(), 'IDENTIFICADOR')
                tokens.append((lexema.strip(), token_tipo))
                lexema = ''
                estado = 'q0'
        elif estado == 'q2':
            if cat == 'DIGITO':
                lexema += char
                i += 1
            else:
                tokens.append((lexema.strip(), 'NUMERO'))
                lexema = ''
                estado = 'q0'
        elif estado == 'q3':
            if char == '/':
                lexema += char
                estado = 'q10'
                i += 1
            else:
                tokens.append(('/', 'OPERADOR_ARITMETICO'))
                lexema = ''
                estado = 'q0'
        elif estado == 'q10':
            if char == '\n':
                estado = 'q0'
                lexema = ''
                linha += 1
            i += 1

    # Tratamento do último token
    if lexema and estado == 'q1':
        token_tipo = PALAVRAS_RESERVADAS.get(lexema.strip(), 'IDENTIFICADOR')
        tokens.append((lexema.strip(), token_tipo))
    elif lexema and estado == 'q2':
        tokens.append((lexema.strip(), 'NUMERO'))

    return tokens, erros