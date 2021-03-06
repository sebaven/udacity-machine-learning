#!/usr/bin/python

"""

skeleton code for k-means clustering mini-project

"""

import pickle
import matplotlib.pyplot as plt
from tools.feature_format import featureFormat, targetFeatureSplit

def Draw(pred, features, poi, mark_poi=False, name="image.png", f1_name="feature 1", f2_name="feature 2"):
    """ some plotting code designed to help you visualize your clusters """

    ### plot each cluster with a different color--add more colors for
    ### drawing more than 4 clusters
    colors = ["b", "c", "k", "m", "g"]
    for ii, pp in enumerate(pred):
        plt.scatter(features[ii][0], features[ii][1], color = colors[pred[ii]])

    ### if you like, place red stars over points that are POIs (just for funsies)
    if mark_poi:
        for ii, pp in enumerate(pred):
            if poi[ii]:
                plt.scatter(features[ii][0], features[ii][1], color="r", marker="*")
    plt.xlabel(f1_name)
    plt.ylabel(f2_name)
    plt.savefig(name)
    plt.show()



### load in the dict of dicts containing all the data on each person in the dataset
data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "rb") )
### there's an outlier--remove it!
data_dict.pop("TOTAL", 0)


### the input features we want to use
### can be any key in the person-level dictionary (salary, director_fees, etc.)
feature_1 = "salary"
feature_2 = "exercised_stock_options"
poi  = "poi"
features_list = [poi, feature_1, feature_2]
data = featureFormat(data_dict, features_list )
poi, finance_features = targetFeatureSplit( data )


### in the "clustering with 3 features" part of the mini-project,
### you'll want to change this line to
### for f1, f2, _ in finance_features:
### (as it's currently written, line below assumes 2 features)
for f1, f2 in finance_features:
    plt.scatter( f1, f2 )
plt.show()



from sklearn.cluster import KMeans
features_list = ["poi", feature_1, feature_2]
data2 = featureFormat(data_dict, features_list )
poi, finance_features = targetFeatureSplit( data2 )
clf = KMeans(n_clusters=2)
pred = clf.fit_predict( finance_features )
Draw(pred, finance_features, poi, name="clusters_before_scaling.pdf", f1_name=feature_1, f2_name=feature_2)


try:
    Draw(pred, finance_features, poi, mark_poi=False, name="clusters.pdf", f1_name=feature_1, f2_name=feature_2)
except NameError:
    print ("no predictions object named pred found, no clusters to plot")


max_exercised_stock_option = 0;
min_exercised_stock_option = 9223372036854775807;
max_salary = 0;
min_salary = 9223372036854775807;
for j in data_dict:
    if data_dict[j]["exercised_stock_options"]  != "NaN" and  data_dict[j]["exercised_stock_options"] > max_exercised_stock_option:
        max_exercised_stock_option = data_dict[j]["exercised_stock_options"];
    if data_dict[j]["exercised_stock_options"]  != "NaN" and  data_dict[j]["exercised_stock_options"] < min_exercised_stock_option:
        min_exercised_stock_option = data_dict[j]["exercised_stock_options"];
    if data_dict[j]["salary"]  != "NaN" and  data_dict[j]["salary"] > max_salary:
        max_salary = data_dict[j]["salary"];
    if data_dict[j]["salary"]  != "NaN" and  data_dict[j]["salary"] < min_salary:
        min_salary = data_dict[j]["salary"];

print ("max exercised stock options",max_exercised_stock_option)
print ("min exercised stock options", min_exercised_stock_option)
print ("max salary",max_salary)
print ("min salary", min_salary)



exercised_stock_options = []
salary = []
for i in data_dict:
    if data_dict[i]["exercised_stock_options"] != 'NaN':
        exercised_stock_options.append(float(data_dict[i]["exercised_stock_options"]))
    if data_dict[i]["salary"] != 'NaN':
        salary.append(float(data_dict[i]["salary"]))

from sklearn.preprocessing import MinMaxScaler
import numpy
exercised_stock_options_ = numpy.array(exercised_stock_options)
exercised_stock_options_ = exercised_stock_options_.astype(float)
scaler = MinMaxScaler()
rescaled_salary = scaler.fit_transform(exercised_stock_options_)

values = numpy.array([[1000000.]])
rescaled = scaler.transform(values)


print(rescaled)
