# Trabalhos de Grafos - AV3

**Integrantes do Grupo:**
- Natan Shinmon
- Diogo Gifoni
- Luca Solon

Repositório destinado ao armazenamento das submissões de exercícios e trabalhos práticos da disciplina de Grafos.

## Problemas Resolvidos

### 1. Grid MST
- **Arquivo:** `src/gridmst/gridmst.py`
- **Plataforma:** [Kattis - Grid MST](https://open.kattis.com/problems/gridmst)
- **Objetivo:** Encontrar o peso da Árvore Geradora Mínima (MST) para um conjunto de pontos num plano cartesiano, utilizando a **Distância de Manhattan**.

- **Evidência de Aceitação:** ![Grid MST Accepted](src/gridmst/evidencias/gridmst_accepted.png)

#### Como Executar
Como a solução consome os dados da entrada padrão (`stdin`), você pode executar o script passando um arquivo de teste:
```bash
python3 src/gridmst/gridmst.py < entrada_teste.txt
```

#### Detalhes da Implementação
Devido à restrição de tempo do juiz online para casos onde $N$ chega a até 100.000 pontos, uma abordagem clássica que calcule o peso de todas as $O(N^2)$ arestas possíveis excede o tempo limite (TLE). 

Para contornar isso e atingir a complexidade de $O(N \log N)$, a solução implementada em Python utiliza:
1. **Propriedade dos Octantes:** Através de 4 transformações geométricas (rotações/reflexões), garantimos que basta conectar cada ponto ao seu vizinho mais próximo em regiões específicas para preservar as arestas que pertencem à MST. Isso reduz drasticamente o total de arestas geradas para $O(N)$.
2. **Sweep Line e Fenwick Tree:** Foi utilizada a técnica de varredura (Sweep Line) em conjunto com uma Binary Indexed Tree (Fenwick Tree) e compressão de coordenadas para consultar rapidamente os vizinhos mais próximos no plano.
3. **Algoritmo de Kruskal:** Após filtrar o subconjunto seguro de arestas candidatas, o clássico Algoritmo de Kruskal é executado utilizando a estrutura Disjoint Set Union (DSU) com path compression e union by rank.

#### Análise de Complexidade
- **Tempo:** $O(N \log N)$ dominante pela etapa de ordenação das projeções e pelas consultas na Fenwick Tree. O Kruskal roda em $O(V \log V)$ (ou quase linear $O(V \alpha(V))$ com união por rank), o que está dentro do limite global.
- **Espaço:** $O(N)$ para armazenar as coordenadas, vértices do DSU e nós na árvore de indexação binária. Onde $N$ é o número de pontos do grid.

### 2. Almost Shortest Path
- **Arquivo:** `src/almost_shortest_path/main.py`
- **Plataforma:** [UVA Online Judge - 12144](https://onlinejudge.org/external/121/12144.pdf)
- **Objetivo:** Encontrar o menor caminho entre uma origem (S) e um destino (D) descartando qualquer aresta que pertença a *algum* dos caminhos mínimos (Shortest Paths) originais.
- **Evidência de Aceitação:** ![Almost Shortest Path Accepted](src/almost_shortest_path/evidencias/almost_shortest_path_accepted.png)
- **Apresentação:** [Slides em PDF](src/almost_shortest_path/apresentacao/Almost_Shortest_Path_Strategy.pdf)

#### Como Executar
Você pode testar a solução utilizando o arquivo de entradas de exemplo gerado com base no PDF do problema:
```bash
python3 src/almost_shortest_path/main.py < src/almost_shortest_path/dados/entradas_do_problema.txt
```

#### Detalhes da Implementação
Para solucionar o problema de forma eficiente e estruturada:
1. **Modelagem Orientada a Objetos (algs4):** A solução foi arquitetada utilizando as abstrações de grafos vistas na disciplina, com a implementação das classes `DirectedEdge`, `EdgeWeightedDigraph` e `DijkstraSP`.
2. **Dois Passos de Dijkstra:** Primeiramente rodamos o Algoritmo de Dijkstra a partir do vértice de origem ($S$) no grafo normal, e depois a partir do vértice de destino ($D$) no **grafo reverso**.
3. **Filtro de Arestas:** Com as distâncias pré-computadas, iteramos sobre todas as arestas do grafo original. Se `dist[S->U] + peso(U->V) + dist[D->V] == distância_minima_total`, a aresta pertence a um dos menores caminhos e é **descartada**.
4. **Cálculo Final:** Um novo `EdgeWeightedDigraph` é instanciado apenas com as arestas "seguras", e executamos o Dijkstra uma última vez para achar a menor rota válida.

#### Análise de Complexidade
- **Tempo:** O algoritmo de Dijkstra com fila de prioridade (Min-Heap) possui complexidade $O(E \log V)$. Como executamos o algoritmo 3 vezes (Ida, Volta, Caminho Final) e fazemos uma varredura linear nas $E$ arestas para filtrar o grafo, a complexidade total se mantém em $O(E \log V)$.
- **Espaço:** A representação do grafo via lista de adjacências (`EdgeWeightedDigraph`) e as estruturas do Dijkstra (`distTo`, `edgeTo`, Min-Heap) ocupam espaço $O(V + E)$ na memória.

