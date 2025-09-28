import random
import numpy as np

def elegibilidade_maquinas(num_maquinas: int, 
                           operacoes_por_area: dict[str, list[int]], 
                           operacoes_por_caminhao: dict[str, list[int]], 
                           proporcao_maquinas: dict[str, float], 
                           classificacao_empilhadeiras: dict[str, int]) -> dict:
    """
    Define a elegibilidade de máquinas para operações em diferentes áreas e caminhões, atribuindo máquinas conforme a classificação das empilhadeiras e a proporção de máquinas por área.

    Parâmetros:
    -----------
    num_maquinas : int
        Número total de máquinas (empilhadeiras, por exemplo) disponíveis para alocação.
    operacoes_por_area : dict[str, list[int]]
        Dicionário contendo as áreas (e.g., 'Picking', 'Docas entrada', 'Estoque') como chaves e as listas de operações associadas como valores.
    operacoes_por_caminhao : dict[str, list[int]]
        Dicionário que mapeia cada caminhão (chaves) para as operações que ele realiza (valores).
    proporcao_maquinas : dict[str, float]
        Dicionário que define a proporção de máquinas alocadas a cada área. As chaves representam as áreas (e.g., 'Docas entrada', 'Estoque') e os valores são as proporções (e.g., 0.3 para 30%).
    classificacao_empilhadeiras : dict[str, int]
        Dicionário que associa cada empilhadeira ao número de áreas em que ela pode atuar. A chave é o nome da empilhadeira (e.g., 'Empilhadeira 1') e o valor é a quantidade de áreas.

    Retorno:
    --------
    dict
        Dicionário ajustado contendo a elegibilidade de cada operação. Para cada operação, o dicionário retorna:
        - 'caminhao': O número do caminhão associado à operação.
        - 'maquinas': Lista de números das máquinas elegíveis para a operação.
        Exemplo: {operação: {'caminhao': número_do_caminhão, 'maquinas': [1, 2, 5]}, ...}.
    """

    # Definir o número de máquinas para cada tipo de operação
    maquinas_por_tipo = {
        'Docas entrada': max(1, int(proporcao_maquinas['Docas entrada'] * num_maquinas)),
        'Estoque': max(1, int(proporcao_maquinas['Estoque'] * num_maquinas)),
        'Picking': max(1, int(proporcao_maquinas['Picking'] * num_maquinas)),
    }

    # Ajustar caso a soma não seja igual ao número total de máquinas (devido ao arredondamento)
    total_maquinas_alocadas = sum(maquinas_por_tipo.values())
    while total_maquinas_alocadas < num_maquinas:
        maquinas_por_tipo['Picking'] += 1  # Adicionar a máquina extra ao Picking por default
        total_maquinas_alocadas += 1
    while total_maquinas_alocadas > num_maquinas:
        maquinas_por_tipo['Picking'] -= 1  # Remover a máquina extra do Picking por default
        total_maquinas_alocadas -= 1

    # Inicializar a matriz de elegibilidade
    elegibilidade = {}
    for tipo, operacoes in operacoes_por_area.items():
        for operacao in operacoes:
            elegibilidade[operacao] = {
                'caminhao': None,
                'maquinas': np.zeros(num_maquinas, dtype=int).tolist()
            }

    # Atribuir caminhões e definir elegibilidade de máquinas
    maquinas_alocadas = {'Docas entrada': [], 'Estoque': [], 'Picking': []}

    # Garantir que as empilhadeiras atuem em várias áreas conforme sua classificação
    for emp, qtd_areas in classificacao_empilhadeiras.items():
        emp_numero = int(emp.split()[1]) - 1  # Extrair o número da empilhadeira (indexado em 0)
        areas_sorteadas = random.sample(list(maquinas_por_tipo.keys()), qtd_areas)  # Sortear as áreas para a empilhadeira
        for area in areas_sorteadas:
            maquinas_alocadas[area].append(emp_numero)

    # Atribuir caminhões e definir elegibilidade de máquinas para as áreas
    for tipo, operacoes in operacoes_por_area.items():
        if tipo == 'Docas saída':
            tipo = 'Picking'  # Tratar Docas saída como Picking
        elif 'Estoque' in tipo:
            tipo = 'Estoque'  # Tratar todos os "Estoque X" como "Estoque"
        
        for operacao in operacoes:
            # Definir o caminhão responsável pela operação
            for caminhao, ops in operacoes_por_caminhao.items():
                if operacao in ops:
                    elegibilidade[operacao]['caminhao'] = int(caminhao.split()[1])  # Extrair o número do caminhão
                    break

            # Marcar elegibilidade para as máquinas correspondentes
            for maquina in maquinas_alocadas[tipo]:
                elegibilidade[operacao]['maquinas'][maquina] = 1

    # Ajustar o output para retornar as máquinas de forma legível e ordenar as operações
    elegibilidade_ajustada = {}
    for operacao in sorted(elegibilidade.keys()):
        caminhao = elegibilidade[operacao]['caminhao']
        maquinas_binarias = elegibilidade[operacao]['maquinas']
        
        # Traduzir as máquinas em uma lista de números
        maquinas_atuantes = [i + 1 for i, ativo in enumerate(maquinas_binarias) if ativo == 1]
        
        # Ajustar para a saída com o número do caminhão
        elegibilidade_ajustada[operacao] = {
            'caminhao': caminhao,  # Retorna o número do caminhão
            'maquinas': maquinas_atuantes  # Retorna a lista de máquinas
        }

    return elegibilidade_ajustada
