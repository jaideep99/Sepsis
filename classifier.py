import tensorflow as tf
import numpy as np
import pandas as pd
import random
from sms4india import sendPostRequest

URL = 'https://www.sms4india.com/api/v1/sendCampaign'

unwanted_params = ['EtCO2',
       'BaseExcess', 'HCO3', 'FiO2', 'pH', 'PaCO2', 'SaO2', 'AST', 'BUN',
       'Alkalinephos', 'Calcium', 'Chloride', 'Creatinine', 'Bilirubin_direct',
       'Glucose', 'Lactate', 'Magnesium', 'Phosphate', 'Potassium',
       'Bilirubin_total', 'TroponinI', 'Hct', 'Hgb', 'PTT', 'WBC',
       'Fibrinogen', 'Platelets', 'Unit1', 'Unit2']

prediction = ''
def predict(data):
    
    data.drop(unwanted_params,axis=1,inplace=True)
    data.drop(['SepsisLabel'],axis=1,inplace=True)
    data.dropna(thresh=6,how='all',inplace=True)
    data.fillna(data.median(),inplace=True)
    data.fillna(0,inplace=True)
    req_df = []
    length = len(data)

    if(length>=30):
        req_df = data[length-30:].values
    else:
        temp_df = pd.DataFrame(dict(zip(data.columns,np.zeros((11,30-length),dtype=np.float32))))
        temp_df = pd.concat([temp_df,data],axis=0)
        req_df= temp_df.values

    req_df = np.array([req_df]).reshape(-1,30,11)
    
    model = tf.keras.models.load_model('model.h5')
    pred = model.predict(req_df)

    pred = np.argmax(pred[0])

    rand = random.randint(1,24)
    if pred==1:
        prediction='positive'
        sendPostRequest(URL, 'provided-api-key', 'provided-secret', 'prod/stage', 'valid-to-mobile', 'active-sender-id', 'Sepsis-Positive. Emergency Required in Ward Number : '+ str(rand))
        return 'positive'
    else:
        prediction='negative'
        sendPostRequest(URL, 'provided-api-key', 'provided-secret', 'prod/stage', 'valid-to-mobile', 'active-sender-id', 'Sepsis-Negative. Ward Number : '+ str(rand))
        return 'negative'

    

