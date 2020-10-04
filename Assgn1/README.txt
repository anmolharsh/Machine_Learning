*** Installations **

$ pip install pandas
$ pip install graphviz
$ sudo apt-get install graphviz
$ pip install matplotlib
$ pip install numpy


*** Instructions **

To run the file --> (in the terminal)
First download and extract data file from https://drive.google.com/drive/folders/1BpLqIlO2UHe6Q4XKVUpNdM38UjkG5pvH?usp=sharing
Extract the data file and the assgn1 zip file in a common folder
Run:  
 $ python main.py

Terminal:
After running the file we see:
	Initial best_depth and max_accuracy
	Pruned nodes and the change in accuracy (new_accuracy, old_accuracy)
	Final maximum accuracy


To see the image of the tree --> (in the terminal)
after running : python main.py
Run:
 $	dot -Tpng finaltree.gv -o finaltree.png

Open 'plot.png' to view the plot of Accuracy vs Depth 
Open 'finaltree.png' to view the tree
