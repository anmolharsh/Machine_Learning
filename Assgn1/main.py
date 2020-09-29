import csv

class attribute_set:
	attribute_names = []
	attribute_values = []
	
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
		reader = csv.reader(f);

	

if __name__ == '__main__':
    main()