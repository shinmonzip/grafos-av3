# Atividade de Acompanhamento — UVA 11045 (My T-shirt suits me)

## 1. Resumo do problema

Victor tem **N** camisetas e **M** voluntários ($N \geq M$). Cada voluntário recebe **no máximo 1** camiseta.

Existem 6 tamanhos (XXL, XL, L, M, S, XS) e **a mesma quantidade de cada um**: $N/6$ por tamanho. Cada voluntário aceita **só 2** tamanhos.

**O que calcular:** para cada caso de teste, dizer se dá para vestir **todos** os M voluntários. Resposta: `YES` ou `NO`. Sobrar camiseta não é problema.

---

## 2. Entrada e saída

**Entrada:**
- 1ª linha: quantidade de casos de teste.
- Em cada caso:
  - linha com `N M`
  - M linhas com os 2 tamanhos que servem naquele voluntário (ex.: `L XL`)

**Saída:**
- Uma linha por caso: `YES` ou `NO`.

**Como tirar a resposta do fluxo:** depois de achar o fluxo máximo, se fluxo $= M$ → `YES`; senão → `NO`.

---

## 3. Modelagem como rede de fluxo

Ideia geral: montamos um grafo em camadas. Cada unidade de fluxo = **1 camiseta indo para 1 voluntário que aceita aquele tamanho**.

```text
S  →  tamanhos  →  voluntários  →  T
     (estoque)     (quem aceita)
```

### Vértices

| Vértice | O que é |
| --- | --- |
| `S` | Origem — de onde saem as camisetas |
| 6 nós de tamanho | XXL, XL, L, M, S, XS |
| `vol_1` … `vol_M` | Um nó por voluntário |
| `T` | Sorvedouro — voluntário que já recebeu camiseta |

### Arestas e capacidades

| De → Para | Capacidade | Por quê |
| --- | ---: | --- |
| `S` → tamanho | $N/6$ | Só existem $N/6$ camisetas daquele tamanho |
| tamanho → voluntário | 1 | Só criamos se o voluntário aceita aquele tamanho |
| voluntário → `T` | 1 | Cada voluntário recebe no máximo 1 camiseta |

### Origem e sorvedouro

- **`S`:** representa todo o estoque disponível.
- **`T`:** cada fluxo que chega em `T` = 1 voluntário vestido.
- Se o fluxo máximo for **M**, todos foram atendidos.

---

## 4. Ford-Fulkerson ou Edmonds-Karp?

**Vamos usar Edmonds-Karp** (Ford-Fulkerson escolhendo o caminho com **BFS**).

Por quê:
- O grafo é pequeno (no máximo ~38 vértices), então os dois funcionariam.
- Edmonds-Karp é mais **previsível** — sempre pega o caminho mais curto no residual.
- BFS em Python: `collections.deque`.

---

## 5. Exemplo pequeno (1º caso do PDF)

```
N = 18, M = 6  →  3 camisetas de cada tamanho

Vol 1: L, XL      Vol 4: S, XS
Vol 2: XL, L      Vol 5: M, S
Vol 3: XXL, XL    Vol 6: M, L
```

Resposta esperada: **YES**.

---

## 6. Resolução manual (Edmonds-Karp)

Rede do exemplo (cada tamanho recebe 3 camisetas de `S`):

```text
S → XXL(3) → vol_3
  → XL(3)  → vol_1, vol_2, vol_3
  → L(3)   → vol_1, vol_2, vol_6
  → M(3)   → vol_5, vol_6
  → S(3)   → vol_4, vol_5
  → XS(3)  → vol_4

  vol_1 … vol_6 → T (capacidade 1 cada)
```

Encontramos 6 caminhos aumentantes (BFS), um por voluntário:

| Passo | Caminho | Quem veste | Fluxo total |
| --- | --- | --- | ---: |
| 1 | S → L → vol_1 → T | vol_1 usa L | 1 |
| 2 | S → XL → vol_2 → T | vol_2 usa XL | 2 |
| 3 | S → XXL → vol_3 → T | vol_3 usa XXL | 3 |
| 4 | S → S → vol_4 → T | vol_4 usa S | 4 |
| 5 | S → M → vol_5 → T | vol_5 usa M | 5 |
| 6 | S → L → vol_6 → T | vol_6 usa L | 6 |

Em cada passo o gargalo é **1** (capacidades unitárias nesse trecho).

**Para:** fluxo $= 6 = M$ → não dá para mandar mais fluxo para `T`.

**Exemplo de NO (2º caso do PDF):** $N=6$, $M=4$ → só 1 camiseta de cada tamanho. No máximo 3 voluntários conseguem ser vestidos → fluxo $= 3 < 4$ → `NO`.

---

## 7. Verificação final

- Fluxo máximo $= 6 = M$.
- Distribuição encontrada:
  - vol_1 ← L, vol_2 ← XL, vol_3 ← XXL
  - vol_4 ← S, vol_5 ← M, vol_6 ← L
- Estoque respeitado: L usado 2 vezes (máx. 3), demais tamanhos 1 vez.
- **Resposta: YES** ✓

**Grafo residual (resumo):** depois de cada caminho, a aresta usada fica com menos capacidade e aparece uma aresta reversa. Isso permite **trocar** quem recebeu qual tamanho se precisar. Quando BFS não acha mais caminho de `S` a `T`, o fluxo já é o máximo.
