import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import pandas as pd

def grafico_gantt_empilhadeiras(alpha, t, p, n_caminhoes: int, n_maquinas: int):
    """
    Gera um gráfico de Gantt das operações para cada empilhadeira e caminhão.

    Parâmetros:
    - alpha: Dicionário com as atribuições de operações (matriz para cada caminhão ou empilhadeira, dependendo da relação n_caminhoes/n_maquinas).
    - t: Dicionário com os tempos de início de cada operação.
    - p: Lista de tuplas com os tempos de processamento de cada operação (i, k, tempo).
    - n_caminhoes: Número de caminhões.
    - n_maquinas: Número de empilhadeiras.
    """
    # Preparar os dados para o gráfico de Gantt
    operacoes = []

    # Converter lista de tempos de processamento para dicionário
    tempos_processamento = {(op, emp): tempo for op, emp, tempo in p}

    # Gerar uma paleta de cores em escala de cinza para os caminhões
    cinzas = np.linspace(0.3, 0.7, n_caminhoes)  # Tonalidades de cinza de 0.3 a 0.7
    caminhao_cores = {c: str(cor) for c, cor in zip(range(1, n_caminhoes + 1), cinzas)}

    # Organizar operações por empilhadeira e tempo de início
    empilhadeira_operacoes_t = defaultdict(list)
    
    # Processar alpha dependendo do número de caminhões e máquinas
    if n_maquinas < n_caminhoes:
        # Caso onde há mais máquinas do que caminhões (empilhadeiras em linhas e caminhões em colunas)
        for empilhadeira, matriz_alpha in alpha.items():
            for i in range(matriz_alpha.shape[0]):  # Para cada operação (linha)
                for k in range(matriz_alpha.shape[1]):  # Para cada caminhão (coluna)
                    if matriz_alpha[i, k] == 1:  # Se a empilhadeira realizou a operação
                        op = i + 1  # Operação começa na linha 1
                        caminhao = k + 1  # Caminhão começa na coluna 1
                        if op in t and (op, empilhadeira) in tempos_processamento:
                            start_time = t[op]
                            duration = tempos_processamento[(op, empilhadeira)]
                            empilhadeira_operacoes_t[empilhadeira].append((op, caminhao, start_time, duration))
                        else:
                            print(f"Aviso: Tempo de início ou processamento para operação {op} na empilhadeira {empilhadeira} não encontrado.")
    else:
        # Caso onde há mais caminhões do que máquinas (caminhões em linhas e empilhadeiras em colunas)
        for caminhao, matriz_alpha in alpha.items():
            for i in range(matriz_alpha.shape[0]):  # Para cada operação (linha)
                for k in range(matriz_alpha.shape[1]):  # Para cada empilhadeira (coluna)
                    if matriz_alpha[i, k] == 1:  # Se o caminhão realizou a operação
                        op = i + 1  # Operação começa na linha 1
                        empilhadeira = k + 1  # Empilhadeira começa na coluna 1
                        if op in t and (op, empilhadeira) in tempos_processamento:
                            start_time = t[op]
                            duration = tempos_processamento[(op, empilhadeira)]
                            empilhadeira_operacoes_t[empilhadeira].append((op, caminhao, start_time, duration))
                        else:
                            print(f"Aviso: Tempo de início ou processamento para operação {op} na empilhadeira {empilhadeira} não encontrado.")

    # Criar DataFrame das operações processadas
    operacoes = []
    for empilhadeira, ops in empilhadeira_operacoes_t.items():
        for op, caminhao, start_time, duration in ops:
            operacoes.append({
                'Empilhadeira': f'Empilhadeira {empilhadeira}',
                'Operação': f'{op}',  # Nome da operação
                'Início': start_time,
                'Fim': start_time + duration,
                'Caminhão': caminhao,
            })

    # Criar dataframe das operações
    df_ops = pd.DataFrame(operacoes)

    # Ordenar empilhadeiras do maior para o menor
    df_ops['Empilhadeira_Num'] = df_ops['Empilhadeira'].apply(lambda x: int(x.split()[1]))
    df_ops.sort_values(by='Empilhadeira_Num', ascending=True, inplace=True)

    # Plotar gráfico de Gantt
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for idx, row in df_ops.iterrows():
        cor = caminhao_cores.get(row['Caminhão'], 'lightgray')
        ax.barh(row['Empilhadeira'], row['Fim'] - row['Início'], left=row['Início'],
                color=cor, edgecolor='black')
        ax.text(row['Início'] + (row['Fim'] - row['Início']) / 2, row['Empilhadeira'],
                row['Operação'], va='center', ha='center', color='black', fontsize=10, fontweight='bold')
    
    # Ajuste das cores para legendas
    handles = [plt.Line2D([0], [0], color=caminhao_cores[c], lw=4) for c in caminhao_cores]
    labels = [f'Caminhão {c}' for c in caminhao_cores]
    ax.legend(handles, labels, title='Caminhões', loc='upper right')

    ax.set_xlabel('Tempo')
    plt.tight_layout()
    plt.show()

def grafico_gantt_caminhoes(alpha, t, p, d, A, n_caminhoes: int, n_maquinas: int):
    """
    Gera um gráfico de Gantt das operações para cada caminhão.

    Parâmetros:
    - alpha: Dicionário com as atribuições de operações (matriz para cada caminhão).
    - t: Dicionário com os tempos de início de cada operação.
    - p: Lista de tuplas com os tempos de processamento de cada operação (i, k, tempo).
    - d: Dicionário com os tempos de saída de cada caminhão.
    - A: Dicionário com os atrasos de cada caminhão.
    - n_caminhoes: Número de caminhões.
    - n_maquinas: Número de empilhadeiras.
    """
    # Preparar os dados para o gráfico de Gantt
    operacoes = []

    # Converter lista de tempos de processamento para dicionário
    tempos_processamento = {(op, emp): tempo for op, emp, tempo in p}

    # Processar alpha dependendo do número de caminhões e máquinas
    if n_maquinas < n_caminhoes:
        # Caso onde há mais máquinas do que caminhões (empilhadeiras em linhas e caminhões em colunas)
        for empilhadeira, matriz_alpha in alpha.items():
            for i in range(matriz_alpha.shape[0]):  # Para cada operação (linha)
                for k in range(matriz_alpha.shape[1]):  # Para cada caminhão (coluna)
                    if matriz_alpha[i, k] == 1:  # Se a empilhadeira realizou a operação
                        op = i + 1  # Operação começa na linha 1
                        caminhao = k + 1  # Caminhão começa na coluna 1
                        if caminhao not in d:
                            print(f"Caminhão {caminhao} não possui uma data de saída definida.")
                            continue  # Ignora caminhões que não possuem data de saída

                        # Verificar se tempos de início e processamento estão disponíveis
                        if op in t and (op, empilhadeira) in tempos_processamento:
                            start_time = t[op]
                            duration = tempos_processamento[(op, empilhadeira)]
                            fim_operacao = start_time + duration

                            atraso = fim_operacao > d[caminhao]  # Verificar se há atraso

                            operacoes.append({
                                'Caminhão': f'Caminhão {caminhao}',
                                'Operação': f'{op}',
                                'Início': start_time,
                                'Fim': fim_operacao,
                                'Empilhadeira': empilhadeira,
                                'Atraso': atraso,
                                'Data Saída': d[caminhao]
                            })
                        else:
                            print(f"Aviso: Tempo de início ou processamento para operação {op} na empilhadeira {empilhadeira} não encontrado.")
    else:
        # Caso onde há mais caminhões do que máquinas (caminhões em linhas e empilhadeiras em colunas)
        for caminhao, matriz_alpha in alpha.items():
            for i in range(matriz_alpha.shape[0]):  # Para cada operação (linha)
                for k in range(matriz_alpha.shape[1]):  # Para cada empilhadeira (coluna)
                    if matriz_alpha[i, k] == 1:  # Se o caminhão realizou a operação
                        op = i + 1  # Operação começa na linha 1
                        empilhadeira = k + 1  # Empilhadeira começa na coluna 1
                        if caminhao not in d:
                            print(f"Caminhão {caminhao} não possui uma data de saída definida.")
                            continue  # Ignora caminhões que não possuem data de saída

                        # Verificar se tempos de início e processamento estão disponíveis
                        if op in t and (op, empilhadeira) in tempos_processamento:
                            start_time = t[op]
                            duration = tempos_processamento[(op, empilhadeira)]
                            fim_operacao = start_time + duration

                            atraso = fim_operacao > d[caminhao]  # Verificar se há atraso

                            operacoes.append({
                                'Caminhão': f'Caminhão {caminhao}',
                                'Operação': f'{op}',
                                'Início': start_time,
                                'Fim': fim_operacao,
                                'Empilhadeira': empilhadeira,
                                'Atraso': atraso,
                                'Data Saída': d[caminhao]
                            })
                        else:
                            print(f"Aviso: Tempo de início ou processamento para operação {op} na empilhadeira {empilhadeira} não encontrado.")
    
    df_ops = pd.DataFrame(operacoes)
    
    # Ordenar caminhões do maior para o menor
    df_ops['Caminhão_Num'] = df_ops['Caminhão'].apply(lambda x: int(x.split()[1]))
    df_ops.sort_values(by='Caminhão_Num', ascending=True, inplace=True)

    # Definir cores para operações normais e atrasadas
    cor_normal = 'lightgray'
    cor_atrasada = 'darkgray'
    cor_saida = 'red'  # Cor para a linha de saída dos caminhões
    
    # Plotar gráfico de Gantt
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for idx, row in df_ops.iterrows():
        # Desenhar a parte normal da operação
        cor = cor_normal
        if row['Início'] < row['Data Saída']:
            fim_parte_normal = min(row['Fim'], row['Data Saída'])
            ax.barh(row['Caminhão'], fim_parte_normal - row['Início'], left=row['Início'],
                    color=cor, edgecolor='black')
        # Desenhar a parte atrasada da operação, se existir
        if row['Fim'] > row['Data Saída']:
            inicio_parte_atrasada = max(row['Início'], row['Data Saída'])
            ax.barh(row['Caminhão'], row['Fim'] - inicio_parte_atrasada, left=inicio_parte_atrasada,
                    color=cor_atrasada, edgecolor='black')
            
        ax.text(row['Início'] + (row['Fim'] - row['Início']) / 2, row['Caminhão'],
                row['Operação'], va='center', ha='center', color='black', fontsize=9)
            
    # Adicionar linha vertical para o atraso da última operação mais demorada
    if not df_ops.empty:
        fim_max = df_ops['Fim'].max()  # Tempo máximo de finalização das operações
        ultima_operacao = df_ops[df_ops['Fim'] == fim_max].iloc[0]  # Última operação mais demorada
        if A.get(int(ultima_operacao['Caminhão'].split()[1]), 0) > 0:  # Verificar se há atraso para o caminhão
            # Adicionar linha vertical vermelha na última operação mais demorada
            ax.axvline(fim_max, color='black', linestyle='--', linewidth=1.5)
            # Centralizar o texto verticalmente na linha do atraso e deslocar um pouco para a direita
            ax.text(fim_max + 1, df_ops['Caminhão'].unique().tolist().index(ultima_operacao['Caminhão']) + 0.5,
                    f'Atraso: {A[int(ultima_operacao["Caminhão"].split()[1])]:.1f}', va='center', ha='center', color='black', fontsize=9, fontweight='bold', rotation=270)

    # Adicionar legenda para as cores das operações
    handles = [
        plt.Line2D([0], [0], color=cor_normal, lw=6, label='Operações Não Atrasadas'),
        plt.Line2D([0], [0], color=cor_atrasada, lw=6, label='Operações Atrasadas'),
        plt.Line2D([0], [0], color=cor_saida, linestyle='--', lw=2, label='Data de Saída'),
        plt.Line2D([0], [0], color='black', linestyle='--', lw=1.5, label='Última Operação com Atraso')
    ]
    ax.legend(handles=handles, title='Status das Operações', loc='upper right')

    ax.set_xlabel('Tempo')
    plt.tight_layout()
    plt.show()

def grafico_gantt_por_tarefas(alpha, t, p):
    """
    Gera um gráfico de Gantt com as tarefas no eixo y, onde cada tarefa é formada por pares consecutivos de operações.

    Parâmetros:
    - alpha: Dicionário com as atribuições de operações (matriz para cada caminhão).
    - t: Dicionário com os tempos de início de cada operação.
    - p: Lista de tuplas com os tempos de processamento de cada operação (i, k, tempo).
    """
    # Converter lista de tempos de processamento para dicionário
    tempos_processamento = {(op, emp): tempo for op, emp, tempo in p}

    # Criar DataFrame de operações
    operacoes = []
    for empilhadeira, matriz_alpha in alpha.items():
        for i in range(matriz_alpha.shape[0]):
            for k in range(matriz_alpha.shape[1]):
                if matriz_alpha[i, k] == 1:  # Considerar apenas as operações atribuídas
                    start_time = t[i + 1]
                    duration = tempos_processamento[(i + 1, empilhadeira)]
                    fim_operacao = start_time + duration
                    operacoes.append({
                        'Caminhão': k + 1,  # Caminhão começa em 1
                        'Operação': i + 1,  # Operação começa em 1
                        'Início': start_time,
                        'Fim': fim_operacao,
                        'Empilhadeira': empilhadeira
                    })

    df_ops = pd.DataFrame(operacoes)
    
    # Criar tarefas baseadas em pares de operações consecutivas
    tarefas = []
    num_tarefas = int(df_ops['Operação'].max() // 2)
    for tarefa_num in range(1, num_tarefas + 1):
        tarefa_operacoes = df_ops[(df_ops['Operação'] == 2 * tarefa_num - 1) | 
                                  (df_ops['Operação'] == 2 * tarefa_num)]
        tarefa_operacoes = tarefa_operacoes.sort_values(by='Início')
        
        # Adicionar as operações para a tarefa
        for _, row in tarefa_operacoes.iterrows():
            tarefas.append({
                'Tarefa': f'Tarefa {tarefa_num}',
                'Operação': f'{row["Operação"]:.0f}',
                'Início': row['Início'],
                'Fim': row['Fim'],
                'Caminhão': row['Caminhão'],
                'Empilhadeira': row['Empilhadeira']
            })

    df_tarefas = pd.DataFrame(tarefas)

    # Definir as cores para os caminhões em tons de cinza
    num_caminhoes = len(df_tarefas['Caminhão'].unique())
    cmap = plt.get_cmap('Greys')
    cores_caminhoes = {c: cmap(0.3 + 0.5 * i / (num_caminhoes - 1)) for i, c in enumerate(sorted(df_tarefas['Caminhão'].unique()))}

    # Plotar gráfico de Gantt
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for idx, row in df_tarefas.iterrows():
        cor = cores_caminhoes.get(row['Caminhão'], 'gray')
        ax.barh(row['Tarefa'], row['Fim'] - row['Início'], left=row['Início'],
                color=cor, edgecolor='black')
        ax.text(row['Início'] + (row['Fim'] - row['Início']) / 2, row['Tarefa'],
                row['Operação'], va='center', ha='center', color='black', fontsize=9)
    
    # Legenda para os caminhões, ordenada de forma crescente
    handles = [plt.Line2D([0], [0], color=cores_caminhoes[c], lw=6, label=f'Caminhão {c:.0f}') for c in sorted(cores_caminhoes.keys())]
    ax.legend(handles=handles, title='Caminhões', loc='upper right')

    ax.set_xlabel('Tempo')
    plt.tight_layout()
    plt.show()

def grafico_gantt_por_tarefas(alpha, t, p, n_caminhoes: int, n_maquinas: int):
    """
    Gera um gráfico de Gantt com as tarefas no eixo y, onde cada tarefa é formada por pares consecutivos de operações.

    Parâmetros:
    - alpha: Dicionário com as atribuições de operações (matriz para cada caminhão ou empilhadeira).
    - t: Dicionário com os tempos de início de cada operação.
    - p: Lista de tuplas com os tempos de processamento de cada operação (i, k, tempo).
    - n_caminhoes: Número de caminhões.
    - n_maquinas: Número de empilhadeiras.
    """
    # Converter lista de tempos de processamento para dicionário
    tempos_processamento = {(op, emp): tempo for op, emp, tempo in p}

    operacoes = []

    # Verificar se temos mais empilhadeiras ou caminhões e processar de acordo
    if n_maquinas < n_caminhoes:
        # Caso onde há mais empilhadeiras do que caminhões
        for empilhadeira, matriz_alpha in alpha.items():
            for i in range(matriz_alpha.shape[0]):  # Para cada operação
                for k in range(matriz_alpha.shape[1]):  # Para cada caminhão
                    if matriz_alpha[i, k] == 1:  # Considerar apenas as operações atribuídas
                        start_time = t[i + 1]
                        duration = tempos_processamento[(i + 1, empilhadeira)]
                        fim_operacao = start_time + duration
                        operacoes.append({
                            'Caminhão': k + 1,  # Caminhão começa em 1
                            'Operação': i + 1,  # Operação começa em 1
                            'Início': start_time,
                            'Fim': fim_operacao,
                            'Empilhadeira': empilhadeira
                        })
    else:
        # Caso onde há mais caminhões do que empilhadeiras
        for caminhao, matriz_alpha in alpha.items():
            for i in range(matriz_alpha.shape[0]):  # Para cada operação
                for k in range(matriz_alpha.shape[1]):  # Para cada empilhadeira
                    if matriz_alpha[i, k] == 1:  # Considerar apenas as operações atribuídas
                        start_time = t[i + 1]
                        duration = tempos_processamento[(i + 1, caminhao)]
                        fim_operacao = start_time + duration
                        operacoes.append({
                            'Caminhão': caminhao + 1,  # Caminhão começa em 1
                            'Operação': i + 1,  # Operação começa em 1
                            'Início': start_time,
                            'Fim': fim_operacao,
                            'Empilhadeira': k + 1  # Empilhadeira numerada
                        })

    df_ops = pd.DataFrame(operacoes)

    # Criar tarefas baseadas em pares de operações consecutivas
    tarefas = []
    num_tarefas = int(df_ops['Operação'].max() // 2)
    for tarefa_num in range(1, num_tarefas + 1):
        tarefa_operacoes = df_ops[(df_ops['Operação'] == 2 * tarefa_num - 1) | 
                                  (df_ops['Operação'] == 2 * tarefa_num)]
        tarefa_operacoes = tarefa_operacoes.sort_values(by='Início')
        
        # Adicionar as operações para a tarefa
        for _, row in tarefa_operacoes.iterrows():
            tarefas.append({
                'Tarefa': f'Tarefa {tarefa_num}',
                'Operação': f'{row["Operação"]:.0f}',
                'Início': row['Início'],
                'Fim': row['Fim'],
                'Caminhão': row['Caminhão'],
                'Empilhadeira': row['Empilhadeira']
            })

    df_tarefas = pd.DataFrame(tarefas)

    # Definir as cores para os caminhões em tons de cinza
    num_caminhoes = len(df_tarefas['Caminhão'].unique())
    cmap = plt.get_cmap('Greys')
    cores_caminhoes = {c: cmap(0.3 + 0.5 * i / (num_caminhoes - 1)) for i, c in enumerate(sorted(df_tarefas['Caminhão'].unique()))}

    # Plotar gráfico de Gantt
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for idx, row in df_tarefas.iterrows():
        cor = cores_caminhoes.get(row['Caminhão'], 'gray')
        ax.barh(row['Tarefa'], row['Fim'] - row['Início'], left=row['Início'],
                color=cor, edgecolor='black')
        ax.text(row['Início'] + (row['Fim'] - row['Início']) / 2, row['Tarefa'],
                row['Operação'], va='center', ha='center', color='black', fontsize=9)
    
    # Legenda para os caminhões, ordenada de forma crescente
    handles = [plt.Line2D([0], [0], color=cores_caminhoes[c], lw=6, label=f'Caminhão {c:.0f}') for c in sorted(cores_caminhoes.keys())]
    ax.legend(handles=handles, title='Caminhões', loc='upper right')

    ax.set_xlabel('Tempo')
    plt.tight_layout()
    plt.show()


