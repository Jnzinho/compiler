from analisador_lexico import analisar_lexico
from analisador_sintatico import AnalisadorSintatico

def main():
    with open("entrada.txt", "r") as f:
        codigo = f.read()

    print("📥 Código de entrada:")
    print(codigo)
    print("\n🔍 Análise léxica...")

    tokens, erros_lexicos = analisar_lexico(codigo)

    print("\nTokens:")
    for lex, tipo in tokens:
        print(f"{lex:<15} {tipo}")

    if erros_lexicos:
        print("\n❌ Erros léxicos:")
        for linha, msg in erros_lexicos:
            print(f"Linha {linha}: {msg}")
        return

    print("\n🧠 Análise sintática...")
    parser = AnalisadorSintatico(tokens)
    parser.analisar()

if __name__ == "__main__":
    main()
