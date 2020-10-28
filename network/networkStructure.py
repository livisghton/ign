import numpy as np

class NetworkStructure:
    """
    Esta classe implementa toda a estrutura da rede.
    """

    def __init__(self, data):
        self.setDegree(data['degree'])
        self.setNumChannels(self.degree)
        self.setPhysicalMatrix(self.degree)
        self.setNumVertex(self.degree)
        self.aresta = None
        self.grafo = None


    def setDegree(self, degree):
        """
        Atribui o valor do grau da rede.
        """
        self.degree = degree

    def getDegree(self):
        """
        Retorna o grau da rede.
        """
        return self.degree

    def setNumChannels(self, degree):
        """
        Seta a o numero de canais na rede.
        """
        self.numChannels = degree * (degree - 1)

    def getNumChannels(self):
        """
        Retorna o número de canais da rede.
        """
        return self.numChannels

    def setPhysicalMatrix(self, degree):
        """
        Inicializa a matriz fisica da rede.
        """
        self.physicalMatrix = np.zeros((degree, degree))

    def getPhysicalMatrix(self):
        """
        Retorna a matriz fisica da rede.
        """
        return self.physicalMatrix

    def setNumVertex(self, degree):
        """
        Seta o número de vértice da rede.
        """
        self.numVertex = degree

    def getNumVertex(self):
        """
        Retorna o número de vértice da rede.
        """
        return self.numVertex

    def networkStructure(self):
        """
        Imprime toda a estrutura da rede.
        """
        print("degree: " + str(self.degree) )
        print("number Channels: " + str(self.numChannels) )
        print("Matriz física: " + str(self.physicalMatrix))
        print("Número de aresta: "+ str(self.numVertex) )