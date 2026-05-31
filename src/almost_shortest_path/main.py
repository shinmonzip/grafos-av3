import sys
import heapq

class DirectedEdge:
    """Representa uma aresta direcionada com peso (algs4)."""
    def __init__(self, v: int, w: int, weight: int):
        self._v = v
        self._w = w
        self._weight = weight
        
    def from_vertex(self) -> int:
        return self._v
        
    def to_vertex(self) -> int:
        return self._w
        
    def weight(self) -> int:
        return self._weight

class EdgeWeightedDigraph:
    """Grafo direcionado com pesos nas arestas."""
    def __init__(self, V: int):
        self._V = V
        self._E = 0
        self._adj = [[] for _ in range(V)]
        
    def V(self) -> int:
        return self._V
        
    def add_edge(self, e: DirectedEdge):
        self._adj[e.from_vertex()].append(e)
        self._E += 1
        
    def adj(self, v: int) -> list[DirectedEdge]:
        return self._adj[v]
        
    def edges(self) -> list[DirectedEdge]:
        all_edges = []
        for v in range(self._V):
            all_edges.extend(self._adj[v])
        return all_edges

    def reverse(self) -> 'EdgeWeightedDigraph':
        """Retorna o grafo reverso para encontrar caminhos até o destino."""
        rev = EdgeWeightedDigraph(self._V)
        for v in range(self._V):
            for e in self._adj[v]:
                rev.add_edge(DirectedEdge(e.to_vertex(), v, e.weight()))
        return rev

class DijkstraSP:
    """Algoritmo de Dijkstra para caminhos mínimos."""
    def __init__(self, G: EdgeWeightedDigraph, s: int):
        self._distTo = [float('inf')] * G.V()
        self._distTo[s] = 0.0
        
        self._pq = []
        heapq.heappush(self._pq, (0.0, s))
        
        while self._pq:
            d, v = heapq.heappop(self._pq)
            if d > self._distTo[v]:
                continue
            self._relax(G, v)
            
    def _relax(self, G: EdgeWeightedDigraph, v: int):
        for e in G.adj(v):
            w = e.to_vertex()
            if self._distTo[w] > self._distTo[v] + e.weight():
                self._distTo[w] = self._distTo[v] + e.weight()
                heapq.heappush(self._pq, (self._distTo[w], w))
                
    def dist_to(self, v: int) -> float:
        return self._distTo[v]
        
    def has_path_to(self, v: int) -> bool:
        return self._distTo[v] < float('inf')


def solve():
    """Função principal que gerencia a entrada e a lógica de resolução."""
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    idx = 0
    while idx < len(input_data):
        n = int(input_data[idx])
        m = int(input_data[idx+1])
        idx += 2
        
        if n == 0 and m == 0:
            break
            
        s = int(input_data[idx])
        d = int(input_data[idx+1])
        idx += 2
        
        G = EdgeWeightedDigraph(n)
        
        for _ in range(m):
            u = int(input_data[idx])
            v = int(input_data[idx+1])
            w = int(input_data[idx+2])
            idx += 3
            G.add_edge(DirectedEdge(u, v, w))
            
        # Passo 1: Dijkstra a partir da Origem
        sp_from_s = DijkstraSP(G, s)
        
        # Passo 2: Dijkstra a partir do Destino no Grafo Reverso
        G_rev = G.reverse()
        sp_from_d = DijkstraSP(G_rev, d)
        
        shortest_path_dist = sp_from_s.dist_to(d)
        
        # Passo 3: Criar um novo grafo filtrando todas as arestas 
        # que pertencem a ALGUM dos menores caminhos
        almost_G = EdgeWeightedDigraph(n)
        for e in G.edges():
            u = e.from_vertex()
            v = e.to_vertex()
            w = e.weight()
            
            # Se a soma das distâncias bater com o menor caminho exato,
            # ignoramos a aresta (não adicionamos no novo grafo).
            if sp_from_s.dist_to(u) + w + sp_from_d.dist_to(v) != shortest_path_dist:
                almost_G.add_edge(e)
                
        # Passo 4: Rodar o Dijkstra no novo grafo
        almost_sp = DijkstraSP(almost_G, s)
        
        if almost_sp.has_path_to(d):
            print(int(almost_sp.dist_to(d)))
        else:
            print("-1")

if __name__ == '__main__':
    solve()
