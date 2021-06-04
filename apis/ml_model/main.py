# Creating feature columns
from apis.ml_model.model import AppearancesModel
import pandas as pd
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":
    df = pd.read_csv('%s/sample.csv'%dir_path)
    train_class = AppearancesModel()
    model = train_class.get_model(df)
    train_class.save_model('%s/model.pckl'%dir_path,model)
    

