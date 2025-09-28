from .print_parametros import print_tarefas, print_maquinas, print_n_operations
from .print_parametros import print_datas_saida, print_predecessores
from .print_parametros import print_elegibilidade, print_tempo_processamento
from .print_parametros import print_tempo_setup, print_tempo_bloqueio
from .print_parametros import print_caminhoes

# Função principal que utiliza as funções acima
def pipeline_gerar_prints_parametros(n_maquinas: int, 
                                     n_tarefas_docas : int,
                                     n_tarefas_estoque: int,
                                     resultados: dict[str, any], 
                                     elegibilidade: dict[int, dict], 
                                     tempos_processamento: dict[str, dict], 
                                     datas_saida: dict[str, float], 
                                     n_operacoes_por_tarefa: int, 
                                     tempos_bloqueios: dict[str, dict[str, int]], 
                                     n_caminhoes: int, 
                                     tempos_setup: dict[str, dict[str, int]],
                                     todos_caminhoes_atrasados: bool,
                                     todos_caminhoes_adiantados: bool,
                                     pasta) -> None:

    
    if todos_caminhoes_atrasados:
        nome_arquivo = f"{pasta}{n_tarefas_docas}_{n_tarefas_estoque}_{n_maquinas}_{n_caminhoes}_at_AMPL.txt"
    elif todos_caminhoes_adiantados:
        nome_arquivo = f"{pasta}{n_tarefas_docas}_{n_tarefas_estoque}_{n_maquinas}_{n_caminhoes}_ad_AMPL.txt"
    else:
        nome_arquivo = f"{pasta}{n_tarefas_docas}_{n_tarefas_estoque}_{n_maquinas}_{n_caminhoes}_AMPL.txt"
    
    with open(nome_arquivo, 'w') as f:
        print_tarefas(resultados, f)
        print_maquinas(n_maquinas, f)
        print_caminhoes(n_caminhoes, f)
        print_n_operations(resultados['n_total_tarefas'], n_operacoes_por_tarefa, f)
        print_datas_saida(datas_saida, f)
        print_predecessores(resultados, f)
        print_elegibilidade(elegibilidade, n_caminhoes, n_maquinas, f)
        print_tempo_processamento(elegibilidade, tempos_processamento, n_maquinas, f)
        print_tempo_setup(tempos_setup, resultados['n_total_operacoes'], n_maquinas, f)
        print_tempo_bloqueio(tempos_bloqueios, resultados['n_total_operacoes'], n_maquinas, f)
