import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pylab as pl

# list of names of people i've taken test data from`
#targets=['brian','seyks','william','amanda','frances','maxim','autiSIM','alberta','drew','james','mattA','meatball','dad','mom2','dadtobii'] #i love you man
#targets=['saraganz','brayden','jackson','emme_monitor'] #mom test video
targets=['leah_vr','will_carkhuff_vr','elias_vr','sam_vr','nathan_vr','hudson_vr','grayson_vr','briana_vr','tiera_vr','brylnee_vr','tara_grescara_vr','randy_ctc_vr']#'randy_ctc_vr','mikekirchner'] #'alex_carkhuff_vr',

num_eig_vectors=3


#rows_of_data=2600 #i love you man
rows_of_data=5400 #mom.mp4


# this is a list of arrays, each array is a 1-D vector of the test data for a particular human (convert N dimentional data to 1xN)
list_o_gaze_datas=[]

for name in targets:
    #load a csv value with data
    file_name=name+'/'+name+'_video_gazed.csv'
    # load video gazed csv into Pandas DataFrame
    gaze_data = pd.read_csv(file_name, names=['frame','left_x','left_y','right_x','right_y','combined_x','combined_y'])
    features=['combined_x','combined_y']
    #grab the data we want to be feature data and put it in a numpy array
    gaze_samples = gaze_data.loc[1:rows_of_data,features].values
    # re-arrange the array to be 1 dimensional
    gaze_samples = gaze_samples.reshape(1,2*len(gaze_samples[:,1]),order='F')
    # add it to the list of arrays
    print(gaze_samples.shape)
    list_o_gaze_datas.append(gaze_samples)


# put all the 1-d arrays of feature data into a 2-d array where the index is the human    
two_d_array=np.concatenate(list_o_gaze_datas,axis=0)
#print(two_d_array)

# put that data into a dataframe
dataset=pd.DataFrame(data=two_d_array,index=targets)
#print(dataset)

# grab only the feature data from the dataframe and put it into a numpy array 
x=dataset.loc[:,:].values

x=StandardScaler().fit_transform(x)

#print(x)

pca = PCA(n_components=num_eig_vectors)
principalComponents = pca.fit_transform(x)
print(principalComponents)

if num_eig_vectors==1:
    principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1'])
elif num_eig_vectors==2:
    principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
else:   
    principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2','principal component 3'])

targets_df=pd.DataFrame(dataset.index.values,columns=['targets'])
finalDf = pd.concat([principalDf, targets_df[['targets']]], axis = 1)
print(finalDf)


fig = plt.figure(figsize = (8,8))

if num_eig_vectors==1 or num_eig_vectors==2:
    ax = fig.add_subplot(1,1,1) 
else:
    ax= plt.axes(projection='3d')

ax.set_xlabel('Autism Index', fontsize = 15)
if num_eig_vectors==2 or num_eig_vectors==3:
    ax.set_ylabel('Principal Component 2', fontsize = 15)
if num_eig_vectors==3:
    ax.set_zlabel('Principal Component 3', fontsize = 15)

colors = pl.cm.jet(np.linspace(0,1,len(targets)))
for target, color in zip(targets,colors):
    # only keep the rows for that have this particular targets that you are plotting a particular color
    indicesToKeep = finalDf['targets'] == target
    if num_eig_vectors==1:
        ax.plot(finalDf.loc[indicesToKeep,'principal component 1'],np.zeros_like(finalDf.loc[indicesToKeep,'principal component 1']),'o',color=color)
    elif num_eig_vectors==2:
        ax.plot(finalDf.loc[indicesToKeep,'principal component 1'],finalDf.loc[indicesToKeep,'principal component 2'],'o',color=color)
    else:   
        #ax.plot(finalDf.loc[indicesToKeep,'principal component 1'],finalDf.loc[indicesToKeep,'principal component 2'],finalDf.loc[indicesToKeep,'principal component 3'],'o',color=color)
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'], finalDf.loc[indicesToKeep, 'principal component 2'],finalDf.loc[indicesToKeep,'principal component 3'],marker='o',color=color)
    #           , c = color
    #           , s = 50)
ax.legend(targets)
ax.grid()
plt.show()

# features = ['sepal length', 'sepal width', 'petal length', 'petal width']
# # Separating out the features, any row, but only colluns from "features"
# x = df.loc[:, features].values
# print(x)

# # Separating out the target (only the "target") column
# y = df.loc[:,['target']].values
# # Standardizing the features
# x = StandardScaler().fit_transform(x)
# print(x)

# print(y)


# # declare the number of eigenvectors you want
# #pca = PCA(n_components=1)
# #pca = PCA(n_components=2)
# pca = PCA(n_components=3)

# # project the data onto the eigen space WHAT DOES FIT_TRANSFORM MEAN COMPARED TO JUST FIT
# principalComponents = pca.fit_transform(x)
# print(principalComponents)


# #make a pandas dataframe with the new projected data
# #principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1'])
# #principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
# principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2','principal component 3'])

# print(principalDf)


# #now add the targets to the final dF
# finalDf = pd.concat([principalDf, df[['target']]], axis = 1)
# print(finalDf)



# # create a figure and size it
# fig = plt.figure(figsize = (8,8))
# #add a plot to the figure
# #ax = fig.add_subplot(1,1,1) 
# ax= plt.axes(projection='3d')

# #add labels
# ax.set_xlabel('Principal Component 1', fontsize = 15)
# ax.set_ylabel('Principal Component 2', fontsize = 15)
# ax.set_zlabel('Principal Component 3', fontsize = 15)
# ax.set_title('3 component PCA', fontsize = 20)

# #map targets to colors and plot each target/color of the DF on a scatter plot
# targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
# colors = ['r', 'g', 'b']
# for target, color in zip(targets,colors):
    # # only keep the rows for that have this particular target that you are plotting a particular color
    # indicesToKeep = finalDf['target'] == target
    # #ax.plot(finalDf.loc[indicesToKeep,'principal component 1'],np.zeros_like(finalDf.loc[indicesToKeep,'principal component 1']),'o',color=color)
    # #ax.plot(finalDf.loc[indicesToKeep,'principal component 1'],finalDf.loc[indicesToKeep,'principal component 2'],'o',color=color)
    # ax.plot(finalDf.loc[indicesToKeep,'principal component 1'],finalDf.loc[indicesToKeep,'principal component 2'],finalDf.loc[indicesToKeep,'principal component 3'],'o',color=color)
    # #ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
    # #           , finalDf.loc[indicesToKeep, 'principal component 2']
    # #           , c = color
    # #           , s = 50)
# ax.legend(targets)
# ax.grid()
# plt.show()