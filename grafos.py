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

class vertice:
	def __init__(self, key):
		self.key = key
		self.pred = None
		self.dist = float("Inf")

	def __str__(self):
		return "%s -> d:%s" % (self.key, self.dist)

	def __repr__(self):
		return "\n[%s]->(d:%s) %s" % (self.key, self.dist, self.pred)


def parse_input():
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

def mtr_adj_filt(mtr_adj, limited_devices):
	return None


def reordenar(fila):
	fila.sort(key=lambda x: x.dist)


def na_fila(vertice, fila):
	for v in fila:
		if v.key == vertice:
			return True
	return False


def AGM_prim(mtr_adj, limited_nodes=[], raiz=None):
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
	for i in range( num_vertices ):
		vertices.append( vertice(i+1) )

	vertices.sort(key = lambda x: x.key)


	if raiz is None:
		raiz = 1
	vertices[raiz-1].dist = 0
	
	# definindo qual o nodo nao limitado mais proximo da raiz, para comecar a partir dele.
	if raiz in limited_nodes:
		proximo = vertices[0]
		for v in vertices:
			if v.key != raiz and \
			v.key not in limited_nodes and \
			mtr_adj[ v.key-1 ][ raiz-1 ] < mtr_adj[ proximo.key-1 ][ raiz-1 ]:
				proximo = v
		log.debug('nova raiz: %s' % proximo.key)
		proximo.dist = mtr_adj[ proximo.key-1 ][ raiz-1 ]
		proximo.pred = raiz
		
	while raiz in limited_nodes and raiz-1 < len(vertices):
		raiz += 1
			
	for nodo in vertices:
		fila.append(nodo)
	
	reordenar(fila)
	log.debug('fila: %s' % fila)	
	# criando arvore com os nodos que aceitam mais de 1 grau
	while len(fila):
		u = fila.pop(0)
		if u.dist == float('inf'):
			#print(fila)
			None
		if u == 43:
			pdb.set_trace()
		log.debug('u: %s' % u.key)
		if u.key in limited_nodes:
			continue

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

		if u.key in limited_nodes or u.dist == float('inf'):
			for v in range(num_vertices):
				v_dist = mtr_adj[u.key-1][v]
				if v+1 != u.key and v_dist < u.dist and v+1 not in limited_nodes:
					u.dist = v_dist
					u.pred = v+1
	return vertices

def soma(vertices, limited_devices):
	soma = 0
	for v in vertices:
		soma += v.dist

	for l in limited_devices:
		total = 0
		for v in vertices:
			if v.key == l:
				log.debug('v[%s].pred= %s; d=%s' % (v.key, v.pred, v.dist))
			if v.pred == l:
				total += 1

	#if total != 1:
	log.debug('repetido ou ausente: %s(%s)' % (l, total))
	return soma


def main():
	format = ('%(funcName)s %(lineno)d %(msg)s')
	LEVELS = ['INFO', 'DEBUG']
	level = LEVELS[0]
	log.basicConfig(level=level)
	campis = int(raw_input())
	lista_total = [21, 33]
	if level == 'DEBUG':
		campis = 1
	
	respostas = open('../casos_de_teste/teste100b_respostas.txt','r')

	for i in range(1, campis+1):
		devices = parse_input()
		for line in devices['mtr_adj']:
			log.debug(line)
		log.debug('size of mtr_adj: %s' % len(devices['mtr_adj']))
		log.debug('lim_devices: %d' % (len(devices['limited_devices'])))
		log.debug('lim_devices: %s' % devices['limited_devices'])

		for v in range(1, len(devices['mtr_adj'])+1):
			vertices = AGM_prim( devices['mtr_adj'], devices['limited_devices'], 2)
			total = soma(vertices, devices['limited_devices'])

			# validando resultados:
			resposta = respostas.readline().replace('\n','').split(" ")
			certo = False
			#print('original: %s' % (resposta))
			#print('resposta "%s" e "%s"' % (resposta[1][:-1], resposta[-1]))
			if int(resposta[1][:-1]) == i and int(resposta[-1]) == total:
				certo = True
			print('Campus %s: %s = %s' % (i, total, certo))
			if total not in lista_total and total == float('inf'):
				log.info('raiz: %s / vertices: \n%s' %(v, vertices))
			if level != LEVELS[1]:
				break
			
		# tentando de outra forma
		# nao utilizar a chave do nome para acessar diretamente o vetor
		#mtr_adj_filt  # matriz que nao contem os nodos limitados
		#mtr_adj_filt = filter( devices['mtr_adj'], devices['limited_devices'] )
		log.debug('\n')

if __name__ == "__main__":
	main()
