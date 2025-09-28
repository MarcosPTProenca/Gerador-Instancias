
def distancia_manhattan(ponto1: tuple[int,int], ponto2: tuple[int,int]) -> float:
    """
    Calcula a distância de Manhattan entre dois pontos.

    Parâmetros:
    ponto1 (tuple): Coordenadas (x, y) do primeiro ponto.
    ponto2 (tuple): Coordenadas (x, y) do segundo ponto.

    Retorno:
    float: Distância de Manhattan entre os dois pontos.
    """
    x1, y1 = ponto1
    x2, y2 = ponto2
    return abs(x1 - x2) + abs(y1 - y2)