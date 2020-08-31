from scipy import constants
import math

class Gnli:
    """
    Implementação da eq. 41 de P. Poggiolini do artigo "The GN-Model of Fiber Non-Linear Propagation
    and its Applications".
    """

    #Definições de constantes
   

    
    def __init__(self, data):

        self.d = data['D']                   #coeficiente de dispersão cromática ps/nm/km  
        self.gamma = data['gamma']                   #1/W/m0
        self.deltaFch = data['deltaFch']                #channel spacing [Hz]
        self.numberChannels = data['numberChannels']                #numbers of channels
        self.potTxdBm = data['potTxdBm']                    #Potência/canal lancada do transmissor [dBm]
        self.initialChannelFrequency = data['initialChannelFrequency']          #Frequência do canal inicial [THz]
        self.listChannelFrequency = [x*self.deltaFch + self.initialChannelFrequency for x in range(0, self.numberChannels)]     #Frequencia de todos os canais
        self.bandwidthSignal = data['bandwidthSignal']              #largura de banda do sinal [Hz]
        self.lenghtSpan = data['lenghtSpan']                    #Comprimento dos span [m]
        self.alpha = data['alpha']                          #atenuação da fibra [dB/m]
        self.numberSpan = data['numberSpan']                #numero de spans
        self.numberPolarizations = data['numberPolarizations']      #numero de polarização
        self.NFdb = data['NFdb']
        self.gaindB = data['gaindB']

        #constantes
        self.h = constants.Planck
        self.nu = constants.speed_of_light/1550e-9
        self.SNR2OSNR = 10*math.log(10)*(self.bandwidthSignal/(12.5e9*self.numberPolarizations/2))      #Eq. (34) of Essiambre et al., "0," J. Light. Technol., vol. 28, no. 4, pp. 662-701, Feb. 2010.
        self.dB2Neper = 10/(math.log(10))


    def beta2(self):
        """
        Calcula o coeficiente de disperção
        """

        return -( math.pow(1550e-9, 2) * (self.d * 1e-6) / (2 * constants.pi * 3e8) )


    def leff(self):
        """
        Calcula o comprimento efetivo [m]
        """

        return ( (1 - math.exp(-(self.alpha/self.dB2Neper) * self.lenghtSpan )) / (self.alpha / self.dB2Neper) )

    
    def powerSpectralDensity(self):
        """
        Calcula a densidade spectral de potencia (PSD) do canal no 1º span
        """

        return math.pow(10, (self.potTxdBm - 30) / 10) / self.bandwidthSignal

    #calcular o coeficiente ASE
    def coeficienteAse(self):
        """
        Calcula o coeficiente ASE
        """

        aseCoef = (math.pow(10, self.NFdb/10) / 2) * (math.pow(10, (self.gaindB / 10)) - 1)

        i = 1
        while( i < self.numberSpan):
            aseCoef = (math.pow(10, self.NFdb/10) / 2) * (math.pow(10, (self.gaindB / 10)) - 1) + aseCoef * math.pow(10, (self.gaindB - self.alpha*self.lenghtSpan) / 10)
            i += 1
        return aseCoef

    
    def ase(self):
        """
        Calculo da ase
        """
        return self.numberPolarizations * self.h * self.nu * self.coeficienteAse()



    def printInput(self):
        print("D: " + str(self.d))
        print("gamma: " + str(self.gamma))
        print("deltaFch: " + str(self.deltaFch))
        print("nummberChannels: " + str(self.numberChannels))
        print("potTxdBm: " + str(self.potTxdBm))
        print("initialChannelFrequency: " + str(self.initialChannelFrequency))
        print("listChannelFrequency: " + str(self.listChannelFrequency))
        print("bandwidthSignal: "+ str(self.bandwidthSignal))
        print("lenghtSpan: " + str(self.lenghtSpan))
        print("alpha: " + str(self.alpha))
        print("numberSpan: " + str(self.numberSpan))
        print("numberPolarizations: " + str(self.numberPolarizations))
        print("NFdb: " + str(self.NFdb))
        print("gaindB: " + str(self.gaindB))

    def printConstants(self):
        print("h: " + str(self.h))
        print("nu: " + str(self.nu))
        print("SNR2OSNR: " + str(self.SNR2OSNR))
        print("dB2Neper: " + str(self.dB2Neper))