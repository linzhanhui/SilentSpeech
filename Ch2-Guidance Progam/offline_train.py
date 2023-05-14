import scipy.io as scio
import numpy as np
from utils import feature_extraction
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
import pickle
import os
 

subjectID = '1'
Date = '2023-04-01'
Mode = 'SS'
category = 'word'
pca_active = False
Dataset_path = './DataSave/' + subjectID + '_' + Date + '_' + Mode + '/Data/' +  category + '/' + 'emg_active.mat'
label_path = './DataSave/' + subjectID + '_' + Date + '_' + Mode + '/Data/' +  category + '/' + 'label.mat'

data = scio.loadmat(Dataset_path)['EMGData']
label = scio.loadmat(label_path)['label']

N_samples = data.shape[0]
n_channels = 64
n_feature = 4
features = np.zeros((N_samples, n_channels*n_feature))
for i in range(N_samples):
    features[i, :] = feature_extraction(data[i, :, :].T)

y = label
# normalize the features
sc = StandardScaler()
X = sc.fit_transform(features)
# use PCA ?
if pca_active == True:
    pca = PCA(n_components=0.95)
    X = pca.fit_transform(X)

# model establishment
model = LDA(solver='svd')
model.fit(X, y.reshape(-1))

# save the model
model_path = './Model/' + category + '/' + subjectID + '/' + 'model.pkl'
if not os.path.exists(os.path.dirname(model_path)):
    os.makedirs(os.path.dirname(model_path))
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

# save the scaler
scaler_path = './Model/' + category + '/' + subjectID + '/' + 'scaler.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(sc, f)

# save the pca
if pca_active == True:
    pca_path = './Model/' + category + '/' + subjectID + '/' + 'pca.pkl'
    with open(pca_path, 'wb') as f:
        pickle.dump(pca, f)



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
label = np.concatenate([np.ones((active_data.shape[0], 1)), np.zeros((rest_data.shape[0], 1))], axis=0)

# extract features
N_samples = data.shape[0]
n_channels = 64
n_feature = 4
features = np.zeros((N_samples, n_channels*n_feature))
for i in range(N_samples):
    features[i, :] = feature_extraction(data[i, :, :].T, window_len=emg_len/1000, step_len=emg_len/1000)

# train a logistic regression binary classifier

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
model.fit(X, y.reshape(-1))

# save the model
model_path = './Model/' + category + '/' + subjectID + '/' + 'pre_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

# save the scaler
scaler_path = './Model/' + category + '/' + subjectID + '/' + 'pre_scaler.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(sc, f)

# save the pca
if pca_active == True:
    pca_path = './Model/' + category + '/' + subjectID + '/' + 'pre_pca.pkl'
    with open(pca_path, 'wb') as f:
        pickle.dump(pca, f)


