import os
import sys
module_path = os.path.abspath(os.path.join(os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)
import pandas as pd
import numpy as np
import pickle
from utils.exploratory_data_utils import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class DataProcessor:
    def __init__(self, df: pd.DataFrame, model_path: str):
        self.df = df.copy()
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)
    
    def drop_columns(self, columns: list = ['id', 'nome', 'host_name', 'ultima_review','bairro']):
        self.df.drop(columns=columns, inplace=True)
        return self.df
    
    def fillna(self, columns: list = ['reviews_por_mes'], value: int = 0):
        self.df[columns] = self.df[columns].fillna(value)
        return self.df
    
    def dropna_and_duplicated(self):
        self.df.dropna()
        self.df.drop_duplicates()
        return self.df
    
    # def get_bairro_mean_prices(self, bairro: list):
    #     self.df = get_bairro_mean_price(self.df,bairro)
    #     self.df.drop(columns=['bairro'], inplace=True)
    #     return self.df
    
    def one_hot_encoding(self, columns: list):
        self.df = pd.get_dummies(self.df, columns=columns, prefix=columns)
        return self.df
    
    def prepare_data_to_model(self, bairro_group: list = ['bairro_group'], room_type: list = ['room_type']):
        self.drop_columns()
        self.fillna()
        # self.get_bairro_mean_prices(['bairro'])  # Calcula a média de preços por bairro
        self.dropna_and_duplicated()
        self.one_hot_encoding(bairro_group)
        self.one_hot_encoding(room_type)
        
        # Lista das colunas esperadas pelo modelo
        colunas_esperadas = [
            "latitude", "longitude", "minimo_noites", "numero_de_reviews", 
            "reviews_por_mes", "calculado_host_listings_count", "disponibilidade_365", 
            "bairro_group_Manhattan", "room_type_Entire home/apt", "bairro_group_Queens", 
            "bairro_group_Bronx", "bairro_group_Brooklyn", "bairro_group_Staten Island",
            "room_type_Private room", "room_type_Shared room", "media_bairro", "host_id"
        ]
        
        # Garantir que todas as colunas esperadas estejam presentes no DataFrame
        for coluna in colunas_esperadas:
            if coluna not in self.df.columns:
                self.df[coluna] = 0  # Adiciona a coluna com valor 0 se estiver ausente
        
        # Garantir que as colunas estejam na mesma ordem do que o modelo espera
        self.df = self.df[colunas_esperadas]
        
        return self.df

    
    def test_model(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return y_pred, accuracy
    
    
dados_teste = pd.DataFrame([{
    'id': 2595,
    'nome': 'Skylit Midtown Castle',
    'host_id': 2845,
    'host_name': 'Jennifer',
    'bairro_group': 'Manhattan',
    'bairro': 'Midtown',
    'latitude': 40.75362,
    'longitude': -73.98377,
    'room_type': 'Entire home/apt',
    'minimo_noites': 1,
    'numero_de_reviews': 45,
    'ultima_review': '2019-05-21',
    'reviews_por_mes': 0.38,
    'calculado_host_listings_count': 2,
    'disponibilidade_365': 355
}])

processor = DataProcessor(dados_teste, "../../src/models/xg_reg_model.pkl")

dados_processados = processor.prepare_data_to_model()

colunas_treinamento = ["latitude", "longitude", "minimo_noites", "numero_de_reviews", 
                       "reviews_por_mes", "calculado_host_listings_count", "disponibilidade_365", 
                       "bairro_group_Manhattan", "room_type_Entire home/apt"]

for coluna in colunas_treinamento:
    if coluna not in dados_processados.columns:
        dados_processados[coluna] = 0

X_teste = dados_processados[colunas_treinamento]

y_pred = processor.model.predict(X_teste)

print("Previsão do modelo:", y_pred[0])