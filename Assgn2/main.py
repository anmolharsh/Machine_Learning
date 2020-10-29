import ast
import csv
import sys
import math
import os
import copy
import random
import matplotlib.pyplot as plt
import numpy as np

class attribute_set :
	attribute_names = []
	attribute_values = []
	target =  "life_expectancy"
	target_values = []
	non_continuous = ["iso_code","continent","location","life_expectancy"]

def encode(idx) :
	for i in range(len(attribute_set.attribute_values[idx]["orig_values"])) :
		attribute_set.attribute_values[idx]["encoded_values"].append(i)

def transform_example_list(example_list) :
	for x in example_list :
		for i,mp in zip(x,attribute_set.attribute_values) :
			if mp["continuous"] ==  0 :
				orig_values = mp["orig_values"]
				x[x.index(i)] = mp["encoded_values"][orig_values.index(i)] 


def main() :
	with open('Train_E.csv',newline = '') as f :
		reader = csv.reader(f)
		example_list = list(reader)
	for x in example_list[0] :
		attribute_set.attribute_names.append(x)
		mp = {}
		mp["continuous"] = 1
		mp["orig_values"] = []
		mp["encoded_values"] = []
		if x in attribute_set.non_continuous :
			mp["continuous"] = 0
		attribute_set.attribute_values.append(mp)
	example_list.pop(0)
	for x in example_list :
		for i,mp in zip(x,attribute_set.attribute_values) :
			if mp["continuous"] ==  0 :
				if i not in mp["orig_values"] :
					mp["orig_values"].append(i)
	attribute_set.target_values = attribute_set.attribute_values[len(attribute_set.attribute_values)-1]["orig_values"]

	for mp,i in zip(attribute_set.attribute_values,range(len(attribute_set.attribute_values))) :
		if mp["continuous"] == 0 :
			encode(i)

	transform_example_list(example_list)






if __name__ == '__main__':
    main()