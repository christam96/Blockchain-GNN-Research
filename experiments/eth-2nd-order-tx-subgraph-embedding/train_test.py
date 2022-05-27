from itertools import count
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import numpy as np

## Create train and test sets

# Phishing embeddings
unpickle = open('p-embeddings.pickle', 'rb')
p_embeddings = pickle.load(unpickle)

X_y = np.append(p_embeddings, np.ones((len(p_embeddings),1)), axis=1)
X = X_y[:,:-1]
y = X_y[:,-1]
pX_train, pX_test, py_train, py_test = train_test_split(X, y, test_size=0.25, random_state=42)


# Non-Phishing embeddings
unpickle = open('np-embeddings.pickle', 'rb')
np_embeddings = pickle.load(unpickle)

X_y = np.append(np_embeddings, np.zeros((len(np_embeddings),1)), axis=1)
X = X_y[:,:-1]
y = X_y[:,-1]
npX_train, npX_test, npy_train, npy_test = train_test_split(X, y, test_size=0.25, random_state=42)


# Stack X and y
X_train = np.concatenate((pX_train, npX_train))
y_train = np.concatenate((py_train, npy_train))
X_test = np.concatenate((pX_test, npX_test))
y_test = np.concatenate((py_test, npy_test))

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

svm = SVC()
svm.fit(X_train, y_train)
preds = svm.predict(X_test).tolist()
print(preds)

p_preds = preds[:len(py_test)]
np_preds = preds[len(py_test):]

print('Phishing: correct: ', p_preds.count(1),len(py_test), p_preds.count(1)/len(py_test))
print('Non-Phishing: correct: ',np_preds.count(0),len(npy_test), np_preds.count(0)/len(npy_test))
