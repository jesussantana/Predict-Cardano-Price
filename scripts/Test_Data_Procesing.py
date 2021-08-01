import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

import warnings

warnings.filterwarnings("ignore") 

def transform(df_clust):
    # Si es df_mino, hay que eliminar punk_skin
    #df_clust = df_clust.drop('punk_skin',axis=1)
    
    # Codificación de les variables categóricas por frecuencia. Eliminar 'punk_skin' si es df_mino
    dic_cat = {}
    categoriques = ['id_punk', 'punk_type', 'punk_skin', 'rarity', 'date', 'transaction_id']
    for i in categoriques:
        dic_cat[i] = (df_clust.groupby(i).size()) / len(df_clust)
        
    # Reemplaçament de les categories per la freqüència en X_train
    for i in categoriques:
        df_clust[i] = df_clust[i].apply(lambda x : dic_cat[i][x])
     
     ## Escalado de variables numéricas
     
     # Copia
    df_escalado = df_clust.copy()
    
    # Escalado de los datos numéricos: estandarización
    atributos = ['n_traits','amount_ether']
    scaler = StandardScaler()
    df_escalado[atributos] = scaler.fit_transform(df_escalado[atributos].values)
    
    #RobustScaler
    
    # Copia
    df_robusto = df_clust.copy()
    
    # Escalado de los datos numéricos: robust scaler
    atributos = ['n_traits','amount_ether']
    scaler = RobustScaler()
    df_robusto[atributos] = scaler.fit_transform(df_robusto[atributos].values)
    
    return df_escalado, df_robusto