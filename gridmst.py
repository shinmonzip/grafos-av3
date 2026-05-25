import sys

def kruskal(n, edges):
    """
    Algoritmo de Kruskal para encontrar a Árvore Geradora Mínima (MST).
    Usa a estrutura de dados Disjoint Set Union (DSU) com compressão de caminho e união por rank.
    """
    parent = list(range(n))
    rank = [0] * n

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False

    edges.sort(key=lambda x: x[0])
    mst_weight = 0
    edges_used = 0

    for weight, u, v in edges:
        if union(u, v):
            mst_weight += weight
            edges_used += 1
            if edges_used == n - 1:
                break
                
    return mst_weight

class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) para encontrar o mínimo.
    Armazena o menor valor e o ID do ponto correspondente.
    """
    def __init__(self, size):
        self.tree = [float('inf')] * (size + 1)
        self.id = [-1] * (size + 1)

    def update(self, i, val, pt_id):
        while i < len(self.tree):
            if val < self.tree[i]:
                self.tree[i] = val
                self.id[i] = pt_id
            i += i & (-i)

    def query(self, i):
        min_val = float('inf')
        min_id = -1
        while i > 0:
            if self.tree[i] < min_val:
                min_val = self.tree[i]
                min_id = self.id[i]
            i -= i & (-i)
        return min_id

def solve():
    # Aumentar o limite de recursão para o DSU (precaução)
    sys.setrecursionlimit(200000)
    
    # Lê toda a entrada de uma vez para maior eficiência
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    if n <= 1:
        print(0)
        return

    points = []
    idx = 1
    for i in range(n):
        points.append((int(input_data[idx]), int(input_data[idx+1]), i))
        idx += 2

    edges = []

    # O grafo completo tem O(N^2) arestas, o que é inviável para N=100.000.
    # Usamos a propriedade de que em cada octante, basta conectar um ponto ao 
    # seu vizinho mais próximo para garantir a construção correta da MST.
    # Como o grafo é não-direcionado, cobrir 4 octantes (metade do plano) é suficiente.
    # Definimos 4 transformações geométricas para mapear esses 4 octantes para o primeiro octante.
    transformations = [
        lambda x, y: (x, y),    # Octante 2 (y >= x >= 0)
        lambda x, y: (y, x),    # Octante 1 (x >= y >= 0)
        lambda x, y: (-x, y),   # Octante 3 (y >= -x >= 0)
        lambda x, y: (y, -x)    # Octante 4 (-x >= y >= 0)
    ]

    for transform in transformations:
        # Transforma os pontos de acordo com a função atual
        transformed = []
        for x, y, original_id in points:
            nx, ny = transform(x, y)
            transformed.append((nx, ny, original_id))

        # Ordena por x decrescente, e por y decrescente em caso de empate.
        # Ao processar em ordem decrescente de x, quando estivermos no ponto P,
        # todos os pontos Q já processados terão x_Q >= x_P (condição do octante).
        transformed.sort(key=lambda p: (p[0], p[1]), reverse=True)

        # Compressão de coordenadas: precisamos usar (y - x) como índice na Fenwick Tree.
        # Mapeamos os valores únicos de (y - x) para inteiros de 1 a M.
        y_minus_x_values = sorted(list(set(p[1] - p[0] for p in transformed)))
        # rank mapeia o valor original para um índice de 1 até M
        rank = {val: i + 1 for i, val in enumerate(y_minus_x_values)}

        fenwick = FenwickTree(len(rank))

        for nx, ny, original_id in transformed:
            # Procuramos um ponto Q já processado tal que (y_Q - x_Q) >= (y_P - x_P)
            # Como a Fenwick Tree padrão calcula o mínimo de 1 a 'i', 
            # nós invertemos a ordem do rank para consultar um "sufixo" de valores.
            pos = rank[ny - nx]
            rev_pos = len(rank) - pos + 1

            best_id = fenwick.query(rev_pos)

            if best_id != -1:
                # Calcula a distância de Manhattan original entre P e o melhor ponto Q encontrado
                px, py, _ = points[original_id]
                bx, by, _ = points[best_id]
                weight = abs(px - bx) + abs(py - by)
                edges.append((weight, original_id, best_id))

            # Adiciona o ponto atual na Fenwick Tree.
            # O valor a ser minimizado é (nx + ny), que equivale a minimizar a distância.
            fenwick.update(rev_pos, nx + ny, original_id)

    # Executa Kruskal com as arestas candidatas (O(N) arestas no total)
    mst_cost = kruskal(n, edges)
    print(mst_cost)

if __name__ == '__main__':
    solve()
