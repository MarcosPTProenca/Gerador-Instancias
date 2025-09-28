import random

def classificar_empilhadeiras(n_maquinas: int, proporcao_rapidas: float) -> dict:
    """
    Retorna um dicionário classificando empilhadeiras como rápidas ou lentas,
    de acordo com a proporção fornecida.

    Parâmetros:
    n_maquinas (int): Número total de empilhadeiras.
    proporcao_rapidas (float): Proporção de empilhadeiras rápidas (em percentual, de 0 a 100).

    Retorno:
    dict: Dicionário com a classificação das empilhadeiras.
    """
    # Validar se a proporção está entre 0 e 100
    if proporcao_rapidas < 0 or proporcao_rapidas > 100:
        raise ValueError("A proporção de empilhadeiras rápidas deve estar entre 0 e 100%.")

    # Calcular a quantidade de empilhadeiras rápidas e lentas
    n_rapidas = int(round(n_maquinas * (proporcao_rapidas / 100)))
    n_lentas = n_maquinas - n_rapidas

    # Criar uma lista de empilhadeiras com base na classificação
    classificacao = ['rápida'] * n_rapidas + ['lenta'] * n_lentas

    # Embaralhar a lista para que a distribuição seja aleatória
    random.shuffle(classificacao)

    # Criar o dicionário resultante com as classificações
    empilhadeiras = {f"Empilhadeira {i + 1}": classificacao[i] for i in range(n_maquinas)}

    return empilhadeiras

def classificar_empilhadeiras_por_areas(num_maquinas: int, proporcao_areas: dict) -> dict:
    """
    Classifica as empilhadeiras quanto ao número de áreas em que elas podem atuar.
    
    Parâmetros:
    num_maquinas (int): Número total de empilhadeiras.
    proporcao_areas (dict): Dicionário com as proporções de empilhadeiras que atuam em 1, 2 ou 3 áreas.

    Retorno:
    dict: Dicionário com a classificação das empilhadeiras e a quantidade de áreas em que cada uma pode atuar.
    """
    
    # Definir quantas empilhadeiras atuarão em 1, 2 ou 3 áreas, com base nas proporções
    num_empilhadeiras_1_area = max(1, int(proporcao_areas['1_area'] * num_maquinas))
    num_empilhadeiras_2_areas = max(1, int(proporcao_areas['2_areas'] * num_maquinas))
    num_empilhadeiras_3_areas = num_maquinas - num_empilhadeiras_1_area - num_empilhadeiras_2_areas

    # Ajuste para garantir que a soma das empilhadeiras seja igual ao total
    if num_empilhadeiras_3_areas < 0:
        num_empilhadeiras_2_areas += num_empilhadeiras_3_areas
        num_empilhadeiras_3_areas = 0

    # Inicializar a classificação das empilhadeiras
    classificacao_empilhadeiras = {}

    # Sortear empilhadeiras para 1 área
    empilhadeiras_disponiveis = list(range(1, num_maquinas + 1))
    empilhadeiras_1_area = random.sample(empilhadeiras_disponiveis, num_empilhadeiras_1_area)
    for emp in empilhadeiras_1_area:
        classificacao_empilhadeiras[f'Empilhadeira {emp}'] = 1
    empilhadeiras_disponiveis = [emp for emp in empilhadeiras_disponiveis if emp not in empilhadeiras_1_area]

    # Sortear empilhadeiras para 2 áreas
    empilhadeiras_2_areas = random.sample(empilhadeiras_disponiveis, num_empilhadeiras_2_areas)
    for emp in empilhadeiras_2_areas:
        classificacao_empilhadeiras[f'Empilhadeira {emp}'] = 2
    empilhadeiras_disponiveis = [emp for emp in empilhadeiras_disponiveis if emp not in empilhadeiras_2_areas]

    # As empilhadeiras restantes atuarão em 3 áreas
    for emp in empilhadeiras_disponiveis:
        classificacao_empilhadeiras[f'Empilhadeira {emp}'] = 3

    return classificacao_empilhadeiras