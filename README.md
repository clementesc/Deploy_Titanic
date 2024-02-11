# Deploy_Titanic

## Passos para a criação e execução deste projeto

### Criar um ambiente virtual

```commandline
python -m venv venv
```

### Ativar o ambiente virtual

#### Linux ou OSX
```commandline
source venv/bin/activate
```

#### Windows 10
```commandline
.\venv\Scripts\Activate.ps1
```

### Instalar o Streamlit
```commandline
pip install streamlit
```

### Instalar o Matplotlib
```commandline
pip install matplotlib
```
### Instalar o XGBoost Classifier
```commandline
pip install xgboost 
```

### Criar arquivo para autenticação
Criar .streamlit/secrets.toml
Incluir no secrets.toml a seguinte linha
```commandline
password = "streamlit1234"
```

### Executar o App
```commandline
streamlit run app.py
```