import csv
import itertools
import numpy as np

def carregar_itens(arquivo_csv):

    nomes, pesos, valores = [], [], []

    with open(arquivo_csv, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)
        for linha in leitor:
            if not linha: continue
            nomes.append(linha[0])
            pesos.append(float(linha[1]))
            valores.append(float(linha[2]))
    return nomes, np.array(pesos), np.array(valores)

def gerar_populacao(tamanho, qtd_genes):

    return np.random.randint(0, 2, (tamanho, qtd_genes))

def calcular_aptidao(populacao, pesos, valores, capacidade):

    peso_total = np.dot(populacao, pesos)
    valor_total = np.dot(populacao, valores)

    return np.where(peso_total <= capacidade, valor_total, 0)

def selecionar_roleta(populacao, aptidoes):

    total = np.sum(aptidoes)

    if total == 0:
        probabilidades = np.full(len(populacao), 1 / len(populacao))
    else:
        probabilidades = aptidoes / total

    indice = np.random.choice(len(populacao), p=probabilidades)

    return populacao[indice]

def cruzar(pai1, pai2, taxa_cruzamento):

    if np.random.rand() > taxa_cruzamento:
        return pai1.copy(), pai2.copy()

    ponto = np.random.randint(1, len(pai1))

    filho1 = np.concatenate((pai1[:ponto], pai2[ponto:]))
    filho2 = np.concatenate((pai2[:ponto], pai1[ponto:]))

    return filho1, filho2

def mutar(cromossomo, taxa_mutacao):

    sorteio = np.random.rand(len(cromossomo)) < taxa_mutacao

    return np.where(sorteio, 1 - cromossomo, cromossomo)

def itens_selecionados(cromossomo, nomes):

    return [nome for nome, gene in zip(nomes, cromossomo) if gene == 1]

def calcular_solucao_otima(pesos, valores, capacidade):

    combinacoes = np.array(list(itertools.product([0, 1], repeat=len(pesos))))

    aptidoes = calcular_aptidao(combinacoes, pesos, valores, capacidade)

    indice = np.argmax(aptidoes)

    return combinacoes[indice], aptidoes[indice]

def salvar_solucao(arquivo_csv, cromossomo, capacidade, peso_total, valor_total, geracao):

    with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["cromossomo", "capacidade", "peso_total", "valor_total", "melhor_geracao"])
        escritor.writerow(["".join(str(g) for g in cromossomo), capacidade, round(peso_total, 2), valor_total, geracao])
