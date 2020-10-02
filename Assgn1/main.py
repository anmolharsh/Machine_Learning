import ast
import csv
import sys
import math
import os
import copy




class attribute_set:
	attribute_names = []
	attribute_values = []
	target = "Class"
	positive = "recurrence-events"
	negative = "no-recurrence-events"

class data_set :
	
	def __init__(self,sz,example_list) :
		self.sz = sz;
		self.example_list = example_list;

class node :

	def __init__(self,attribute_number,example_list) :
		self.attribute_number = attribute_number
		self.child = []
		for x in attribute_set.attribute_values[attribute_number] :
			child_content = {}
			child_content['edge'] = x;
			child_content['pointer'] = None;
			self.child.append(child_content);
		self.leaf = 0;
		self.target_val = ""
		self.example_list = example_list


def entropy_pnv(sp,sn,sv):
	if(sp == sv or sn == sv or sp == 0 or sn == 0):
		return 0
	if sp == sn:
		return 1
	sp = float(sp)/sv
	sn = float(sn)/sv
	res = (-1)*(sp*math.log2(sp)+sn*math.log2(sn))

	return res


#calcs |s|*Entropy(s)
def calc_entropy(example_list,target):
	p_pos = 0
	p_neg = 0

	positive = attribute_set.positive
	negative = attribute_set.negative
	for x in example_list:
		if x[target] == positive:
			p_pos += 1
		elif x[target] == negative:
			p_neg += 1
	return entropy_pnv(p_pos,p_neg,len(example_list))


def calc_info_gain(attribute_number,example_list,target) :
	positive = attribute_set.positive
	negative = attribute_set.negative
	entropy=calc_entropy(example_list,target)
	Esv = 0
	for y in range(len(attribute_set.attribute_values[attribute_number])):
		sp = 0
		sn = 0
		sv = 0
		for x in example_list:
			if x[attribute_number] == attribute_set.attribute_values[attribute_number][y]:
				sv += 1
				if x[target] == positive:
					sp  += 1
				elif x[target] == negative:
					sn += 1
		val = (entropy_pnv(sp,sn,sv)*float(sv)/float(len(example_list)))
		Esv += val
	return entropy-Esv




def all_pos(example_list,target):
	positive = attribute_set.positive
	negative = attribute_set.negative

	for x in example_list :
		if x[target] == attribute_set.negative :
			return 0
	return 1

def all_neg(example_list,target):
	positive = attribute_set.positive
	negative = attribute_set.negative	
	for x in example_list:
		if x[target] == attribute_set.positive :
			return 0
	return 1


def base_check(max_depth,example_list,target,vis):
	if max_depth == 0:
		return 1
	else:
		if all_pos(example_list,target):
			return 1
		elif all_neg(example_list,target):
			return 1
		else:
			for x in vis:
				if x == 0:
					return 0
			return 1
	return 0

def solve_missing_values(instance,example_list,attribute,target) :
	attribute_values  = attribute_set.attribute_values[attribute]
	sz = len(attribute_values)
	freq_pos = [0]*sz
	freq_neg = [0]*sz
	
	for i in range(sz) :
		for x in example_list :
			if x[attribute] == attribute_values[i] :
				if x[target] == attribute_set.positive :
					freq_pos[i] += 1
				elif x[target] == attribute_set.negative :
					freq_neg[i] += 1
	
	new_instance = instance.copy()
	if new_instance[attribute] == '?' :
			if new_instance[target] == attribute_set.positive :
				new_instance[attribute] = attribute_values[freq_pos.index(max(freq_pos))]
			elif new_instance[target] == attribute_set.negative :
				new_instance[attribute] = attribute_values[freq_neg.index(max(freq_neg))]

	return new_instance

def build_tree(max_depth,example_list,target,vis) :
	positive = attribute_set.positive
	negative = attribute_set.negative

	if base_check(max_depth,example_list,target,vis) == 1 :
		#make leaf
		leaf_node = node(target,example_list)
		leaf_node.leaf = 1
		p_count = 0
		n_count = 0	

		# assign most common result in verdict
		for x in example_list:
			if x[target] == positive:
				p_count += 1
			if x[target] == negative:
				n_count += 1	

		if p_count > n_count:
			leaf_node.target_val = positive
		else:
			leaf_node.target_val = negative
		return leaf_node 		# return node
	else:
		max_att = 0
		index = 0
		curr_max_gain = -1000000
		for x in vis:
			if x == 0:
				# selecting best attribute
				temp_gain = calc_info_gain(index,example_list,target)
				if curr_max_gain <= temp_gain:
					curr_max_gain = temp_gain
					max_att = index
			index += 1
		# //we divide example_list over max_att

		temp_vis = vis.copy();
		temp_vis[max_att] = 1;
		present_node = node(max_att,example_list)

		for i in range(len(attribute_set.attribute_values[max_att])) :

			example_list_v = []
			for j in example_list:
				instance = j;
				if j[max_att] == '?' :
					instance = solve_missing_values(j,example_list,max_att,target)

				if attribute_set.attribute_values[max_att][i] == instance[max_att]:
					example_list_v.append(j)
			if len(example_list_v) == 0:
				
				# add leaf here
				branch_node = node(target,example_list_v)
				branch_node.leaf = 1
				p_count = 0
				n_count = 0

				# assign most common result in verdict
				for x in example_list:
					if x[target] == positive:
						p_count += 1
					if x[target] == negative:
						n_count += 1

				if p_count > n_count:
					branch_node.target_val = positive
				else:
					branch_node.target_val = negative
				present_node.child[i]['pointer'] = branch_node
			
			else:
				present_node.child[i]['pointer'] = build_tree(max_depth-1,example_list_v,target,temp_vis)

		return present_node










def getVerdict(my_node,data_instance,target):
	if my_node.leaf == 1 :
		return my_node.target_val

	att_num = my_node.attribute_number
	instance = copy.deepcopy(data_instance)
	
	if instance[att_num] == '?' :
		instance = solve_missing_values(instance,my_node.example_list,att_num,target)
	for x in my_node.child:
		if x['edge'] == instance[att_num]:
			return getVerdict(x['pointer'],data_instance,target)


def getAccuracy(tree_node,example_list,target):
	res = 0
	total = 0
	for x in example_list:
		predicted = getVerdict(tree_node,x,target)
		if x[target] == predicted :
			res += 1
		total += 1

	print("res=",res)
	print("total=",total)
	return res/total





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


	example_list = []
	with open('breast-cancer.csv',newline = '') as f :
		reader = csv.reader(f)
		example_list = list(reader)


	d1 = data_set(len(example_list),example_list)	

	target_attribute = 0

	for x in range(11):
		vis = [0]*len(attribute_set.attribute_names)
		vis[target_attribute] = 1;
		getAccuracy(build_tree(x, example_list, target_attribute,vis),example_list,target_attribute)
	

if __name__ == '__main__':
    main()