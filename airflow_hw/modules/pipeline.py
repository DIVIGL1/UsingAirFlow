import logging
import os
from datetime import datetime
import hashlib

import dill
import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = [
        'id',
        'url',
        'region',
        'region_url',
        'price',
        'manufacturer',
        'image_url',
        'description',
        'posting_date',
        'lat',
        'long'
    ]
    return df.drop(columns_to_drop, axis=1)


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    def calculate_outliers(data):
        q25 = data.quantile(0.25)
        q75 = data.quantile(0.75)
        iqr = q75 - q25
        bounds = (q25 - 1.5 * iqr, q75 + 1.5 * iqr)
        return bounds

    df = df.copy()
    boundaries = calculate_outliers(df['year'])
    df.loc[df['year'] < boundaries[0], 'year'] = round(boundaries[0])
    df.loc[df['year'] > boundaries[1], 'year'] = round(boundaries[1])
    return df


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    def short_model(x):
        if not pd.isna(x):
            return x.lower().split(' ')[0]
        else:
            return x

    df = df.copy()
    df.loc[:, 'short_model'] = df['model'].apply(short_model)
    df.loc[:, 'age_category'] = df['year'].apply(lambda x: 'new' if x > 2013 else ('old' if x < 2006 else 'average'))
    return df


def pipeline_func() -> (None):
    logging.info(f'pipeline_func() started...')
    path = os.environ.get('PROJECT_PATH', '.')

    train_file = f'{path}/data/train/homework.csv'
    hash_str = hashlib.blake2b(open(train_file,'rb').read(), digest_size=5).hexdigest()
    model_filename = os.path.join(path, "data", "models", f"cars_pipe_{hash_str}.pkl")
    
    # Проверим была ли раньше сформирована модель для этого файла (с таким hash)
    if os.path.exists(model_filename):
        # Для данного датасата модель уже сформирована.
        logging.info(f'Model already exists: {model_filename}')
        return(0)
    
    logging.info(f'A data file was read to train the model.')
    df = pd.read_csv(train_file)

    X = df.drop('price_category', axis=1)
    y = df['price_category']

    numerical_features = make_column_selector(dtype_include=['int64', 'float64'])
    categorical_features = make_column_selector(dtype_include=object)

    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    column_transformer = ColumnTransformer(transformers=[
        ('numerical', numerical_transformer, numerical_features),
        ('categorical', categorical_transformer, categorical_features)
    ])

    preprocessor = Pipeline(steps=[
        ('filter', FunctionTransformer(filter_data)),
        ('outlier_remover', FunctionTransformer(remove_outliers)),
        ('feature_creator', FunctionTransformer(create_features)),
        ('column_transformer', column_transformer)
    ])
    logging.info(f'Pipeline has been constructed.')

    models = [
        LogisticRegression(solver='liblinear'),
        RandomForestClassifier(),
        SVC()
    ]
    logging.info(f'Models have been selected.')

    best_score = .0
    best_pipe = None
    for model in models:

        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])

        score = cross_val_score(pipe, X, y, cv=4, scoring='accuracy')
        logging.info(f'model: {type(model).__name__}, acc_mean: {score.mean():.4f}, acc_std: {score.std():.4f}')
        if score.mean() > best_score:
            best_score = score.mean()
            best_pipe = pipe

    logging.info(f'best model: {type(best_pipe.named_steps["classifier"]).__name__}, accuracy: {best_score:.4f}')

    best_pipe.fit(X, y)

    # Проверим ЕЩЁ раз не была ли зха это время сформирована модель для этого датасета (с таким hash)?
    if os.path.exists(model_filename):
        # Для данного датасата модель уже сформирована.
        logging.info(f'Model already exists: {model_filename}.')
        return(0)

    with open(model_filename, 'wb') as file:
        dill.dump(best_pipe, file)

    logging.info(f'Model is saved as {model_filename}')
    
    return(0)


if __name__ == '__main__':
    pipeline_func()
