import numpy as np
import matplotlib.pyplot as plt

def plot_heatmap_caminhos_horizontal(area_indices, coordenadas_detalhadas, alpha, grid=5):
    """
    Gera um mapa de calor com base nos caminhos percorridos pelas empilhadeiras,
    mantendo o layout das áreas e ajustando o gráfico para um formato mais horizontal.

    Parâmetros:
    - area_indices: Dicionário com as coordenadas das áreas.
    - coordenadas_detalhadas: Dicionário com as coordenadas dos pontos das operações.
    - alpha: Dicionário com as atribuições de operações para cada empilhadeira.
    - grid: Número de divisões do grid no gráfico (padrão = 5).
    """
    # Calcular os limites do gráfico com base nas áreas fornecidas
    max_x = max([x + largura for x, _, largura, _ in area_indices.values()])
    max_y = max([y + altura for _, y, _, altura in area_indices.values()])
    min_x = min([x for x, _, _, _ in area_indices.values()])
    min_y = min([y for _, y, _, _ in area_indices.values()])

    # Definir a matriz de calor
    heatmap_matrix = np.zeros((max_y // grid + 1, max_x // grid + 1))

    # Definir o incremento de calor para cada passagem de empilhadeira
    heat_increment = 1

    # Ponto especial para origem e destino indefinidos
    ponto_especial = coordenadas_detalhadas.get('*d,*o', None)

    # Iterar sobre as operações das empilhadeiras e atualizar a matriz de calor
    for caminhao, matriz_alpha in alpha.items():
        for i, linha in enumerate(matriz_alpha):
            for empilhadeira, operacao in enumerate(linha):
                if operacao == 1:  # Operação realizada pela empilhadeira
                    op_name = f'{i+1}o'  # Operação origem
                    op_dest = f'{i+1}d'  # Operação destino

                    # Verifica se a operação de origem ou destino está no dicionário de coordenadas
                    x1, y1 = coordenadas_detalhadas.get(op_name, ponto_especial)  # Usa o ponto especial se origem não existir
                    x2, y2 = coordenadas_detalhadas.get(op_dest, ponto_especial)  # Usa o ponto especial se destino não existir

                    if x1 is not None and x2 is not None:  # Verifica se os pontos foram encontrados ou atribuídos
                        # Converta para inteiros para usar no range()
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        
                        # Atualizar a matriz de calor para a distância de Manhattan
                        # Movimento na direção x
                        x_step = grid if x1 < x2 else -grid
                        for x in range(x1, x2 + x_step, x_step):
                            heatmap_matrix[y1 // grid, x // grid] += heat_increment
                        # Movimento na direção y
                        y_step = grid if y1 < y2 else -grid
                        for y in range(y1, y2 + y_step, y_step):
                            heatmap_matrix[y // grid, x2 // grid] += heat_increment

    # Criar a figura do mapa de calor
    fig, ax = plt.subplots(figsize=(18, 10))  # Ajuste do tamanho da figura para um gráfico mais horizontal

    # Plotar as áreas com as bordas e nomes em preto
    for area, (x, y, largura, altura) in area_indices.items():
        rect = plt.Rectangle((x, y), largura, altura, linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(rect)
        ax.text(x + largura / 2, y + altura / 2, area, color='black', ha='center', va='center', fontsize=10, fontweight='bold', rotation=90)  # Nome das áreas rotacionado

    # Ajustar limites dos eixos para que coincidam exatamente com as áreas
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # Ajustar aspecto do gráfico para ser mais horizontal
    ax.set_aspect(aspect=(max_y / max_x) * 2, adjustable='box')  # Multiplicando o aspecto para deixar mais achatado

    # Plotar o mapa de calor sobre as áreas
    heatmap_extent = [min_x, max_x, min_y, max_y]
    heatmap = ax.imshow(heatmap_matrix, cmap='Reds', interpolation='nearest', origin='lower', alpha=0.7, extent=heatmap_extent)

    # Adicionar barra de cor para o mapa de calor
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label('Frequência de Passagem')

    # Ajustar as grades para os eixos
    ax.set_xticks(np.arange(min_x, max_x + grid, grid))
    ax.set_yticks(np.arange(min_y, max_y + grid, grid))
    ax.grid(True)

    # Remover títulos dos eixos
    ax.set_xlabel('')
    ax.set_ylabel('')

    # Ajustar o layout para o gráfico se encaixar bem
    plt.tight_layout()
    plt.show()
