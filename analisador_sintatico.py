class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.erros = []

    def token_atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', 'EOF')

    def consumir(self, tipo_esperado):
        token = self.token_atual()
        if token[1] == tipo_esperado:
            print(f"[OK] Consumiu: {token}")
            self.pos += 1
        else:
            self.erros.append(f"Erro sintático: esperado '{tipo_esperado}', encontrado '{token[1]}' ({token[0]})")
            self.pos += 1  # avança para tentar sincronizar

    def analisar(self):
        self.programa()
        if self.erros:
            print("\nErros encontrados:")
            for erro in self.erros:
                print(erro)
        else:
            print("\nAnálise sintática concluída com sucesso!")

    def programa(self):
        # programa → tipo identificador ( ) { corpo }
        self.tipo()
        self.consumir("IDENTIFICADOR")
        self.consumir("PARENTESE_ESQUERDO")
        self.consumir("PARENTESE_DIREITO")
        self.consumir("CHAVE_ESQUERDA")
        self.corpo()
        self.consumir("CHAVE_DIREITA")

    def tipo(self):
        token = self.token_atual()
        if token[1] == "TIPO_VARIAVEL":
            self.consumir("TIPO_VARIAVEL")
        else:
            self.erros.append(f"Esperado tipo de variável, mas encontrado '{token[0]}'")
            self.pos += 1

    def corpo(self):
        # corpo → { tipo identificador ; }*
        while self.token_atual()[1] == "TIPO_VARIAVEL":
            self.tipo()
            self.consumir("IDENTIFICADOR")
            self.consumir("PONTO")  # Simulando ; com ponto
