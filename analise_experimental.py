# Ylana Maria Araujo Torres - 541566
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def medir_tempo(func):
    def wrapper(lista):
        lista_copia = lista.copy()
        inicio = time.perf_counter()
        func(lista_copia)
        fim = time.perf_counter()
        return fim - inicio
    return wrapper

@medir_tempo
def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        trocou = False
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        if not trocou:
            break

@medir_tempo
def insertion_sort(lista):
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and chave < lista[j]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave

def merge_sort_recursivo(lista):
    if len(lista) > 1:
        meio = len(lista) // 2
        esq, dir = lista[:meio], lista[meio:]
        merge_sort_recursivo(esq)
        merge_sort_recursivo(dir)
        i = j = k = 0
        while i < len(esq) and j < len(dir):
            if esq[i] < dir[j]: lista[k] = esq[i]; i += 1
            else: lista[k] = dir[j]; j += 1
            k += 1
        while i < len(esq): lista[k] = esq[i]; i += 1; k += 1
        while j < len(dir): lista[k] = dir[j]; j += 1; k += 1
@medir_tempo
def merge_sort(lista):
    merge_sort_recursivo(lista)

def quick_sort_recursivo(lista, baixo, alto):
    if baixo < alto:
        pivo_idx = particao(lista, baixo, alto)
        quick_sort_recursivo(lista, baixo, pivo_idx - 1)
        quick_sort_recursivo(lista, pivo_idx + 1, alto)
def particao(lista, baixo, alto):
    pivo = lista[alto]
    i = baixo - 1
    for j in range(baixo, alto):
        if lista[j] <= pivo:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]
    lista[i + 1], lista[alto] = lista[alto], lista[i + 1]
    return i + 1
@medir_tempo
def quick_sort(lista):
    quick_sort_recursivo(lista, 0, len(lista) - 1)

def heapify(lista, n, i):
    maior = i
    esq, dir = 2 * i + 1, 2 * i + 2
    if esq < n and lista[esq] > lista[maior]: maior = esq
    if dir < n and lista[dir] > lista[maior]: maior = dir
    if maior != i:
        lista[i], lista[maior] = lista[maior], lista[i]
        heapify(lista, n, maior)
@medir_tempo
def heap_sort(lista):
    n = len(lista)
    for i in range(n // 2 - 1, -1, -1):
        heapify(lista, n, i)
    for i in range(n - 1, 0, -1):
        lista[i], lista[0] = lista[0], lista[i]
        heapify(lista, i, 0)

@medir_tempo
def counting_sort(lista):
    if not lista or not all(isinstance(x, int) for x in lista): return
    offset = min(lista)
    max_val = max(lista)
    count = [0] * (max_val - offset + 1)
    for num in lista: count[num - offset] += 1
    for i in range(1, len(count)): count[i] += count[i-1]
    output = [0] * len(lista)
    for i in range(len(lista) - 1, -1, -1):
        num = lista[i]
        output[count[num - offset] - 1] = num
        count[num - offset] -= 1
    for i in range(len(lista)): lista[i] = output[i]

def counting_sort_para_radix(lista, exp):
    n = len(lista)
    output, count = [0] * n, [0] * 10
    for i in range(n): count[(lista[i] // exp) % 10] += 1
    for i in range(1, 10): count[i] += count[i-1]
    i = n - 1
    while i >= 0:
        idx = (lista[i] // exp) % 10
        output[count[idx] - 1] = lista[i]
        count[idx] -= 1
        i -= 1
    for i in range(n): lista[i] = output[i]
@medir_tempo
def radix_sort(lista):
    if not lista or not all(isinstance(x, int) for x in lista): return
    negativos = [abs(x) for x in lista if x < 0]
    positivos = [x for x in lista if x >= 0]
    if positivos:
        max_val_pos = max(positivos) if positivos else 0
        exp = 1
        while max_val_pos // exp > 0:
            counting_sort_para_radix(positivos, exp)
            exp *= 10
    if negativos:
        max_val_neg = max(negativos) if negativos else 0
        exp = 1
        while max_val_neg // exp > 0:
            counting_sort_para_radix(negativos, exp)
            exp *= 10
    resultado_final = [-x for x in reversed(negativos)] + positivos
    for i in range(len(lista)): lista[i] = resultado_final[i]


def executar_analise():

    algoritmos_a_testar = {
        "Bubble Sort": bubble_sort, "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort, "Quick Sort": quick_sort,
        "Heap Sort": heap_sort, "Counting Sort": counting_sort,
        "Radix Sort": radix_sort,
    }

    dados_base_por_algoritmo = {
        "Bubble Sort": [-49, 43, -17, 92, 54, -76, 32, 14, -4, 47],
        "Insertion Sort": ['Y', 'L', 'A', 'N', 'A', 'M', 'A', 'R', 'I', 'A'],
        "Merge Sort": [88, 69, 66, 27, 80, 71, 65, 80, 17, 55],
        "Quick Sort": [64, 39, 70, 54, 46, 42, 53, 58, 9, 33],
        "Heap Sort": [64, 39, 70, 54, 46, 42, 53, 58, 9, 33], # Base para Heap Sort
        "Counting Sort": [6, 1, 5, 5, 6, 4, 1, 3, 6, 3],
        "Radix Sort": [19580, 98467, 79939, 81534, 33585, 24080, 21644, 76995, 48573, 23943]
    }

    resultados = []
    tamanhos_n = range(10, 201, 10)

    print(">>> Iniciando Análise Experimental <<<")

    for nome_algoritmo, lista_base in dados_base_por_algoritmo.items():
        print(f"\nProcessando Algoritmo: {nome_algoritmo}...")
        funcao_algoritmo = algoritmos_a_testar[nome_algoritmo]
        
        for n in tamanhos_n:
            original = (lista_base * (n // 10 + 1))[:n]
            
            pode_processar = all(isinstance(x, (int, float)) for x in original) or nome_algoritmo == "Insertion Sort"

            if not pode_processar and nome_algoritmo in ["Counting Sort", "Radix Sort"]:
                continue

            crescente = sorted(original)
            decrescente = sorted(original, reverse=True)
            
            listas_para_teste = { "Original": original, "Crescente": crescente, "Decrescente": decrescente }
            
            for tipo_lista, lista in listas_para_teste.items():
                tempo = funcao_algoritmo(lista)
                resultados.append({
                    "Algoritmo": nome_algoritmo, "Tipo de Lista": tipo_lista,
                    "Tamanho (n)": n, "Tempo (s)": tempo,
                })

    df_resultados = pd.DataFrame(resultados)
    print("\nProcessamento concluído!")


    print("\nGerando gráficos de desempenho...")
    sns.set_theme(style="whitegrid")
    
    for tipo in ["Original", "Crescente", "Decrescente"]:
        subset = df_resultados[df_resultados["Tipo de Lista"] == tipo]
        
        plt.figure(figsize=(14, 8))
        sns.lineplot(data=subset, x="Tamanho (n)", y="Tempo (s)", hue="Algoritmo", marker='o', errorbar=None)
        
        plt.title(f"Desempenho dos Algoritmos (Entrada {tipo})", fontsize=16)
        plt.xlabel("Tamanho da Entrada (n)", fontsize=12)
        plt.ylabel("Tempo de Execução (segundos)", fontsize=12)
        plt.legend(title="Algoritmos")
        plt.tight_layout()
        
        nome_arquivo = f"grafico_desempenho_{tipo.lower()}.png"
        plt.savefig(nome_arquivo)
        print(f"Gráfico salvo: {nome_arquivo}")

    print("\nAnálise experimental finalizada com sucesso!")

if __name__ == "__main__":
    executar_analise()