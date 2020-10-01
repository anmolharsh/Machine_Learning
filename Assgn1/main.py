import ast
import csv
import sys
import math
import os





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


def entropy_pnv(sp,sn,sv):
	if(sp==sv or sn==sv or sp==0 or sn==0):
		return 0

	# if sp==sn:
	# 	return 1
	# sp=(sp*1)/sv
	# sn=(sn*1)/sv
	# res=(-1)*(sp*math.log(sp,2)+sn*math.log(sn,2))

	res=(-1)*(sn*(math.log(sn,2)) + sp*(math.log(sp,2)) - (sn+sp)*(math.log(sv,2)))
	return res


#calcs |s|*Entropy(s)
def calc_entropy(example_list,target):
	p_pos = 0
	p_neg = 0
	# res=0
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
<<<<<<< HEAD
	entropy=calc_entropy(example_list,target) # Entropy(S)
=======

	entropy=calc_entropy(example_list,target) # |S|*Entropy(S)
>>>>>>> 5d2f047e1244c57809691b13122260d3ab055b2e
	# segregated_list=[]
	Esv = 0
	# for x in attribute_set.attribute_values[attribute_number]:
		# segregated_list.append((0,0)) 		# ( #+ , #- )
	for y in range(len(attribute_set.attribute_values[attribute_number])):
		sp = 0
		sn = 0
		sv = 0
		for x in example_list:
			if x[attribute_number]==attribute_set.attribute_values[attribute_number][y]:
				sv+=1
				if x[target]==positive:
					sp+=1
				elif x[target]==negative:
					sn+=1
		Esv+=(entropy_pnv(sp,sn,sv))
	# print(entropy," ",Esv," ",Esv/len(example_list))
		# we calculate |S|Entropy(S) - E |Sv|Entropy(Sv) 
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
			# print("all_pos ",max_depth)
			return 1
		elif all_neg(example_list,target):
			# print("all_neg ",max_depth)
			return 1
		else:
			for x in vis:
				if x==0:
					return 0
			# print("no att ",max_depth)
			return 1
	return 0

def solve_missing_values(example_list,attribute,target) :
	new_list = []
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
	
	for x in example_list :
		new_x = x.copy()
		if new_x[attribute] == '?' :
			if new_x[target] == attribute_set.positive :
				new_x[attribute] = freq_pos.index(max(freq_pos))
			elif new_x[target] == attribute_set.negative :
				new_x[attribute] = freq_neg.index(max(freq_neg))
		new_list.append(new_x)		

	return new_list

<<<<<<< HEAD
def build_tree( max_depth , example_list , target, attribute_set , vis ) :
	positive = attribute_set.positive
	negative = attribute_set.negative

	if base_check(max_depth,example_list,target,attribute_set,vis)==1 :
=======

def build_tree(max_depth,example_list,target,vis) :
	positive = attribute_set.positive
	negative = attribute_set.negative

	if base_check(max_depth,example_list,target,vis)==1 :
>>>>>>> 5d2f047e1244c57809691b13122260d3ab055b2e
		#make leaf
		leaf_node=node(target)
		leaf_node.leaf=1
		p_count=0
		n_count=0	
		# print("leaf_node")

		# assign most common result in verdict
		for x in example_list:
			if x[target] == positive:
				p_count += 1
			if x[target] == negative:
				n_count += 1


		if p_count >= n_count:
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
<<<<<<< HEAD
				temp_gain=calc_info_gain(index,example_list,target,attribute_set)
				# print(index," " , temp_gain, " " , curr_max_gain, " " , max_depth)
				if curr_max_gain <= temp_gain:
					curr_max_gain = temp_gain
=======
				temp_gain=calc_info_gain(index,example_list,target)
				print(index," ",temp_gain, " ", max_depth)
				if curr_max_gain<=temp_gain:
					curr_max_gain=temp_gain
>>>>>>> 5d2f047e1244c57809691b13122260d3ab055b2e
					max_att=index
			index+=1
		# //we divide example_list over max_att

		if curr_max_gain==0:
			#make leaf
			leaf_node=node(target)
			leaf_node.leaf=1
			p_count=0
			n_count=0
			# assign most common result in verdict
			for x in example_list:
				if x[target] == positive:
					p_count += 1
				if x[target] == negative:
					n_count += 1
			if p_count >= n_count:
				leaf_node.target_val = positive
			else:
				leaf_node.target_val = negative
			return leaf_node


		temp_vis = []
		for v in vis:
			temp_vis.append(v)
		temp_vis[max_att] = 1
		temp_example_list = solve_missing_values(example_list,max_att,target)
		present_node = node(max_att)
		for i in range(len(attribute_set.attribute_values[max_att])) :
			example_list_v = []
<<<<<<< HEAD
			for j in example_list:
=======
			for j in temp_example_list:
>>>>>>> 5d2f047e1244c57809691b13122260d3ab055b2e
				if attribute_set.attribute_values[max_att][i] == j[max_att]:
					example_list_v.append(j)
			if len(example_list_v) == 0:
				# add leaf here
				# print("branch leaf ",max_depth)
				branch_node=node(target)
				branch_node.leaf=1
				p_count=0
				n_count=0
				# assign most common result in verdict
				for x in temp_example_list:
					if x[target] == positive:
						p_count += 1
					if x[target] == negative:
						n_count += 1
				if p_count >= n_count:
					branch_node.target_val = positive
				else:
					branch_node.target_val = negative
				present_node.child[i]['pointer'] = branch_node
			else:
<<<<<<< HEAD
				present_node.child[i]['pointer'] = build_tree(max_depth-1,example_list_v,target,attribute_set ,temp_vis)
=======
				present_node.child[i]['pointer'] = build_tree(max_depth-1,example_list_v,target,vis)
>>>>>>> 5d2f047e1244c57809691b13122260d3ab055b2e

		return present_node

















def getVerdict(my_node,data_instance,target):
	if my_node.leaf==1 or my_node==None:
		return my_node.target_val
	att_num=my_node.attribute_number
	for x in my_node.child:
		if x['edge']==data_instance[att_num]:
			# print(x['edge'])
			return getVerdict(x['pointer'],data_instance,target)
	return attribute_set.positive #strange line


def getAccuracy(tree_node,example_list,target):
	res = 0
	total = 0
	for x in example_list:
		if x[target]==getVerdict(tree_node,x,target):
			res+=1
		total+=1
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

		# print(attribute_set.attribute_names)
		# print(attribute_set.attribute_values)

	example_list = []
	with open('breast-cancer.csv',newline = '') as f :
		reader = csv.reader(f)
		example_list = list(reader)
		# print(example_list)


	d1 = data_set(len(example_list),example_list)	
	# print(d1.example_list,d1.sz)
	# new_node = node(1)
	# print(new_node.child)
	vis = []
	target_attribute = 0
	for x in range(len(attribute_set.attribute_names)):
		vis.append(0)
	vis[target_attribute]=1
	print("entropy(S) = ",calc_entropy(example_list,target_attribute))
	print("gain for 1st att = ",calc_info_gain(1 ,example_list ,target_attribute) )
	print(vis)
	new_node = build_tree(140, example_list, target_attribute, attribute_set, vis)
	print("\nroot_node-->\n",new_node.child)
	print(new_node.child[0]['pointer'].child)
	getAccuracy(new_node,example_list[0:],target_attribute)
	print(vis)

	# iter for height
<<<<<<< HEAD
	# newnode=[]
	# for x in range(11):
	# 	newnode.append(build_tree(x, example_list, target_attribute, attribute_set, vis))
=======
	newnode=[]
	for x in range(11):
		newnode.append(build_tree(x, example_list, target_attribute,vis))
>>>>>>> 5d2f047e1244c57809691b13122260d3ab055b2e

	# print("\ndonez\n")
	# for x in range(11):
	# 	getAccuracy(newnode[x],example_list,target_attribute)

	# print((-10)/2)


if __name__ == '__main__':
    main()