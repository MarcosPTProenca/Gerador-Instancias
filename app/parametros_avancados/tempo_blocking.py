import random

def calcular_bloqueio(coordenadas_por_area: dict[str, dict], deterministico: bool, t_min: float, t_max: float, n_maquinas: int) -> dict:
    """
    Calcula o tempo de bloqueio entre combinações de operações, levando em consideração diferentes áreas (excluindo a área de 'Picking') e uma quantidade de máquinas, como empilhadeiras.

    Parâmetros:
    -----------
    coordenadas_por_area : dict[str, dict]
        Dicionário contendo áreas como chaves e operações associadas a essas áreas como valores.
        O formato esperado é {'Area': {'Operacao': valor, ...}}.
    deterministico : bool
        Define se o cálculo do tempo de bloqueio será determinístico (média entre t_min e t_max) ou aleatório (valor gerado dentro do intervalo entre t_min e t_max).
    t_min : float
        Tempo mínimo de bloqueio, usado como limite inferior no cálculo.
    t_max : float
        Tempo máximo de bloqueio, usado como limite superior no cálculo.
    n_maquinas : int
        Número de máquinas (empilhadeiras, por exemplo) que serão consideradas no cálculo de bloqueio.

    Retorno:
    --------
    dict
        Dicionário onde cada chave representa uma máquina e cada valor é um dicionário de combinações de operações com seus respectivos tempos de bloqueio.
        O formato retornado é {'Empilhadeira 1': {'Operacao1,Operacao2': tempo_bloqueio, ...}, ...}.
    """
    # Mapeia cada operação à sua área correspondente, excluindo 'Picking'
    operacoes = []
    for area, ops in coordenadas_por_area.items():
        if area != 'Picking':
            operacoes.extend(ops.keys())

    # Ordena as operações para garantir combinações consistentes
    operacoes = sorted(set(operacoes))

    # Gera todas as combinações possíveis de operações (do menor para o maior)
    combinacoes = []
    for i in range(len(operacoes)):
        for j in range(i+1, len(operacoes)):
            op1 = operacoes[i]
            op2 = operacoes[j]
            combinacoes.append((op1, op2))

    tempos_bloqueios = {}
    for maquina in range(1, n_maquinas + 1):
        bloqueios = {}
        for op1, op2 in combinacoes:
            chave = f'{op1},{op2}'

            # Calcula o tempo de bloqueio
            if deterministico:
                tempo_bloqueio = (t_min + t_max) / 2
            else:
                tempo_bloqueio = random.uniform(t_min, t_max)
            bloqueios[chave] = round(tempo_bloqueio)

        tempos_bloqueios[f'Empilhadeira {maquina}'] = bloqueios

    return tempos_bloqueios