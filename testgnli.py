from mathfunction import gnli
import numpy as np
import json

def main():

    #Carrega as entradas para do projeto
#     data = {
#     "D": 3.8,
#     "gamma": 1.5e-3,
#     "deltaFch": 100e9,
#     "numberChannels": 39,
#     "potTxdBm": 2,
#     "initialChannelFrequency": 193.1e12,
#     "bandwidthSignal": 50e9,
#     "lenghtSpan": 100e3,
#     "alpha": 0.2e-3,
#     "numberSpan": 10,
#     "numberPolarizations":2,
#     "NFdb": 5,
#     "gaindB": 20
# }

    #Carrega as entradas para do projeto
    data = None
    with open("test/testGnli.json", "r") as json_file:
        data = json.load(json_file)

    #cria uma instancia do gnli
    g = gnli.Gnli(data)

    #calcula o Gnli
    gnil = g.calculateGnli()
    print(gnil)



if __name__ == "__main__":
    main()