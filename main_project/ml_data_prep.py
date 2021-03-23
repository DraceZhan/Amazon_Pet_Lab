import numpy as np
import pandas as pd
import sys

def file_dump_():
    
    main_df = pd.read_json(sys.argv[1], lines = True)
    meta_df = pd.read_json(sys.argv[2], lines = True)
    
    print('Main Data Preview')
    print('-' * 50)
    print(main_df.head(3))
    print('-' * 50)
    print('Meta_df Preview')
    print(meta_df.head(3))
    print('-' * 50)
        
    pd.options.mode.chained_assignment = None 
    
    meta_df['sub_category'] = meta_df['category'].str[1:3].str.join('_')
    
    assert(np.sum(meta_df['sub_category'].isnull())==0),'NaN in col: sub_category'

    #creating temp df's for data manipulating
    
    print('Merging Tables & converting values')
    
    df = pd.merge(main_df, meta_df,how='left', on = 'asin')
    df['sub_category'] = df['sub_category'].fillna(df['asin'])
    df['reviewTime'] = pd.to_datetime(df['unixReviewTime'], unit='s')
    df.sort_values(by='reviewTime', inplace=True)
    
    print('creating new table')

    order_cart_df = df.groupby('reviewerID')['sub_category'].apply(list).reset_index()
    for col_name in ['overall', 'summary', 'reviewText', 'reviewTime']:
        order_cart_df[f'{col_name}'+'_list'] = df.groupby('reviewerID')[col_name].apply(list).values
    
    first_two_purch_df = pd.DataFrame({'First_buy': order_cart_df['sub_category'].str[0],
                                   'Second_buy': order_cart_df['sub_category'].str[1],
                                  'target': order_cart_df['sub_category'].str[2]})

    for col in ['overall_list', 'reviewTime_list']:
        first_two_purch_df[f'{col}_first'] = order_cart_df[col].str[0]
        first_two_purch_df[f'{col}_second'] = order_cart_df[col].str[1]
    
    top_twenty_df = first_two_purch_df[np.logical_and(first_two_purch_df['First_buy'].isin( 
                                   list(first_two_purch_df['First_buy'].value_counts()[:20].keys())),
                                  first_two_purch_df['Second_buy'].isin( 
                                   list(first_two_purch_df['Second_buy'].value_counts()[:20].keys())))]

    top_twenty_df['purchase_delta'] = (top_twenty_df[
        'reviewTime_list_second'] - top_twenty_df['reviewTime_list_first']).dt.days
   
    print('exporting')
    
    top_twenty_df.to_csv('pet_purchase.csv')
    
    print('Successful dump of pet_purchase.csv as file for training')
    
if __name__=='__main__':
    file_dump_()
