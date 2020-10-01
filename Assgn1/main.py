import csv
import math

class attribute_set:
	attribute_names = []
	attribute_values = []
	target_attribute = None
	pos = None
	neg = None

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


class tree :

	def __init__(self,root) :
		self.root = root

def calc_entropy(p,n) :
	s = p+n
	p = p/s
	n = n/s
	entropy = -p*math.log2(p) - n*math.log2(n)
	return entropy

def calc_info_gain(attribute_number,example_list) :
	value_list  = attribute_set.attribute_values[attribute_number]
	p = 0
	n = 0
	for x in example_list :
		p += (x[0] == attribute_set.pos)
		n += (x[0] == attribute_set.neg)
	s_entropy = calc_entropy(p,n)
	print(s_entropy)


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

	attribute_set.target_attribute = attribute_set.attribute_names[0];
	attribute_set.neg = attribute_set.attribute_values[0][0]
	attribute_set.pos = attribute_set.attribute_values[0][1]
	
	example_list = []
	with open('breast-cancer.csv',newline = '') as f :
		reader = csv.reader(f)
		example_list = list(reader)

	d1 = data_set(len(example_list),example_list)	
	# print(d1.example_list,d1.sz)
	new_node = node(1)
	print(new_node.child)
	calc_info_gain(0,example_list)

if __name__ == '__main__':
    main()