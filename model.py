import csv
import pickle
from pprint import pprint
from typing import Optional

from yaml import load, dump, Loader
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split

MODEL_SERIALIZATION_FILEPATH = 'files/model_dump.dat'
VECTORIZER_SERIALIZATION_FILEPATH = 'files/vectorizer_dump.dat'
DATAFRAME_FILEPATH = 'files/tickets_dataframe.csv'


class Model:
    model: Optional[LinearSVC]
    vectorizer: Optional[TfidfVectorizer]

    def __init__(self):
        try:
            self._load_current()
            print('Model loaded successfully')
        except FileNotFoundError:
            print('Not model found on local disc. Please, call fit() method to create the new one')

    def _save(self):
        with open(MODEL_SERIALIZATION_FILEPATH, 'wb') as file:
            pickle.dump(obj=self.model, file=file)
        with open(VECTORIZER_SERIALIZATION_FILEPATH, 'wb') as file:
            pickle.dump(obj=self.vectorizer, file=file)

    def _load_current(self):
        with open(MODEL_SERIALIZATION_FILEPATH, 'rb') as file:
            self.model = pickle.load(file)
        with open(VECTORIZER_SERIALIZATION_FILEPATH, 'rb') as file:
            self.vectorizer = pickle.load(file)

    def _load_dataframe_vectorized(self):
        X_raw = list()
        y = list()
        with open(DATAFRAME_FILEPATH, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                X_raw.append(row[0])
                y.append(row[1])
        return self.vectorizer.fit_transform(X_raw), y

    def fit(self):
        models = dict()
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(3, 3),
            analyzer='char'
        )
        for i in range(1000):
            print(f'{i} model learning...')
            X_train, X_test, y_train, y_test = train_test_split(
                *self._load_dataframe_vectorized(),
                test_size=0.33,
                shuffle=True
            )
            model = LinearSVC()
            model.fit(X_train, y_train)
            score = model.score(X_test, y_test)
            models[score] = model
            print(f'Added to list with score={score}')
        best_model_score = max(models.keys())
        self.model = models[best_model_score]
        self._save()
        print(f'Model with score={best_model_score} serialized to local disc')

    def predict(self, text: str):
        try:
            vectorized_list = self.vectorizer.transform([text])
            topic_id = self.model.predict(vectorized_list)[0]
        except AttributeError:
            print('Not model found on local disc. Please, call fit() method to create the new one')
        else:
            return self.get_topic_name_by_id(topic_id)

    @staticmethod
    def get_topic_name_by_id(topic_id: int):
        with open('topics.yaml', 'r') as file:
            topics_data = load(file, Loader=Loader)
            return topics_data[int(topic_id)]
