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

class attribute_set :
	attribute_names = []
	attribute_values = {}
	target =  "life_expectancy"
	target_values = []
	non_continuous = ["iso_code","continent","location","life_expectancy"]

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


def learn_naive_bayes(example_list,target,target_values) :
	#diving the example list into training set (80%) and test set (20%) 
	example_list = example_list.sample(frac = 1)
	lim = round((0.8)*len(example_list.index))
	training_set = example_list.iloc[0:lim]
	test_set = example_list.iloc[lim:]
	handle_missing_values(training_set)
	handle_missing_values(test_set)




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