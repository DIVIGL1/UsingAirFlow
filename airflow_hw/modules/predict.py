import json
import logging
import pandas as pd
import os
import dill

def predict_func():
    logging.info(f'predict_func() started...')
    path = os.environ.get('PROJECT_PATH', '.')
    
    path_models = os.path.join(path, "data", "models")
    path_test = os.path.join(path, "data", "test")
    path_preds = os.path.join(path, "data", "predictions")
    
    # Если несколько моделей, то выберем модель с максимальной датой создания:
    list_of_models = [os.path.join(path_models, one_file) for one_file in os.listdir(path_models) if (one_file[-4:] == ".pkl")]
    if len(list_of_models) == 0:
        # Нет ни одного файла, поэтому выходим без обработки.
        logging.info(f'There are no files to process.')
        return(0)
    
    full_model_file_name = max(list_of_models, key=os.path.getctime)
    model_version = full_model_file_name.split("cars_pipe_")[1].split(".pkl")[0]
    
    with open(full_model_file_name, 'rb') as hfile:
        curr_model = dill.load(hfile)

    # Записывать файл с предсказаниями:
    df_save_preds = pd.DataFrame(columns=["ModelName", "DataFile", "Prediction"])
    for test_filename in os.listdir(path_test):
        cur_test_file = os.path.join(path_test, test_filename)

        with open(cur_test_file) as hfile:
            test_data = json.load(hfile)
        
        df = pd.DataFrame.from_dict([test_data])
        y = curr_model.predict(df)
        
        df_save_preds = df_save_preds.append(
            [
                {
                    "ModelName": "cars_pipe_" + model_version,
                    "DataFile": test_filename,
                    "Prediction": y[0]
                }
            ]
        )
        
        # Сохраним все предсказания для данной модели:
        csv_file = os.path.join(path_preds, "preds_" + model_version + ".csv")
    
    df_save_preds.to_csv(csv_file, index=False)
    logging.info(f'Saved prediction for model {"cars_pipe_" + model_version}')

    return(0)

if __name__ == '__main__':
    predict_func()
