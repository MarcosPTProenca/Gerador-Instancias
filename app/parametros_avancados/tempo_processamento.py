import random
from .utils import distancia_manhattan

def calcular_tempo_processamento(tipo_empilhadeiras: dict, 
                                 coordenadas_por_area: dict, 
                                 vel_min_emp_rapida: float, 
                                 vel_max_emp_rapida: float,
                                 vel_min_emp_lenta: float, 
                                 vel_max_emp_lenta: float, 
                                 deterministico: bool = False) -> dict:
    """
    Calcula o tempo de processamento em segundos para cada máquina para todas as operações, incluindo distâncias.

    Parâmetros:
    tipo_empilhadeiras (dict): Dicionário com o tipo da empilhadeira ('rápida' ou 'lenta') para cada empilhadeira.
    coordenadas_por_area (dict): Dicionário com as áreas e as coordenadas de cada operação.
    vel_min_emp_rapida (float): Velocidade mínima de uma empilhadeira rápida (em km/h).
    vel_max_emp_rapida (float): Velocidade máxima de uma empilhadeira rápida (em km/h).
    vel_min_emp_lenta (float): Velocidade mínima de uma empilhadeira lenta (em km/h).
    vel_max_emp_lenta (float): Velocidade máxima de uma empilhadeira lenta (em km/h).
    deterministico (bool): Se True, a velocidade será calculada como média entre mínima e máxima. Se False, será aleatória.

    Retorno:
    dict: Dicionário com o tempo de processamento e a distância para cada empilhadeira e operação, arredondado para 2 casas decimais.
    """
    
    # Função para converter km/h para m/s
    def kmh_para_ms(velocidade_kmh):
        return (velocidade_kmh * 1000) / 3600  # Converte para m/s

    # Função para calcular a velocidade conforme o tipo da empilhadeira
    def obter_velocidade(tipo, deterministico):
        if tipo == "rápida":
            if deterministico:
                # Velocidade determinística (média entre mínimo e máximo)
                velocidade_kmh = (vel_min_emp_rapida + vel_max_emp_rapida) / 2
            else:
                # Velocidade aleatória
                velocidade_kmh = random.uniform(vel_min_emp_rapida, vel_max_emp_rapida)
        else:  # Empilhadeira lenta
            if deterministico:
                # Velocidade determinística (média entre mínimo e máximo)
                velocidade_kmh = (vel_min_emp_lenta + vel_max_emp_lenta) / 2
            else:
                # Velocidade aleatória
                velocidade_kmh = random.uniform(vel_min_emp_lenta, vel_max_emp_lenta)
        
        return kmh_para_ms(velocidade_kmh)

    # Dicionário para armazenar o tempo de processamento de cada empilhadeira
    tempos_processamento = {emp: {} for emp in tipo_empilhadeiras}

    # Associar operações ímpares das áreas com operações ímpares no Picking
    operacoes_picking = coordenadas_por_area.get('Picking', {})

    # Calcular os tempos para cada empilhadeira
    for empilhadeira, tipo in tipo_empilhadeiras.items():
        for area, operacoes in coordenadas_por_area.items():
            for operacao, coordenadas in operacoes.items():
                # Operações ímpares das áreas fora do Picking (conectar ao Picking)
                if operacao % 2 != 0 and area != 'Picking':
                    if operacao in operacoes_picking:
                        coordenadas_picking = operacoes_picking[operacao]
                        # Calcular a distância de Manhattan entre a área e o Picking
                        distancia = distancia_manhattan(coordenadas, coordenadas_picking)
                        
                        # Obter a velocidade em m/s
                        velocidade_ms = obter_velocidade(tipo, deterministico)
                        
                        # Calcular o tempo para ir e voltar (tempo em segundos)
                        tempo_total = (2 * distancia) / velocidade_ms
                        
                        # Armazenar o tempo de processamento e a distância
                        tempos_processamento[empilhadeira][operacao] = {
                            'tempo': round(tempo_total),
                            'distancia': round(distancia)
                        }
        
        # Conectar operações ímpares do Picking com pares subsequentes nas Docas de saída
        for operacao, coordenadas in operacoes_picking.items():
            if operacao % 2 != 0 and (operacao + 1) in coordenadas_por_area.get('Docas saída', {}):
                coordenadas_docas_saida = coordenadas_por_area['Docas saída'][operacao + 1]
                # Calcular a distância de Manhattan entre o Picking e as Docas de saída
                distancia = distancia_manhattan(coordenadas, coordenadas_docas_saida)
                
                # Obter a velocidade em m/s
                velocidade_ms = obter_velocidade(tipo_empilhadeiras[empilhadeira], deterministico)
                
                # Calcular o tempo para ir e voltar (tempo em segundos)
                tempo_total = (2 * distancia) / velocidade_ms
                
                # Armazenar o tempo de processamento e a distância
                tempos_processamento[empilhadeira][operacao + 1] = {
                    'tempo': round(tempo_total),
                    'distancia': round(distancia)
                }
                
    # Ordenar as operações para cada empilhadeira
    for emp in tempos_processamento:
        tempos_processamento[emp] = dict(sorted(tempos_processamento[emp].items()))

    return tempos_processamento