from collections import defaultdict
import numpy as np
import re

def parse_mac(lines):
    for line in lines:
        if line.startswith('MAC ='):
            return int(line.split('=')[1].strip())
    return None

def parse_alpha_caminhao(lines):
    """
    Função para parsing de dados de alpha para caminhões no formato [*,num,*] 
    que lidam com quebras de páginas.
    """
    alpha = defaultdict(dict)  # {truck_number: numpy_array}
    collecting = False  # Flag para indicar quando estamos coletando dados
    truck_number = None  # Número do caminhão atual
    current_truck_data = []  # Dados temporários para um caminhão
    additional_columns = []  # Colunas adicionais para concatenar

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Início da primeira ou subsequente seção alpha para um caminhão específico
        if re.match(r'alpha \[\*,\d+,\*\]', line) or re.match(r'\[\*,\d+,\*\]', line):
            # Finaliza o bloco anterior, se houver, e inicia um novo
            if collecting and current_truck_data:
                if additional_columns:
                    # Adiciona as colunas adicionais ao final do bloco atual
                    current_truck_data = [row + add_row for row, add_row in zip(current_truck_data, additional_columns)]
                    additional_columns = []
                
                alpha[truck_number] = np.array(current_truck_data)
                current_truck_data = []  # Reinicializa os dados para o próximo caminhão
            
            # Extrair o número do caminhão
            truck_number = int(re.search(r'\d+', line).group())
            collecting = True  # Começar a coletar dados
            i += 2  # Pular a linha de cabeçalho e ir para a primeira linha de dados
            continue

        # Coletar os dados enquanto não encontrar o delimitador ';'
        if collecting:
            if line.startswith(';'):  # Fim da seção alpha
                if additional_columns:
                    # Adiciona colunas adicionais ao bloco atual antes de finalizar
                    current_truck_data = [row + add_row for row, add_row in zip(current_truck_data, additional_columns)]
                    additional_columns = []
                
                alpha[truck_number] = np.array(current_truck_data)  # Armazena os dados finais do caminhão
                collecting = False
                current_truck_data = []  # Limpa os dados temporários
            else:
                parts = line.split()
                # Verifica se a linha tem dados válidos para o alpha
                if len(parts) > 1 and all(x.isdigit() for x in parts):
                    row_data = [int(x) for x in parts[1:]]  # Coleta a linha de dados e ignora a primeira coluna
                    if len(current_truck_data) < len(row_data):
                        current_truck_data.append(row_data)
                    else:
                        additional_columns.append(row_data)
            i += 1
        else:
            i += 1

    # Finaliza o último bloco, caso ele termine sem um delimitador ';'
    if collecting and current_truck_data:
        if additional_columns:
            current_truck_data = [row + add_row for row, add_row in zip(current_truck_data, additional_columns)]
        alpha[truck_number] = np.array(current_truck_data)

    return alpha

def parse_alpha_empilhadeira(lines):
    """
    Função para parsing de dados de alpha para empilhadeiras no formato [*,*,num] 
    que lida com quebras de páginas.
    """
    alpha = defaultdict(dict)  # {forklift_number: numpy_array}
    collecting = False  # Flag para indicar quando estamos coletando dados
    forklift_number = None  # Número da empilhadeira atual
    current_forklift_data = []  # Dados temporários para uma empilhadeira
    additional_columns = []  # Colunas adicionais para concatenar

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Início da primeira ou subsequente seção alpha para uma empilhadeira específica
        if re.match(r'alpha \[\*,\*,\d+\]', line) or re.match(r'\[\*,\*,\d+\]', line):
            # Finaliza o bloco anterior, se houver, e inicia um novo
            if collecting and current_forklift_data:
                if additional_columns:
                    # Adiciona colunas adicionais ao final do bloco atual
                    current_forklift_data = [row + add_row for row, add_row in zip(current_forklift_data, additional_columns)]
                    additional_columns = []
                
                alpha[forklift_number] = np.array(current_forklift_data).T  # Transpõe para colunas de caminhões
                current_forklift_data = []  # Reinicializa os dados para a próxima empilhadeira
            
            # Extrair o número da empilhadeira
            forklift_number = int(re.search(r'\d+', line).group())
            collecting = True  # Começar a coletar dados
            i += 2  # Pular a linha de cabeçalho e ir para a primeira linha de dados
            continue

        # Coletar os dados enquanto não encontrar o delimitador ';'
        if collecting:
            if line.startswith(';'):  # Fim da seção alpha
                if additional_columns:
                    # Adiciona colunas adicionais ao bloco atual antes de finalizar
                    current_forklift_data = [row + add_row for row, add_row in zip(current_forklift_data, additional_columns)]
                    additional_columns = []
                
                alpha[forklift_number] = np.array(current_forklift_data).T  # Transpõe para colunas de caminhões
                collecting = False
                current_forklift_data = []  # Limpa os dados temporários
            else:
                parts = line.split()
                # Verifica se a linha tem dados válidos para o alpha
                if len(parts) > 1 and all(x.isdigit() for x in parts):
                    row_data = [int(x) for x in parts[1:]]  # Coletar a linha de dados e ignorar a primeira coluna
                    if len(current_forklift_data) < len(row_data):
                        current_forklift_data.append(row_data)
                    else:
                        additional_columns.append(row_data)
            i += 1
        else:
            i += 1

    # Finaliza o último bloco, caso ele termine sem um delimitador ';'
    if collecting and current_forklift_data:
        if additional_columns:
            current_forklift_data = [row + add_row for row, add_row in zip(current_forklift_data, additional_columns)]
        alpha[forklift_number] = np.array(current_forklift_data).T

    return alpha

def parse_t_and_A(lines):
    t = {}
    A = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith(':') and 't' in line and 'A' in line:
            i += 1
            while i < len(lines):
                line = lines[i].strip()
                if line == ';' or line == '':
                    break
                parts = line.split()
                if len(parts) >= 3:
                    op_num = int(parts[0])
                    t_value = float(parts[1])
                    A_value = parts[2]
                    t[op_num] = t_value
                    if A_value != '.':
                        A[op_num] = float(A_value)
                i += 1
        i += 1
    return t, A

def parse_processing_time(lines):
    p = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('p [*,*]'):
            i += 1
            while i < len(lines):
                line = lines[i].strip()
                if line == ';' or line == '':  # Encerramento da seção de p
                    break
                if line.startswith(':') or line.startswith(':='):
                    # Ignorar linhas de cabeçalho que começam com ':' ou ':='
                    i += 1
                    continue
                
                parts = line.split()
                
                if len(parts) > 1:  # Certifica-se de que há pelo menos 1 valor de operação
                    try:
                        op_num = int(parts[0])  # Primeira coluna é o número da operação
                    except ValueError:
                        i += 1
                        continue  # Pula a linha se a conversão falhar

                    for j, time_value in enumerate(parts[1:], start=1):  # Itera sobre os tempos
                        if time_value != '.':  # Ignora valores faltantes
                            p.append((op_num, j, float(time_value)))
                i += 1
        else:
            i += 1
    return p

def parse_d(lines):
    d = {}
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('d [*] :='):
            i += 1  # Move to the next line (data lines)
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith(';') or line == '':
                    break
                parts = line.split()
                if len(parts) == 2:
                    truck_num = int(parts[0])
                    departure_time = float(parts[1])
                    d[truck_num] = departure_time
                i += 1
        i += 1
    return d

def parse_lines(filename):
    with open(filename, 'r') as file:
        lines = [line.rstrip('\n') for line in file]
    
    return lines

def parse_log_file(filename):
    with open(filename, 'r') as file:
        lines = [line.rstrip('\n') for line in file]
    
    # Chamar as funções independentes para ler cada parâmetro
    mac = parse_mac(lines)
    alpha = parse_alpha_caminhao(lines)
    if not alpha:  # ou if len(alpha) == 0:
        alpha = parse_alpha_empilhadeira(lines)
    t, A = parse_t_and_A(lines)
    processing_times = parse_processing_time(lines)
    departure_times = parse_d(lines)  # Chamar a nova função para o parâmetro 'd'
    
    return {
        'MAC': mac,
        'alpha': alpha,
        't': t,
        'A': A,
        'p': processing_times,
        'd': departure_times
    }


