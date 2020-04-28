import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

nomes = ['01','05','08','12','15','19','22','26','29']
path = r'csv_radares-20200426T211130Z-001_selecionados\\'

#para cada um dos arquivos
for name in nomes:
    #leio
    df_new = pd.read_csv(path + name + "_selecionado" + ".csv")
    df_new.Data=pd.to_datetime(df_new.Data)
    
    df_new_s = df_new[(df_new.Data.dt.hour >=7) & (df_new.Data.dt.hour <9)]
    df_new_s.reset_index(drop=True,inplace=True)
    df_new_s.Data.dt.time
    
    #dropa vazios
    df_new_s.drop(df_new_s[df_new_s.Velocidade =='   '].index, inplace=True) 
    #dropa não válidos (nan)
    df_new_s.Velocidade.dropna(inplace=True) 
    #coloca tudo no mesmo formato de dado int
    df_new_s.Velocidade = pd.to_numeric(df_new_s.Velocidade)
    
    ### velocidades vem em int64
    #criando copias da coluna de interesse pq
    #quando se faz um agrupamento, ela se perde
    df_new_s['V1'] = df_new_s['Velocidade'].copy()    
    df_new_s['V2'] = df_new_s['Velocidade'].copy()
    

    df_group = df_new_s.groupby([pd.Grouper(key='Data', freq='4Min')]).agg({'Velocidade': 'mean',
                                                                        'V1':'median',
                                                                        'V2':'std',
                                                                        'Registro':'count'})
    # Renomeia
    df_group.columns=['Vel_media',
                  'Vel_mediana',
                  'Vel_std',
                  'Volume'] 
    display(df_group)
    df_group.to_csv(name + "_filha"+".csv")