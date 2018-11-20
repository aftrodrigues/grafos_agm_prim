# grafos_agm_prim
Trabalho prático da cadeira Teoria dos Grafos (UFRGS) com uma modificação do algoritmo da Árvore Geradora Mínima (AGMin) de Prim considerando que há vértices com grau máximo igual a 1.

A história para esse projeto: Uma universidade deseja conectar vários roteadores com uma nova topologia e deseja saber quantos metros ou kilometros de fibra precisa comprar.
No entanto, alguns roteadores comportam apenas uma conexão ( vértice de grau 1).

Minha solução usa o algoritmo de Prim para fazer a AGMin com os nodos que podem ter grau > 1, e depois conecta todos os nodos de grau = 1 ao nodo mais próximo que não seja um nodo de gra máximo 1.
