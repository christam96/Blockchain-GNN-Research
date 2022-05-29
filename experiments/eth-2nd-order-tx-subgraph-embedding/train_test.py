import pickle
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
import numpy as np

## Create train and test sets

# Phishing embeddings
unpickle = open('p-embeddings.pickle', 'rb')
p_embeddings = pickle.load(unpickle)
p_X_y = np.append(p_embeddings, np.ones((len(p_embeddings),1)), axis=1)


# Non-Phishing embeddings
unpickle = open('np-embeddings.pickle', 'rb')
np_embeddings = pickle.load(unpickle)
np_X_y = np.append(np_embeddings, np.zeros((len(np_embeddings),1)), axis=1)

X = np.concatenate((p_X_y[:,:-1], np_X_y[:,:-1]))
y = np.concatenate((p_X_y[:,-1], np_X_y[:,-1]))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=True, random_state=1)

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

svm = SVC()
svm.fit(X_train, y_train)
cross_val_score = cross_val_score(svm, X_test, y_test, cv=5, scoring='accuracy')
print(cross_val_score)
print(np.mean(cross_val_score))
