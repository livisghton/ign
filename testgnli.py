from mathfunction import gnli
import json

def main():

    #Carrega as entradas para do projeto
    data = None
    with open("test/testGnli.json", "r") as json_file:
        data = json.load(json_file)
        # print(data['gamma'])

    #cria uma instancia do gnli
    g = gnli.Gnli(data)

    #calcula o gnli
    # g.printInput()
    # g.coeficienteAse()
    print(g.coeficienteAse())
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