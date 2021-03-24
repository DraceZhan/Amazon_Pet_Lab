from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.metrics import classification_report
from joblib import dump, load

def model_builder():
	train = pd.read_csv('training_data.csv', index_col=0)
	target = pd.read_csv('target.csv', index_col=0)


	rf_ = RandomForestClassifier(n_estimators=500)

	rf_.fit(train,target['target'].ravel())

	test = pd.read_csv('holdout.csv', index_col=0)
	response_holdout = pd.read_csv('holdout_response.csv', index_col=0)
	labels = pd.read_csv('target_labels')

	print(classification_report(response_holdout['target'], rf_.predict(test)))

	dump(rf_, 'random_forest.joblib')
	print('Model dumped via job lib under random_forest.joblib')

if __name__ == '__main__':
	model_build()
