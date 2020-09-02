from mathfunction import gnli
import numpy as np
import json

def main():

    #Carrega as entradas para do projeto
    data = {
    "D": 3.8,
    "gamma": 1.5e-3,
    "deltaFch": 100e9,
    "numberChannels": 39,
    "potTxdBm": 2,
    "initialChannelFrequency": 193.1e12,
    "bandwidthSignal": 50e9,
    "lenghtSpan": 100e3,
    "alpha": 0.2e-3,
    "numberSpan": 10,
    "numberPolarizations":2,
    "NFdb": 5,
    "gaindB": 20
}

    # data = None
    # with open("test/testGnli.json", "r") as json_file:
    #     data = json.load(json_file)
        # print(data['gamma'])

    #cria uma instancia do gnli
    g = gnli.Gnli(data)

    #calcula o gnli
    # g.printInput()
    # print(g.powerSpectralDensity())
    # g.calculateGnli1()
    print(g.calculateGnli1())
    # g.printConstants()


    # carregar um arquivo json com todos os paremetros do gnli
    # f = json.load("testGnli.json")
    # print(f)


    # print("pegou!!!")
    # x = gnli.Gnli("pegou")
    # print(x)
    # x.printResult()


if __name__ == "__main__":
    main()