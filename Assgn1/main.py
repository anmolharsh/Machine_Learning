import ast
import csv
import sys
import math
import os





class attribute_set:
	attribute_names = []
	attribute_values = []
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
	if(sp==sv or sn==sv):
		return 0
	if sp==sn:
		return 1
	sp=(sp*100)/sv
	sn=(sn*100)/sv

	res=(-1)*(sp*math.log(sp,2)+sn*math.log(sn,2))
	# res=(-1)*(sn*(math.log(sn,2)) + sp*(math.log(sp,2)) - (2)*(math.log(sv,2)))
	return res


#calcs |s|*Entropy(s)
def calc_entropy(example_list,target):
	p_pos=0
	p_neg=0
	# res=0
	positive = attribute_set.positive
	negative = attribute_set.negative
	for x in example_list:
		if x[target]==positive:
			p_pos+=1
		elif x[target]==negative:
			p_neg+=1
	return entropy_pnv(p_pos,p_neg,len(example_list))


def calc_info_gain(attribute_number,example_list,target,attribute_set_all) :
	positive = attribute_set.positive
	negative = attribute_set.negative
	entropy=calc_entropy(example_list,target)
	# segregated_list=[]
	Esv=0
	# for x in attribute_set.attribute_values[attribute_number]:
		# segregated_list.append((0,0)) 		# ( #+ , #- )
	for y in range(len(attribute_set_all.attribute_values[attribute_number])):
		sp=0
		sn=0
		sv=0
		for x in example_list:
			if x[attribute_number]==attribute_set_all.attribute_values[attribute_number][y]:
				sv+=1
				if x[target]==positive:
					sp+=1
				elif x[target]==negative:
					sn+=1
		Esv+=(entropy_pnv(sp,sn,sv)*sv)
		print(entropy," ",Esv," ",Esv/len(example_list))

	return entropy-(Esv/1)




def all_pos(example_list,target):
	for x in example_list:
<<<<<<< HEAD
		if x[target]==negative:
=======
		if x[0]==attribute_set.negative:
>>>>>>> a3b1aa7ea6e2015d3b34c7fcd15003bf3200db0d
			return 0
	return 1

def all_neg(example_list,target):
	for x in example_list:
<<<<<<< HEAD
		if x[target]==positive:
=======
		if x[0]==attribute_set.positive:
>>>>>>> a3b1aa7ea6e2015d3b34c7fcd15003bf3200db0d
			return 0
	return 1


def base_check(max_depth,example_list,target,all_att,vis):
	if max_depth==0:
		return 1
	else:
		if all_pos(example_list,target):
			print("all_pos ",max_depth)
			return 1
		elif all_neg(example_list,target):
			print("all_neg ",max_depth)
			return 1
		else:
			for x in vis:
				if x==0:
					return 0
			print("no att ",max_depth)
			return 1
	return 0


def build_tree(max_depth,example_list,target, attribute_set_all,vis) :
<<<<<<< HEAD
	if base_check(max_depth,example_list,target,attribute_set_all,vis)==1 :
=======
	positive = attribute_set.positive
	negative = attribute_set.negative

	if base_check(max_depth,example_list,attribute_set_all,vis)==1 :
>>>>>>> a3b1aa7ea6e2015d3b34c7fcd15003bf3200db0d
		#make leaf
		leaf_node=node(target)
		leaf_node.leaf=1
		p_count=0
<<<<<<< HEAD
		n_count=0
		print("leaf_node")
=======
		n_count=0	
>>>>>>> a3b1aa7ea6e2015d3b34c7fcd15003bf3200db0d
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
		curr_max_gain = 0
		for x in vis:
			if x == 0:
				# selecting best attribute
				temp_gain=calc_info_gain(index,example_list,target,attribute_set)
				print(index," ",temp_gain, " ", max_depth)
				if curr_max_gain<=temp_gain:
					curr_max_gain=temp_gain
					max_att=index
			index+=1
		# //we divide example_list over max_att
		# temp_vis[max_att]=1
		temp_vis = []
		for v in vis:
			temp_vis.append(v)
		temp_vis[max_att] = 1
		present_node = node(max_att)
		for i in range(len(attribute_set.attribute_values[max_att])):
			example_list_v = []
			for j in example_list:
				if attribute_set_all.attribute_values[max_att][i] == j[max_att]:
					example_list_v.append(j)
			if len(example_list_v) == 0:
				# add leaf here
				# print("branch leaf ",max_depth)
				branch_node=node(target)
				branch_node.leaf=1
				p_count=0
				n_count=0
				# assign most common result in verdict
				for x in example_list:
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
				present_node.child[i]['pointer'] = build_tree(max_depth-1,example_list_v,target,attribute_set_all,temp_vis)

		return present_node

















def getVerdict(my_node,data_instance,target):
	if my_node.leaf==1 or my_node==None:
		return my_node.target_val
	att_num=my_node.attribute_number
	for x in my_node.child:
		if x['edge']==data_instance[att_num]:
			# print(x['edge'])
			return getVerdict(x['pointer'],data_instance,target)
	


def getAccuracy(tree_node,example_list,target):
	res=0
	total=0
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
	vis=[]
	target_attribute=0
	for x in range(len(attribute_set.attribute_names)):
		vis.append(0)
	vis[target_attribute]=1
	print("entropy(S) = ",calc_entropy(example_list,target_attribute))
	print("gain for 1st att = ",calc_info_gain(1 ,example_list ,target_attribute , attribute_set ) )
	print(vis)
	# new_node = build_tree(140, example_list, target_attribute, attribute_set, vis)
	# print("\nroot_node-->\n",new_node.child)
	# print(new_node.child[1]['pointer'].child)
	# getAccuracy(new_node,example_list[0:],target_attribute)
	# print(vis)

	# iter for height
	newnode=[]
	for x in range(11):
		newnode.append(build_tree(x, example_list, target_attribute, attribute_set, vis))

	print("\ndonez\n")
	for x in range(11):
		getAccuracy(newnode[x],example_list,target_attribute)

	# print((-10)/2)

if __name__ == '__main__':
    main()