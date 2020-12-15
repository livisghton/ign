from mathfunction import gnli
from network import networkStructure
import numpy as np
import json
import matplotlib.pyplot as plt
# import matplotlib
# import plotly
#https://python-graph-gallery.com/122-multiple-lines-chart/

def main():

    #Carrega as entradas para do projeto
    # data = {
    # "degree": 14,
    # "D": 3.8,
    # "gamma": 1.5e-3,
    # "deltaFch": 100e9,
    # "numberChannels": 39,
    # "potTxdBm": 2,
    # "initialChannelFrequency": 193.1e12,
    # "bandwidthSignal": 50e9,
    # "lenghtSpan": 100e3,
    # "alpha": 0.2e-3,
    # "numberSpan": 10,
    # "numberPolarizations":2,
    # "NFdb": 5,
    # "gaindB": 20
    # }

    #Carrega as entradas para do projeto
    data = None
    with open("test/testGnli.json", "r") as json_file:
        data = json.load(json_file)
    # matplotlib, plotly

    #carrega estrutura da rede
    # net = networkStructure.NetworkStructure(data)

    # net.networkStructure()

    #cria uma instancia do gnli
    g = gnli.Gnli(data)

    #calcula o Gnli
    gnil = g.calculateGnli()
    
    exp1(data)
    # exp2(data)
    


def exp1(data):
    numSpan = 5
    result_snrNli = []
    result_snrAse = []
    result_osnrNli = []
    result_osnr = []
    result_numSpan = []

    while(numSpan < 26):
        data['numberSpan'] = numSpan

        g = gnli.Gnli(data)
        # gnil = g.calculateGnli()    #calcula a não linearidade

        snrNli = g.snrNli() #Calcula a SNR_NLI
        snrAse = g.snr()    #Calcula a SNR_ASE
        result_snrNli.append(snrNli)
        result_snrAse.append(snrAse)

        result_osnrNli.append(g.osnrNli(snrNli))
        result_osnr.append(g.osnrEdfa(snrAse))

        result_numSpan.append(numSpan)
        numSpan += 5
    
    # print(gnil)
    # print(g.snr())
    showGraphicSnr(result_snrNli, result_snrAse, result_numSpan)
    showGraphicOsnr(result_osnrNli, result_osnr, result_numSpan)

def exp2(data):
    potTx = -5
    result_PotTxsnrNli = []
    result_PotTxsnr = []
    result_PotTxosnr = []
    result_PotTxNli = []
    result_PotTx = []

    while(potTx < 6):
        data["potTxdBm"] = potTx

        g = gnli.Gnli(data)
        # gnil = g.calculateGnli()    #calcula a não linearidade

        snrNli = g.snrNli() #Calcula a SNR_NLI
        snrAse = g.snr()    #Calcula a SNR_ASE
        result_PotTxsnrNli.append(snrNli)
        result_PotTxsnr.append(snrAse)

        result_PotTxNli.append(g.osnrNli(snrNli))
        result_PotTxosnr.append(g.osnrEdfa(snrAse))

        result_PotTx.append(potTx)
        potTx += 1
    
    # print(gnil)
    # print(g.snr())
    showGraphicPotTx1(result_PotTxsnrNli, result_PotTxsnr, result_PotTx)
    showGraphicPotTx(result_PotTxNli, result_PotTxosnr, result_PotTx)


def showGraphicSnr(result_snrNli, result_snr, result_numSpan):
    
    fig, ax = plt.subplots()
    ax.set(xlabel='Número de span', ylabel='SNR [db]', title='relação sinal ruído por número de span')

    plt.plot(result_numSpan, result_snrNli, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=4, label="SNR_NLI")
    plt.plot(result_numSpan, result_snr, marker='o', markerfacecolor='red', markersize=10, color='#FA8072', linewidth=4, label="SNR_ASE")
    plt.legend()
    # fig.save()
    plt.show()


def showGraphicOsnr(result_osnrNli, result_osnr, result_numSpan):
    
    fig, ax = plt.subplots()
    ax.set(xlabel='Número de span', ylabel='OSNR [db]', title='relação sinal ruído óptico por número de span')

    plt.plot(result_numSpan, result_osnrNli, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=4, label="OSNR_NLI")
    plt.plot(result_numSpan, result_osnr, marker='o', markerfacecolor='red', markersize=10, color='#FA8072', linewidth=4, label="OSNR_EDFA")
    plt.legend()
    # fig.save()
    plt.show()

def showGraphicPotTx(result_PotTxNli, result_PotTxosnr, result_PotTx):
    
    fig, ax = plt.subplots()
    ax.set(xlabel='Potência Tx [dBm]', ylabel='osnr [db]', title='relação da potência de transmissão por osnr')

    plt.plot(result_PotTx, result_PotTxNli, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=4, label="OSNR_NLI")
    plt.plot(result_PotTx, result_PotTxosnr, marker='o', markerfacecolor='red', markersize=10, color='#FA8072', linewidth=4, label="OSNR_EDFA")
    plt.legend()
    # fig.save()
    plt.show()

def showGraphicPotTx1(result_PotTxNli, result_PotTxosnr, result_PotTx):
    
    fig, ax = plt.subplots()
    ax.set(xlabel='Potência Tx [dBm]', ylabel='snr [db]', title='relação da potência de transmissão por snr')

    plt.plot(result_PotTx, result_PotTxNli, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=4, label="SNR_NLI")
    plt.plot(result_PotTx, result_PotTxosnr, marker='o', markerfacecolor='red', markersize=10, color='#FA8072', linewidth=4, label="SNR_ASE")
    plt.legend()
    # fig.save()
    plt.show()

if __name__ == "__main__":
    main()