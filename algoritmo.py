import time
import random

ARRAY_SIZE = 25
SLEEP_TIME = 0.1  # Em Python, o tempo é em segundos (0.1s = 100.000 microssegundos)

# Função para exibir o array de forma visual
def print_array(arr, size=None):
    if size is None:
        size = len(arr)
        
    for i in range(size):
        print(f"|{arr[i]:3d}| ", end="")
    print()

# Funções Bubble Sort com exibição de passos
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                # Troca de valores em Python (dispensa variável temporária)
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

                # Exibir o array após cada troca
                print_array(arr)
                time.sleep(SLEEP_TIME)

# Funções Quick Sort com exibição de passos
def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

            # Exibir o array após cada troca
            print_array(arr, high + 1)
            time.sleep(SLEEP_TIME)
            
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

# Funções Merge Sort com exibição de passos
def merge(arr, l, m, r):
    # Em Python, podemos fatiar (slice) a lista diretamente
    L = arr[l:m + 1]
    R = arr[m + 1:r + 1]

    i = 0
    j = 0
    k = l

    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

        # Exibir o array após cada passo de mesclagem
        print_array(arr, r + 1)
        time.sleep(SLEEP_TIME)

    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1

    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1

def merge_sort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r)

# Função para salvar os resultados no arquivo resultado.txt
def save_results_to_file(bubble_time, quick_time, merge_time):
    # O comando 'with' cuida de fechar o arquivo automaticamente
    try:
        with open("resultado.txt", "a") as file:
            file.write("\n\nResultados da execucao:\n")
            file.write(f"Bubble Sort: {bubble_time:.6f} segundos\n")
            file.write(f"Quick Sort: {quick_time:.6f} segundos\n")
            file.write(f"Merge Sort: {merge_time:.6f} segundos\n")

            # Determina o algoritmo mais rápido
            if bubble_time < quick_time and bubble_time < merge_time:
                file.write("Bubble Sort foi o mais rapido.\n")
            elif quick_time < bubble_time and quick_time < merge_time:
                file.write("Quick Sort foi o mais rapido.\n")
            else:
                file.write("Merge Sort foi o mais rapido.\n")
                
            file.write("\n--------------------------------")
    except IOError:
        print("Erro ao abrir o arquivo resultado.txt")

# Função para ler e exibir o conteúdo do arquivo resultado.txt
def display_results_from_file():
    try:
        with open("resultado.txt", "r") as file:
            print("\nConteúdo do arquivo resultado.txt:")
            for line in file:
                print(line, end="") # end="" pois a linha já tem a quebra de linha do arquivo
    except IOError:
        print("Erro ao abrir o arquivo resultado.txt")

# Função Principal
def main():
    bubble_time, quick_time, merge_time = -1.0, -1.0, -1.0
    bubble_done, quick_done, merge_done = False, False, False

    while True:
        # Preenche o array com números aleatórios
        arr = [random.randint(0, 99) for _ in range(ARRAY_SIZE)]

        print("\nArray das imagens atuais sem ordenacao:")
        print_array(arr)

        print("\nEscolha o algoritmo de ordenacao:")
        print("1. Bubble Sort")
        print("2. Quick Sort")
        print("3. Merge Sort")
        print("4. Ver Resultados")
        print("5. Sair")
        
        try:
            choice = int(input("Escolha: "))
        except ValueError:
            print("Entrada inválida! Digite um número.")
            continue

        if choice == 1:
            if not bubble_done:
                start = time.perf_counter()
                bubble_sort(arr)
                end = time.perf_counter()
                bubble_time = end - start
                bubble_done = True
                print(f"\nBubble Sort concluído em {bubble_time:.6f} segundos")
            else:
                print("Bubble Sort ja foi executado.")

        elif choice == 2:
            if not quick_done:
                start = time.perf_counter()
                quick_sort(arr, 0, len(arr) - 1)
                end = time.perf_counter()
                quick_time = end - start
                quick_done = True
                print(f"\nQuick Sort concluído em {quick_time:.6f} segundos")
            else:
                print("Quick Sort ja foi executado.")

        elif choice == 3:
            if not merge_done:
                start = time.perf_counter()
                merge_sort(arr, 0, len(arr) - 1)
                end = time.perf_counter()
                merge_time = end - start
                merge_done = True
                print(f"\nMerge Sort concluído em {merge_time:.6f} segundos")
            else:
                print("Merge Sort ja foi executado.")

        elif choice == 4:
            if bubble_done and quick_done and merge_done:
                save_results_to_file(bubble_time, quick_time, merge_time)
                print("\nResultados salvos em resultado.txt")
                display_results_from_file()
            else:
                print("Execute todos os metodos de ordenacao primeiro!")

        elif choice == 5:
            print("Saindo do programa.")
            break

        else:
            print("Opção invalida! Tente novamente.")

        print("\n\n------------------PROGRAMA DE ORDENACAO--------------------")

if __name__ == "__main__":
    main()