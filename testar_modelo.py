import csv
import numpy as np
import funcoes as f

def carregar_solucao(arquivo_csv):
    try:
        with open(arquivo_csv, mode="r", encoding="utf-8") as arq:
            leitor = csv.reader(arq)
            next(leitor)
            linha = next(leitor)
            cromossomo = np.array([int(g) for g in linha[0]])
            capacidade = float(linha[1])
            valor_total = float(linha[3])
            return cromossomo, capacidade, valor_total
    except FileNotFoundError:
        print("Erro: Arquivo 'arquivos_texto/melhor_solucao.csv' não encontrado.")
        print("Você precisa rodar o arquivo 'algoritmo_genetico.py' primeiro!")
        exit()

cromossomo_ag, capacidade, valor_ag = carregar_solucao("arquivos_texto/melhor_solucao.csv")

nomes, pesos, valores = f.carregar_itens("arquivos_texto/itens.csv")

print("----- TESTE DO ALGORITMO GENÉTICO -----")
print(f"Solução carregada! (Capacidade: {capacidade} kg | Valor obtido pelo AG: R$ {valor_ag:.2f})")
print(f"Itens escolhidos pelo AG: {', '.join(f.itens_selecionados(cromossomo_ag, nomes))}")

print("\nCalculando a solução ótima por força bruta (testando todas as combinações)...")

cromossomo_otimo, valor_otimo = f.calcular_solucao_otima(pesos, valores, capacidade)

print(f"Valor da solução ótima: R$ {valor_otimo:.2f}")
print(f"Itens da solução ótima: {', '.join(f.itens_selecionados(cromossomo_otimo, nomes))}")

if valor_otimo > 0:
    print(f"--> O AG atingiu {(valor_ag / valor_otimo) * 100:.2f}% da solução ótima.")

print("\nItens disponíveis:")
for i, (nome, peso, valor) in enumerate(zip(nomes, pesos, valores), start=1):
    print(f"{i:2d} - {nome} ({peso} kg | R$ {valor:.2f})")

print("\nMonte uma mochila para avaliar (ou 'sair' para encerrar).\n")

while True:
    entradas = input(f"Digite os números dos itens separados por vírgula (1 a {len(nomes)}): ")

    if entradas.lower().strip() == 'sair':
        break

    try:
        indices = [int(v.strip()) - 1 for v in entradas.split(",")]

        if any(i < 0 or i >= len(nomes) for i in indices):
            print(f"Digite apenas números entre 1 e {len(nomes)}!\n")
            continue

        cromossomo = np.zeros(len(nomes), dtype=int)
        cromossomo[indices] = 1

        peso_total = np.dot(cromossomo, pesos)
        aptidao = f.calcular_aptidao(cromossomo, pesos, valores, capacidade)

        if peso_total > capacidade:
            print(f"--> Mochila inválida! Peso total de {peso_total:.2f} kg ultrapassa a capacidade. Aptidão: 0\n")
        else:
            print(f"--> Peso total: {peso_total:.2f} kg | Aptidão (Valor total): R$ {aptidao:.2f} (AG: R$ {valor_ag:.2f})\n")

    except ValueError:
        print("Entrada inválida! Digite apenas números inteiros separados por vírgula.\n")
