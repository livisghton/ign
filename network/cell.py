

class Cell():

    def __init__(self,  vertex, weight):
        self.setVertex(vertex)
        self.setWeight(weight)


    def setVertex(self, vertex):
        """
        Seta um vertice
        """
        self.vertex = vertex


    def getVertex(self):
        """
        Retorna um vertice
        """
        return vertex


    def setWeight(self, weight):
        """
        Seta um peso ao vertice.
        """
        self.weight = weight


    def getWeight(self):
        """
        Retorna o peso do vertice.
        """
        return weight


    def equals(self, vertex):
        """
        Verifica se os verttices são iguais. Se forem iguais retorna True, caso contrário retorna False.
        """
        return (self.getVertex() == vertex)
