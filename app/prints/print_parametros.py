# Função auxiliar para escrever no arquivo e também imprimir no console
def escrever_arquivo(f, conteudo: str) -> None:
    f.write(conteudo + '\n')

def print_datas_saida(datas_saida: dict[str, float], f) -> None:
    """
    Imprime os dados de saída dos caminhões no formato necessário para um modelo AMPL.

    Parâmetros:
    -----------
    datas_saida : dict[str, float]
        Dicionário onde as chaves são os caminhões (e.g., 'Caminhão 1') e os valores são as datas de saída.

    Retorno:
    --------
    None
    """

    escrever_arquivo(f, "# Parametro data de saida dos caminhoes")
    escrever_arquivo(f, "param d :=")
    for caminhao, data_saida in datas_saida.items():
        numero_caminhao = int(caminhao.split()[1])
        escrever_arquivo(f, f"{numero_caminhao} {round(data_saida)}")
    escrever_arquivo(f, ";\n")

def print_tempo_processamento(elegibilidade: dict[int, dict], 
                              tempos_processamento: dict[str, dict], 
                              n_maquinas: int, 
                              f) -> None:
    """
    Imprime o tempo de processamento de cada operação para cada máquina no formato AMPL.

    Parâmetros:
    -----------
    elegibilidade : dict[int, dict]
        Dicionário que mapeia as operações às suas máquinas elegíveis e caminhões.
    tempos_processamento : dict[str, dict]
        Dicionário que mapeia o tempo de processamento para cada operação e máquina.
    n_maquinas : int
        Número total de máquinas.

    Retorno:
    --------
    None
    """

    escrever_arquivo(f, "# Parametro do tempo de processamento de cada operacao")
    escrever_arquivo(f, "param p :=")
    for operacao in sorted(elegibilidade.keys()):
        for maquina in range(1, n_maquinas + 1):
            if maquina in elegibilidade[operacao]['maquinas']:
                tempo = tempos_processamento[f'Empilhadeira {maquina}'][operacao]['tempo']
                escrever_arquivo(f, f"{operacao} {maquina} {round(tempo)}")
            else:
                escrever_arquivo(f, f"{operacao} {maquina} .")
    escrever_arquivo(f, ";\n")

def print_elegibilidade(elegibilidade: dict[int, dict], 
                        n_caminhoes: int, 
                        n_maquinas: int, 
                        f) -> None:
    """
    Imprime a elegibilidade de cada operação para cada máquina no formato AMPL.

    Parâmetros:
    -----------
    elegibilidade : dict[int, dict]
        Dicionário que mapeia as operações às suas máquinas elegíveis e caminhões.
    n_caminhoes : int
        Número total de caminhões.
    n_maquinas : int
        Número total de máquinas.

    Retorno:
    --------
    None
    """

    escrever_arquivo(f, "# Parametro de elegibilidade das operacoes para cada maquina")
    escrever_arquivo(f, "param Ri :=")
    for idx, operacao in enumerate(sorted(elegibilidade.keys())):
        for caminhao in range(1, n_caminhoes + 1):
            for maquina in range(1, n_maquinas + 1):
                if elegibilidade[operacao]['caminhao'] == caminhao and maquina in elegibilidade[operacao]['maquinas']:
                    escrever_arquivo(f, f"{operacao} {caminhao} {maquina} 1")
                else:
                    escrever_arquivo(f, f"{operacao} {caminhao} {maquina} 0")
        if idx == len(elegibilidade) - 1:
            escrever_arquivo(f, ";\n")
        else:
            escrever_arquivo(f, "")

def print_predecessores(resultados: dict[str, dict[int, int]], f) -> None:
    """
    Imprime os predecessores de cada operação no formato AMPL.

    Parâmetros:
    -----------
    resultados : dict[str, dict[int, int]]
        Dicionário contendo os predecessores de cada operação.

    Retorno:
    --------
    None
    """

    predecessores = resultados["predecessores"]
    escrever_arquivo(f, "# Parametro dos predecessores de cada operacao")
    escrever_arquivo(f, "param pr :=")
    for operacao, predecessor in predecessores.items():
        escrever_arquivo(f, f"{operacao} {predecessor}")
    escrever_arquivo(f, ";\n")

def print_maquinas(n_maquinas: int, f) -> None:
    """
    Imprime a quantidade de máquinas no formato AMPL.

    Parâmetros:
    -----------
    n_maquinas : int
        Número total de máquinas.

    Retorno:
    --------
    None
    """

    escrever_arquivo(f, "# Quantidade de máquinas")
    escrever_arquivo(f, f"param n_machines := {n_maquinas};\n")

def print_caminhoes(n_caminhoes: int, f) -> None:
    """
    Imprime a quantidade de caminhões no formato AMPL.

    Parâmetros:
    -----------
    n_maquinas : int
        Número total de caminhões.

    Retorno:
    --------
    None
    """

    escrever_arquivo(f, "# Quantidade de caminhões")
    escrever_arquivo(f, f"param n_caminhoes := {n_caminhoes};\n")

def print_tarefas(resultados: dict[str, int], f) -> None:
    """
    Imprime a quantidade de jobs (tarefas) no formato AMPL.

    Parâmetros:
    -----------
    resultados : dict[str, int]
        Dicionário contendo o número total de tarefas.

    Retorno:
    --------
    None
    """

    n_jobs = resultados["n_total_tarefas"]
    escrever_arquivo(f, "# Quantidade de jobs")
    escrever_arquivo(f, f"param n_jobs := {n_jobs};\n")

def print_tempo_setup(tempos_setup: dict[str, dict[str, int]], 
                      n_operacoes: int, 
                      n_maquinas: int, 
                      f) -> None:
    """
    Imprime o tempo de setup entre operações para cada máquina no formato AMPL.

    Parâmetros:
    -----------
    tempos_setup : dict[str, dict[str, int]]
        Dicionário que contém os tempos de setup entre pares de operações por máquina.
    n_operacoes : int
        Número total de operações.
    n_maquinas : int
        Número total de máquinas.

    Retorno:
    --------
    None
    """

    escrever_arquivo(f, '# Parametro tempo de setup entre operacoes')
    escrever_arquivo(f, "param s :=")
    for machine in range(1, n_maquinas + 1):
            machine_key = f'Empilhadeira {machine}'
            if machine_key not in tempos_setup:
                escrever_arquivo(f, f"[*,*,{machine}]")
                for i in range(1, n_operacoes + 1):
                    line = []
                    for j in range(1, n_operacoes + 1):
                        setup_time = '.' if i == j else 0
                        line.extend([i, j, setup_time])
                    escrever_arquivo(f, ' '.join(map(str, line)))
            else:
                escrever_arquivo(f, f"\n[*,*,{machine}]")
                for i in range(1, n_operacoes + 1):
                    line = []
                    for j in range(1, n_operacoes + 1):
                        if i == j:
                            setup_time = '.'
                        else:
                            pair_key_1 = f"{i},{j}"
                            pair_key_2 = f"{j},{i}"
                            setup_time = tempos_setup[machine_key].get(pair_key_1, tempos_setup[machine_key].get(pair_key_2, 0))
                            
                            # Garantir que setup_time é numérico
                            if isinstance(setup_time, str):
                                try:
                                    setup_time = float(setup_time)  # Tenta converter para float
                                except ValueError:
                                    setup_time = 0  # Valor padrão se não puder converter
                            
                            setup_time = int(round(setup_time))  # Garantir que é inteiro
                        line.extend([i, j, setup_time])
                    escrever_arquivo(f, ' '.join(map(str, line)))
    
    escrever_arquivo(f, ";\n")

def print_tempo_bloqueio(tempos_bloqueios: dict[str, dict[str, int]], 
                         n_operacoes: int, 
                         n_maquinas: int, 
                         f) -> None:

    """
    Imprime o tempo de bloqueio entre operações para cada máquina no formato AMPL.

    Parâmetros:
    -----------
    tempos_bloqueios : dict[str, dict[str, int]]
        Dicionário que contém os tempos de bloqueio entre pares de operações por máquina.
    n_operacoes : int
        Número total de operações.
    n_maquinas : int
        Número total de máquinas.

    Retorno:
    --------
    None
    """

    escrever_arquivo(f, '# Parametro tempo de bloqueio entre operacoes')
    escrever_arquivo(f, "param bk :=")
    for machine in range(1, n_maquinas + 1):
        machine_key = f'Empilhadeira {machine}'
        if machine_key not in tempos_bloqueios:
            escrever_arquivo(f, f"[*,*,{machine}]")
            for i in range(1, n_operacoes + 1):
                line = []
                for j in range(1, n_operacoes + 1):
                    setup_time = '.' if i == j else 0
                    line.extend([i, j, setup_time])
                escrever_arquivo(f, ' '.join(map(str, line)))
        else:
            escrever_arquivo(f, f"\n[*,*,{machine}]")
            for i in range(1, n_operacoes + 1):
                line = []
                for j in range(1, n_operacoes + 1):
                    if i == j:
                        setup_time = '.'
                    else:
                        pair_key_1 = f"{i},{j}"
                        pair_key_2 = f"{j},{i}"
                        setup_time = tempos_bloqueios[machine_key].get(pair_key_1, tempos_bloqueios[machine_key].get(pair_key_2, 0))
                        
                        # Garantir que setup_time é numérico
                        if isinstance(setup_time, str):
                            try:
                                setup_time = float(setup_time)  # Tenta converter para float
                            except ValueError:
                                setup_time = 0  # Valor padrão se não puder converter
                        
                        setup_time = int(round(setup_time))  # Garantir que é inteiro
                    line.extend([i, j, setup_time])
                escrever_arquivo(f, ' '.join(map(str, line)))
    
    escrever_arquivo(f, ";\n")

def print_n_operations(n_total_tarefas: int, n_operacoes_por_tarefa: int, f) -> None:
    """
    Imprime o número de operações por tarefa no formato AMPL.

    Parâmetros:
    -----------
    n_total_tarefas : int
        Número total de tarefas.
    n_operacoes_por_tarefa : int
        Número de operações associadas a cada tarefa.

    Retorno:
    --------
    None
    """

    escrever_arquivo(f, "param n_operations :=")
    for tarefa in range(1, n_total_tarefas + 1):
        escrever_arquivo(f, f"{tarefa} {n_operacoes_por_tarefa}")
    escrever_arquivo(f, ";\n")



