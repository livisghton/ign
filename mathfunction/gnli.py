from scipy import constants
import math
import numpy as np
from scipy import signal

class Gnli:
    """
    Implementação da eq. 41 de P. Poggiolini do artigo "The GN-Model of Fiber Non-Linear Propagation
    and its Applications".
    """

    def __init__(self, data):

        self.d = data['D']                   #coeficiente de dispersão cromática ps/nm/km  
        self.gamma = data['gamma']                   #1/W/m0
        self.deltaFch = data['deltaFch']                #channel spacing [Hz]
        self.numberChannels = data['numberChannels']                #numbers of channels
        self.potTxdBm = data['potTxdBm']                    #Potência/canal lancada do transmissor [dBm]
        self.initialChannelFrequency = data['initialChannelFrequency']          #Frequência do canal inicial [THz]
        self.listChannelFrequency = [x*self.deltaFch + self.initialChannelFrequency for x in range(0, self.numberChannels)]     #lista de canais
        # self.bandwidthSignal = data['bandwidthSignal']              #largura de banda do sinal [Hz]
        self.bandwidthSignal = data['bandwidthSignal'] #* np.ones(self.numberChannels)
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
        Calcula a densidade spectral de potencia (PSD) do canal no 1º span.
        """

        return math.pow(10, (self.potTxdBm - 30) / 10) / self.bandwidthSignal


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


    #calcula o modelo ign
    def calculateGnli(self):
        bandwidthSignal = [x * self.bandwidthSignal for x in [1] * self.numberChannels]

        G_tx_ch = [x * self.powerSpectralDensity() for x in [1] * self.numberChannels]

        result = 1
        i = 0
        while(i < self.numberSpan):
            n = 0
            while(n < self.numberChannels):
                result *= np.prod(np.math.exp(( 1 / self.dB2Neper) * (2 * self.gaindB + self.gaindB - (3 * self.alpha * self.lenghtSpan) ) ) ) \
                * np.prod( math.exp( (1 / self.dB2Neper) * self.gaindB -(self.alpha * self.lenghtSpan) ) ) \
                    * math.pow(G_tx_ch[n], 2) * G_tx_ch[i] * (2 - signal.unit_impulse(self.numberChannels, n)) \
                    * self.psi2(bandwidthSignal[i], bandwidthSignal[n], self.listChannelFrequency[i], self.listChannelFrequency[n])
                n += 1
            
            i += 1
        
        return result


    def calculateGnli1(self):
        bandwidthSignal = [x * self.bandwidthSignal for x in [1] * self.numberChannels]
        G_tx_ch = [x * self.powerSpectralDensity() for x in [1] * self.numberChannels]
        # gaindB = [x * self.dB2Neper for x in [1] * self.numberChannels]
        gaindB = np.ones((self.numberChannels, self.numberSpan)) * self.gaindB
        print("beta2: " + str(self.beta2() ) )
        print("alpha: " + str(self.alpha))
        print("Neper: " + str(self.dB2Neper))

        # result = 0
        result = np.ones((self.numberChannels, self.numberSpan))
        i = 0
        while(i < self.numberChannels):
            print(i)
            j = 0
            while(j < self.numberSpan):
                n = 0
                while(n < self.numberChannels):
                    # print(type())
                    
                    result[n][j] = np.prod(np.exp( (1 / self.dB2Neper) * (2 * gaindB[n][0:j] + gaindB[i][0:j] - (3 * self.alpha * self.lenghtSpan) ) ) ) \
                    * np.prod( np.exp( (1 / self.dB2Neper) * (gaindB[i][j+1:self.numberSpan] -(self.alpha * self.lenghtSpan) ) ) ) \
                    * math.pow(G_tx_ch[n], 2) * G_tx_ch[i] * (2 - (1 if n == i else 0) ) \
                    * (1 / (4 * constants.pi * abs(self.beta2()) * math.pow((self.alpha / self.dB2Neper), -1) )) \
                    * (math.asinh( math.pow(constants.pi, 2) * math.pow((self.alpha/self.dB2Neper), -1) * abs(self.beta2()) * (self.listChannelFrequency[n] - self.listChannelFrequency[i] + (bandwidthSignal[n]/2)) *bandwidthSignal[i] ) \
                    - math.asinh( math.pow(constants.pi, 2) * math.pow((self.alpha/self.dB2Neper), -1) * abs(self.beta2()) * (self.listChannelFrequency[n] - self.listChannelFrequency[i] - (bandwidthSignal[n]/2)) *bandwidthSignal[i] ) )
                    
                    # print(result)
                    # if(n == 15):
                        # print("i: "+ str(i))
                        # print("j: "+ str(j))
                        # print("n: "+ str(n))
                        # exit()

                    n += 1

                j += 1
            i += 1
        
        return result
    
    def psi1(self, B_ch_i):
        """
        Implementa a equação psi, quando n = i
        """
        a = 2 * constants.pi * abs(self.beta2()) * abs(math.pow((2 * self.alpha), -1))
        b = math.asinh( (math.pow(constants.pi, 2)/2) * abs(self.beta2) * abs(math.pow((2 * self.alpha), -1)) * math.pow(B_ch_i, 2) )

        return b / a


    def psi2(self, B_ch_i, B_ch_n, f_ch_i, f_ch_n):
        """
        Implementa a equação psi, quando n != i
        """
        a = 4 * constants.pi * math.pow((2 * self.alpha), -1) * abs(self.beta2())
        b = math.pow(constants.pi, 2) * abs(math.pow(2 * self.alpha, -1)) * abs(self.beta2()) * abs(f_ch_n - f_ch_i + (B_ch_n / 2) ) * B_ch_i
        c = math.pow(constants.pi, 2) * abs(math.pow(2 * self.alpha, -1)) * abs(self.beta2()) * abs(f_ch_n - f_ch_i - (B_ch_n / 2) ) * B_ch_i

        return (b - c) / a



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
