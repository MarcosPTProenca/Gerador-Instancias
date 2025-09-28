from layout import pipeline_gerar_layout_e_caminhos_processamento
from prints import pipeline_gerar_prints_parametros
from parametros_basicos import pipeline_gerar_todas_tarefas_e_operacoes
from parametros_avancados import pipeline_parametros_avancados

def main(num_estoques, 
         n_tarefas_estoque,
         n_tarefas_docas,
         num_docas, 
         picking_width_units, 
         n_caminhoes, 
         mesmo_ponto_picking, 
         n_maquinas,  
         n_operacoes_por_tarefa, 
         proporcao_maquinas, 
         proporcao_areas,
         proporcao_rapidas,
         deterministico,
         vel_min_emp_rapida, 
         vel_max_emp_rapida, 
         vel_min_emp_lenta, 
         vel_max_emp_lenta, 
         t_min_block, 
         t_max_block, 
         t_min_setup, 
         t_max_setup, 
         todos_caminhoes_atrasados, 
         todos_caminhoes_adiantados,
         pasta = '../data/instancias/',
         grid_spacing = 5):

     parametros_basicos = pipeline_gerar_todas_tarefas_e_operacoes(num_estoques,
                                                                   n_tarefas_estoque,
                                                                   n_tarefas_docas,
                                                                   n_caminhoes, 
                                                                   n_operacoes_por_tarefa)     
     
     
     coordenadas_por_area, area_indices, coordenadas_detalhadas = pipeline_gerar_layout_e_caminhos_processamento(num_estoques, 
                                                                           parametros_basicos['operacoes_por_area_final'], 
                                                                           num_docas, 
                                                                           picking_width_units, 
                                                                           n_caminhoes, 
                                                                           parametros_basicos['operacoes_por_caminhao'], 
                                                                           mesmo_ponto_picking, 
                                                                           grid_spacing)

     elegibilidade, datas_entrega, tempos_setup, tempos_bloqueios, tempos_processamento = pipeline_parametros_avancados(n_maquinas, 
                                                                                                  parametros_basicos['operacoes_por_area_final'], 
                                                                                                  parametros_basicos['operacoes_por_caminhao'], 
                                                                                                  proporcao_maquinas, 
                                                                                                  proporcao_rapidas, 
                                                                                                  proporcao_areas, 
                                                                                                  coordenadas_por_area, 
                                                                                                  deterministico, 
                                                                                                  vel_min_emp_rapida, 
                                                                                                  vel_max_emp_rapida, 
                                                                                                  vel_min_emp_lenta, 
                                                                                                  vel_max_emp_lenta, 
                                                                                                  t_min_block, 
                                                                                                  t_max_block, 
                                                                                                  t_min_setup, 
                                                                                                  t_max_setup, 
                                                                                                  todos_caminhoes_atrasados, 
                                                                                                  todos_caminhoes_adiantados)

     pipeline_gerar_prints_parametros(n_maquinas,
                                      n_tarefas_docas,
                                      n_tarefas_estoque,
                                      parametros_basicos, 
                                      elegibilidade, 
                                      tempos_processamento, 
                                      datas_entrega, 
                                      n_operacoes_por_tarefa, 
                                      tempos_bloqueios, 
                                      n_caminhoes, 
                                      tempos_setup,
                                      todos_caminhoes_atrasados,
                                      todos_caminhoes_adiantados, 
                                      pasta)
     
     return area_indices, coordenadas_detalhadas, elegibilidade