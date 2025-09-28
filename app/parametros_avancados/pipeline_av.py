from .datas_entrega import calcular_datas_entrega
from. elegibilidade import elegibilidade_maquinas
from .empilhadeiras import classificar_empilhadeiras, classificar_empilhadeiras_por_areas
from .tempo_blocking import calcular_bloqueio
from .tempo_processamento import calcular_tempo_processamento
from .tempo_setup import calcular_setup

def pipeline_parametros_avancados(num_maquinas: int, 
                                  operacoes_por_area: dict[str, list[int]], 
                                  operacoes_por_caminhao: dict[str, list[int]], 
                                  proporcao_maquinas: dict[str, float], 
                                  proporcao_rapidas: float, 
                                  proporcao_areas: dict[str, float], 
                                  coordenadas_por_area: dict[str, dict[int, tuple[float, float]]], 
                                  deterministico: bool, 
                                  vel_min_emp_rapida: float, 
                                  vel_max_emp_rapida: float, 
                                  vel_min_emp_lenta: float, 
                                  vel_max_emp_lenta: float, 
                                  t_min_block: float, 
                                  t_max_block: float, 
                                  t_min_setup: float, 
                                  t_max_setup: float, 
                                  todos_caminhoes_atrasados: bool, 
                                  todos_caminhoes_adiantados: bool) -> tuple[dict, dict, dict, dict]:

    # Classifica as empilhadeiras em rápidas ou lentas, com base na proporção de empilhadeiras rápidas
    classificacao_empilhadeiras_velocidade = classificar_empilhadeiras(num_maquinas, 
                                                                       proporcao_rapidas)

    # Define a alocação de empilhadeiras para diferentes áreas, com base nas proporções fornecidas
    classificacao_empilhadeiras_areas = classificar_empilhadeiras_por_areas(num_maquinas, 
                                                                            proporcao_areas)
    
    # Calcula a elegibilidade das máquinas para operar em determinadas áreas e associar operações aos caminhões
    elegibilidade = elegibilidade_maquinas(num_maquinas, 
                                           operacoes_por_area, 
                                           operacoes_por_caminhao, 
                                           proporcao_maquinas, 
                                           classificacao_empilhadeiras_areas)


    # Calcula os tempos de bloqueio entre operações com base nas áreas e nas máquinas envolvidas
    tempos_bloqueios = calcular_bloqueio(coordenadas_por_area, 
                                         deterministico, 
                                         t_min_block, 
                                         t_max_block, 
                                         num_maquinas)
    
    # Calcula os tempos de processamento das operações, considerando a velocidade das empilhadeiras rápidas e lentas
    tempos_processamento = calcular_tempo_processamento(classificacao_empilhadeiras_velocidade, 
                                                        coordenadas_por_area, 
                                                        vel_min_emp_rapida, 
                                                        vel_max_emp_rapida,
                                                        vel_min_emp_lenta, 
                                                        vel_max_emp_lenta, 
                                                        deterministico)
    
    # Calcula os tempos de setup entre as operações, considerando a localização e a ordem das operações
    tempos_setup = calcular_setup(coordenadas_por_area, 
                                  deterministico, 
                                  t_min_setup, 
                                  t_max_setup, 
                                  num_maquinas)

    # Calcula as datas de entrega estimadas para as operações com base nos tempos de processamento e parâmetros de caminhões
    datas_entrega = calcular_datas_entrega(tempos_processamento, 
                                           operacoes_por_caminhao, 
                                           deterministico, 
                                           todos_caminhoes_atrasados,
                                           todos_caminhoes_adiantados)
    
    return elegibilidade, datas_entrega, tempos_setup, tempos_bloqueios, tempos_processamento