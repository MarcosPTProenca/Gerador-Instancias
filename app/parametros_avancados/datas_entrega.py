import random

def calcular_datas_entrega(tempos_processamento: dict, 
                           operacoes_por_caminhao: dict, 
                           deterministico: bool = False, 
                           todos_caminhoes_atrasados: bool = False, 
                           todos_caminhoes_adiantados: bool = False) -> dict:
    """
    Calcula as datas de entrega para cada caminhão, usando alfas específicos e média de tempos de processamento.

    Parâmetros:
    - tempos_processamento: dict com tempos de processamento de cada operação em cada empilhadeira.
    - operacoes_por_caminhao: dict mapeando cada caminhão às suas operações.
    - deterministico: bool, se True, usa média dos tempos de processamento das operações.
    - todos_caminhoes_atrasados: bool, se True, sorteia alfas entre 0.5 e 1 para caminhões atrasados.
    - todos_caminhoes_adiantados: bool, se True, sorteia alfas entre 1 e 1.5 para caminhões adiantados.

    Retorna:
    - datas_entrega: dict com as datas de entrega para cada caminhão.
    """

    # Definir alfas com base no estado de cada caminhão
    alfa_caminhao = {}
    if todos_caminhoes_adiantados:
        for caminhao in operacoes_por_caminhao:
            alfa_caminhao[caminhao] = random.uniform(0.1, 0.9)
    elif todos_caminhoes_atrasados:
        for caminhao in operacoes_por_caminhao:
            alfa_caminhao[caminhao] = random.uniform(1.1, 2)
    else:
        for caminhao in operacoes_por_caminhao:
            alfa_caminhao[caminhao] = random.uniform(0.1, 2)

    # 1. Calcular o tempo total de processamento para cada caminhão em todas as empilhadeiras
    tempos_totais_caminhao = {}
    for caminhao, operacoes in operacoes_por_caminhao.items():
        tempo_min_total = float('inf')
        tempo_max_total = 0
        soma_dos_tempos = []

        for maquina in tempos_processamento.keys():
            tempo_total_maquina = 0
            for operacao in operacoes:
                if operacao in tempos_processamento[maquina]:
                    tempo_total_maquina += tempos_processamento[maquina][operacao]['tempo']

            if tempo_total_maquina > 0:
                soma_dos_tempos.append(tempo_total_maquina)
                tempo_min_total = min(tempo_min_total, tempo_total_maquina)
                tempo_max_total = max(tempo_max_total, tempo_total_maquina)

        if soma_dos_tempos:
            tempo_medio = sum(soma_dos_tempos) / len(soma_dos_tempos)
        else:
            raise ValueError(f"Caminhão {caminhao} não possui tempos de processamento válidos.")

        tempos_totais_caminhao[caminhao] = {
            'minimo': tempo_min_total,
            'maximo': tempo_max_total,
            'media': tempo_medio
        }

    # 3. Calcular as datas de entrega com os alfas aplicados
    datas_entrega = {}
    for caminhao, tempos in tempos_totais_caminhao.items():
        # Definir o alfa aplicado ao caminhão
        alfa = alfa_caminhao[caminhao]

        if deterministico:
            # Se determinístico, usa a média dos tempos de processamento multiplicada pelo alfa
            data_entrega = tempos['media'] * alfa
        else:
            # Aleatório entre soma mínima e máxima dos tempos de processamento
            tempo_processamento_aleatorio = random.uniform(tempos['minimo'], tempos['maximo'])
            data_entrega = tempo_processamento_aleatorio * alfa

        # Arredondar para duas casas decimais
        datas_entrega[caminhao] = round(data_entrega)

    return datas_entrega