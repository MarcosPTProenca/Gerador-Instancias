import random

def calcular_setup(coordenadas_por_area: dict[str, dict[int, tuple[float, float]]], 
                   deterministico: bool, 
                   t_min: float, 
                   t_max: float, 
                   n_maquinas: int) -> dict:
    """
    Calcula os tempos de setup entre combinações de operações, levando em consideração as áreas correspondentes das operações e se são subsequentes ou ocorrem na mesma área.

    Parâmetros:
    -----------
    coordenadas_por_area : dict[str, dict[int, tuple[float, float]]]
        Dicionário contendo áreas como chaves e operações associadas a essas áreas como valores, onde as operações são mapeadas a suas coordenadas.
        O formato esperado é {'Area': {operacao: (x, y), ...}}.
    deterministico : bool
        Define se o cálculo do tempo de setup será determinístico (média entre t_min e t_max) ou aleatório (valor gerado dentro do intervalo entre t_min e t_max).
    t_min : float
        Tempo mínimo de setup, usado como limite inferior no cálculo.
    t_max : float
        Tempo máximo de setup, usado como limite superior no cálculo.
    n_maquinas : int
        Número de máquinas (empilhadeiras, por exemplo) que serão consideradas no cálculo de setup.

    Retorno:
    --------
    dict
        Dicionário onde cada chave representa uma máquina e cada valor é um dicionário de combinações de operações com seus respectivos tempos de setup.
        O formato retornado é {'Empilhadeira 1': {'Operacao1,Operacao2': tempo_setup, ...}, ...}.
    """

    # Mapeia cada operação à sua área correspondente
    operacao_para_area = {}
    for area, operacoes in coordenadas_por_area.items():
        if area != 'Picking':
            for operacao in operacoes.keys():
                operacao_para_area[operacao] = area

    # Lista de operações excluindo as do 'Picking'
    operacoes = sorted(operacao_para_area.keys())

    # Pares de operações com setup zero por serem subsequentes
    pares_zero = [(1, 2), (3, 4), (5, 6)]

    # Gera todas as combinações possíveis de operações (do menor para o maior)
    combinacoes = []
    for i in range(len(operacoes)):
        for j in range(i+1, len(operacoes)):
            op1 = operacoes[i]
            op2 = operacoes[j]
            combinacoes.append((op1, op2))

    tempos_setup = {}
    for maquina in range(1, n_maquinas + 1):
        setups = {}
        for op1, op2 in combinacoes:
            chave = f'{op1},{op2}'

            # Verifica se as operações são subsequentes de 2 em 2
            if (op1, op2) in pares_zero:
                setups[chave] = 0
                continue

            # Verifica se as operações estão na mesma área
            area_op1 = operacao_para_area.get(op1)
            area_op2 = operacao_para_area.get(op2)
            if area_op1 == area_op2:
                setups[chave] = 0
                continue

            # Caso contrário, calcula o setup
            if deterministico:
                tempo_setup = (t_min + t_max) / 2
            else:
                tempo_setup = random.uniform(t_min, t_max)
            setups[chave] = round(tempo_setup)

        tempos_setup[f'Empilhadeira {maquina}'] = setups

    return tempos_setup