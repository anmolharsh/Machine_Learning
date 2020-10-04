*** Installations **

$ pip install pandas
$ pip install graphviz
$ sudo apt-get install graphviz
$ pip install matplotlib
$ pip install numpy


*** Instructions **

To run the file --> (in the terminal)
$ python main.py

Terminal:
After running the file we see:
	Initial best_depth and max_accuracy
	Pruned nodes and the change in accuracy (new_accuracy, old_accuracy)
	Final maximum accuracy


To see the image of the tree --> (in the terminal)
after running : python main.py
Run: $	dot -Tpng finaltree.gv -o finaltree.png

-> g1 & g2 are the graphs formed after running the code.
-> set depth to -1 to allow tree to grow as much as possible
-> to see the plot in 2nd ques. kindly run in jupyter notebook