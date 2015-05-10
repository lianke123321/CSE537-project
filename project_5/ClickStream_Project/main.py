# main file for test ID3 decision tree

import ID3
import Helper

# This part is for test a simple case in the slides
simple_feature = [[1, 1, 1, 1],
                  [1, 1, 1, 2],
                  [2, 1, 1, 1],
                  [3, 2, 1, 1],
                  [3, 3, 2, 1],
                  [3, 3, 2, 2],
                  [2, 3, 2, 2],
                  [1, 2, 1, 1],
                  [1, 3, 2, 1],
                  [3, 2, 2, 1],
                  [1, 2, 2, 2],
                  [2, 2, 1, 2],
                  [2, 1, 2, 1],
                  [3, 2, 1, 2]]

simple_label = [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0]
simple_name = ["outlook","temperature","humidity","wind"]
used = [False for i in range(0, 4)]
# You can test the algorithm by use simple_feature and simple label
# instead of trainf and testf

trainf = 'trainfeat.csv'
testf  = 'testfeat.csv'
trainl = 'trainlabs.csv'
testl  = 'testlabs.csv'
fname  = 'featnames.csv'

train_feature, train_label, \
test_feature,  test_label, \
feature_name = Helper.readData(trainf, trainl, testf, testl, fname)

print "finish reading data!"

dc_tree = ID3.ID3Tree(0.05)
dc_tree.trainDTree(train_feature, train_label)
#dc_tree.trainDTree(simple_feature, simple_label)
predict, precision, recall, accuracy = dc_tree.predictSet(test_feature, test_label)
print "Node in the decision tree is: %d" % dc_tree.number_nodes

print "Precision is: %.3f" %precision
print "Recall is: %.3f" %recall
print "Accuracy is: %.3f" %accuracy

