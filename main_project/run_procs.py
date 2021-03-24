from ml_data_prep import file_dump_
from preprocessing import preprocess
from model_build import model_builder
    
if __name__ == '__main__':
    file_dump_(features_gen = 4)
    print('-'*50)
    print('Purchase file successfully generated!')    
    preprocess()
    print('-'*50)
    print('Files processed for ML training')
    
    model_builder()
    