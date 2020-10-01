import ast
import csv
import sys
import math
import os


positive="recurrence-events"
negative="no-recurrence-events"


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

def calc_info_gain(attribute_number,example_list) :


def pos(example_list):
	for x in example_list:
		if x[0]==negative:
			return 0
	return 1

def neg(example_list):
	for x in example_list:
		if x[0]==positive:
			return 0
	return 1


def base_check(max_depth,example_list,all_att,vis):
	if max_depth==0:
		return 1
	else:
		if pos(example_list):
			return 1
		elif neg(example_list):
			return 1
		for x in vis:
			if x==0:
				return 0
		return 1
	return 0


def build_tree(max_depth,example_list,target, all_att,vis) :
	if base_check(max_depth,example_list,all_att,vis)==1 :
		#make leaf
		return 1 # return node
	else:
		max_att=0
		index=0
		for x in vis:
			if x==0:
				max_att=max(max_att,calc_info_gain(index,example_list))
			index+=1
		return 0


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
		# print(example_list)


	d1 = data_set(len(example_list),example_list)	
	# print(d1.example_list,d1.sz)
	new_node = node(1)
	print(new_node.child)
	vis=[]
	for x in range(len(attribute_set.attribute_names)):
		vis.append(0)
	vis[0]=1


if __name__ == '__main__':
    main()