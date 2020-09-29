import csv

class attributes_set:
	attributes = {}
	attributes['class'] = {'recurrence-events','recurrence-events'}

def main():
	with open('breast-cancer.csv',newline = '') as f :
		reader = csv.reader(f);
		for row in reader :
			print(', '.join(row))
	print(attributes_set.attributes)

if __name__ == '__main__':
    main()