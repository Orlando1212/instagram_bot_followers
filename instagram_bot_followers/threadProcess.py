import multiprocessing
import os
import time

# Função que será executada em um processo
def funcao_1():
    print("Iniciando a função 1")
    for i in range(5):
        print("Função 1 executando")
        time.sleep(1)
    print("Função 1 concluída")

# Função que será executada em outro processo
def funcao_2():
    print("Iniciando a função 2")
    for i in range(5):
        print("Função 2 executando")
        time.sleep(1)
    print("Função 2 concluída")

if __name__ == '__main__':
    num_cores = os.cpu_count()

    if num_cores >= 2:  # Verifica se há pelo menos 2 núcleos
        # Criação dos processos
        processo1 = multiprocessing.Process(target=funcao_1)
        processo2 = multiprocessing.Process(target=funcao_2)

        # Inicia os processos
        processo1.start()
        processo2.start()

        # Aguarda até que os processos sejam concluídos
        processo1.join()
        processo2.join()

        print("Todos os processos foram concluídos")
    else:
        print("O processador não possui capacidade suficiente para multiprocessamento. Executando em single-thread.")
        funcao_1()
        funcao_2()
