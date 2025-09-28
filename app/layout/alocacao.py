import random
import numpy as np

def associar_caminhoes_docas_aleatorio(n_caminhoes: int, num_docas: int) -> dict:
    """
    Associa caminhões a docas de saída de forma aleatória.
    
    Parâmetros:
    - n_caminhoes: número total de caminhões (int)
    - num_docas: número de docas disponíveis (int)
    
    Retorno:
    - Dicionário com as chaves 'caminhão' e 'doca' seguidas pelos números correspondentes.
    """
    # Lista com os números das docas
    docas = list(range(1, num_docas + 1))
    
    # Dicionário para armazenar a associação
    associacao = {}
    
    # Para garantir que as docas não se repitam inicialmente
    for caminhao in range(1, n_caminhoes + 1):
        if not docas:
            # Se todas as docas foram atribuídas pelo menos uma vez, reiniciar a lista
            docas = list(range(1, num_docas + 1))
        
        # Sorteia uma doca para o caminhão e remove essa doca temporariamente da lista
        doca_atribuida = random.choice(docas)
        docas.remove(doca_atribuida)
        
        # Adiciona a associação no dicionário com a chave 'caminhão' e 'doca' e o valor como número
        associacao[f'caminhão {caminhao}'] = doca_atribuida
    
    return associacao

def alocar_pontos_operacoes(operacoes_por_area_final: dict[str, list[int]], 
                            area_indices: dict[str, tuple[float, float, float, float]], 
                            grid_spacing: float, 
                            associacao_caminhoes_docas: dict[str, int], 
                            operacoes_por_caminhao: dict[str, list[int]], 
                            mesmo_ponto_picking: bool = False) -> dict:
    """
    Aloca pontos no grid para as operações em várias áreas, como 'Docas saída' e 'Picking', respeitando as associações de caminhões às docas e alocando operações pares e ímpares conforme especificado.

    Parâmetros:
    -----------
    operacoes_por_area_final : dict[str, list[int]]
        Dicionário contendo as áreas como chaves e uma lista de operações associadas a essas áreas como valores.
    area_indices : dict[str, tuple[float, float, float, float]]
        Dicionário contendo os limites das áreas no formato (x_min, y_min, largura, altura), usados para definir o grid onde as operações serão alocadas.
    grid_spacing : float
        Distância entre os pontos no grid, usado para definir a posição das operações.
    associacao_caminhoes_docas : dict[str, int]
        Dicionário que associa caminhões (chaves) ao número da doca (valores) onde suas operações serão alocadas.
    operacoes_por_caminhao : dict[str, list[int]]
        Dicionário que mapeia caminhões (chaves) para suas respectivas listas de operações (valores).
    mesmo_ponto_picking : bool, opcional
        Indica se todas as operações ímpares no 'Picking' devem ser alocadas no mesmo ponto central (padrão é False).

    Retorno:
    --------
    dict
        Dicionário que mapeia cada área para outro dicionário que contém as operações como chaves e suas coordenadas (tuplas de x, y) como valores.
        Exemplo: {'Docas saída': {operação: (x, y), ...}, 'Picking': {operação: (x, y), ...}}.
    """

    coordenadas_por_area = {}
    pontos_ocupados_picking = set()
    
    # Processar 'Docas saída'
    if 'Docas saída' in area_indices:
        coordenadas_por_area['Docas saída'] = {}
        
        x_min_docas_saida, y_min_docas_saida, width_docas_saida, height_docas_saida = area_indices['Docas saída']
        x_possible_docas_saida = np.arange(x_min_docas_saida + grid_spacing, x_min_docas_saida + width_docas_saida, grid_spacing)
        
        num_docas = len(set(associacao_caminhoes_docas.values()))
        
        # Gerar y-coordinates para as docas, do topo (maior y) para baixo
        y_max = y_min_docas_saida + height_docas_saida - grid_spacing
        y_min = y_min_docas_saida + grid_spacing
        y_possible_docas_saida = np.arange(y_max, y_min - grid_spacing, -grid_spacing)
        
        # Mapear número da doca para y-coordinate
        dock_y_coords = {}
        for idx, y in enumerate(y_possible_docas_saida):
            dock_number = idx + 1  # Docas numeradas a partir de 1
            dock_y_coords[dock_number] = y
        
        # Para cada caminhão, alocar operações pares na doca atribuída
        for caminhao_str, operacoes in operacoes_por_caminhao.items():
            # Uniformizar a chave do caminhão, convertendo para minúsculas
            caminhao_lower = caminhao_str.lower()
            
            # Verificar se o caminhão está na associação de docas
            if caminhao_lower in associacao_caminhoes_docas:
                assigned_dock = associacao_caminhoes_docas[caminhao_lower]
                y_dock = dock_y_coords[assigned_dock]
                
                for operacao in operacoes:
                    if operacao % 2 == 0:
                        x = random.choice(x_possible_docas_saida)
                        y = y_dock
                        coordenadas_por_area['Docas saída'][operacao] = (x, y)
    
    # Processar 'Picking' para operações ímpares
    if 'Picking' in area_indices:
        coordenadas_por_area['Picking'] = {}
        
        x_min_picking, y_min_picking, width_picking, height_picking = area_indices['Picking']
        
        if mesmo_ponto_picking:
            # Calcular o ponto médio da área de picking
            x_central = x_min_picking + width_picking / 2
            y_central = y_min_picking + height_picking / 2
            ponto_central_picking = (x_central, y_central)
            
            for caminhao_str, operacoes in operacoes_por_caminhao.items():
                # Uniformizar a chave do caminhão, convertendo para minúsculas
                caminhao_lower = caminhao_str.lower()
                
                for operacao in operacoes:
                    if operacao % 2 != 0:
                        # Atribuir todas as operações ímpares ao ponto central
                        coordenadas_por_area['Picking'][operacao] = ponto_central_picking
        else:
            # Manter alocação aleatória normal se mesmo_ponto_picking for False
            x_possible_picking = np.arange(x_min_picking + grid_spacing, x_min_picking + width_picking, grid_spacing)
            y_possible_picking = np.arange(y_min_picking + grid_spacing, y_min_picking + height_picking, grid_spacing)
            possible_points_picking = [(x, y) for x in x_possible_picking for y in y_possible_picking]
            
            for caminhao_str, operacoes in operacoes_por_caminhao.items():
                # Uniformizar a chave do caminhão, convertendo para minúsculas
                caminhao_lower = caminhao_str.lower()
                
                for operacao in operacoes:
                    if operacao % 2 != 0:
                        available_points = [p for p in possible_points_picking if p not in pontos_ocupados_picking]
                        if available_points:
                            ponto = random.choice(available_points)
                            pontos_ocupados_picking.add(ponto)
                            coordenadas_por_area['Picking'][operacao] = ponto
                        else:
                            # Se todos os pontos estiverem ocupados, começa a repetir
                            ponto = random.choice(possible_points_picking)
                            coordenadas_por_area['Picking'][operacao] = ponto
    
    # Processar outras áreas normalmente
    for area, operacoes in operacoes_por_area_final.items():
        if area not in ['Docas saída', 'Picking']:
            x_min, y_min, width, height = area_indices[area]
            coordenadas_por_area[area] = {}
            
            x_possible = np.arange(x_min + grid_spacing, x_min + width, grid_spacing)
            y_possible = np.arange(y_min + grid_spacing, y_min + height, grid_spacing)
            
            for operacao in operacoes:
                x = random.choice(x_possible)
                y = random.choice(y_possible)
                coordenadas_por_area[area][operacao] = (x, y)
    
    return coordenadas_por_area