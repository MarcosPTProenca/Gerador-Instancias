from .tarefas_operacoes import gerar_tarefas_estoque_e_docas, criar_lista_tarefas, distribuir_tarefas_caminhoes
from .tarefas_operacoes import calcular_totais, criar_predecessores, distribuir_operacoes_por_area
from .tarefas_operacoes import criar_operacoes_por_caminhao

def pipeline_gerar_todas_tarefas_e_operacoes(n_areas_estoque: int, 
                                             n_tarefas_estoque: int,
                                             n_tarefas_docas: int,
                                             n_caminhoes: int, 
                                             n_operacoes_por_tarefa: int) -> dict[dict, dict, int, int, dict, dict, dict]:
    
    # Gerando tarefas para as áreas de crossdocking
    tarefas_por_area = gerar_tarefas_estoque_e_docas(n_areas_estoque, n_tarefas_estoque, n_tarefas_docas)
    
    # Criando lista de tarefas numeradas sequencialmente
    tarefas = criar_lista_tarefas(tarefas_por_area)
    
    # Distribuindo tarefas aleatoriamente entre os caminhões
    tarefas_por_caminhao = distribuir_tarefas_caminhoes(tarefas, n_caminhoes)
    
    # Calculando o total de tarefas e operações
    n_total_tarefas, n_total_operacoes = calcular_totais(tarefas_por_area, n_operacoes_por_tarefa)
    
    # Criando predecessores de operações
    predecessores = criar_predecessores(n_total_operacoes, n_operacoes_por_tarefa)
    
    # Distribuindo operações ímpares e pares entre as áreas
    operacoes_por_area_final = distribuir_operacoes_por_area(tarefas_por_area, n_total_operacoes, n_operacoes_por_tarefa)
    
    # Criando o dicionário de operações por caminhão
    operacoes_por_caminhao = criar_operacoes_por_caminhao(tarefas_por_caminhao)
    
    # Retornando todos os outputs
    return {
        "tarefas_por_area": tarefas_por_area,
        "operacoes_por_area_final": operacoes_por_area_final,
        "n_total_tarefas": n_total_tarefas,
        "n_total_operacoes": n_total_operacoes,
        "tarefas_por_caminhao": tarefas_por_caminhao,
        "operacoes_por_caminhao": operacoes_por_caminhao,
        "predecessores": predecessores
    }