import warnings
import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

warnings.filterwarnings(action='ignore', category=DeprecationWarning)



def preprocess():
    
    if len(sys.argv) == 1:
    	df = pd.read_csv('pet_purchase.csv')
    
    else:
    	df = pd.read_csv(sys.argv[1])

    
    features = ['First_buy', 'Second_buy','overall_list_first',
       'overall_list_second', 'purchase_delta']
    
    df['target'] = df['target'].astype(str)

    #keep only frequently purchased products

    df.replace('amp;','',regex=True,inplace=True)

    df = df[df['target'].isin((df['target'].value_counts()[df['target'].value_counts()>20]).index)]



    print('Label Encoding features')
    
    # Label Encoding
    le_ = LabelEncoder()
    target_le_ = LabelEncoder()

    df[['First_buy','Second_buy']] = df[['First_buy','Second_buy']].apply(le_.fit_transform)
    
    df['target'] = target_le_.fit_transform(df['target'])
    
    #Train Test split and apply label encoder
    X_train, X_test, y_train, y_test = train_test_split(df[features], df['target'], 
                                                        test_size=.10)
    
    #file outs


    X_train.to_csv('training_data.csv')
    X_test.to_csv('holdout.csv')

    y_train.to_csv('target.csv')
    y_test.to_csv('holdout_response.csv')

    pd.Series(target_le_.classes_).to_csv('target_labels')

    print('''File outs: /n training_data.csv /n holdout.csv /n target.csv 
     /n holdout_response.csv /n target_labels.csv''')


if __name__=='__main__':
	preprocess()
