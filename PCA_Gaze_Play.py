import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

test_data=['brian','lindsay2','seyks']
list_o_gaze_datas=[]

for name in test_data:
    #load a csv value with data
    file_name=name+'/'+name+'_video_gazed.csv'
    # load dataset into Pandas DataFrame
    gaze_data = pd.read_csv(file_name, names=['frame','left_x','left_y','right_x','right_y','combined_x','combined_y'])
    features=['combined_x','combined_y']
    gaze_samples = gaze_data.loc[:,features].values
    gaze_samples = gaze_samples.reshape(1,2*len(gaze_samples[:,1]),order='F')
    list_o_gaze_datas.append(gaze_samples)
    
two_d_array=np.concatenate(list_o_gaze_datas,axis=0)
#print(list_o_gaze_datas)

dataset=pd.DataFrame(data=two_d_array,index=test_data)
print(dataset)




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