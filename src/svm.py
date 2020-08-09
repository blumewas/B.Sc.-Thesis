# Support Vector Machine
from sklearn import svm
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
import numpy as np

def perform_SVM(X, y, n_fold=10):
    
    X = np.array(X)
    y = np.array(y)

    X,y = shuffle(X,y)
    skf = StratifiedKFold(n_splits=n_fold)
    predictions = []
    accuracies = []

    for train_index, test_index in skf.split(X, y):
        X_train = np.array(X)[train_index.astype(int)]
        X_test = np.array(X)[test_index.astype(int)]
        y_train = np.array(y)[train_index.astype(int)]
        y_test = np.array(y)[test_index.astype(int)]

        # define grid parameters
        C_params = [10**i for i in [-4,-3,-2,-1,0,1,2,3,4]]
        params = {'C': C_params}

        # setup svm and perform classification
        svc = svm.SVC(kernel='linear', max_iter=10000)
        clf = GridSearchCV(svc, params, scoring='accuracy', cv=3, n_jobs=8)
        clf.fit(X_train, y_train)

        # predict
        y_pred = clf.predict(X_test)
        predictions.append(y_pred)
        accuracies.append(accuracy_score(y_test, y_pred))

    # return
    accs = np.array(accuracies)
    preds = np.array(predictions)
    return accs, preds
