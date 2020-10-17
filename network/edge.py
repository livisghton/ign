# criação de Aresta para o grafo
# https://github.com/RenanCbcc/Grafos-Python/blob/master/Aresta.py

class Edge():
    
    def __init__(self, source, destiny, weight):
        self.source = source
        self.destiny = destiny
        self.weight = weight
    
    def getSource(self):
        """
        Retorna a origem da aresta.
        """
        return self.source

    def setSource(self, source):
        """
        Seta a origem.
        """
        self.source = source
    
    def getDestiny(self):
        """
        Retorna o destino da aresta.
        """
        return self.destiny

    def setDestiny(self, destiny):
        """
        Seta o destino.
        """
        self.destiny = destiny

    def getWeight(self):
        """
        Retorna o peso da aresta.
        """
        return self.weight

    def setWeight(self, weight):
        """
        Seta o peso na aresta.
        """
        self.weight = weight

	# def __str__(self):
	# 	return "A(%s----%i---->%s)" % (self.origem.getId(),self.peso,self.destino.getId())