from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico
from datetime import datetime
import os

def write_output(content, file):
    print(content)  # Saída no terminal
    file.write(content + "\n")  # Saída no arquivo

def main():
    # Cria o diretório de resultados se não existir
    if not os.path.exists("resultados"):
        os.makedirs("resultados")
    
    # Cria arquivo de saída com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join("resultados", f"analise_resultado_{timestamp}.txt")
    
    with open("entrada.txt", "r") as f:
        codigo = f.read()
    
    with open(output_filename, "w") as output_file:
        write_output("📥 Código de entrada:", output_file)
        write_output(codigo, output_file)
        write_output("\n🔍 Análise léxica...", output_file)

        tokens, erros_lexicos = AnalisadorLexico(codigo)

        write_output("\nTokens encontrados:", output_file)
        for lex, tipo in tokens:
            write_output(f"{lex:<15} {tipo}", output_file)

        if erros_lexicos:
            write_output("\n❌ Erros léxicos encontrados:", output_file)
            for linha, msg in erros_lexicos:
                write_output(f"Linha {linha}: {msg}", output_file)
            return

        write_output("\n🧠 Iniciando análise sintática...", output_file)
        parser = AnalisadorSintatico(tokens)
        mensagens_sintaticas = parser.analisar()
        
        # Escreve todas as mensagens da análise sintática
        for mensagem in mensagens_sintaticas:
            write_output(mensagem, output_file)

if __name__ == "__main__":
    main()
