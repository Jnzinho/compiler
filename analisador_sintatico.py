class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.erros = []
        self.output_messages = []  # Nova lista para armazenar mensagens de saída

    def token_atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', 'EOF')

    def consumir(self, tipo_esperado):
        token = self.token_atual()
        if token[1] == tipo_esperado:
            self.output_messages.append(f"[OK] Token consumido: {token}")
            self.pos += 1
        else:
            self.erros.append(f"Erro sintático: esperava '{tipo_esperado}', mas encontrou '{token[1]}' ({token[0]})")
            self.pos += 1  # Avança para tentar sincronizar a análise

    def analisar(self):
        self.programa()
        if self.erros:
            self.output_messages.append("\nErros sintáticos encontrados:")
            for erro in self.erros:
                self.output_messages.append(erro)
        else:
            self.output_messages.append("\nAnálise sintática concluída com sucesso!")
        
        return self.output_messages  # Retorna todas as mensagens

    def programa(self):
        # programa → tipo identificador ( ) { corpo }
        # Regra: Um programa é composto por um tipo seguido de identificador, parênteses, e um corpo entre chaves
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
            self.erros.append(f"Erro: esperava um tipo de variável, mas encontrou '{token[0]}'")
            self.pos += 1

    def corpo(self):
        # corpo → { tipo identificador ; }*
        # Regra: O corpo pode conter múltiplas declarações de variáveis (tipo seguido de identificador e ponto-e-vírgula)
        while self.token_atual()[1] == "TIPO_VARIAVEL":
            self.tipo()
            self.consumir("IDENTIFICADOR")
            self.consumir("PONTO")  # Usando ponto como ponto-e-vírgula
