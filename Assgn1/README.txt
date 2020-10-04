*** Installations **

$ pip install pandas
$ pip install graphviz
$ sudo apt-get install graphviz
$ pip install matplotlib
$ pip install numpy


*** Instructions **

To run the file --> (in the terminal)
$ python main.py

Parameters : 
	1) dataset_path : set the dataset path to load the dataset
	2) depth_input : depth input for the first part 
	3) ITERATIONS : no. of iterations in the first part (set to 10)
	4) MAX_DEPTH : no. of depths data we want to get in the 2nd part
	5) save_model_name : name given to the saved model trained
	6) load_model_name : name of the model we want to load


To see the image of the tree --> (in the terminal)
after running : python main.py
Run: $	dot -Tpng finaltree.gv -o finaltree.png

-> g1 & g2 are the graphs formed after running the code.
-> set depth to -1 to allow tree to grow as much as possible
-> to see the plot in 2nd ques. kindly run in jupyter notebook