#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 14:26:51 2025

@author: jesus
"""
#%%

import ollama
import pandas as pd
import numpy as np
import pickle
import os

pd.set_option('display.max_columns', None)



path = '/home/jesus/Documentos/analise_funk/ensemble_prompt'


df = pd.read_excel(path+'/gpt4_cot_labes_revisada_final_fp.xlsx',sheet_name='NOVO')


df.columns

#%%



df = df.drop_duplicates(subset=['trecho','topic_num']).reset_index(drop=True)

#%% 


# Dicionário com as descrições originais e labels equivalentes
descricao_topicos = {
    9: 'Este tópico descreve a aparência física, atitudes, comportamentos e ações das mulheres, especialmente em contextos de festas, relacionamentos ou situações cotidianas, frequentemente envolvendo sensualidade, interesse financeiro e atitudes provocativas.',
    3: 'Trechos associados a interações eróticas, desejos explícitos, práticas sexuais ou comportamentos relacionados à sedução e à atração sexual explícita, muitas vezes ambientados em contextos festivos ou íntimos.',
    7: 'Aborda relações entre membros de uma família, como interações com pais, mães ou filhos, desafios e conflitos familiares, declarações de afeto ou arrependimento relacionados à família e ao ambiente doméstico.',
    2: 'Reflete sobre experiências pessoais, dificuldades enfrentadas, sonhos, lutas diárias, perseverança e reflexões sobre crescimento pessoal, aprendizado com a vida e esperança por um futuro melhor.',
    0: 'Enfatiza a aquisição, uso e exibição de bens materiais como carros caros, roupas de marca, joias e dinheiro. Geralmente associado ao estilo de vida de luxo e status social, frequentemente relacionado ao ambiente do funk.',
    11: 'Explora o cotidiano, as dificuldades, a realidade social e comunitária das favelas, expressando orgulho, solidariedade entre moradores, desafios da pobreza, violência, mas também a força e união da comunidade.',
    4: 'Trechos relacionados especificamente ao contexto dos bailes funk, envolvendo dança, música, ambiente festivo, atitudes provocativas e interação entre as pessoas em festas características da cultura funk.',
    6: 'Descreve situações envolvendo atividades criminosas, violência explícita, conflito com a lei, roubos, uso de armas e contextos de violência urbana.',
    5: 'Foca na produção, tráfico, comercialização e consumo explícito de drogas, álcool e substâncias ilícitas ou legais em contextos de lazer ou crime.',
    1: 'Aborda interações emocionais e sentimentais, amor romântico, relações íntimas, declarações de afeto, conflitos amorosos, fidelidade ou infidelidade e dinâmica entre casais.',
    12: 'Trechos que expressam sentimentos profundos de culpa, arrependimento, pedidos de perdão e reflexão sobre erros cometidos no passado, frequentemente associados a consequências pessoais ou familiares negativas.'
}

# base_topics = pd.read_excel('/home/jesus/Documentos/analise_funk/info_topics.xlsx')
# topics = base_topics.drop(0)
# topics = topics.drop(index=[9,11]).head(14)

#%%

import re

def remove_non_numeric(text):
    return int(re.sub(r'\D', '', text))  # Substitui todos os caracteres não numéricos

# Exemplo de uso
string = "Exemplo: 123-abc!45"
result = remove_non_numeric(string)
print(result)  # Saída será '12345'


df['trecho'].nunique()

#%%


list_models = ['model1','model2','model3','model4'] #0.2, 0.5 0.7 and 1 temp

repete = range(1,11)

all_results = []

for model in list_models:
 for trecho in df['trecho'].unique():
     print(trecho)
     for num_topico, descricao in descricao_topicos.items():
            prompt = [
                {"role": "system", "content": """Você é um analista de tópicos dentro de textos de música.
                
                Considere a seguinte escala para realizar a comparação entre um tópico e um trecho:
                
                1: Não há nenhuma relação semântica entre o trecho e o tópico.
                2: A relação semântica é fraca entre o trecho e o tópico. Existe uma conexão mínima ou superficial entre o trecho e os temas discutidos no tópico, mas essa conexão não é particularmente evidente ou relevante.
                3: A relação semântica é moderada entre o trecho e o tópico. O trecho compartilha algumas semelhanças ou temas gerais com o tópico, indicando uma conexão discernível, mas não muito substancial.
                4: A relação semântica é forte entre o trecho e o tópico. O trecho está relacionado de forma significativa aos temas discutidos no tópico.
                5: A relação semântica é muito forte entre o trecho e o tópico. O trecho está altamente alinhado com os temas e conceitos discutidos no tópico.
                
                responda exclusivamente um número entre 1 e 5"""},
                {"role": "user", "content": f"Considere o tópico ({num_topico}): {descricao}\n\nTrecho: \"{trecho}\""}
            ]

            aux_mean = 0
            dic_score = {1:0,2:0,3:0,4:0,5:0}
#-----------                                    
            for rep in repete:     
                 
                response = ollama.chat(model=model, messages=prompt,options={'num_predict':1000 })
           
                try:
                    r1 = remove_non_numeric(response['message']['content'])
                except:
                    r1 = 1
                if r1 not in [1,2,3,4,5]:
                    r1 = 1
                
                aux_mean = (r1 + aux_mean*(rep-1))/rep
                dic_score[r1] += 1
                print(aux_mean)
        
#-----------        
            result = {}
            result['trecho'] = trecho
            result['num_topico'] = num_topico
            result['mean_score'] = aux_mean
            result['descricao'] = descricao
            result['model'] = model
            result['count_5'] = dic_score[5]
            result['count_4'] = dic_score[4]
            result['count_3'] = dic_score[3]
            result['count_2'] = dic_score[2]    
            result['count_1'] = dic_score[1]
        
            all_results.append(result)
          
            # Save the list to a file
            with open(path+'/new_prompt_zero_shots_anota.pkl', 'wb') as file:
                pickle.dump(all_results, file)