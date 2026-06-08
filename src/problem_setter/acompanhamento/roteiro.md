# Atividade de Acompanhamento — UVA 10092 (The Problem with the Problem Setter)

**Grupo I** · T3 — Fluxo Máximo

---

## 1. Resumo do problema

Há um pool com **np** problemas e **nk** categorias. Cada categoria $i$ precisa de exatamente $d_i$ problemas na prova. Cada problema pode ir em **uma ou mais** categorias (lista dada na entrada), mas na prova cada problema entra em **no máximo 1** categoria.

**O que calcular:** dá para escolher problemas do pool respeitando as quantidades por categoria? Se sim, imprimir `1` e quais problemas vão em cada categoria; se não, imprimir `0`.

---

## 2. Entrada e saída

**Entrada (por caso de teste):**
- `nk np` — número de categorias e de problemas no pool.
- Linha com $d_1, d_2, \ldots, d_{nk}$ — quantos problemas cada categoria precisa.
- $np$ linhas: para o problema $j$, quantas categorias aceita e os números dessas categorias.

Termina com `0 0`.

**Saída:**
- `1` + $nk$ linhas com os números dos problemas de cada categoria (qualquer solução válida), ou
- `0` se não for possível.

**Do fluxo para a resposta:** fluxo máximo $=$ soma das demandas → `1` e lemos quais arestas categoria→problema ficaram com fluxo; senão → `0`.

---

## 3. Modelagem como rede de fluxo

Ideia: cada unidade de fluxo = **1 problema escolhido para 1 categoria**.

```text
S  →  categorias  →  problemas  →  T
     (demanda)       (pool)
```

### Vértices

| Vértice | O que é |
| --- | --- |
| `S` | Origem |
| `cat_1` … `cat_nk` | Cada categoria da prova |
| `prob_1` … `prob_np` | Cada problema do pool |
| `T` | Sorvedouro |

### Arestas e capacidades

| De → Para | Capacidade | Por quê |
| --- | ---: | --- |
| `S` → `cat_i` | $d_i$ | Categoria $i$ precisa de $d_i$ problemas |
| `cat_i` → `prob_j` | 1 | Só se o problema $j$ pode ir na categoria $i$ |
| `prob_j` → `T` | 1 | Cada problema usado no máximo 1 vez |

### Origem e sorvedouro

- **`S`:** fornece o total de vagas ($\sum d_i$).
- **`T`:** cada fluxo que chega = 1 problema alocado.
- Sucesso quando fluxo máximo $= \sum d_i$.

---

## 4. Ford-Fulkerson ou Edmonds-Karp?

**Edmonds-Karp** (BFS no residual).

- Grafo moderado ($nk \leq 20$, $np \leq 1000$, soma das demandas $\leq 100$).
- BFS dá caminhos curtos e comportamento estável.
- Capacidades pequenas na maior parte das arestas.

---

## 5. Exemplo pequeno (1º caso do PDF)

```
nk=3, np=15
Demandas: cat1=3, cat2=3, cat3=4  (total = 10)

Problema 1: categorias 1 ou 2
Problema 2: só categoria 3
...
```

Resposta esperada: **1** (há seleção válida).

---

## 6. Resolução manual (ideia)

Precisamos encaixar **10** problemas no total: 3 na cat.1, 3 na cat.2, 4 na cat.3.

Alguns problemas só servem em uma categoria (ex.: prob. 2, 3, 4, 5 → só cat.3). Outros servem em várias.

Uma solução válida do PDF:

| Categoria | Problemas |
| --- | --- |
| 1 | 8, 11, 12 |
| 2 | 1, 6, 7 |
| 3 | 2, 3, 4, 5 |

No fluxo, isso corresponde a 10 caminhos `S → cat_i → prob_j → T`, sem repetir problema.

**2º caso do PDF:** demandas 7+3+4=14, mas só há 15 problemas com restrições apertadas → fluxo máximo $< 14$ → **0**.

---

## 7. Verificação final

- Soma das demandas do caso 1: $3+3+4 = 10$.
- Se o algoritmo acha fluxo 10, imprime `1` e a lista por categoria.
- Cada problema aparece no máximo uma vez; cada categoria recebe a quantidade certa.
- **Grafo residual:** arestas reversas permitem trocar qual problema vai em qual categoria até não haver mais caminho `S → T`.
