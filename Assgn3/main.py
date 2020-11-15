import ast
import csv
import sys
import math
import os
import copy
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.utils._testing import ignore_warnings
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

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
def calc_accuracy(Y_test, Y_predicted) :
	sz = len(Y_test)
	count = 0
	for x,y in zip(Y_test, Y_predicted) :
		count += (x == y)

	return count/sz

def mlp_classification(attribute_set, training_set, test_set) :

	print("-"*100, "\n")
	print("~ Performing Multi-Layer Perceptron Classification ~")
	X_train = training_set.iloc[:,0:-1].values
	Y_train = training_set.iloc[:,-1].values

	X_test = test_set.iloc[:,0:-1].values
	Y_test = test_set.iloc[:,-1].values

	
	architectures = [(), (2), (6), (2,3), (3,2)]

	# comparing accuracy vs learning rate for each model
	for i,hidden_layer in zip(range(5),architectures) :
		rate = 0.1
		x_pts = []
		y_pts = []
		for x in range(5) :
			x_pts.append(rate)
			classifier = MLPClassifier(random_state = 1000,max_iter = 2000,activation = 'logistic',solver = 'sgd',hidden_layer_sizes = hidden_layer, learning_rate_init = rate)
			classifier.fit(X_train,Y_train)
			Y_predicted = classifier.predict(X_test)
			y_pts.append(calc_accuracy(Y_test, Y_predicted)*100)
			rate /= 10

		# line graph
		fig = plt.figure()
		plt.xlabel('Learning Rate')  # Add an x-label to the axes.
		plt.ylabel('Accuracy (%)')  # Add a y-label to the axes.
		plt.title("Accuracy vs. Learning Rate for Model " + str(i+1))  # Add a title to the axes.
		plt.ylim([0,100])
		plt.semilogx(x_pts, y_pts)
		file_name = "graph_architecture_" + str(i+1)
		plt.savefig(file_name)


	# comapring accuracy vs architecture for each learning rate
	rate = 0.1
	max_accuracy = 0
	best_rate = -1
	best_architecture = ()
	for i in range(5) :
		x_pts = []
		y_pts = []
		exec_time = []
		for j,x in zip(range(5),architectures) :
			start_time = time.time()
			classifier = MLPClassifier(random_state = 1000,max_iter = 2000,activation = 'logistic', solver = 'sgd',hidden_layer_sizes = x, learning_rate_init = rate)
			classifier.fit(X_train,Y_train)
			exec_time.append(time.time()-start_time)
			Y_predicted = classifier.predict(X_test)
			x_pts.append("Model " + str(j))
			acc = calc_accuracy(Y_test, Y_predicted)*100
			y_pts.append(acc)
			if acc > max_accuracy :
				max_accuracy = acc
				best_rate = rate
				best_architecture = x

		# bar graph
		fig = plt.figure()
		plt.xlabel('Model')  # Add an x-label to the axes.
		plt.ylabel('Accuracy (%)')  # Add a y-label to the axes.	
		plt.title("Accuracy vs Model for Learning Rate = " + str(rate))  # Add a title to the axes.
		plt.ylim([0,100])
		plt.bar(x = x_pts, height = y_pts, width = 0.4)
		file_name = "graph_learning_rate_" + str(i+1) + ".png"
		plt.savefig(file_name)
		print(max(y_pts))

		rate /= 10

	print("The best model found :")
	print("Learning Rate = ",best_rate)
	print("Architecture of the Neural Network :")
	print(" "*6,"Number of hidden layers = ",len(best_architecture))
	for x,i in zip(best_architecture,range(len(best_architecture))) :
		print(" "*12,"Number of neurons in layer ",i," = ", x)
	print("Accuracy of the model = ",max_accuracy,"%")


def main() :

	example_list = pd.read_csv("hcc-data.csv")

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
	example_list = example_list.sample(frac = 1,random_state = 1000)
	lim = round((0.8)*len(example_list.index))
	training_set = example_list.iloc[0:lim]
	test_set = example_list.iloc[lim:]


	#handling the missing values
	handle_missing_values(attributes,training_set)
	handle_missing_values(attributes,test_set)


	# standardizing the training and data set
	target_train = training_set.iloc[:,-1].values
	target_test = test_set.iloc[:,-1].values

	scaler = StandardScaler()
	scaler.fit(training_set)
	training_set = pd.DataFrame(scaler.transform(training_set))
	test_set = pd.DataFrame(scaler.transform(test_set))
	training_set.iloc[:,-1] = target_train
	test_set.iloc[:,-1] = target_test

	# part 1
	C_values = [0.001,0.01,0.1,1,10,100,1000]
	lin_acc = []
	rbf_acc = []
	poly_acc = []
	for i in C_values:
		clf = svm.SVC(kernel='linear',C=i)
		clf.fit(training_set, target_train)
		y_pred = clf.predict(test_set)
		lin_acc.append(clf.score(test_set, target_test))
		
		clf = svm.SVC(kernel='rbf',C=i)
		clf.fit(training_set, target_train)
		y_pred = clf.predict(test_set)
		rbf_acc.append(clf.score(test_set, target_test))
		
		clf = svm.SVC(kernel='poly',degree = 2,C=i)
		clf.fit(training_set, target_train)
		y_pred = clf.predict(test_set)
		poly_acc.append(clf.score(test_set, target_test))
	best_acc = max(max(lin_acc),max(rbf_acc),max(poly_acc))
	print("\nPart 1\n")
	print("Best_accuracy = ",best_acc)
	print("\nLinear Kernel" )
	print(lin_acc)
	print("\nRbf Kernel" )
	print(rbf_acc)
	print("\nPoly_ Kernel" )
	print(poly_acc)
	print("\n")
	mlp_classification(attribute_set, training_set, test_set)

	
	



if __name__ == '__main__':
	main()