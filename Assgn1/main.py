<<<<<<< HEAD
import ast
import csv
import sys
import math
import os

class attribute_set:
	attribute_names = []
	attribute_values = []
	

class node:
	self.att_check = ""
	self.edge_array = []
	self.child_array = []

# hi
def main():
	with open('attribute_info.txt',newline = '') as f : 	
		content = f.read().splitlines();
		i = 0
		for x in content :
			line = x.split(", ")
			attribute_set.attribute_names.append(line[0]);
			temp_list = []
			for y in line[1:] :
				temp_list.append(y);
			attribute_set.attribute_values.append(temp_list)

		print(attribute_set.attribute_names)
		print(attribute_set.attribute_values)
	with open('breast-cancer.csv',newline = '') as f :
		reader = csv.reader(f);		#first divide into random 80/20 split



if __name__ == '__main__':
=======
import ast
import csv
import sys
import math
import os

class attribute_set:
	attribute_names = []
	attribute_values = []

class data_set :
	
	def __init__(self,sz,example_list) :
		self.sz = sz;
		self.example_list = example_list;

class node :

	def __init__(self,attribute_number) :
		self.attribute_number = attribute_number
		self.child = []
		for x in attribute_set.attribute_values[attribute_number] :
			child_content = {}
			child_content['edge'] = x;
			child_content['pointer'] = None;
			self.child.append(child_content);
		self.leaf = 0;
		self.target_val = ""


# class tree :

# def calc_info_gain(attribute_number,example_list) :


# def build_tree(max_depth,data_set) :
# 	for i in 




def main():
	with open('attribute_info.txt',newline = '') as f : 	
		content = f.read().splitlines();
		i = 0
		for x in content :
			line = x.split(", ")
			attribute_set.attribute_names.append(line[0]);
			temp_list = []
			for y in line[1:] :
				temp_list.append(y);
			attribute_set.attribute_values.append(temp_list)

		# print(attribute_set.attribute_names)
		# print(attribute_set.attribute_values)

	example_list = []
	with open('breast-cancer.csv',newline = '') as f :
		reader = csv.reader(f)
		example_list = list(reader)


	d1 = data_set(len(example_list),example_list)	
	# print(d1.example_list,d1.sz)
	new_node = node(1)
	print(new_node.child)


if __name__ == '__main__':
>>>>>>> 301ca94b01b6fc6e164e71a8b21dc6e5457d7845
    main()