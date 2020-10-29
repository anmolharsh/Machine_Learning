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

class attribute_set :
	attribute_names = []
	attribute_values = {}
	target =  "life_expectancy"
	target_values = []
	non_continuous = ["iso_code","continent","location","life_expectancy"]

class probabilities :
	class_probabilties = {}
	attribute_probabilites = {}

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
	print(example_list)
	target_col = len(example_list.columns)-1
	unique_targets = example_list[target_col].array.unique()
	probabilities.target_values = unique_targets
	target_freq = example_list[target_col].value_counts().to_dict()

	for x in unique_targets :
		probabilities.class_probabilties[x] = target_freq[x]/(len(example_list.index))

	for y in unique_targets :
		sz = target_freq[y]
		targ_df = example_list[example_list[target_col] == y]
		for x in example_list.columns :
			name = attribute_set.attribute_names[x]
			if name == attribute_set.target :
				continue
			if attribute_set.attribute_values[name]["continuous"] == 0 :
				col_values = example_list[x].array.unique()
				for i in col_values :
					temp_df = example_list[(example_list[x] == i) & (example_list[target_col] == y)]
					probabilities.attribute_probabilites[(x,i,y)] = len(temp_df.index)/sz
			else :
				mean = targ_df[x].mean()
				std = targ_df[x].std()
				probabilities.attribute_probabilites[(x,y)] = (mean,std)


def calc_gaussian_prob(val,mean,std) :
	if std == 0 :
		return 1 
	var = std**2
	d = (2*var*math.pi)**0.5
	n = num = math.exp(-(float(val)-float(mean))**2/(2*var))
	return n/d


def calc_accuracy(test_set,target_values) :
	correct = 0
	total = len(test_set.index)
	for x in test_set.itertuples(index = False) :
		max_prob = -1;
		ans = -1
		for targ in target_values :
			prob = probabilities.class_probabilties[targ]
			for y in test_set.columns :
				name = attribute_set.attribute_names[y]
				if name == attribute_set.target :
					continue
				if attribute_set.attribute_values[name]["continuous"] == 0 :
					curr_prob = probabilities.attribute_probabilites[(y,x[y],targ)]
					prob *= curr_prob
				else :
					tpl = probabilities.attribute_probabilites[y,targ]
					mean = tpl[0]
					std = tpl[1]
					curr_prob = calc_gaussian_prob(x[y],mean,std)
					prob *= curr_prob
				print(prob,targ)
			if prob > max_prob :
				max_prob = prob
				ans = targ
		if ans == x[len(test_set.columns)-1] :
			correct += 1
		print("\n\n")

	return correct/total



		


def learn_naive_bayes(example_list,target,target_values) :
	
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

	compute_probabilities(training_set)

	unique_targets = training_set[len(training_set.columns)-1].array.unique()

	print(calc_accuracy(test_set,unique_targets))











def main() :

	example_list = pd.read_csv("Train_E.csv")
	attribute_set.attribute_names = example_list.columns
	print(example_list)
	#building attribtue-set
	for x in attribute_set.attribute_names :
		mp = {}
		mp["continuous"] = 1
		mp["orig_values"] = []
		mp["encoded_values"] = []
		if x in attribute_set.non_continuous :
			mp["continuous"] = 0
		attribute_set.attribute_values[x] = mp

	for x,y in example_list.iteritems() :
		if attribute_set.attribute_values[x]["continuous"] == 1 :
			continue
		attribute_set.attribute_values[x]["orig_values"] = list(set(y.tolist()))
		encode(attribute_set.attribute_values[x])


	transform_example_list(example_list)
	learn_naive_bayes(example_list,attribute_set.target,attribute_set.target_values)





if __name__ == '__main__':
    main()