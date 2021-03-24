import numpy as np
import pandas as pd
from sys import argv
from impute_subcat import imputer


def make_other_cols(purch_df, order_cart_df, col_name = 'overall_list', num_cols =2):
    for i in range(num_cols):
        purch_df[f'{col_name}_{i}'] = order_cart_df[col_name].str[i]
    
    return(purch_df)

def generate_purchase(df, num_ = 2):
    '''
    df: pd.DataFrame
    merged dataframe that contains individual rows of reviewers, orders, and time stamps of order
    num_: int
    count of orders use as predictors, 2, 3,4 allowed only
    '''

    if num_ not in [2,3,4]:
        raise ValueError('Please only use values 2,3, or 4')

    order_cart_df = df.groupby('reviewerID')['sub_category'].apply(list).reset_index()
    for col_name in ['overall', 'summary', 'reviewText', 'reviewTime']:
        order_cart_df[f'{col_name}'+'_list'] = df.groupby('reviewerID')[col_name].apply(list).values
    
    purch_df = pd.DataFrame({f'{i}_buy': order_cart_df['sub_category'].str[n] for i,n in enumerate(range(num_))})
    purch_df['target'] = order_cart_df['sub_category'].str[num_]

    for col in ['overall_list', 'reviewTime_list']:
        make_other_cols(purch_df, order_cart_df, col_name=col, num_cols = num_)

    top_twenty_df = purch_df[purch_df['target'].isin( 
                                   list(purch_df['target'].value_counts()[:20].keys()))]

    for i in range(num_ - 1):
        top_twenty_df[f'purchase_delta_{i}'] = abs(top_twenty_df[f'reviewTime_list_{i}'
            ] - top_twenty_df[f'reviewTime_list_{i+1}']).dt.days

   
    print('exporting')
    
    top_twenty_df.to_csv('pet_purchase.csv')
    
    print('Successful dump of pet_purchase.csv as file for training')


#as py executable

main_df_link = 'https://graderdata.s3.amazonaws.com/reviews_Pet_Supplies_5.json'
meta_df_link = 'https://pet-amz-lab.s3.amazonaws.com/meta_dict.json'
features_to_gen = 2
def file_dump_(main_df= main_df_link, meta_df = meta_df_link, features_gen = features_to_gen):
    
    main_df = pd.read_json(main_df_link, lines = True)
    meta_dict = pd.read_json(meta_df_link)
    
    print('Main Data Preview')
    print('-' * 50)
    print(main_df.head(3))
    print('-' * 50)
    print('Meta_df Preview')
    print(meta_dict.head(3))
    print('-' * 50)
        
    pd.options.mode.chained_assignment = None 

    assert(np.sum(meta_dict['sub_category'].isnull())==0),'NaN in col: sub_category'

    #creating temp df's for data manipulating
    
    print('Merging Tables & converting values')
    
    df = pd.merge(main_df, meta_dict,how='left', on = 'asin')
    df = imputer(df)
    df['reviewTime'] = pd.to_datetime(df['unixReviewTime'], unit='s')
    df.sort_values(by='reviewTime', inplace=True)
    
    print('creating new table')

    generate_purchase(df, features_gen)


def run_file():
    file_dump_(*argv[1:])
    
    
    
if __name__=='__main__':
    run_file()
