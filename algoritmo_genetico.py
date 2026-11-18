import numpy as np
import funcoes as f

capacidade = float(input("Informe a capacidade máxima da mochila em kg (Ex: 15): "))
tamanho_populacao = int(input("Informe o tamanho da população (Ex: 30): "))
taxa_cruzamento = float(input("Informe a taxa de cruzamento (Entre 0 e 1): "))
taxa_mutacao = float(input("Informe a taxa de mutação (Entre 0 e 1): "))
geracoes = 100

nomes, pesos, valores = f.carregar_itens("arquivos_texto/itens.csv")

populacao = f.gerar_populacao(tamanho_populacao, len(nomes))

melhor_aptidao = -1
melhor_cromossomo = []
melhor_geracao = 0

print("\nIniciando evolução...\n")

for geracao in range(1, geracoes + 1):

    aptidoes = f.calcular_aptidao(populacao, pesos, valores, capacidade)

    indice_melhor = np.argmax(aptidoes)

    print(f"Geração {geracao} finalizada. Melhor aptidão: {aptidoes[indice_melhor]:.2f}")

    if aptidoes[indice_melhor] > melhor_aptidao:
        melhor_aptidao = aptidoes[indice_melhor]
        melhor_cromossomo = populacao[indice_melhor].copy()
        melhor_geracao = geracao

    nova_populacao = [populacao[indice_melhor].copy()]

    while len(nova_populacao) < tamanho_populacao:

        pai1 = f.selecionar_roleta(populacao, aptidoes)
        pai2 = f.selecionar_roleta(populacao, aptidoes)

        filho1, filho2 = f.cruzar(pai1, pai2, taxa_cruzamento)

        nova_populacao.append(f.mutar(filho1, taxa_mutacao))

        if len(nova_populacao) < tamanho_populacao:
            nova_populacao.append(f.mutar(filho2, taxa_mutacao))

    populacao = np.array(nova_populacao)

peso_total = np.dot(melhor_cromossomo, pesos)

print("\n----- RESULTADO FINAL DA EVOLUÇÃO -----")
print(f"Melhor Geração: {melhor_geracao}")
print(f"Melhor Aptidão (Valor total): R$ {melhor_aptidao:.2f}")
print(f"Peso total: {peso_total:.2f} kg (Capacidade: {capacidade} kg)")
print(f"Melhor Cromossomo: {melhor_cromossomo}")
print(f"Itens selecionados: {', '.join(f.itens_selecionados(melhor_cromossomo, nomes))}")
print(f"Total de gerações: {geracoes}")

f.salvar_solucao("arquivos_texto/melhor_solucao.csv", melhor_cromossomo, capacidade, peso_total, melhor_aptidao, melhor_geracao)
print("\nSolução salva com sucesso em 'arquivos_texto/melhor_solucao.csv'!")
