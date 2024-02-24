
#spell-checker: disable

import streamlit as st
import data_handler
import util
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import requests
import json

# Validação com senha
#if not util.check_password():
#    st.stop()

API_URL = 'http://127.0.0.1:8000'

st.set_page_config(page_title="App dos dados do Titanic")

st.title('App dos dados do Titanic')

data_analyses_on = st.toggle("Exibir análise de dados")

if data_analyses_on:

    st.header("Dataframe")
    #dados = data_handler.load_data()
    response = requests.get(API_URL + "/get-titanic-data")
    if response.status_code == 200:
        dados_json = json.loads(response.json())
        dados = pd.DataFrame(dados_json)
        
    if dados.empty == False:
        st.dataframe(dados)

        # plota um histograma das idades dos passageiros
        st.header('Histograma das idades')
        fig = plt.figure()
        plt.hist(dados['Age'], bins=30)
        plt.xlabel('Idade')
        plt.ylabel('Quantidade')
        st.pyplot(fig)
    else:
        st.write('Não foi possivel carregar o dataframe')
    
    # plota um gráfico de barras com a contagem dos sobreviventes
    st.header('Sobreviventes')
    st.bar_chart(dados.Survived.value_counts())


st.header('Preditor de sobrevivência')

# ler as seguintes informações de input:
# Pclass - int
# Sex - 'male' or 'female'
# Age - int
# SibSp - int
# Parch - int
# Fare - float
# Embarked - C = Cherbourg, Q = Queenstown, S = Southampton

# linha 1 do form
col1, col2, col3 = st.columns(3)

# captura a p_class do passageiro, com base na lista de classes disponibilizadas 
with col1:
    # pclass: A proxy for socio-economic status (SES)
    # 1st = Upper
    # 2nd = Middle
    # 3rd = Lower
    classes = ['1st', '2nd', '3rd']
    p_class = st.selectbox('Ticket class', classes)

# captura o sex do passageiro, com base na lista de classes disponibilizadas
with col2:
    classes = ['Male', 'Female']
    sex = st.selectbox('Sex', classes)
    
# captura a idade do passageiro, como o step é 1, ele considera a idade como inteira
with col3:
    # age: Age is fractional if less than 1. If the age is estimated, is it in the form of xx.5
    age = st.number_input('Age in years', step=1, max_value=100)

# linha 2 do form
col1, col2, col3 = st.columns([2,2,1])

# captura o número de irmãos e esposa(o)
with col1:
    # sibsp: The dataset defines family relations in this way...
    # Sibling = brother, sister, stepbrother, stepsister
    # Spouse = husband, wife (mistresses and fiancés were ignored)
    sib_sp = st.number_input('Number of siblings / spouses aboard the Titanic', step=1)

# captura o número de pais e filhos
with col2:
    # parch: The dataset defines family relations in this way...
    # Parent = mother, father
    # Child = daughter, son, stepdaughter, stepson
    # Some children travelled only with a nanny, therefore parch=0 for them.
    par_ch = st.number_input('Number of parents / children aboard the Titanic', step=1)

# captura o valor pago pela passagem, agora em float
with col3:
    fare = st.number_input('Passenger fare')

# linha 3 do form
col1, col2 = st.columns([1,3])

# captura o porto de embarque do passageiro, com base na lista de classes disponibilizadas
with col1:
    classes = ['Cherbourg', 'Queenstown', 'Southampton']
    embarked = st.selectbox('Port of Embarkation', classes)
    
# define o botão de verificar, que deverá ser pressionado para o sistema realizar a predição
submit = st.button('Verificar')

if submit or 'survived' in st.session_state:
    # data mapping
    # essa parte do código realiza o mapeamento dos campos p_class, sex e embarked para valores numéricos
    # o mesmo procedimento foi realizado durante o treinamento do modelo
    # assim, isso também deve ser feito aqui para haver compatibilidade nos dados
    

    passageiro = {
        'Pclass': p_class,
        'Sex': sex,
        'Age': age,
        'SibSp': sib_sp,
        'Parch': par_ch,
        'Fare': fare,
        'Embarked': embarked
    }
    
    # carrega o modelo de predição já treinado e validado
    #model = pickle.load(open('./models/model.pkl', 'rb'))

    #values = pd.DataFrame([passageiro])
    #result = model.predict(values)

    passageiro_json = json.dumps(passageiro)

    response = requests.post(API_URL + "/predict", json=passageiro_json)
    result = None

    if response.status_code == 200:
        result = response.json()
    else:
        print('Erro no request do predict')

    if result is not None:
        survived = result

         # verifica se o passageiro sobreviveu
        if survived == 1:
            # se sim, exibe uma mensagem que o passageiro sobreviveu
            st.subheader('Passageiro SOBREVIVEU! 😃🙌🏻')
        else:
            # se não, exibe uma mensagem que o passageiro não sobreviveu
            st.subheader('Passageiro NÃO sobreviveu! 😢')
        
        st.session_state['survived'] = survived

    # verifica se existe um passageiro e se já foi verificado se ele sobreviveu ou não
    if passageiro and 'survived' in st.session_state:
        # se sim, pergunta ao usuário se a predição está certa e salva essa informação
        st.write("A predição está correta?")
        col1, col2, col3 = st.columns([1,1,5])
        with col1:
            correct_prediction = st.button('👍🏻')
        with col2:
            wrong_prediction = st.button('👎🏻')
        
        # exibe uma mensagem para o usuário agradecendo o feedback
        if correct_prediction or wrong_prediction:
            message = "Muito obrigado pelo feedback"
            if wrong_prediction:
                message += ", iremos usar esses dados para melhorar as predições"
            message += "."
            
            # adiciona no dict do passageiro se a predição está correta ou não
            if correct_prediction:
                passageiro['CorrectPrediction'] = True
            elif wrong_prediction:
                passageiro['CorrectPrediction'] = False
                
            # adiciona no dict do passageiro se ele sobreviveu ou não
            passageiro['Survived'] = st.session_state['survived']
            
            # escreve a mensagem na tela
            st.write(message)
            print(message)

            # salva a predição no JSON para cálculo das métricas de avaliação do sistema
            #data_handler.save_prediction(passageiro)
            passageiro_json = json.dumps(passageiro)
            response = requests.post (API_URL + "/save-prediction", json=passageiro_json)
            if response.status_code == 200:
                print("Predição salva")
            else:
                print("Erro no request do save_prediction")


    # adiciona um botão para permitir o usuário realizar uma nova análise
    col1, col2, col3 = st.columns(3)
    with col2:
        new_test = st.button('Iniciar Nova Análise')
        
        # se o usuário pressionar no botão e já existe um passageiro, remove ele do cache
        if new_test and 'survived' in st.session_state:
            del st.session_state['survived']
            st.rerun()

# calcula e exibe as métricas de avaliação do modelo
metrics_predictions_on = st.toggle('Exibir métricas')

if metrics_predictions_on:
    # pega todas as predições salvas no JSON
    response = requests.get(API_URL + "/get-all-predictions")
    if response.status_code == 200:
        predictions = response.json()
    else:
        st.write('Não foi possivel carregar o histórico de predições.')

    if len(predictions) > 0:
        r_vp = 0
        r_vn = 0
        r_fp = 0
        r_fn = 0

        # calcula o número de predições corretas e salva os resultados conforme as predições foram sendo realizadas
        accuracy_hist = [0]
    
        # percorre cada uma das predições, salvando o total móvel e o número de predições corretas
        for index, dados in enumerate(predictions):
            if dados['CorrectPrediction'] == True:
                if dados['Survived'] == 1:
                    r_vp += 1
                else:
                    r_vn += 1
            else:
                if dados['Survived'] == 1:
                    r_fp += 1
                else:
                    r_fn += 1
                
            # calcula a acurácia móvel para depois montar o gráfico
            temp_accuracy = (r_vp + r_vn) / (index + 1)
            accuracy_hist.append(round(temp_accuracy, 2))
        
        # calcula a acurácia atual
        accuracy = (r_vp + r_vn) / len(predictions) #if num_total_predictions else 0

        #st.write('vp =' + str(r_vp))
        #st.write('vn =' + str(r_vn))
        #st.write('fp =' + str(r_fp))
        #st.write('fn =' + str(r_fn))

        # calcula a precisão atual
        precision = r_vp / (r_vp + r_fp) if r_vp > 0 or r_fp > 0 else 0

        # calcula o recall
        recall = r_vp / (r_vp + r_fn) if r_vp > 0 or r_fn > 0 else 0

        # calcula o fator f1
        f1_score = 2 * ((precision * recall)/(precision * recall)) if precision > 0 or recall > 0 else 0
        
        
        # TODO: usar o attr delta do st.metric para exibir a diferença na variação da acurácia

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # exibe a Acurácia atual
            st.metric(label='Acurácia (Accuracy)', value=round(accuracy, 2))

        with col2:
            # exibe a Precisão atual
            st.metric(label='Precisão (Precision)', value=round(precision, 2))

        with col3:
            # exibe o Recall atual
            st.metric(label='Revocação (Recall)', value=round(recall, 2))
        
        with col4:
            # exibe o Fator F1 atual
            st.metric(label='Fator F1 (F1-Score)', value=round(f1_score, 2))
        
        # exibe o histórico da acurácia
        st.subheader("Histórico de acurácia")
        st.line_chart(accuracy_hist)

