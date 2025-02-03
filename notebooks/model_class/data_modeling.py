import os
import sys
import json
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
    
    def drop_columns(self, columns: list = ['id', 'nome', 'host_name', 'ultima_review']):
        self.df.drop(columns=columns, inplace=True)
        return self.df
    
    def fillna(self, columns: list = ['reviews_por_mes'], value: int = 0):
        self.df[columns] = self.df[columns].fillna(value)
        return self.df
    
    def dropna_and_duplicated(self):
        self.df.dropna(inplace=True)
        self.df.drop_duplicates(inplace=True)
        return self.df
    
    def get_bairro_mean_prices(self):
        mean_price_df = pd.read_csv('../../src/data/silver/media_preco_bairros.csv')
        bairro_mean_price_map = dict(zip(mean_price_df['bairro'], mean_price_df['media_bairro']))
        self.df['media_bairro'] = self.df['bairro'].map(bairro_mean_price_map)
        self.df.drop(columns=['bairro'], inplace=True)
        return self.df
    
    def one_hot_encoding(self, columns: list):
        self.df = pd.get_dummies(self.df, columns=columns, prefix=columns)
        return self.df
    
    def prepare_data_to_model(self, bairro_group: list = ['bairro_group'], room_type: list = ['room_type']):
        self.drop_columns()
        self.fillna()
        self.get_bairro_mean_prices()
        self.dropna_and_duplicated()
        self.one_hot_encoding(bairro_group + room_type)  
        
        colunas_esperadas = [
            "host_id", 
            "latitude", 
            "longitude", 
            "minimo_noites", 
            "numero_de_reviews", 
            "reviews_por_mes", 
            "calculado_host_listings_count", 
            "disponibilidade_365", 
            "media_bairro", 
            "bairro_group_Bronx", 
            "bairro_group_Brooklyn", 
            "bairro_group_Manhattan", 
            "bairro_group_Queens", 
            "bairro_group_Staten Island", 
            "room_type_Entire home/apt",
            "room_type_Hotel room", 
            "room_type_Private room", 
            "room_type_Shared room",
            
        ]
        
        # Garantir colunas faltantes (preencher com 0)
        for coluna in colunas_esperadas:
            if coluna not in self.df.columns:
                self.df[coluna] = 0
        
        # Reordenar colunas exatamente como o modelo espera
        self.df = self.df[colunas_esperadas]
        
        return self.df

    def test_model(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return y_pred, accuracy

with open('../../src/data/testing_data/test.json', 'r', encoding='utf-8') as file:
    data_teste = pd.DataFrame([json.load(file)])
processor = DataProcessor(data_teste, "../../src/models/random_forest_model.pkl")

dados_processados = processor.prepare_data_to_model()
X_teste = dados_processados.copy()

y_pred = processor.model.predict(X_teste)
print("Previsão do modelo (revertida):", np.expm1(y_pred[0]))

