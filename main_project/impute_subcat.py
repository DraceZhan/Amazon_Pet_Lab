#Uses a bayesian approach to impute subcategory values based on word counts of reviews

def imputer(df):
    
    #required libs
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.model_selection import cross_validate, cross_val_predict, cross_val_score
    from sklearn.preprocessing import LabelEncoder
    import numpy as np
    import string
    
    import pandas as pd
    pd.options.mode.chained_assignment = None 
    
    df['sub_category'] = df['sub_category'].replace('', np.NaN)
    
    df['cleaned_review'] = df['reviewText'].str.translate({'':string.punctuation})

    #iterating through the cross validatioon scores, max features ideal appears to be around 3K-4K
    tf_idf = TfidfVectorizer(stop_words='english',strip_accents='unicode',max_df=.9, max_features=4000)

    train_df = df[df['sub_category'].notnull()]
    impute_df = df[df['sub_category'].isnull()]

    features_for_train = tf_idf.fit_transform(train_df['cleaned_review'])
    features_for_pred = tf_idf.transform(impute_df['cleaned_review'])

    target_label_encoder = LabelEncoder()
    train_df['labels'] = target_label_encoder.fit_transform(train_df['sub_category'])

    nb_ = MultinomialNB()

    nb_.fit(features_for_train, train_df['labels'])

    print(f'Score for imputation model 5 fold: {cross_val_score(nb_, features_for_train, train_df["labels"])}')
    
    impute_df['labels'] = nb_.predict(features_for_pred)
    df.loc[df['sub_category'].isnull(), 'sub_category'] = target_label_encoder.inverse_transform(impute_df['labels'])
    
    return df