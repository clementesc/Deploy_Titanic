# Deploy_Titanic

## Passos para a criação e execução deste projeto

### Criar um ambiente virtual

```commandline
python -m venv venv
```

### Ativar o ambiente virtual

#### a. Linux ou OSX
```commandline
source venv/bin/activate
```

#### b. Windows 10 ou 11
```commandline
.\venv\Scripts\Activate.ps1
```

### Instalar os pacotes requeridos
Em tese a instalação os pacotes streamlit, matplotlib e scikit-learn são o suficiente.
Outra opção seria a instalação dos pacotes nas versões utilizadas no desenvolvimento deste projeto.

#### a. Instalação dos pacotes individualmente
```commandline
pip install streamlit matplotlib xgboost fastapi uvicorn
```

#### b. Instalação/atualização de todos os pacotes 
```commandline
pip install -r requirements.txt
```

### Criar arquivo para autenticação
Criar .streamlit/secrets.toml
Incluir no secrets.toml a seguinte linha
```commandline
password = "streamlit1234"
```

### Iniciar uvicorn (API)
```commandline
uvicorn main:api --reload
```

### Executar o App
```commandline
streamlit run app.py
```