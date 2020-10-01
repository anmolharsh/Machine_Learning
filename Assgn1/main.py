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


def entropy_pnv(sp,sn,sv):
	if(sp==sv or sn==sv):
		return 0
	if sp==sn:
		return 1
	sp=sp/sv
	sn=sn/sv
	res=(-1)*(sp*math.log(sp,2)+sn*math.log(sn,2))
	return res



def calc_entropy(example_list):
	p_pos=0
	p_neg=0
	# res=0
	for x in example_list:
		if x[0]==positive:
			p_pos+=1
		elif x[0]==negative:
			p_neg+=1
	return entropy_pnv(p_pos,p_neg,len(example_list))


def calc_info_gain(attribute_number,example_list) :
	entropy=calc_entropy(example_list)
	# segregated_list=[]
	Esv=0
	# for x in attribute_set.attribute_values[attribute_number]:
		# segregated_list.append((0,0)) 		# ( #+ , #- )
	for y in range(len(attribute_set.attribute_values[attribute_number])):
		sp=0
		sn=0
		sv=0
		for x in example_list:
			if x[attribute_number]==attribute_set.attribute_values[attribute_number][y]:
				sv+=1
				if x[0]==positive:
					sp+=1
				elif x[0]==negative:
					sn+=1
		Esv+=entropy_pnv(sp,sn,sv)*((sv)/len(example_list))
	return entropy-Esv




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
		curr_max_gain=0
		for x in vis:
			if x==0:
				# selecting best attribute
				if curr_max_gain<calc_info_gain(index,example_list):
					max_att=index
			index+=1
		# //we divide example_list over max_att
		vis[max_att]=1

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
	print("entropy(S) = ",calc_entropy(example_list))
	print(calc_info_gain(1,example_list))

if __name__ == '__main__':
    main()