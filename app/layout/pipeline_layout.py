import matplotlib.pyplot as plt
from .alocacao import associar_caminhoes_docas_aleatorio, alocar_pontos_operacoes
from .figura_layout import create_layout_and_coordinate_matrix_with_grid, plotar_layout_com_pontos, plotar_caminhos
from .func_aux import plotar_todas_combinacoes, plotar_caminhos_picking

def pipeline_gerar_layout_e_caminhos_processamento(num_estoques: int, 
                                                   operacoes_por_area_final: dict, 
                                                   num_docas: int,
                                                   picking_width_units: int,
                                                   n_caminhoes: int,
                                                   operacoes_por_caminhao: dict,
                                                   mesmo_ponto_picking: bool, 
                                                   grid_spacing: int = 5) -> dict:
    
    # Cria o layout e a matriz de coordenadas
    area_indices = create_layout_and_coordinate_matrix_with_grid(num_estoques, num_docas, picking_width_units, grid_spacing)

    associacao_caminhoes_docas = associar_caminhoes_docas_aleatorio(n_caminhoes, num_docas)

    # Aloca os pontos nas áreas
    coordenadas_por_area = alocar_pontos_operacoes(operacoes_por_area_final, area_indices, grid_spacing, associacao_caminhoes_docas, operacoes_por_caminhao, mesmo_ponto_picking)

    coordenadas_detalhadas = plotar_layout_com_pontos(coordenadas_por_area, mesmo_ponto_picking)
    
    # # Plota os caminhos e retorna a figura e o eixo
    # fig, ax = plotar_caminhos(fig, ax, coordenadas_por_area)
    
    return coordenadas_por_area, area_indices, coordenadas_detalhadas

#### FUNCOES ALTERNATIVAS ####

def gerar_layout_e_caminhos_setup(num_estoques, num_docas, picking_width_units, coordenadas_por_area, grid_spacing = 5):
    
    # Cria o layout e a matriz de coordenadas
    area_indices = create_layout_and_coordinate_matrix_with_grid(num_estoques, num_docas, picking_width_units, grid_spacing)

    # fig, ax, coordenadas_detalhadas = plotar_layout_com_pontos(ax, fig, coordenadas_por_area)

    # fig, ax = plotar_todas_combinacoes(fig, ax, coordenadas_detalhadas)

def gerar_layout_e_caminhos_setup_picking(num_estoques, num_docas, picking_width_units, coordenadas_por_area, grid_spacing = 5):
    
    # Cria o layout e a matriz de coordenadas
    area_indices = create_layout_and_coordinate_matrix_with_grid(num_estoques, num_docas, picking_width_units, grid_spacing)

    # fig, ax, coordenadas_detalhadas = plotar_layout_com_pontos(ax, fig, coordenadas_por_area)

    # plotar_caminhos_picking(fig, ax, coordenadas_por_area, linewidth=3)

    # plt.show()
