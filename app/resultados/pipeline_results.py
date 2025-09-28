from .leitura_result import parse_log_file
from .gantt import grafico_gantt_por_tarefas, grafico_gantt_empilhadeiras, grafico_gantt_caminhoes
from .heatmap import plot_heatmap_caminhos_horizontal
from .metricas import calculate_metrics

def pipeline_graficos_resultados(file_path, area_indices, coordenadas_detalhadas):
    try:
        # Parse do arquivo de log
        parametros = parse_log_file(file_path)
    except Exception as e:
        print(f"Erro ao analisar o arquivo de log: {e}")
        return

    try:
        # Cálculo das métricas
        result_metricas = calculate_metrics(parametros['n_caminhoes'], parametros['n_maquinas'], parametros['alpha'], parametros['p'], parametros['t'], parametros['d'])
        
        # Exibindo os resultados
        print("Makespan:", result_metricas['makespan'])
        print("Atraso máximo:", result_metricas['max_delay'])
        print("Número de operações atrasadas:", result_metricas['num_delays'])
        print("Soma dos atrasos:", result_metricas['sum_delays'])
    
    except Exception as e:
        print(f"Erro ao calcular as métricas: {e}")

    try:
        # Gráfico de Gantt das empilhadeiras
        grafico_gantt_empilhadeiras(parametros['alpha'], parametros['t'], parametros['p'], parametros['n_caminhoes'], parametros['n_maquinas'])
    except Exception as e:
        print(f"Erro ao gerar gráfico de Gantt das empilhadeiras: {e}")

    try:
        # Gráfico de Gantt dos caminhões
        grafico_gantt_caminhoes(parametros['alpha'], parametros['t'], parametros['p'], parametros['d'], parametros['A'], parametros['n_caminhoes'], parametros['n_maquinas'])
    except Exception as e:
        print(f"Erro ao gerar gráfico de Gantt dos caminhões: {e}")

    try:
        # Gráfico de Gantt por tarefas
        grafico_gantt_por_tarefas(parametros['alpha'], parametros['t'], parametros['p'], parametros['n_caminhoes'], parametros['n_maquinas'])
    except Exception as e:
        print(f"Erro ao gerar gráfico de Gantt por tarefas: {e}")

    try:
        # Mapa de calor dos caminhos percorridos pelas empilhadeiras
        plot_heatmap_caminhos_horizontal(area_indices, coordenadas_detalhadas, parametros['alpha'])
    except Exception as e:
        print(f"Erro ao gerar o mapa de calor: {e}")

    
    
    



