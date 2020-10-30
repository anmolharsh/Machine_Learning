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

class attribute_set :
	attribute_names = []
	attribute_values = {}
	target =  "life_expectancy"
	target_values = []
	non_continuous = []

class probabilities :

	def __init__(self,class_probabilities,attribute_probabilities) :
		self.class_probabilities = class_probabilities
		self.attribute_probabilities = attribute_probabilities

	

#encode the categorical attributes using integer encoding
def encode(mp) :
	
	for i in range(len(mp["orig_values"])) :
		mp["encoded_values"].append(i)

#incorporate the encoded values into example_list
def transform_example_list(example_list) :
	
	for x in example_list.columns :
		if attribute_set.attribute_values[x]["continuous"] == 1 or x == attribute_set.target :
			continue
		orig_values = attribute_set.attribute_values[x]["orig_values"]
		for i in example_list.index :
			data = example_list.at[i,x]
			example_list.at[i,x] = attribute_set.attribute_values[x]["encoded_values"][orig_values.index(data)]
		

def handle_missing_values(example_list) :
	
	means = example_list.mean(skipna = True).to_dict() #for continuous attributes
	modes = example_list.mode(dropna = True) 		   #for discrete attributes
	#handling for continuous varai
	for x in example_list.columns :
		for i in example_list.index :
			data = example_list.at[i,x]
			if pd.isna(data) :
				if attribute_set.attribute_values[x]["continuous"] == 1:
					example_list.at[i,x] = means[x]
				else :
					example_list.at[i,x] = modes.at[0,x]

def compute_probabilities(example_list) :
	class_probabilities = {}
	attribute_probabilities = {}
	target_col = example_list.columns[len(example_list.columns)-1]
	unique_targets = example_list[target_col].array.unique()
	target_freq = example_list[target_col].value_counts().to_dict()

	for x in unique_targets :
		class_probabilities[x] = target_freq[x]/(len(example_list.index))

	for y in unique_targets :
		sz = target_freq[y]
		targ_df = example_list[example_list[target_col] == y]
		for x in example_list.columns :
			if x == attribute_set.target :
				continue
			if attribute_set.attribute_values[x]["continuous"] == 0 :
				col_values = example_list[x].array.unique()
				for i in col_values :
					temp_df = example_list[(example_list[x] == i) & (example_list[target_col] == y)]
					attribute_probabilities[(x,i,y)] = len(temp_df.index)/sz
			else :
				mean = targ_df[x].mean()
				std = targ_df[x].std()
				attribute_probabilities[(x,y)] = (mean,std)

	return probabilities(class_probabilities,attribute_probabilities)


def calc_gaussian_prob(val,mean,std) :
	if std == 0 :
		return 1 
	var = std**2
	d = (2*var*math.pi)**0.5
	power = ((float(val)-float(mean))**2)/(2*var)
	n = math.exp(-power)
	return n/d


def calc_accuracy(classifier,test_set,target_values) :
	correct = 0
	total = len(test_set.index)
	for x in test_set.itertuples(index = False) :
		max_prob = -1;
		ans = -1
		for targ in target_values :
			prob = classifier.probabilities.class_probabilities[targ]
			for y,name in zip(range(len(test_set.columns)),test_set.columns) :
				if name == attribute_set.target :
					continue
				if attribute_set.attribute_values[name]["continuous"] == 0 :
					curr_prob = classifier.probabilities.attribute_probabilities[(name,x[y],targ)]
					prob *= curr_prob	
				else :
					tpl = classifier.probabilities.attribute_probabilities[name,targ]
					mean = tpl[0]
					std = tpl[1]
					curr_prob = calc_gaussian_prob(x[y],mean,std)
					prob *= curr_prob
					
			if prob > max_prob :
				max_prob = prob
				ans = targ
		if ans == x[len(test_set.columns)-1] :
			correct += 1

	return correct/total



class naive_bayes_classifier :

	def __init__(self,probabilities) :
		self.probabilities = probabilities


def learn_naive_bayes(example_list,target,target_values) :

	return naive_bayes_classifier(compute_probabilities(example_list)) 

def five_cross_val(example_list,target,target_values) :

	width = round(len(example_list.index)*0.2)
	set_a = example_list.iloc[0:width]
	set_b = example_list.iloc[width:2*width]
	set_c = example_list.iloc[2*width:3*width]
	set_d = example_list.iloc[3*width:4*width]
	set_e = example_list.iloc[4*width:]

	s = 0

	train = pd.concat([set_a,set_b,set_c,set_d])
	test = set_e
	classifier = learn_naive_bayes(train,target,target_values)
	unique_targets = train[train.columns[-1]].array.unique()
	s += calc_accuracy(classifier,test,unique_targets)

	train = pd.concat([set_a,set_b,set_c,set_e])
	test = set_d
	classifier = learn_naive_bayes(train,target,target_values)
	unique_targets = train[train.columns[-1]].array.unique()
	s += calc_accuracy(classifier,test,unique_targets)

	train = pd.concat([set_a,set_b,set_d,set_e])
	test = set_c
	classifier = learn_naive_bayes(train,target,target_values)
	unique_targets = train[train.columns[-1]].array.unique()
	s += calc_accuracy(classifier,test,unique_targets)

	train = pd.concat([set_a,set_c,set_d,set_e])
	test = set_b
	classifier = learn_naive_bayes(train,target,target_values)
	unique_targets = train[train.columns[-1]].array.unique()
	s += calc_accuracy(classifier,test,unique_targets)

	train = pd.concat([set_b,set_c,set_d,set_e])
	test = set_a
	classifier = learn_naive_bayes(train,target,target_values)
	unique_targets = train[train.columns[-1]].array.unique()
	s += calc_accuracy(classifier,test,unique_targets)

	print("Average validation accuracy = ",s/5)

	
def naive_bayes_classification(training_set,test_set,target) :
	target_col = training_set.columns[len(training_set.columns)-1]
	unique_targets = training_set[target_col].array.unique()

	five_cross_val(training_set,target,unique_targets)

	classifier = learn_naive_bayes(training_set,target,unique_targets)
	acc = calc_accuracy(classifier,test_set,unique_targets)
	return acc,classifier

def sample_seiving(example_list) :
	x = 0

def sequential_backward_selection(classifier,test_set,target_values) :

	final_features = test_set.columns.to_list()
	final_features.remove(attribute_set.target)
	removed_features = []

	acc = calc_accuracy(classifier,test_set,target_values)

	for i in range(len(test_set.columns)) :
		curr_acc = -1
		removed_feature = ""
		for x in final_features :
			temp_removed = removed_features.copy()
			temp_removed.append(x)
			temp_test_set = test_set.drop(columns = temp_removed)
			temp_acc = calc_accuracy(classifier,temp_test_set,target_values)
			if temp_acc > curr_acc :
				curr_acc = temp_acc
				removed_feature = x
		if curr_acc >= acc :
			final_features.remove(x)
			removed_features.append(x)
			acc = curr_acc
		else :
			break

	return final_features,removed_features
	



def apply_pca(example_list):
	df = pd.DataFrame(example_list, columns = example_list.columns)
	pca = PCA(n_components=len(df.columns))
	scaler=StandardScaler()
	scaler.fit(df)
	scaled_data=scaler.transform(df)
	pca.fit(scaled_data)

	y_label = pca.explained_variance_ratio_.cumsum()
	x_label = []
	for i in range(1,len(df.columns)+1):
		x_label.append(i)
	
	# print("yoyoyooyoyoyoyoyoyoyoyoyoyo	")
	fig, ax = plt.subplots()  # Create a figure and an axes.
	plt.xlim(0, 25)
	plt.ylim(0.0, 1.01)
	ax.plot(x_label, y_label)
	ax.set_xlabel('Number of components')  # Add an x-label to the axes.
	ax.set_ylabel('Variance ratio')  # Add a y-label to the axes.
	ax.set_title("Variance ratio vs. Number of components ")  # Add a title to the axes.
	plt.savefig('plot.png')

	comp_num=1
	for i in range(len(df.columns)):
		if y_label[i]<0.95 :
			comp_num += 1
		else :
			break
	# print(comp_num)
	pca_new = PCA(n_components = comp_num)
	pca_new.fit(scaled_data)
	x_pca = pca_new.transform(scaled_data)

	# lim = round((0.8)*len(x_pca.index))
	# training_set = x_pca.iloc[0:lim]
	# test_set = x_pca.iloc[lim:]

	msk = np.random.rand(len(x_pca)) <= 0.8
	training_set = x_pca[msk]
	test_set = x_pca[~msk]

	# print(training_set)
	# print(test_set)
	
	#normalization using sklearn library
	scaler1 = preprocessing.MinMaxScaler()
	training_set = pd.DataFrame(scaler1.fit_transform(training_set))
	test_set = pd.DataFrame(scaler1.fit_transform(test_set))

	# mp = {}
	# for x in test_set.columns :
	# 	mp[x] = attribute_set.attribute_names[x]
	# test_set = test_set.rename(columns = mp)
	# training_set = training_set.rename(columns = mp)

	
	# print(training_set)
	# print(test_set)
	# # we do five fold cross validation
	acc = 0
	# acc,classifier = naive_bayes_classification(training_set, test_set, attribute_set.target)
	print("Test accuracy after step 2 = ",acc)





def main() :

	example_list = pd.read_csv("Train_E.csv")
	attribute_set.attribute_names = example_list.columns
	print(example_list)
	#building attribtue-set
	for x in example_list.columns :
		mp = {}
		mp["continuous"] = 1
		mp["orig_values"] = []
		mp["encoded_values"] = []
		if len(example_list[x].array.unique()) <= 5 :
			attribute_set.non_continuous.append(x)
			mp["continuous"] = 0
		attribute_set.attribute_values[x] = mp

	for x,y in example_list.iteritems() :
		if attribute_set.attribute_values[x]["continuous"] == 1 :
			continue
		attribute_set.attribute_values[x]["orig_values"] = list(set(y.tolist()))
		encode(attribute_set.attribute_values[x])


	transform_example_list(example_list)

	#dividng the example list into training set (80%) and test set (20%) 
	example_list = example_list.sample(frac = 1)
	lim = round((0.8)*len(example_list.index))
	training_set = example_list.iloc[0:lim]
	test_set = example_list.iloc[lim:]

	#handling the missing values
	handle_missing_values(training_set)
	handle_missing_values(test_set)

	#normalization using sklearn library
	scaler = preprocessing.MinMaxScaler()
	training_set = pd.DataFrame(scaler.fit_transform(training_set))
	test_set = pd.DataFrame(scaler.fit_transform(test_set))

	#renaming colum labels
	mp = {}
	for x in test_set.columns :
		mp[x] = attribute_set.attribute_names[x]
	test_set = test_set.rename(columns = mp)
	training_set = training_set.rename(columns = mp)

	#performing Naive-Bayes Classification with 5 fold Cross Validation
	acc,classifier = naive_bayes_classification(training_set,test_set,attribute_set.target)

	print("Final test accuracy = ",acc)

	#peforming Sequential Backward Selection to reduce the number of features
	target_col = training_set.columns[len(training_set.columns)-1]
	final_features,removed_features = sequential_backward_selection(classifier,test_set,training_set[target_col].array.unique())

	print("Number of features removed :",len(removed_features))
	print("The final set of features are :",final_features)

	print("Performing 5-Cross Validation on the new set of features")

	new_train = training_set.drop(columns = removed_features)
	new_test = test_set.drop(columns = removed_features)

	acc,classifier = naive_bayes_classification(new_train,new_test,attribute_set.target)

	print("Final test accuracy = ",acc)







if __name__ == '__main__':
    main()