import ast
import csv
import sys
import math
import os
import copy
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier

class attribute_set :

	def __init__(self,attribute_names,attribute_values,target,target_values,non_continuous) :
		self.attribute_names = attribute_names
		self.attribute_values = attribute_values
		self.target =  target
		self.target_values = target_values
		self.non_continuous = non_continuous

def handle_missing_values(attribute_set,example_list) :
	
	means = example_list.mean(skipna = True).to_dict() #for continuous attributes
	modes = example_list.mode(dropna = True) 		   #for discrete attributes

	for x in example_list.columns :
		for i in example_list.index :
			data = example_list.at[i,x]
			if pd.isna(data) :
				if attribute_set.attribute_values[x]["continuous"] == 1:
					example_list.at[i,x] = means[x]
				else :
					example_list.at[i,x] = modes.at[0,x]


def main() :

	example_list = pd.read_csv("hcc-data.csv")
	print(example_list)

	attribute_names = []
	attribute_values = {}
	target =  "Class"
	target_values = []
	non_continuous = []

	attribute_names = example_list.columns

	#building attribtue-set
	for x in example_list.columns :
		mp = {}
		mp["continuous"] = 1
		mp["orig_values"] = []
		if len(example_list[x].array.unique()) <= 10 :
			non_continuous.append(x)
			mp["continuous"] = 0
		attribute_values[x] = mp

	attributes = attribute_set(attribute_names,attribute_values,target,target_values,non_continuous)

	#dividng the example list into training set (80%) and test set (20%) 
	example_list = example_list.sample(frac = 1)
	lim = round((0.8)*len(example_list.index))
	training_set = example_list.iloc[0:lim]
	test_set = example_list.iloc[lim:]

	#handling the missing values
	handle_missing_values(attributes,training_set)
	handle_missing_values(attributes,test_set)

	print(example_list)

	# standardizing the training and data set
	target_train = training_set.iloc[:,-1].values
	target_test = test_set.iloc[:,-1].values

	scaler = StandardScaler()
	scaler.fit(training_set)
	training_set = pd.DataFrame(scaler.transform(training_set))
	test_set = pd.DataFrame(scaler.transform(test_set))
	training_set.iloc[:,-1] = target_train
	test_set.iloc[:,-1] = target_test

	print(training_set)
	print(test_set)

	X_train = training_set.iloc[:,0:-1].values
	Y_train = training_set.iloc[:,-1].values

	X_test = test_set.iloc[:,0:-1].values
	Y_test = test_set.iloc[:,-1].values

	print(X_train)
	print(Y_train)

	print(X_test)
	print(Y_test)

	classifier = MLPClassifier(solver = 'sgd',hidden_layer_sizes = ())

	classifier.fit(X_train,Y_train)
	print(classifier.predict(X_test))
	



if __name__ == '__main__':
    main()