import matplotlib.pyplot as plt

def plotar_todas_combinacoes(fig, ax, coordenadas_detalhadas, linewidth=3):
    """
    Função que plota os caminhos entre todas as operações de origem usando a distância de Manhattan.

    Parâmetros:
    fig : matplotlib.figure.Figure
        A figura onde o gráfico será desenhado.
    ax : matplotlib.axes._subplots.AxesSubplot
        Eixo onde o layout e os caminhos serão desenhados.
    coordenadas_detalhadas : dict
        Dicionário contendo as operações como chave e suas coordenadas (x, y) como valor.
        Exemplo: {'1o': (20, 30), '2o': (25, 35), '1d': (30, 40)}
    """
    # Filtrar apenas as operações de origem
    operacoes_origem = {op: coord for op, coord in coordenadas_detalhadas.items() if op.endswith('o')}
    
    # Variável para armazenar a primeira linha traçada
    primeira_linha = None
    
    # Plotar todos os caminhos de todas as combinações de operações de origem
    for op1, (x1, y1) in operacoes_origem.items():
        for op2, (x2, y2) in operacoes_origem.items():
            if op1 != op2:  # Evitar traçar um caminho para si mesmo
                # Caminho em marrom usando a distância de Manhattan
                # Caminho horizontal
                linha_horizontal, = ax.plot([x1, x2], [y1, y1], 'brown', linestyle='--', linewidth=linewidth)
                # Caminho vertical
                linha_vertical, = ax.plot([x2, x2], [y1, y2], 'brown', linestyle='--', linewidth=linewidth)
                
                # Armazenar a primeira linha traçada para a legenda
                if primeira_linha is None:
                    primeira_linha = linha_horizontal
    
    # Adicionar título para o gráfico
    ax.set_title('Caminhos entre todas as operações de origem usando Manhattan')
    
    # Adicionar legenda, se alguma linha foi traçada
    if primeira_linha:
        ax.legend([primeira_linha], ['Deslocamento setup'], loc='best')
    
    return fig, ax

def plotar_caminhos_picking(fig, ax, coordenadas_por_area, linewidth=2):
    """
    Plota todos os caminhos entre as operações no Picking usando a distância de Manhattan.

    Parâmetros:
    fig : matplotlib.figure.Figure
        A figura onde o gráfico será desenhado.
    ax : matplotlib.axes._subplots.AxesSubplot
        Eixo onde o layout e os caminhos serão desenhados.
    coordenadas_por_area : dict
        Dicionário contendo as áreas e as coordenadas de cada operação.
    linewidth : int, optional
        Espessura das linhas dos caminhos (default: 2).
    """

    # Filtrar as coordenadas das operações no Picking
    operacoes_picking = coordenadas_por_area.get('Picking', {})

    # Verificar se há operações suficientes no Picking para calcular caminhos
    if len(operacoes_picking) < 2:
        print("Não há operações suficientes no Picking para traçar caminhos.")
        return fig, ax

    # Variável para armazenar a primeira linha traçada
    primeira_linha = None

    # Plotar todos os caminhos entre as operações no Picking
    for op1, coord1 in operacoes_picking.items():
        for op2, coord2 in operacoes_picking.items():
            if op1 != op2:  # Evitar traçar um caminho para a mesma operação
                # Caminho em marrom usando a distância de Manhattan
                # Caminho horizontal
                linha_horizontal, = ax.plot([coord1[0], coord2[0]], [coord1[1], coord1[1]], 'brown', linestyle='--', linewidth=linewidth)
                # Caminho vertical
                linha_vertical, = ax.plot([coord2[0], coord2[0]], [coord1[1], coord2[1]], 'brown', linestyle='--', linewidth=linewidth)
                
                # Armazenar a primeira linha traçada para a legenda
                if primeira_linha is None:
                    primeira_linha = linha_horizontal

    # Adicionar título para o gráfico
    ax.set_title('Caminhos entre operações no Picking (Distância Manhattan)')

    # Adicionar legenda, se alguma linha foi traçada
    if primeira_linha:
        ax.legend([primeira_linha], ['Deslocamento setup'], loc='best')

    return fig, ax