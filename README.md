# Implementação Algoritmo Genético

Este projeto implementa um Algoritmo Genético em Python para resolver o Problema da Mochila 0-1, um problema clássico de otimização combinatória.

---

### 🎒 O Problema da Mochila:

Imagine que você vai acampar e tem uma mochila que suporta no máximo uma certa quantidade de quilos. Existem vários itens disponíveis (barraca, lanterna, comida, etc.), e cada um deles possui um **peso** e um **valor**. O objetivo é escolher quais itens levar de forma que o **valor total seja o maior possível**, sem que o **peso total ultrapasse a capacidade** da mochila.

Na versão **0-1** do problema, cada item só pode ser levado inteiro (1) ou deixado de fora (0), não sendo possível levar "meio item".

Apesar de ser simples de entender, o problema é difícil de resolver: com $n$ itens existem $2^n$ combinações possíveis. Com 15 itens são 32.768 combinações, mas com 100 itens já seriam mais de $10^{30}$, tornando inviável testar todas. Por isso, ele é classificado como um problema **NP-completo** (um dos 21 problemas NP-completos de Richard Karp, 1972) e é muito utilizado para demonstrar meta-heurísticas como o Algoritmo Genético, que encontram soluções boas (muitas vezes a ótima) sem precisar testar todas as combinações.

---

### 🛠️ Funcionalidades:

- **Evolução / Busca da solução:**
    - Realiza a leitura de um arquivo `.csv` com os itens disponíveis (nome, peso e valor)
    - Usuário indica a capacidade da mochila, o tamanho da população, a taxa de cruzamento e a taxa de mutação
    - Gera a população inicial de cromossomos aleatoriamente
    - Evolui a população através de seleção por roleta, cruzamento de um ponto, mutação e elitismo
    - Mostra o resultado da evolução, ou seja, a melhor geração, a melhor aptidão (valor total), o peso total, o melhor cromossomo, os itens selecionados e o total de gerações

- **Teste / Avaliação:**
    - Carrega a melhor solução encontrada pelo Algoritmo Genético
    - Calcula a solução ótima por força bruta (testando todas as combinações) e mostra quão próximo o Algoritmo Genético chegou dela
    - Usuário monta uma mochila com os itens que quiser e o programa mostra em tela o peso total e a aptidão dessa mochila, comparando com a solução do Algoritmo Genético

---

### ⚙️ Pré-requisitos:

- **Linguagem:** Python 3.12+
- **Bibliotecas:** `numpy` - Operações vetoriais e geração de números aleatórios

---

### 👾 Como executar:

- **Local:**
    <br>Com o Python 3.12+ e a biblioteca numpy instalados, abra o VS Code (ou sua IDE de preferência) e execute:
    - `git clone https://github.com/gabrielpassos7/modelo-algoritmo-genetico` - Para clonar o repositório para sua máquina
    - `python algoritmo_genetico.py` - Para executar o Algoritmo Genético e encontrar a melhor solução
    - `python testar_modelo.py` - Para avaliar a solução encontrada e testar novas combinações de itens

- **Codespaces:**
    <br>No repositório do GitHub, clique em ![](https://img.shields.io/badge/%3C%3E_Code_▾-238636?style=flat), depois em `Codespaces` e por fim em ![](https://img.shields.io/badge/Create_codespace_on_main-238636?style=flat)
    <br>Assim que o Codespace for criado, execute no terminal:
    - `pip install numpy` - Para instalar a biblioteca numpy
    - `python algoritmo_genetico.py` - Para executar o Algoritmo Genético e encontrar a melhor solução
    - `python testar_modelo.py` - Para avaliar a solução encontrada e testar novas combinações de itens

---

### 🧮 Fundamentação matemática e implementação:

- **Formulação do problema:**

$$\text{maximizar} \sum_{i=1}^{n} v_i x_i \text{~~~~sujeito a~~~~} \sum_{i=1}^{n} p_i x_i \le C \text{~~,~~} x_i \in \{0, 1\}$$

Onde $v_i$ representa o valor do item $i$, $p_i$ representa o peso do item $i$, $C$ representa a capacidade da mochila e $x_i$ indica se o item $i$ foi selecionado (1) ou não (0).

<br>

- **Representação do cromossomo e população inicial:**

Cada indivíduo da população é uma possível solução, representada por um cromossomo binário com um gene para cada item:

$$x = (x_1, x_2, \ldots, x_n)$$

Por exemplo, o cromossomo `[1 0 1 0 ...]` indica que o primeiro e o terceiro itens foram colocados na mochila. A população inicial é gerada com genes aleatórios.

<br>

```
def gerar_populacao(tamanho, qtd_genes):

    return np.random.randint(0, 2, (tamanho, qtd_genes))
```

<br>

- **Função de aptidão (Fitness):**

$$
f(x) = \begin{cases}
\sum_{i=1}^{n} v_i x_i, & \text{se } \sum_{i=1}^{n} p_i x_i \le C \\
0, & \text{se } \sum_{i=1}^{n} p_i x_i > C
\end{cases}
$$

Onde $f(x)$ representa o quão boa é a solução. Mochilas que ultrapassam a capacidade são penalizadas com aptidão igual a zero.

<br>

```
def calcular_aptidao(populacao, pesos, valores, capacidade):

    peso_total = np.dot(populacao, pesos)
    valor_total = np.dot(populacao, valores)

    return np.where(peso_total <= capacidade, valor_total, 0)
```

<br>

- **Seleção por roleta:**

Cada indivíduo recebe uma "fatia" de uma roleta proporcional à sua aptidão, assim indivíduos melhores têm mais chance de serem escolhidos como pais:

$$P_k = \frac{f(x_k)}{\sum_{j=1}^{N} f(x_j)}$$

Onde $P_k$ representa a probabilidade do indivíduo $k$ ser selecionado e $N$ representa o tamanho da população. Caso todos os indivíduos tenham aptidão zero, todos recebem a mesma probabilidade.

<br>

```
def selecionar_roleta(populacao, aptidoes):

    total = np.sum(aptidoes)

    if total == 0:
        probabilidades = np.full(len(populacao), 1 / len(populacao))
    else:
        probabilidades = aptidoes / total

    indice = np.random.choice(len(populacao), p=probabilidades)

    return populacao[indice]
```

<br>

- **Cruzamento de um ponto (Crossover):**

Com probabilidade igual à taxa de cruzamento $p_c$, é sorteado um ponto de corte $c$ e os pais trocam seus genes a partir dele, gerando dois filhos:

$$\text{filho}_1 = (\text{pai}_1[1..c] ~,~ \text{pai}_2[c+1..n])$$

$$\text{filho}_2 = (\text{pai}_2[1..c] ~,~ \text{pai}_1[c+1..n])$$

Caso o cruzamento não ocorra, os filhos são cópias dos pais.

<br>

```
def cruzar(pai1, pai2, taxa_cruzamento):

    if np.random.rand() > taxa_cruzamento:
        return pai1.copy(), pai2.copy()

    ponto = np.random.randint(1, len(pai1))

    filho1 = np.concatenate((pai1[:ponto], pai2[ponto:]))
    filho2 = np.concatenate((pai2[:ponto], pai1[ponto:]))

    return filho1, filho2
```

<br>

- **Mutação:**

Cada gene do filho tem uma pequena probabilidade $p_m$ (taxa de mutação) de ser invertido, o que mantém a diversidade da população e evita que ela fique presa em soluções ruins:

$$
x_i' = \begin{cases}
1 - x_i, & \text{com probabilidade } p_m \\
x_i, & \text{com probabilidade } 1 - p_m
\end{cases}
$$

<br>

```
def mutar(cromossomo, taxa_mutacao):

    sorteio = np.random.rand(len(cromossomo)) < taxa_mutacao

    return np.where(sorteio, 1 - cromossomo, cromossomo)
```

<br>

- **Elitismo e nova geração:**

O melhor indivíduo de cada geração é copiado diretamente para a próxima, garantindo que a melhor solução encontrada nunca seja perdida. O restante da nova população é preenchido com os filhos gerados pela seleção, cruzamento e mutação. Esse ciclo se repete até atingir o número máximo de gerações.

<br>

```
nova_populacao = [populacao[indice_melhor].copy()]

while len(nova_populacao) < tamanho_populacao:

    pai1 = f.selecionar_roleta(populacao, aptidoes)
    pai2 = f.selecionar_roleta(populacao, aptidoes)

    filho1, filho2 = f.cruzar(pai1, pai2, taxa_cruzamento)

    nova_populacao.append(f.mutar(filho1, taxa_mutacao))

    if len(nova_populacao) < tamanho_populacao:
        nova_populacao.append(f.mutar(filho2, taxa_mutacao))

populacao = np.array(nova_populacao)
```

<br>

- **Validação por força bruta:**

Como o arquivo de exemplo possui apenas 15 itens, é possível testar todas as $2^{15} = 32.768$ combinações para encontrar a solução ótima e verificar o quão próximo o Algoritmo Genético chegou dela:

$$\text{desempenho} = \frac{f(x_{AG})}{f(x_{ótimo})} \cdot 100\%$$

<br>

```
def calcular_solucao_otima(pesos, valores, capacidade):

    combinacoes = np.array(list(itertools.product([0, 1], repeat=len(pesos))))

    aptidoes = calcular_aptidao(combinacoes, pesos, valores, capacidade)

    indice = np.argmax(aptidoes)

    return combinacoes[indice], aptidoes[indice]
```

---

### 📄 Referências:
- [Problema da mochila (Wikipedia)](https://pt.wikipedia.org/wiki/Problema_da_mochila)
- [Algoritmo genético (Wikipedia)](https://pt.wikipedia.org/wiki/Algoritmo_gen%C3%A9tico)
- [Algoritmos Genéticos - Material de aula (USP)](https://edisciplinas.usp.br/pluginfile.php/7975583/mod_resource/content/1/aula_AG_2023.pdf)
- [Algoritmos Genéticos - Slides de Inteligência Artificial (UEMS)](https://www.comp.uems.br/~osvaldo/IA/2026/GENETICOS/IA-04AlgoritmosGeneticos.pdf)
- [Algoritmo genético em Python (DataCamp)](https://www.datacamp.com/pt/tutorial/genetic-algorithm-python)
