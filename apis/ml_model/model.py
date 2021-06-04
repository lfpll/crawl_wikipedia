import re
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

from urllib.parse import urlparse
from pandas import DataFrame
import numpy as np

class AppearancesModel:
    word_regex = re.compile('[a-zA-Z]')
    number_regex = re.compile('[0-9]')
    arabic_regex = re.compile('[\u0621-\u064A]')
        

    def add_columns(self,df,original_url='wikipedia.com',test_size:float=0.3):
        # Creating feature columns
        if isinstance(df,str):
            df = DataFrame([df], columns=['url'])

        def percent_of_letters(path,regexp):
            if not path or path == '/' or len(regexp.findall(path)) ==0:
                return 0
            elif len(path) >0:
                return len(regexp.findall(path))/len(path)
            
        df['domain'] = df['url'].apply(lambda x: urlparse(x).netloc)
        df['path'] = df['url'].apply(lambda x: urlparse(x).path)
        df['domain_length'] = df['domain'].str.len()
        df['is_file'] = df['path'].apply(lambda path: path[-5:].find('.')>-1)
        df['percent_of_letters_path'] = df['path'].apply(lambda path: percent_of_letters(path,self.word_regex))
        df['percent_of_numbers_path'] = df['path'].apply(lambda path: percent_of_letters(path,self.number_regex))
        df['path_length'] = df['path'].str.len()
        df['last_path_length'] = df['path'].apply(lambda x: len(x.split('/')[-1]))
        df['full_lengh'] = df['url'].str.len()
        df['is_arabic'] = df['url'].apply(lambda x: bool(self.arabic_regex.findall(x)))
        df['number_of_subpaths'] = df['path'].str.split().apply(len)
        df['related_original_url'] = df['url'].str.find(original_url) > -1
        drop_columns = [column for column in ['id',"url",'path','domain'] if column in df.columns]
        return df.drop(columns=drop_columns)
    
    def train_model(self,x_train,y_train):
        regressor = RandomForestRegressor(n_estimators=100,max_depth=10, bootstrap=False,random_state=0)
        return regressor.fit(x_train, y_train)
    
    def metrics(self,y_test,y_pred):
        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    def get_model(self,df:DataFrame=None):

        df_with_features = self.add_columns(df)
        X_train, X_test, y_train, y_test = train_test_split(df_with_features.drop(columns='appearances'), 
                                                            df_with_features['appearances'], random_state=0)
        model = self.train_model(x_train=X_train,y_train=y_train)
        y_pred = model.predict(X_test)
        self.metrics(y_test=y_test,y_pred=y_pred)

        return model

    def save_model(self,path,model):
        pickle.dump(model,open(path,'wb'))
    
    def load_model(self,path):         
        return pickle.load(open(path,'rb'))

