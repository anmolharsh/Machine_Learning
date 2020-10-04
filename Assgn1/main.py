import ast
import csv
import sys
import math
import os
import copy
import random
import matplotlib.pyplot as plt
import numpy as np


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
			if x[attribute_number] == '?' :
				instance = copy.deepcopy(x)
				instance = solve_missing_values(x,example_list,attribute_number,target)

				if instance[attribute_number] == attribute_set.attribute_values[attribute_number][y]:
					sv += 1
					if instance[target] == positive:
						sp  += 1
					elif instance[target] == negative:
						sn += 1
			else :
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






#print tree

def add_nodes(mynode,f,node_num):
	s=""
	
	if mynode.leaf==1:
		s+=str(node_num[0])
		s+=" [label=\""
		s+=str(mynode.target_val)
		if mynode.target_val==attribute_set.positive:
			s+="\",color=\"seagreen\"]\n"
		else:
			s+="\",color=\"red3\"]\n"
		f.write(s)
		return ;
	# node_num+=1
	s+=str(node_num[0])
	s+=" [label=\""
	s+=attribute_set.attribute_names[mynode.attribute_number]
	s+="\",color=\"purple3\"]\n"
	f.write(s)
	for i in mynode.child:
		node_num[0]+=1
		add_nodes(i['pointer'],f,node_num)
	return;


def add_edges(mynode,f,node_num):
	if mynode.leaf==1:
		return 
	s=""
	p_num=node_num[0]
	for i in mynode.child:
		node_num[0]+=1
		s+=str(p_num)
		s+=" -> "
		s+=str(node_num[0])
		s+=" [label=\""
		s+=i['edge']
		s+="\"]\n"

		add_edges(i['pointer'],f,node_num)
	f.write(s)
	return; 


def same_rank(mynode,f,node_num):
	if mynode.leaf==1:
		return
	s=""
	# s="subgraph cluster_"
	# s+=str(node_num[0])
	# s+=" {\n"
	s+="{rank=same;"
	for i in mynode.child:
		node_num[0]+=1
		s+=str(node_num[0])
		s+=" ;"
		same_rank(i['pointer'],f,node_num)
	# s+=" }\n\t}\n"
	s+=" }\n"
	f.write(s)
	return



def tree_img(tree_node):
	f=open("addnode.gv","w+")
	s="digraph{\nnode [shape=box]\n\n"
	f.write(s)
	temp=[]
	temp.append(1)
	add_nodes(tree_node,f,temp)
	# f.close()
	temp[0]=1
	add_edges(tree_node,f,temp)

	temp[0]=1
	# s="subgraph cluster_R {\n"
	# f.write(s)
	same_rank(tree_node,f,temp)

	# s="\t\n}\n}\n"
	s="\n}\n"
	f.write(s)
	f.close()










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
	#print(attribute_set.attribute_names[tree_node.attribute_number])
	for x in example_list:
		predicted = getVerdict(tree_node,x,target)
		if x[target] == predicted :
			res += 1
		total += 1

	# print("res=",res)
	# print("total=",total)
	return float(res)/total


def find_best_Depth(example_list,target) :
	best_trainining_set = []
	best_validation_set = []
	best_test_set = []
	best_tree = None

	first_limit = round(len(example_list)*(0.6))
	second_limit = first_limit + round((len(example_list)*(0.2)))
	
	max_accuracy = 0
	best_depth = -1
	x_points = []
	y_points = []
	z_points = [] # 2 graph
	for i in range(1,11) :
		sum_accuracy = 0
		sum_accuracy_training = 0 #2 graph
		local_max_accuracy = 0
		local_best_training_set = []
		local_best_validation_set = []
		local_best_test_set = []
		local_best_tree = None
		for j in range(10) :
			random.Random(i*10).shuffle(example_list)
			curr_training_set = example_list[0:first_limit]
			curr_validation_set = example_list[first_limit:second_limit]
			curr_test_set = example_list[second_limit:]
			vis = [0]*len(attribute_set.attribute_names)
			vis[target] = 1;
			root = build_tree(i,curr_training_set,target,vis)
			curr_accuracy = getAccuracy(root,curr_test_set,target)
			sum_accuracy += curr_accuracy
			curr_accuracy_training = getAccuracy(root,curr_training_set,target)
			sum_accuracy_training += curr_accuracy_training
			
			if curr_accuracy > local_max_accuracy :
				local_best_trainining_set = curr_training_set
				local_best_validation_set = curr_validation_set
				local_best_test_set = curr_test_set
				local_max_accuracy = curr_accuracy
				local_best_tree = root

		avg_accuracy = sum_accuracy/float(10)
		avg_accuracy_training = sum_accuracy_training/float(10)
		
		x_points.append(i)
		y_points.append(avg_accuracy)
		z_points.append(avg_accuracy_training)
		
		if avg_accuracy > max_accuracy :
			best_trainining_set = local_best_training_set
			best_validation_set = local_best_validation_set
			best_test_set = local_best_test_set
			max_accuracy = avg_accuracy
			best_depth = i
			best_tree = local_best_tree

		
	return best_depth,best_validation_set,best_tree,max_accuracy,x_points,y_points,z_points		

def prune_tree(depth,top_root,sub_root,validation_set,max_accuracy,target) :

	if sub_root.leaf == 1 :
		return 0

	for x in sub_root.child:
		max_accuracy = max(max_accuracy,prune_tree(depth+1,top_root,x['pointer'],validation_set,max_accuracy,target))
		

	sub_root.leaf = 1
	p_count = 0
	n_count = 0
	for x in sub_root.example_list :
		p_count += (x[target] == attribute_set.positive)
		n_count += (x[target] == attribute_set.negative)

	sub_root.target_val = attribute_set.positive if p_count >= n_count else attribute_set.negative

	new_accuracy = getAccuracy(top_root,validation_set,target)

	#print(attribute_set.attribute_names[sub_root.attribute_number], new_accuracy, max_accuracy)
	if new_accuracy > max_accuracy :
		print("at depth =",depth,attribute_set.attribute_names[sub_root.attribute_number], " got pruned", new_accuracy, max_accuracy)
		max_accuracy = new_accuracy
	else :
		sub_root.leaf = 0
		sub_root.target_val = None

	return max_accuracy

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

	best_depth,validation_set,prune_root,max_accuracy,x,y,z = find_best_Depth(example_list,target_attribute)

	# print(x)
	# print(y)
	print(best_depth,max_accuracy)
	print(prune_tree(0,prune_root,prune_root,validation_set,max_accuracy,target_attribute))
	fig, ax = plt.subplots()  # Create a figure and an axes.
	# print(x,y)
	plt.xlim(1, 10)
	plt.ylim(0.5, 1.00)
	plt.figtext(0.65, 0.20, "BLUE = Training_set" , color='blue')
	plt.figtext(0.65, 0.15, "RED = Test_set" , color='red')
	ax.plot(x, y,'red')  # Plot some data on the axes.
	ax.plot(x, z,'blue')
	ax.set_xlabel('Depth')  # Add an x-label to the axes.
	ax.set_ylabel('Average Accuracy')  # Add a y-label to the axes.
	ax.set_title("Accuracy of the tree vs Depth of the tree ")  # Add a title to the axes.
	plt.savefig('plot.png')
	tree_img(prune_root)

	# seed_values = []
	# for i in range(150) : 
	# 	temp_list = copy.deepcopy(example_list)
	# 	best_depth,validation_set,prune_root,max_accuracy,x,y = find_best_Depth(i,temp_list,target_attribute)
	# 	if best_depth <= 3 :
	# 		new_accuracy = prune_tree(0,prune_root,prune_root,validation_set,max_accuracy,target_attribute)
	# 		if new_accuracy > max_accuracy :
	# 			seed_values.append(i)
	# 			print("seed = ", i)
	# 			print("best_depth = ",best_depth)
	# 			print("before = ",max_accuracy)
	# 			print("after = ",new_accuracy,'\n')
			 
	# print(seed_values)			


		
		

	
	

if __name__ == '__main__':
    main()