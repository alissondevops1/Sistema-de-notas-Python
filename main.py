import json
import os
import csv
from colorama import Fore, Style, init

# Inicializa colorama para usar cores no terminal
init(autoreset=True)

# ----------------------------------------
# Parte 1 e 2: Estrutura inicial + Funções básicas
# ----------------------------------------

ARQUIVO_DADOS = "dados_alunos.json"  # arquivo onde os dados ficam salvos
alunos = []  # lista em memória

def carregar_dados():
    """Carrega os dados do arquivo JSON, se existir"""
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []  # retorna lista vazia caso o arquivo não exista

def salvar_dados(dados):
    """Salva dados no arquivo JSON"""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def inicializar():
    """Carrega dados já existentes"""
    global alunos
    alunos = carregar_dados()

# ----------------------------------------
# Parte 3: CRUD de alunos
# ----------------------------------------

def cadastrar_aluno(nome, matricula, curso):
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            print(Fore.RED + "❌ Já existe um aluno com essa matrícula.")
            return
    novo_aluno = {
        "nome": nome,
        "matricula": matricula,
        "curso": curso,
        "notas": []
    }
    alunos.append(novo_aluno)
    salvar_dados(alunos)
    print(Fore.GREEN + f"✅ Aluno {nome} cadastrado com sucesso!")

def atualizar_aluno(matricula, novos_dados):
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            aluno.update(novos_dados)
            salvar_dados(alunos)
            print(Fore.GREEN + f"✅ Dados do aluno {matricula} atualizados!")
            return
    print(Fore.RED + "❌ Aluno não encontrado.")

def excluir_aluno(matricula):
    global alunos
    alunos = [aluno for aluno in alunos if aluno["matricula"] != matricula]
    salvar_dados(alunos)
    print(Fore.GREEN + f"✅ Aluno {matricula} excluído (se existia).")

# ----------------------------------------
# Parte 4: Notas
# ----------------------------------------

def lancar_notas(matricula, notas):
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            aluno["notas"].extend(notas)
            salvar_dados(alunos)
            print(Fore.GREEN + f"✅ Notas lançadas para {aluno['nome']}.")
            return
    print(Fore.RED + "❌ Aluno não encontrado.")

def atualizar_notas(matricula, novas_notas):
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            aluno["notas"] = novas_notas
            salvar_dados(alunos)
            print(Fore.GREEN + f"✅ Notas do aluno {aluno['nome']} atualizadas!")
            return
    print(Fore.RED + "❌ Aluno não encontrado.")

def calcular_media_situacao(matricula):
    for aluno in alunos:
        if aluno["matricula"] == matricula:
            if not aluno["notas"]:
                print(Fore.YELLOW + "⚠️ Esse aluno ainda não tem notas.")
                return None
            media = sum(aluno["notas"]) / len(aluno["notas"])
            situacao = "Aprovado ✅" if media >= 7 else "Reprovado ❌"
            print(Fore.CYAN + f"📊 Média: {media:.2f} | Situação: {situacao}")
            return media, situacao
    print(Fore.RED + "❌ Aluno não encontrado.")
    return None

# ----------------------------------------
# Parte 5: Consultas
# ----------------------------------------

def buscar_aluno(identificador):
    for aluno in alunos:
        if aluno["matricula"] == identificador or aluno["nome"].lower() == identificador.lower():
            print(Fore.CYAN + f"\n🔎 Aluno encontrado:")
            print(Fore.YELLOW + f"Nome: {aluno['nome']}")
            print(Fore.YELLOW + f"Matrícula: {aluno['matricula']}")
            print(Fore.YELLOW + f"Curso: {aluno['curso']}")
            print(Fore.YELLOW + f"Notas: {aluno['notas']}")
            return aluno
    print(Fore.RED + "❌ Aluno não encontrado.")
    return None

def listar_alunos():
    if not alunos:
        print(Fore.RED + "⚠️ Nenhum aluno cadastrado.")
        return
    print(Fore.GREEN + "\n📋 Lista de alunos cadastrados:")
    for aluno in alunos:
        print(Fore.YELLOW + f"- {aluno['nome']} (Matrícula: {aluno['matricula']}, Curso: {aluno['curso']})")

def gerar_relatorio():
    if not alunos:
        print(Fore.RED + "⚠️ Nenhum aluno cadastrado.")
        return
    print(Fore.MAGENTA + "\n📊 Relatório Geral dos Alunos:")
    for aluno in alunos:
        notas = aluno["notas"]
        if notas:
            media = sum(notas) / len(notas)
            situacao = "Aprovado ✅" if media >= 7 else "Reprovado ❌"
        else:
            media = 0
            situacao = "Sem notas"
        print(Fore.CYAN + f"\nNome: {aluno['nome']}")
        print(Fore.YELLOW + f"Matrícula: {aluno['matricula']}")
        print(Fore.YELLOW + f"Curso: {aluno['curso']}")
        print(Fore.YELLOW + f"Notas: {notas}")
        print(Fore.GREEN + f"Média: {media:.2f}")
        print(Fore.MAGENTA + f"Situação: {situacao}")

# ----------------------------------------
# Parte 6: Menu Principal
# ----------------------------------------

def menu():
    while True:
        print("Bem-vindo ao Sistema de Notas!")
        print("Bem-vindo ao Sistema de Notas dos Alunos! 🚀")
        print(Fore.BLUE + Style.BRIGHT + "\n=== MENU PRINCIPAL ===")
        print(Fore.CYAN + "1. Cadastrar aluno")
        print("2. Atualizar aluno")
        print("3. Excluir aluno")
        print("4. Lançar notas")
        print("5. Atualizar notas")
        print("6. Calcular média e situação")
        print("7. Buscar aluno")
        print("8. Listar alunos")
        print("9. Relatório geral")
        print("10. Exportar relatório TXT")
        print("11. Exportar relatório CSV")
        print("0. Sair")

        opcao = input(Fore.WHITE + "\n👉 Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            matricula = input("Matrícula: ")
            curso = input("Curso: ")
            cadastrar_aluno(nome, matricula, curso)

        elif opcao == "2":
            matricula = input("Informe a matrícula do aluno: ")
            novos_dados = {}
            novo_nome = input("Novo nome (deixe vazio para manter): ")
            novo_curso = input("Novo curso (deixe vazio para manter): ")
            if novo_nome:
                novos_dados["nome"] = novo_nome
            if novo_curso:
                novos_dados["curso"] = novo_curso
            atualizar_aluno(matricula, novos_dados)

        elif opcao == "3":
            matricula = input("Matrícula do aluno a excluir: ")
            excluir_aluno(matricula)

        elif opcao == "4":
            matricula = input("Matrícula do aluno: ")
            notas = input("Digite as notas separadas por vírgula: ")
            notas = [float(n.strip()) for n in notas.split(",")]
            lancar_notas(matricula, notas)

        elif opcao == "5":
            matricula = input("Matrícula do aluno: ")
            notas = input("Digite as novas notas separadas por vírgula: ")
            notas = [float(n.strip()) for n in notas.split(",")]
            atualizar_notas(matricula, notas)

        elif opcao == "6":
            matricula = input("Matrícula do aluno: ")
            calcular_media_situacao(matricula)

        elif opcao == "7":
            identificador = input("Digite matrícula ou nome do aluno: ")
            buscar_aluno(identificador)

        elif opcao == "8":
            listar_alunos()

        elif opcao == "9":
            gerar_relatorio()

        elif opcao == "10":
            exportar_relatorio_txt()

        elif opcao == "11":
            exportar_relatorio_csv()

        elif opcao == "0":
            print(Fore.GREEN + "👋 Saindo do sistema...")
            break

        else:
            print(Fore.RED + "❌ Opção inválida, tente novamente.")

# ----------------------------------------
# Parte 7: Extras
# ----------------------------------------

def exportar_relatorio_txt():
    # Verifica se o arquivo de alunos existe
    if not os.path.exists(ARQUIVO_DADOS):
        print("\n⚠️ Nenhum aluno cadastrado ainda para exportar.")
        return

    # Carrega os alunos do arquivo JSON
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        alunos = json.load(f)

    if not alunos:
        print("\n⚠️ Nenhum aluno encontrado no sistema.")
        return

    # Monta o conteúdo do relatório
    conteudo = "📄 RELATÓRIO DE NOTAS\n\n"
    for aluno in alunos:
        conteudo += f"Nome: {aluno['nome']}\n"
        conteudo += f"Matrícula: {aluno['matricula']}\n"
        conteudo += f"Curso: {aluno['curso']}\n"
        conteudo += f"Nota: {aluno.get('nota', 'N/A')}\n"
        conteudo += "-" * 30 + "\n"

    # Pergunta onde salvar
    print("\nEscolha onde salvar o relatório:")
    print("1 - Pasta atual do projeto")
    print("2 - Documentos")
    print("3 - Downloads")
    print("4 - Escolher outro caminho manualmente")

    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        caminho = os.path.join(os.getcwd(), "relatorio_notas.txt")
    elif opcao == "2":
        caminho = os.path.join(os.path.expanduser("~"), "Documents", "relatorio_notas.txt")
    elif opcao == "3":
        caminho = os.path.join(os.path.expanduser("~"), "Downloads", "relatorio_notas.txt")
    elif opcao == "4":
        caminho = input("Digite o caminho completo (ex: C:/Users/aliss/Desktop/relatorio_notas.txt): ")
    else:
        print("⚠️ Opção inválida, salvando na pasta atual.")
        caminho = os.path.join(os.getcwd(), "relatorio_notas.txt")

    # Cria o arquivo
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(f"\n✅ Relatório exportado com sucesso para:\n{caminho}")
def exportar_relatorio_csv(nome_arquivo="relatorio_alunos.csv"):
    if not alunos:
        print(Fore.RED + "⚠️ Nenhum aluno cadastrado para exportar.")
        return
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f, delimiter=";")
        escritor.writerow(["Nome", "Matrícula", "Curso", "Notas", "Média", "Situação"])
        for aluno in alunos:
            notas = aluno["notas"]
            if notas:
                media = sum(notas) / len(notas)
                situacao = "Aprovado" if media >= 7 else "Reprovado"
            else:
                media = 0
                situacao = "Sem notas"
            escritor.writerow([
                aluno["nome"],
                aluno["matricula"],
                aluno["curso"],
                ", ".join(map(str, notas)),
                f"{media:.2f}",
                situacao
            ])
    print(Fore.GREEN + f"✅ Relatório exportado para {nome_arquivo}")

# ----------------------------------------
# Execução
# ----------------------------------------

if __name__ == "__main__":
    inicializar()
    menu()
