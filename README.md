# Trabalhos de Grafos - AV3

Repositório destinado ao armazenamento das submissões de exercícios e trabalhos práticos da disciplina de Grafos.

## Problemas Resolvidos

### 1. Grid MST
- **Arquivo:** `gridmst.py`
- **Plataforma:** [Kattis - Grid MST](https://open.kattis.com/problems/gridmst)
- **Objetivo:** Encontrar o peso da Árvore Geradora Mínima (MST) para um conjunto de pontos num plano cartesiano, utilizando a **Distância de Manhattan**.

#### Detalhes da Implementação
Devido à restrição de tempo do juiz online para casos onde $N$ chega a até 100.000 pontos, uma abordagem clássica que calcule o peso de todas as $O(N^2)$ arestas possíveis excede o tempo limite (TLE). 

Para contornar isso e atingir a complexidade de $O(N \log N)$, a solução implementada em Python utiliza:
1. **Propriedade dos Octantes:** Através de 4 transformações geométricas (rotações/reflexões), garantimos que basta conectar cada ponto ao seu vizinho mais próximo em regiões específicas para preservar as arestas que pertencem à MST. Isso reduz drasticamente o total de arestas geradas para $O(N)$.
2. **Sweep Line e Fenwick Tree:** Foi utilizada a técnica de varredura (Sweep Line) em conjunto com uma Binary Indexed Tree (Fenwick Tree) e compressão de coordenadas para consultar rapidamente os vizinhos mais próximos no plano.
3. **Algoritmo de Kruskal:** Após filtrar o subconjunto seguro de arestas candidatas, o clássico Algoritmo de Kruskal é executado utilizando a estrutura Disjoint Set Union (DSU) com path compression e union by rank.
