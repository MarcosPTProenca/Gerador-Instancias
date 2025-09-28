import matplotlib.pyplot as plt
import numpy as np

def create_layout_and_coordinate_matrix_with_grid(num_estoques: int, 
                                                  num_docas: int, 
                                                  picking_width_units: int, 
                                                  grid_spacing: int = 5) -> tuple:
    """
    Cria um layout visual com uma grade e retorna as coordenadas das áreas para o armazenamento, docas e picking.

    Parâmetros:
    -----------
    num_estoques : int
        Número total de áreas de estoque a serem plotadas.
    num_docas : int
        Número total de docas (tanto para entrada quanto para saída).
    picking_width_units : int
        Largura da área de picking em unidades de grade.
    grid_spacing : int, opcional
        Espaçamento da grade usado para definir o tamanho das áreas (padrão é 5).

    Retorno:
    --------
    tuple
        Retorna uma tupla contendo:
        - fig: Objeto `Figure` do matplotlib com o layout visualizado.
        - ax: Objeto `Axes` do matplotlib, representando o sistema de coordenadas da grade.
        - area_indices: Dicionário contendo as coordenadas e dimensões de cada área no formato 
          {'Área': (x_min, y_min, largura, altura), ...}.
    """

    # Define fixed area dimensions
    docas_width_units = 2
    docas_height_units = num_docas + 1

    picking_width_units = picking_width_units  # input parameter
    picking_height_units = docas_height_units  # same as docas

    total_fixed_width_units = docas_width_units + picking_width_units + docas_width_units

    total_fixed_width = total_fixed_width_units * grid_spacing

    # Decide estoque_width_units that divides total_fixed_width_units evenly
    # For simplicity, let's set estoque_width_units as a divisor of total_fixed_width_units
    # Find the greatest common divisor (GCD) to choose estoque_width_units
    def find_divisors(n):
        divisors = [i for i in range(1, n+1) if n % i == 0]
        return divisors

    possible_divisors = find_divisors(total_fixed_width_units)
    # Choose a reasonable estoque_width_units from possible divisors (excluding 1 and total_fixed_width_units)
    if len(possible_divisors) > 2:
        estoque_width_units = possible_divisors[-2]
    else:
        estoque_width_units = total_fixed_width_units  # If no other divisors, use total width

    num_estoque_cols = total_fixed_width_units // estoque_width_units

    estoque_width = estoque_width_units * grid_spacing

    # Compute number of estoque rows
    num_estoque_rows = (num_estoques + num_estoque_cols - 1) // num_estoque_cols

    # Set estoque_height_units to a reasonable value
    estoque_height_units = docas_height_units  # For uniformity, use the same height units
    estoque_height = estoque_height_units * grid_spacing

    total_estoque_height_units = estoque_height_units * num_estoque_rows

    total_plot_height_units = total_estoque_height_units + docas_height_units

    total_plot_height = total_plot_height_units * grid_spacing

    # # Set up the plot
    # fig, ax = plt.subplots(figsize=(15, 10))
    # ax.set_xlim(0, total_fixed_width)
    # ax.set_ylim(0, total_plot_height)
    # ax.set_xticks(np.arange(0, total_fixed_width + grid_spacing, grid_spacing))
    # ax.set_yticks(np.arange(0, total_plot_height + grid_spacing, grid_spacing))
    # ax.grid(True)

    # Plotting the fixed areas
    area_indices = {}

    # 'Docas entrada'
    x_docas_entrada = 0
    y_docas = total_plot_height - docas_height_units * grid_spacing

    rect = plt.Rectangle((x_docas_entrada, y_docas), docas_width_units * grid_spacing, docas_height_units * grid_spacing, fill=None, edgecolor='black', linewidth=2)
    # ax.add_patch(rect)
    # ax.text(x_docas_entrada + docas_width_units * grid_spacing / 2, y_docas + docas_height_units * grid_spacing / 2, 'Docas entrada', ha='center', va='center')
    area_indices['Docas entrada'] = (x_docas_entrada, y_docas, docas_width_units * grid_spacing, docas_height_units * grid_spacing)

    # 'Picking'
    x_picking = x_docas_entrada + docas_width_units * grid_spacing
    rect = plt.Rectangle((x_picking, y_docas), picking_width_units * grid_spacing, picking_height_units * grid_spacing, fill=None, edgecolor='black', linewidth=2)
    # ax.add_patch(rect)
    # ax.text(x_picking + picking_width_units * grid_spacing / 2, y_docas + picking_height_units * grid_spacing / 2, 'Picking', ha='center', va='center')
    area_indices['Picking'] = (x_picking, y_docas, picking_width_units * grid_spacing, picking_height_units * grid_spacing)

    # 'Docas saída'
    x_docas_saida = x_picking + picking_width_units * grid_spacing
    rect = plt.Rectangle((x_docas_saida, y_docas), docas_width_units * grid_spacing, docas_height_units * grid_spacing, fill=None, edgecolor='black', linewidth=2)
    # ax.add_patch(rect)
    # ax.text(x_docas_saida + docas_width_units * grid_spacing / 2, y_docas + docas_height_units * grid_spacing / 2, 'Docas saída', ha='center', va='center')
    area_indices['Docas saída'] = (x_docas_saida, y_docas, docas_width_units * grid_spacing, docas_height_units * grid_spacing)

    # Plotting the stock areas
    areas_estoque = [f'Estoque {i+1}' for i in range(num_estoques)]
    for idx, area in enumerate(areas_estoque):
        row = idx // num_estoque_cols
        col = idx % num_estoque_cols
        x = col * estoque_width
        y = (total_estoque_height_units - (row + 1) * estoque_height_units) * grid_spacing
        rect = plt.Rectangle((x, y), estoque_width, estoque_height, fill=None, edgecolor='black', linewidth=2)
        # ax.add_patch(rect)
        # ax.text(x + estoque_width / 2, y + estoque_height / 2, area, ha='center', va='center')
        area_indices[area] = (x, y, estoque_width, estoque_height)

    return area_indices


def plotar_layout_com_pontos(coordenadas_por_area: dict[str, dict[int, tuple[float, float]]],
                             mesmo_ponto_picking: bool = False) -> tuple:
    """
    Plota o layout com os pontos das operações nas áreas especificadas, e caso o mesmo_ponto_picking seja True,
    coloca um único label '*d,*o' na área de Picking para indicar que todas as operações têm a mesma origem e destino.

    Parâmetros:
    -----------
    ax : Axes
        O objeto Axes onde os pontos serão plotados.
    fig : Figure
        A figura onde o gráfico será plotado.
    coordenadas_por_area : dict
        Dicionário contendo as coordenadas de cada área e as respectivas operações.
    mesmo_ponto_picking : bool
        Se True, plota apenas um único label '*d,*o' para indicar que todas as operações na área de Picking compartilham a mesma origem e destino.
    """

    # Dicionário para armazenar as coordenadas e as operações que compartilham as mesmas coordenadas
    pontos_agrupados = {}
    
    # Dicionário para armazenar as coordenadas com labels de origem/destino como chave
    coordenadas_detalhadas = {}

    # Variável para controlar se já plotou o *d,*o na área de Picking
    plotou_label_picking = False

    # Agrupar labels por coordenadas (x, y)
    for area, pontos in coordenadas_por_area.items():
        for operacao, (x, y) in pontos.items():
            labels = []

            if 'Estoque' in area or area == 'Docas entrada':
                # Adicionar o número com 'o' de origem
                label = f"{operacao}o"
                labels.append(label)
                coordenadas_detalhadas[label] = (x, y)
            elif area == 'Picking':
                if mesmo_ponto_picking and not plotou_label_picking:
                    # Caso o mesmo_ponto_picking seja True, adiciona um único label '*d,*o'
                    label_picking = '*d,*o'
                    labels.append(label_picking)
                    coordenadas_detalhadas[label_picking] = (x, y)
                    plotou_label_picking = True  # Para garantir que o label seja plotado apenas uma vez
                elif not mesmo_ponto_picking:
                    # Adicionar o número da operação com 'd' de destino
                    label_dest = f"{operacao}d"
                    labels.append(label_dest)
                    coordenadas_detalhadas[label_dest] = (x, y)
                    
                    # Adicionar a operação subsequente com 'o' de origem
                    next_operacao = operacao + 1  # Supondo que a próxima operação seja operacao + 1
                    label_orig = f"{next_operacao}o"
                    labels.append(label_orig)
                    coordenadas_detalhadas[label_orig] = (x, y)
                
            elif area == 'Docas saída':
                # Adicionar o número da operação com 'd' de destino
                label = f"{operacao}d"
                labels.append(label)
                coordenadas_detalhadas[label] = (x, y)
                
            else:
                # Caso padrão, apenas para garantir que todas as áreas sejam tratadas
                label = str(operacao)
                labels.append(label)
                coordenadas_detalhadas[label] = (x, y)

            # Armazenar os labels agrupados por coordenada
            if (x, y) not in pontos_agrupados:
                pontos_agrupados[(x, y)] = []
            pontos_agrupados[(x, y)].extend(labels)

    # # Plotar os pontos e adicionar os labels agrupados
    # for (x, y), labels in pontos_agrupados.items():
    #     # Plotar o ponto vermelho
    #     ax.plot(x, y, 'ro', markersize=8)  # 'ro' para plotar pontos vermelhos

    #     # Adicionar os labels, separados por vírgula
    #     texto_labels = ', '.join(labels)
    #     ax.text(x, y, texto_labels, color="black", fontsize=12, fontweight='bold', ha='center', va='bottom')

    # # Adicionar o asterisco na legenda para explicar que *d,*o indica todas as operações na área de Picking
    # if mesmo_ponto_picking:
    #     ax.text(0.5, -0.1, '*d,*o indica que todas as operações compartilham a mesma origem e destino na área de Picking', 
    #             ha='center', va='top', transform=ax.transAxes, fontsize=12, fontweight='bold', color='blue')

    # Ordenar o dicionário de coordenadas_detalhadas na ordem desejada
    coordenadas_ordenadas = {}
    for operacao in sorted(coordenadas_detalhadas.keys(), key=lambda x: (int(x[:-1]) if '*' not in x else 0, 0 if x.endswith('o') else 1)):
        coordenadas_ordenadas[operacao] = coordenadas_detalhadas[operacao]

    return coordenadas_ordenadas

def plotar_caminhos(fig: plt.Figure, 
                    ax: plt.Axes, 
                    coordenadas_por_area: dict[str, dict[int, tuple[float, float]]], 
                    linewidth: int = 3) -> tuple:
    """
    Plota os caminhos entre as operações em diferentes áreas no layout, conectando operações ímpares das áreas para o Picking e as operações pares subsequentes para as Docas de saída. Usa caminhos verdes e azuis para representar os diferentes deslocamentos.

    Parâmetros:
    -----------
    fig : matplotlib.figure.Figure
        Objeto `Figure` do matplotlib que contém o layout e as plotagens.
    ax : matplotlib.axes.Axes
        Objeto `Axes` do matplotlib onde os caminhos serão plotados.
    coordenadas_por_area : dict[str, dict[int, tuple[float, float]]]
        Dicionário contendo as áreas como chaves, e cada área tem um dicionário de operações associadas às coordenadas (x, y).
    linewidth : int, opcional
        Espessura das linhas que representam os caminhos (padrão é 3).

    Retorno:
    --------
    tuple
        Retorna uma tupla contendo:
        - fig: O objeto `Figure` do matplotlib com os caminhos plotados.
        - ax: O objeto `Axes` atualizado com a plotagem dos caminhos.
    """

    # Encontrar todas as operações e associá-las
    todas_operacoes = []
    for area, pontos in coordenadas_por_area.items():
        for operacao, (x, y) in pontos.items():
            todas_operacoes.append((area, operacao, x, y))
    
    # Ordenar as operações pela ordem crescente
    todas_operacoes.sort(key=lambda op: op[1])
    
    # Associar operações ímpares das áreas com operações ímpares no Picking
    operacoes_picking = coordenadas_por_area.get('Picking', {})
    operacoes_docas_saida = coordenadas_por_area.get('Docas saída', {})

    # Plotando os caminhos
    linhas_verdes = []  # Para armazenar os caminhos verdes
    linhas_azuis = []   # Para armazenar os caminhos azuis
    
    for i, (area, op, x, y) in enumerate(todas_operacoes):
        # Operações ímpares fora do Picking (conectar ao Picking)
        if op % 2 != 0 and area != 'Picking':
            if op in operacoes_picking:
                x_picking, y_picking = operacoes_picking[op]
                
                # Traçar caminho verde da área para o Picking (usando distância de Manhattan)
                linha_verde_1, = ax.plot([x, x_picking], [y, y], 'g--', linewidth=linewidth)  # Caminho horizontal
                linha_verde_2, = ax.plot([x_picking, x_picking], [y, y_picking], 'g--', linewidth=linewidth)  # Caminho vertical
                linhas_verdes.extend([linha_verde_1, linha_verde_2])

        # Conectar operações ímpares no Picking com as pares subsequentes nas Docas saída usando caminho azul
        if op % 2 != 0 and area == 'Picking':
            prox_operacao = op + 1  # Próxima operação par
            # Verificar se a próxima operação par está nas Docas saída
            if prox_operacao in operacoes_docas_saida:
                x_picking, y_picking = operacoes_picking[op]
                x_saida, y_saida = operacoes_docas_saida[prox_operacao]
                
                # Traçar caminho azul do Picking para a Doca de saída
                linha_azul_1, = ax.plot([x_picking, x_saida], [y_picking, y_picking], 'b--', linewidth=linewidth)  # Caminho horizontal
                linha_azul_2, = ax.plot([x_saida, x_saida], [y_picking, y_saida], 'b--', linewidth=linewidth)  # Caminho vertical
                linhas_azuis.extend([linha_azul_1, linha_azul_2])
    
    # Adicionar a legenda
    ax.legend([linhas_verdes[0], linhas_azuis[0]], ['Deslocamento operações Tipo 1', 'Deslocamento operações Tipo 2'], loc='best')
    
    return fig, ax