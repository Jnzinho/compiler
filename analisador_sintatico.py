# analisador_sintatico.py

class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens + [("$", "$")]
        self.pilha = ["$", "<programa>"]
        self.pos = 0
        self.output = []

        # Tabela Sintática completa baseada na GLC fornecida
        self.tabela = {
            # <programa>
            ("<programa>", "CHAVE_ESQUERDA"): ["<lista_comandos>"],
            ("<programa>", "IDENTIFICADOR"): ["<lista_comandos>"],
            ("<programa>", "ESTRUTURA_CONTROLE"): ["<lista_comandos>"],
            ("<programa>", "TIPO_VARIAVEL"): ["<lista_comandos>"],
            ("<programa>", "$"): [],

            # <lista_comandos>
            ("<lista_comandos>", "CHAVE_ESQUERDA"): ["<comando>", "<lista_comandos>"],
            ("<lista_comandos>", "IDENTIFICADOR"): ["<comando>", "<lista_comandos>"],
            ("<lista_comandos>", "ESTRUTURA_CONTROLE"): ["<comando>", "<lista_comandos>"],
            ("<lista_comandos>", "TIPO_VARIAVEL"): ["<comando>", "<lista_comandos>"],
            ("<lista_comandos>", "CHAVE_DIREITA"): [],
            ("<lista_comandos>", "$"): [],

            # <comando>
            ("<comando>", "TIPO_VARIAVEL"): ["<declaracao>"],
            ("<comando>", "IDENTIFICADOR"): ["<atribuicao>"],
            ("<comando>", "ESTRUTURA_CONTROLE"): ["<comando_if>"],

            # <declaracao>
            ("<declaracao>", "TIPO_VARIAVEL"): ["<tipo>", "IDENTIFICADOR", "<declaracao_resto>"],

            # <declaracao_resto>
            ("<declaracao_resto>", "PONTO_VIRGULA"): ["PONTO_VIRGULA"],
            ("<declaracao_resto>", "ATRIBUICAO"): ["ATRIBUICAO", "<expressao>", "PONTO_VIRGULA"],

            # <atribuicao>
            ("<atribuicao>", "IDENTIFICADOR"): ["IDENTIFICADOR", "ATRIBUICAO", "<expressao>", "PONTO_VIRGULA"],

            # <comando_if>
            ("<comando_if>", "ESTRUTURA_CONTROLE"): ["if", "PARENTESE_ESQUERDO", "<expressao>", "PARENTESE_DIREITO", "<bloco>", "<senao>"],

            # <senao>
            ("<senao>", "ESTRUTURA_CONTROLE"): ["else", "<bloco>"],
            ("<senao>", "CHAVE_ESQUERDA"): [],
            ("<senao>", "CHAVE_DIREITA"): [],
            ("<senao>", "IDENTIFICADOR"): [],
            ("<senao>", "TIPO_VARIAVEL"): [],
            ("<senao>", "ESTRUTURA_CONTROLE"): [],
            ("<senao>", "$"): [],

            # <bloco>
            ("<bloco>", "CHAVE_ESQUERDA"): ["CHAVE_ESQUERDA", "<lista_comandos>", "CHAVE_DIREITA"],

            # <tipo>
            ("<tipo>", "TIPO_VARIAVEL"): ["TIPO_VARIAVEL"],

            # <expressao>
            ("<expressao>", "IDENTIFICADOR"): ["<termo>", "<expressao_prime>"],
            ("<expressao>", "NUMERO"): ["<termo>", "<expressao_prime>"],
            ("<expressao>", "PARENTESE_ESQUERDO"): ["<termo>", "<expressao_prime>"],

            # <expressao_prime>
            ("<expressao_prime>", "OPERADOR_ARITMETICO"): ["OPERADOR_ARITMETICO", "<termo>", "<expressao_prime>"],
            ("<expressao_prime>", "PARENTESE_DIREITO"): [],
            ("<expressao_prime>", "PONTO_VIRGULA"): [],
            ("<expressao_prime>", "CHAVE_DIREITA"): [],

            # <termo>
            ("<termo>", "IDENTIFICADOR"): ["<fator>", "<termo_prime>"],
            ("<termo>", "NUMERO"): ["<fator>", "<termo_prime>"],
            ("<termo>", "PARENTESE_ESQUERDO"): ["<fator>", "<termo_prime>"],

            # <termo_prime>
            ("<termo_prime>", "OPERADOR_ARITMETICO"): ["OPERADOR_ARITMETICO", "<fator>", "<termo_prime>"],
            ("<termo_prime>", "PARENTESE_DIREITO"): [],
            ("<termo_prime>", "PONTO_VIRGULA"): [],
            ("<termo_prime>", "CHAVE_DIREITA"): [],

            # <fator>
            ("<fator>", "IDENTIFICADOR"): ["IDENTIFICADOR"],
            ("<fator>", "NUMERO"): ["NUMERO"],
            ("<fator>", "PARENTESE_ESQUERDO"): ["PARENTESE_ESQUERDO", "<expressao>", "PARENTESE_DIREITO"]
        }

    def token_atual(self):
        return self.tokens[self.pos]

    def analisar(self):
        while self.pilha:
            topo = self.pilha.pop()
            atual = self.token_atual()
            lexema, tipo = atual

            if topo == tipo:
                self.output.append(f"[OK] Consumiu: {atual}")
                self.pos += 1

            elif topo.startswith("<"):
                producao = self.tabela.get((topo, tipo))
                if producao is not None:
                    for simbolo in reversed(producao):
                        if simbolo != "":
                            self.pilha.append(simbolo)
                    self.output.append(f"[PRODUCAO] {topo} → {' '.join(producao) if producao else 'ε'}")
                else:
                    self.output.append(f"[ERRO] Nenhuma produção para {topo} com {tipo}. Pulando token: {lexema}")
                    self.pos += 1

            elif topo == "$":
                if tipo == "$":
                    self.output.append("\nAnálise sintática concluída com sucesso!")
                    break
                else:
                    self.output.append(f"[ERRO] Esperado fim de cadeia, mas encontrei: {lexema}")
                    self.pos += 1
            else:
                self.output.append(f"[ERRO] Esperado {topo}, mas encontrei {tipo} ({lexema})")
                self.pos += 1

            if self.pos >= len(self.tokens):
                break

        return self.output
