import random

def gerar_tarefas_estoque_e_docas(n_areas_estoque: int, 
                                  n_tarefas_estoque: int, 
                                  n_tarefas_docas: int) -> dict[str, int]:
    """
    Gera um número aleatório de tarefas para áreas de estoque e para as docas de entrada, garantindo que o total
    de tarefas nas áreas de estoque seja igual a n_tarefas_estoque.

    Parâmetros:
    ----------- 
    n_areas_estoque : int
        Número de áreas de estoque.
    n_tarefas_estoque : int
        Número total de tarefas que serão distribuídas aleatoriamente entre as áreas de estoque.
    n_tarefas_docas : int
        Número de tarefas que podem ser geradas para as docas de entrada.

    Retorno:
    --------
    dict[str, int]
        Dicionário onde as chaves são os nomes das áreas (e.g., 'Estoque 1', 'Docas entrada') e os valores são o número de tarefas geradas para cada área.
    """
    
    tarefas_por_area = {}
    
    # Distribuir aleatoriamente as tarefas entre as áreas de estoque
    tarefas_estoque = [0] * n_areas_estoque
    for _ in range(n_tarefas_estoque):
        # Sorteia uma das áreas e adiciona uma tarefa
        area_sorteada = random.randint(0, n_areas_estoque - 1)
        tarefas_estoque[area_sorteada] += 1
    
    # Associar o número de tarefas a cada área de estoque
    for i in range(n_areas_estoque):
        area_nome = f"Estoque {i + 1}"
        tarefas_por_area[area_nome] = tarefas_estoque[i]
    
    # Gerar tarefas para a área "Docas entrada"
    area_nome_docas = "Docas entrada"
    tarefas_por_area[area_nome_docas] = n_tarefas_docas
    
    return tarefas_por_area

def criar_lista_tarefas(tarefas_por_area: dict[str, int]) -> list[int]:
    """
    Cria uma lista de tarefas numeradas sequencialmente, baseada na quantidade de tarefas por área.

    Parâmetros:
    -----------
    tarefas_por_area : dict[str, int]
        Dicionário contendo as áreas como chaves e o número de tarefas por área como valores.

    Retorno:
    --------
    list[int]
        Lista de tarefas numeradas sequencialmente.
    """

    numero_tarefa = 1
    tarefas = []
    for quantidade in tarefas_por_area.values():
        for _ in range(quantidade):
            tarefas.append(numero_tarefa)
            numero_tarefa += 1
    return tarefas

def distribuir_tarefas_caminhoes(tarefas: list[int], n_caminhoes: int) -> dict[str, list[int]]:
    """
    Distribui aleatoriamente as tarefas entre os caminhões disponíveis.

    Parâmetros:
    -----------
    tarefas : list[int]
        Lista de tarefas a serem distribuídas.
    n_caminhoes : int
        Número de caminhões disponíveis para alocação.

    Retorno:
    --------
    dict[str, list[int]]
        Dicionário que associa cada caminhão a uma lista de tarefas.
        Exemplo: {'Caminhão 1': [tarefa1, tarefa2, ...], 'Caminhão 2': [...]}
    """

    random.shuffle(tarefas)
    tarefas_por_caminhao = {f"Caminhão {i + 1}": [] for i in range(n_caminhoes)}
    for i, tarefa in enumerate(tarefas):
        caminhão = f"Caminhão {i % n_caminhoes + 1}"
        tarefas_por_caminhao[caminhão].append(tarefa)
    return tarefas_por_caminhao

def calcular_totais(tarefas_por_area: dict[str, int], n_operacoes_por_tarefa: int) -> tuple[int, int]:
    """
    Calcula o total de tarefas e o total de operações com base nas tarefas por área.

    Parâmetros:
    -----------
    tarefas_por_area : dict[str, int]
        Dicionário que contém as áreas como chaves e o número de tarefas por área como valores.
    n_operacoes_por_tarefa : int
        Número de operações associadas a cada tarefa.

    Retorno:
    --------
    tuple[int, int]
        Uma tupla contendo:
        - O número total de tarefas.
        - O número total de operações (tarefas multiplicadas pelo número de operações por tarefa).
    """

    n_total_tarefas = sum(tarefas_por_area.values())
    n_total_operacoes = n_total_tarefas * n_operacoes_por_tarefa

    return n_total_tarefas, n_total_operacoes

def criar_predecessores(n_operations: int, n_operacoes_por_tarefa: int) -> dict[int, int]:
    """
    Cria um dicionário de predecessores para as operações, com um reset a cada nova tarefa.

    Parâmetros:
    -----------
    n_operations : int
        Número total de operações.
    n_operacoes_por_tarefa : int
        Número de operações associadas a cada tarefa.

    Retorno:
    --------
    dict[int, int]
        Dicionário que mapeia cada operação ao seu predecessor.
        Exemplo: {operação: predecessor, ...}
    """

    predecessores = {}
    for i in range(1, n_operations + 1):
        if (i - 1) % n_operacoes_por_tarefa == 0:  # Reseta o predecessor a cada n_operacoes_por_tarefa
            predecessores[i] = 0
        else:
            predecessores[i] = i - 1
   
    return predecessores

def distribuir_operacoes_por_area(tarefas_por_area: dict[str, int], 
                                  total_tarefas: int, 
                                  n_operacoes_por_tarefa: int) -> dict[str, list[int]]:
    """
    Distribui operações entre áreas, considerando estoques, docas de entrada, picking e docas de saída.

    Parâmetros:
    -----------
    tarefas_por_area : dict[str, int]
        Dicionário contendo as áreas como chaves e o número de tarefas como valores.
    total_tarefas : int
        Número total de tarefas.
    n_operacoes_por_tarefa : int
        Número de operações associadas a cada tarefa.

    Retorno:
    --------
    dict[str, list[int]]
        Dicionário onde as áreas são as chaves e as listas de operações alocadas a cada área são os valores.
        Exemplo: {'Docas saída': [operação1, operação2, ...], 'Picking': [...], ...}.
    """

    # Inicializar dicionário final
    tarefas_por_area_final = {}
    docas_saida = "Docas saída"
    tarefas_por_area_final[docas_saida] = []
    
    # Listas para armazenar as operações
    operacoes_estoques_docas_entrada = []
    operacoes_picking = []
    
    # Distribuir operações
    for i in range(1, total_tarefas + 1):
        if (i - 1) % n_operacoes_por_tarefa == 0:
            # Operações com reset são alocadas para Estoques e Docas Entrada
            operacoes_estoques_docas_entrada.append(i)
        elif i % n_operacoes_por_tarefa == 0:
            # Operações divisíveis por n_operacoes_por_tarefa vão para Docas saída
            tarefas_por_area_final[docas_saida].append(i)
        else:
            # Operações restantes vão para Picking
            operacoes_picking.append(i)
    
    # Distribuir operações de Estoques e Docas Entrada nas áreas especificadas
    random.shuffle(operacoes_estoques_docas_entrada)
    inicio = 0
    for area, num_tarefas in tarefas_por_area.items():
        if area != docas_saida:
            fim = inicio + num_tarefas
            tarefas_por_area_final[area] = operacoes_estoques_docas_entrada[inicio:fim]
            inicio = fim

    # Adicionar operações restantes no Picking, se houver
    if operacoes_picking:
        picking = "Picking"
        tarefas_por_area_final[picking] = operacoes_picking + operacoes_estoques_docas_entrada[inicio:]

    return tarefas_por_area_final

def criar_operacoes_por_caminhao(tarefas_por_caminhao: dict[str, list[int]]) -> dict[str, list[int]]:
    """
    Cria um dicionário que associa cada caminhão às operações correspondentes às suas tarefas.

    Parâmetros:
    -----------
    tarefas_por_caminhao : dict[str, list[int]]
        Dicionário onde cada caminhão é associado a uma lista de tarefas.

    Retorno:
    --------
    dict[str, list[int]]
        Dicionário que associa cada caminhão a uma lista de operações correspondentes às suas tarefas.
        Exemplo: {'Caminhão 1': [operação1, operação2, ...], 'Caminhão 2': [...]}
    """

    operacoes_por_caminhao = {}

    for caminhao, tarefas in tarefas_por_caminhao.items():
        operacoes_por_caminhao[caminhao] = []
        for tarefa in tarefas:
            operacao1 = 2 * tarefa - 1  # Primeira operação correspondente à tarefa
            operacao2 = 2 * tarefa       # Segunda operação correspondente à tarefa
            operacoes_por_caminhao[caminhao].extend([operacao1, operacao2])

    return operacoes_por_caminhao