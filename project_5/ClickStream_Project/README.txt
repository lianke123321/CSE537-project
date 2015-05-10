Three source file for ClickStream Project

1. Helper.py:
	This file is used for readin the data for training and testing.
	All the data should be placed at the same directory as this script.

2. ID3.py:
	This file implement the decision tree algorithm. It reads in data
	to train the decision tree and one can set the threshold when 
	initiating the ID3 object.
	
3. main.py:
	Main function of the Project. Read in the data, constructing the 
	decision tree, make prediction and print the result.


Platform requirement:
	Code is written under Windows, python2.7. So basically it should 
	work on any system running python2.7.
	
	Also, in order to compute the p-value for chi-square distribution.
	You need to have scipy library that works for python2.7.