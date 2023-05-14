import scipy.io as scio
import numpy as np
from utils import feature_extraction
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import LeaveOneOut
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

 
validation = 'cv' # 'cv' or 'loo'

subjectID = '1'
Date = '2023-04-02'
Mode = 'SS'
category = 'word'
pca_active = False
Dataset_path = './DataSave/' + subjectID + '_' + Date + '_' + Mode + '/Data/' +  category + '/' + 'emg_active.mat'
label_path = './DataSave/' + subjectID + '_' + Date + '_' + Mode + '/Data/' +  category + '/' + 'label.mat'

data = scio.loadmat(Dataset_path)['EMGData']
label = scio.loadmat(label_path)['label'].reshape(-1)

N_samples = data.shape[0]
n_channels = 64
n_feature = 4
features = np.zeros((N_samples, n_channels*n_feature))
for i in range(N_samples):
    features[i, :] = feature_extraction(data[i, :, :].T)


# leave one out CV
if validation == 'loo':
    loo = LeaveOneOut()
    y_pred = np.zeros([N_samples, 1])

    for i_cv, (train_index, test_index) in enumerate(loo.split(features)):
            # training set
            X_train = features[train_index,:]
            y_train = label[train_index]

            # test set
            X_test = features[test_index,:]
            y_test = label[test_index]

            # normalize the features
            sc = StandardScaler()
            X_train = sc.fit_transform(X_train)
            X_test = sc.transform(X_test)
 
            # use PCA ?
            if pca_active == True:
                pca = PCA(n_components=0.95)
                X_train = pca.fit_transform(X_train)
                X_test = pca.transform(X_test)

            # model establishment
            model = LDA(solver='svd')
            model.fit(X_train, y_train.reshape(-1))
            y_pred[i_cv] = model.predict(X_test)

    acc = np.sum((y_pred.reshape(-1) == label)) / len(label)
    print(f'accuracy using leave one out cv: {acc:.4f}')

else:
    model = LDA(solver='svd')
    X = features
    y = label
    # normalize the features
    sc = StandardScaler()
    X = sc.fit_transform(X)
    # use PCA ?
    if pca_active == True:
        pca = PCA(n_components=0.95)
        X = pca.fit_transform(X)

    scores = cross_val_score(model, X, y, cv=3)
    print(f'accuracy using cross validation: {scores.mean():.4f}')


# pre-model

# load the rest data
interrest_path = './DataSave/' + subjectID + '_' + Date + '_' + Mode + '/Data/' +  category + '/' + 'emg_intergroup_rest.mat'
intrarest_path = './DataSave/' + subjectID + '_' + Date + '_' + Mode + '/Data/' +  category + '/' + 'emg_intragroup_rest.mat'
interrest_data = scio.loadmat(interrest_path)['EMGData']
intrarest_data = scio.loadmat(intrarest_path)['EMGData']

# segment them and the active data into pieces of length:emg_len
emg_len = 100 # 100 ms
rest_data = []
for i in range(interrest_data.shape[0]):
    for j in range(interrest_data.shape[1]//emg_len):
        rest_data.append(interrest_data[i, j*emg_len:(j+1)*emg_len, :])
for i in range(intrarest_data.shape[0]):
    for j in range(intrarest_data.shape[1]//emg_len):
        rest_data.append(intrarest_data[i, j*emg_len:(j+1)*emg_len, :])
rest_data = np.array(rest_data)

active_data = []
for i in range(data.shape[0]):
    for j in range(data.shape[1]//emg_len):
        active_data.append(data[i, j*emg_len:(j+1)*emg_len, :])

active_data = np.array(active_data)

data = np.concatenate([active_data, rest_data], axis=0)
label = np.concatenate([np.ones((active_data.shape[0], 1)), np.zeros((rest_data.shape[0], 1))], axis=0).reshape(-1)

# extract features
N_samples = data.shape[0]
n_channels = 64
n_feature = 4
features = np.zeros((N_samples, n_channels*n_feature))
for i in range(N_samples):
    features[i, :] = feature_extraction(data[i, :, :].T, window_len=emg_len/1000, step_len=emg_len/1000)

# train and test a logistic regression binary classifier using cross validation

# normalize the features
sc = StandardScaler()
X = sc.fit_transform(features)
y = label

# use PCA ?
if pca_active == True:
    pca = PCA(n_components=0.95)
    X = pca.fit_transform(X)

# model establishment
model = LogisticRegression(max_iter=1000)

scores = cross_val_score(model, X, y, cv=10)
print(f'pre-accuracy using cross validation: {scores.mean():.4f}')