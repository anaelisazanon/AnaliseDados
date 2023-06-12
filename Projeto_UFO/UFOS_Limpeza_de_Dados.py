import pandas as pd

# Ler o arquivo UFO.csv e relacioná-lo ao dataframe 'df'
df = pd.read_csv(r'C:\Users\Usuário\Desktop\ideais\arquivos\UFO_Original.csv')

# Definir os valores específicos para cada coluna, com base em uma análise da banco de dados
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['city'] = df['city'].str.capitalize()
df['state'].fillna('Unknown', inplace=True)
df['country'] = df['country'].str.upper()
df['shape'] = df['shape'].str.strip().str.capitalize()
df['duration (seconds)'] = pd.to_numeric(df['duration (seconds)'], errors='coerce')
df['comments'].fillna('No comments', inplace=True)
df['date posted'] = pd.to_datetime(df['date posted'], format='%m/%d/%Y', errors='coerce')
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude '] = pd.to_numeric(df['longitude '], errors='coerce')

# Devido ao grande volume de dados e inconsistência que não sejam no território dos EUA, foi necessário filtrar apenas para tal
df = df[df['country'] == 'US'].copy()

# Ao calcular a média com relação à duração, foi visto uma variação gigantesca com relação aos 5% dos maiores valores, representando um aumento de mais de 1500%, então foram retirados tais dados para obter uma média mais confiável
cutoff = df['duration (seconds)'].quantile(0.95)

# Definir a coluna apenas com os valores sem os 5% maiores
df = df[df['duration (seconds)'] <= cutoff]

# Converte a coluna duration seconds para int, pois o powerbi detecta o .0 (float) como um zero adicional, então é enviado como int
df['duration (seconds)'] = df['duration (seconds)'].astype(int)

# Definir o formato da coluna datetime para ano mês dia - hora minuto segundo, isso se viu necessário para um reconhecimento melhor para a próxima ação
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')

# Necessário definir o formato dos horários para ter menor chance de erros na hora de separar as colunas datetime em data e tempo, para obter analises de tempo e data separadas
df['data'] = df['datetime'].dt.date
df['hora'] = df['datetime'].dt.time

# Criar uma coluna com o dia da semana a partir da coluna datetime
df['dia_da_semana'] = df['datetime'].dt.strftime('%A')

# Criar outro arquivo com todas as informações atualizadas
df.to_csv(r'C:\Users\Usuário\Desktop\ideais\arquivos\UFO_Modificado.csv', index=False)

