#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging as log
import json

# saida do exemplo 1
# Nodo -> (distancia) predecessor
# 1 ->(0) None 
# 2 ->(2) 5
# 3 ->(4) 4
# 4 ->(1) 1  
# 5 ->(2) 1
# 6 ->(6) 3
# 7 ->(1) 1
# 8 ->(5) 1

# Saida esperada para o input do pdf:
#Campus 1: 21
#campus 2: 33

class vertice:
	"""
	Classe para armazenar cada vértice, seu predecessor e sua distância
	para o predecessor.
	"""
	def __init__(self, key):
		self.key = key
		self.pred = None
		self.dist = float("Inf")

	def __str__(self):
		return "%s -> d:%s" % (self.key, self.dist)

	def __repr__(self):
		return "\n[%s]->(d:%s) %s" % (self.key, self.dist, self.pred)


def parse_input():
	"""
	faz o parse dos inputs via STDIN, de acordo com a descrição do trabalho
	"""
	devices = int(raw_input())
	log.debug("devices: %d" % devices)
	mtr_adj = [None] * devices #  matriz de adjacencia

	for dev in range(devices):
		line = raw_input()
		filtrado = list( filter( None, line.split(" ")))
		mtr_adj[dev] = [ int(x) for x in filtrado ]

	number_limited_devices = int(raw_input())
	line = raw_input()
	filtrado = list( filter( None, line.split(" ")))
	limited_devices = [ int(x) for x in filtrado ]
	
	return {'mtr_adj': mtr_adj, 'limited_devices':limited_devices}


def reordenar(fila):
	fila.sort(key=lambda x: x.dist)


def na_fila(vertice, fila):
	for v in fila:
		if v.key == vertice:
			return True
	return False


def verificar_raiz(mtr_adj, limited_nodes, vertices, raiz=1):
	"""
	se a raiz for um nodo limitado a grau maximo 1, 
	procura o nodo mais proximo da raiz que não é limitado
	para fazer AGM
	"""

	if raiz in limited_nodes:
		for v in vertices:
			if v.key not in limited_nodes and v.key != raiz:
				proximo = v
				break

		for v in vertices:
			if v.key != raiz and \
			v.key not in limited_nodes and \
			mtr_adj[ v.key-1 ][ raiz-1 ] < mtr_adj[ proximo.key-1 ][ raiz-1 ]:
				proximo = v

		log.debug('nova raiz: %s' % proximo.key)
		proximo.dist = mtr_adj[ proximo.key-1 ][ raiz-1 ]
		proximo.pred = raiz


def AGM_prim(mtr_adj, limited_nodes=[], raiz=1):
	"""
	Arvore Geradora Minima, com o algoritmo de Prim
		Gera uma arvore conexa com a soma das arestas minimizadas
	considerando que alguns nodos (limited_nodes) podem ter grau max = 1

	mtr_adj: matriz de adjacencia, o indice = (nodo.key - 1)
	limited_nodes: nodos a serem ignorados
	raiz: nodo raiz da arvore, isto eh, distancia=0 & predecessor=None
	"""
	num_vertices = len(mtr_adj)

	fila = []
	vertices = []  # ordenados de acordo com a chave
	
	#  adicionando os nodos na lista de vertices e ordenando pela key
	for i in range( 1, num_vertices+1 ):
		vertices.append( vertice(i) )

	vertices.sort(key = lambda x: x.key)
	log.debug('vertices: %s' % vertices)
	
	#  fila a ser ordenada pela distancia
	for nodo in vertices:
		fila.append(nodo)

	#  se a raiz tiver grau máximo =1, seleciona o nodo mais próximo da raiz
	#  para tornar ele a 'raiz'
	verificar_raiz(mtr_adj, limited_nodes, vertices, raiz)
	
	vertices[raiz-1].dist = 0

	#  ordena a fila por ordem de distancia para o predecessor.
	reordenar(fila)
	log.debug('fila: %s' % fila)

	# criando arvore com os nodos que aceitam mais de 1 grau
	while len(fila):
		#  nodo a ser testado
		u = fila.pop(0)
		
		#  evitar os nodos com grau máximo = 1 por enquanto
		if u.key in limited_nodes:
			continue
		

		#  passando por todos os outros vértices, e adicionando
		#  para selecionar os nodos que tem o nodo u como predecessor.
		for v in range(1, num_vertices+1):
			if u.key != v and \
			v not in limited_nodes and \
			mtr_adj[ u.key-1 ][v-1] < vertices[v-1].dist and \
			na_fila(v, fila):
				vertices[v-1].pred = u.key
				vertices[v-1].dist = mtr_adj[ u.key-1 ][v-1]
				reordenar(fila)
		log.debug('fila: %s' % fila)	
	
	# conectando os nodos que aceitam grau maximo = 1 na arvore
	for u in vertices:
		if u == raiz:
			continue

		# para cada nodo u de grau máximo = 1
		if u.key in limited_nodes:
			# verificar qual o nodo mais próximo, não limitado, diferente de u
			for v in range(1, num_vertices+1):
				v_dist = mtr_adj[u.key-1][v-1]  #  distância de u até v
				if v != u.key and v_dist < u.dist and v not in limited_nodes:
					u.dist = v_dist
					u.pred = v

	return vertices


def soma(vertices):
	"""
	Soma as distancias para os predecessores de todos os vertices 
	e retorna esse valor
	"""
	soma = 0
	for v in vertices:
		soma += v.dist

	return soma


def main():
	format = ('DEBUG: %(funcName)-8s [%(lineno)d]:%(msg)s')
	level = 'INFO'
	log.basicConfig(level=level, format=format)

	campis = int(raw_input())
			
	for i in range(1, campis+1):
		devices = parse_input()

		log.debug('size of mtr_adj: %s' % len(devices['mtr_adj']))
		for line in devices['mtr_adj']:
			log.debug(line)
		
		log.debug('size of limimited_devices: %d' % (len(devices['limited_devices'])))
		log.debug('matrix of limited_devices: %s' % devices['limited_devices'])

		vertices = AGM_prim( devices['mtr_adj'], devices['limited_devices'], 1)
		total = soma(vertices)
		
		print('Campus %s: %s' % (i, total))


if __name__ == "__main__":
	main()