import pandas as pd
from sqlalchemy import create_engine
import os

# Caminho completo do arquivo CSV
file_path = 'C:/Users/MATHEUS/Desktop/Portifolio_IOT/IOT_Temp.csv'

# Verificar se o arquivo existe e pode ser lido
if os.path.exists(file_path):
    print(f'O arquivo {file_path} foi encontrado.')
else:
    print(f'O arquivo {file_path} NÃO foi encontrado.')

if os.access(file_path, os.R_OK):
    print('O arquivo pode ser lido!')
    try:
        # Carregar o CSV
        df = pd.read_csv(file_path)
        print('Dados carregados com sucesso:')
        print(df.head())  # Exibir as primeiras linhas dos dados

        # Configuração do banco de dados
        db_url = 'postgresql://postgres:sua_senha@localhost:5432/database'  # Substitua 'sua_senha' e 'database'
        
        # Conexão com o banco de dados PostgreSQL
        engine = create_engine(db_url)

        # Inserir dados no banco de dados
        df.to_sql('temperature_readings', con=engine, if_exists='replace', index=False)
        print('Dados inseridos com sucesso no banco de dados!')

        # Criar views SQL
        with engine.connect() as connection:
            # Criando a view 'avg_temp_por_dispositivo'
            connection.execute("""
            CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
            SELECT device_id, AVG(temperature) AS avg_temp
            FROM temperature_readings
            GROUP BY device_id;
            """)

            # Criando a view 'leituras_por_hora'
            connection.execute("""
            CREATE OR REPLACE VIEW leituras_por_hora AS
            SELECT EXTRACT(HOUR FROM timestamp) AS hora, COUNT(*) AS contagem
            FROM temperature_readings
            GROUP BY hora;
            """)

            # Criando a view 'temp_max_min_por_dia'
            connection.execute("""
            CREATE OR REPLACE VIEW temp_max_min_por_dia AS
            SELECT DATE(timestamp) AS data, 
                   MAX(temperature) AS temp_max, 
                   MIN(temperature) AS temp_min
            FROM temperature_readings
            GROUP BY data;
            """)

        print("Views criadas com sucesso no banco de dados!")

    except Exception as e:
        print(f'Ocorreu um erro ao ler o arquivo ou inserir no banco: {e}')
else:
    print('O arquivo NÃO pode ser lido!')
