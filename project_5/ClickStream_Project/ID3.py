
from math import log
from scipy import stats

class ID3Tree:

    def __init__(self, threshold):
        # reference to training set and label
        self.threshold = threshold
        self.number_nodes = 0

    def trainDTree(self, train, label):
        ''' train a decision tree by training set and labels
        :param train: training data
        :param label: label for training data
        '''

        print "Start Training"
        used = [False for i in range(0, len(train[0]))]

        self.root = self.generateTree(train, label, used)
        print "Done Training"

    def generateTree(self, train, label, used):
        '''
        :param train: generate a tree
        :param label:
        :return: a node that is the root of the subtree
        '''

        root = Node(-1)
        tmp_label, isSame = self.getMajority(label)
        # add one node here
        self.number_nodes += 1

        # if all the feature have been used
        if False not in used:
            print "No feature to use"
            # mark this node as leaf node
            root.setLeaf()
            # set predict label as majority label
            root.setLabel(tmp_label)
            return root
        elif isSame:
            # if the label are all the same
            root.setLeaf()
            root.setLabel(tmp_label)
            return root
        else:
            # choose the best feature to classify
            best_index = self.chooseBestFeature(train, label, used)
            print "Choose feature:%d as best one" %best_index

            if best_index >= len(train[0]):
                print "Big error, best feature index exceeds limit"
                exit()
            # set the feature_index as
            root.setFeatureIndex(best_index)

            split_dataset = {}
            # traversing for every value for this feature
            for val in self.getValues(train, best_index):
                # generate subtree here
                sub_train, sub_label, new_used = self.splitDataSet(train, best_index, label, used, val)
                split_dataset[val] = [sub_train, sub_label, new_used]


            # use the chi-square test to test relevance
            # if irrelevant just stops here and uses majority as label
            num_pos = 0.0
            num_neg = 0.0
            for l in label:
                if l == 0:
                    num_neg += 1
                else:
                    num_pos += 1

            S = 0.0
            for k,v in split_dataset.iteritems():
                pi = num_pos * len(v[1])/float(len(train))
                ni = num_neg * len(v[1])/float(len(train))
                r_pi = 0.0
                r_ni = 0.0
                for l in v[1]:
                    if l == 0:
                        r_ni += 1
                    else:
                        r_pi += 1
                # add to S
                tmp = 0
                if r_pi != 0:
                    tmp += pow(r_pi - pi, 2)/r_pi

                if r_ni != 0:
                    tmp += pow(r_ni - ni, 2)/r_ni

                S += tmp

            # compute the p_value by scipy
            p_value = 1 - stats.chi2.cdf(S, len(split_dataset))
            print "chi-square p-value is: %.3f" %p_value

            if p_value < self.threshold:
                for k,v in split_dataset.iteritems():
                    child = self.generateTree(v[0], v[1], v[2])
                    # add child to this root node
                    root.addChild(child, k)
            else:
                root.setLeaf()
                root.setLabel(tmp_label)
                return root

        return root

    def predictSet(self, test_feature, test_label):
        '''
        Predict a set of samples
        :param test_feature: test set data
        :param test_label: test set label
        :return: predict labels and statistics of the results
        '''
        predict = []
        cnt = 0
        for f in test_feature:
            cnt += 1
            if (cnt % 50) == 0:
                print "Test %d sample"%cnt
            label = self.predictOne(f)
            predict.append(label)

        print "Done predict test set"
        # compute precision and recall for predict labels
        TT = 0
        TF = 0
        FT = 0
        FF = 0

        for (t, p) in zip(test_label, predict):
            if t:
                # true_label is yes
                if p:
                    # predict is yes
                    TT += 1
                else:
                    TF += 1
            else:
                # true_label is no
                if p:
                    # predict is yes
                    FT += 1
                else:
                    FF += 1

        # Do the evaluation here
        precision = TT/float(FT+TT)
        recall = TT/float(TT+TF)
        accuracy = (TT + FF) / float(len(test_label))

        return predict, precision, recall, accuracy

    def predictOne(self, sample):
        ''' use feature to predict label for new sample
        :param sample: a feature vector for a new sample
        :return: 0 or 1 as predict result
        '''

        tmp_node = self.root

        # if we can not judge the label
        # we should loop
        stop = tmp_node.canJudge()
        while not stop:
            f_index = tmp_node.getFeatureIndex()
            #print "Go through feature:%s" % self.attribute[f_index]
            # the value for the sample in this feature
            f_val = sample[f_index]
            tmp_node = tmp_node.getNext(f_val)
            stop = tmp_node.canJudge()

        # if current node can judge the label
        return tmp_node.predictLabel()

    def splitDataSet(self, train, f_index, label, used, f_value):
        '''
        Split the training set: extract subset whose f_index value is f_value
        And extract subset of label as well. Also update the used list
        :param train: whole training set to be split
        :param f_index: based on which feature should we split
        :param label: the label set to be split
        :param used: which feature have we used now, update used[f_index] to be True
        :param f_value: feature value of f_index
        :return: subset for train and subset for label
        '''

        sub_train = []
        sub_label = []
        new_used = used[:]

        for t, l in zip(train, label):
            if t[f_index] == f_value:
                # collect sample where feature value is f_value
                sub_train.append(t)
                sub_label.append(l)

        new_used[f_index] = True
        return sub_train, sub_label, new_used

    def getValues(self, train, index):
        '''
        :param train: training data
        :param index: which feature to extract all the possible values from
        :return: a list containing all the possible value for this feature
        '''
        values = []
        for sample in train:
            val = sample[index]
            if val not in values:
                values.append(val)

        return values

    def getMajority(self, label):
        '''
        get the majority label for current labels
        :param label: label vector for training set
        :return: 0 or 1 as the majority label, and if all the label are the same
        '''
        pos_num = 0.0
        neg_num = 0.0
        for l in label:
            if l == 0:
                neg_num += 1
            elif l == 1:
                pos_num += 1
            else:
                print "Error, wrong label not 1 or 0!"
                exit()

        if pos_num == 0 or neg_num == 0:
            if pos_num > neg_num:
                return 1, True
            else:
                return 0, True
        else:
            # in training set there are more negative set than positive example
            if (neg_num/pos_num) > (32193.0 / 7807.0):
                return 0, False
            else:
                return 1, False

    def targetEntropy(self, label):

        pos = 0.0
        neg = 0.0
        total = len(label)

        for l in label:
            if l == 0:
                neg += 1
            elif l == 1:
                pos += 1
            else:
                print "Error Strange case happen!"
                exit()
        entropy = 0.0
        if pos != 0:
            entropy -= (pos/total)*log(pos/total, 2)
        if neg != 0:
            entropy -= (neg/total)*log(neg/total, 2)

        return entropy

    def featureEntropy(self, train, f_index, label):
        # If split on f_index attribute, how much gain can I get
        # collect how many value and their frequency
        val_freq = {}
        total = len(train)
        for feature in train:
            val = feature[f_index]
            if val in val_freq:
                val_freq[val] += 1.0
            else:
                val_freq[val] = 1.0

        # now compute the entropy for each of this value
        # and average them by frequency
        f_entropy = 0.0
        for k,v in val_freq.iteritems():
            weight = v/total
            sublabel = []
            for f, l in zip(train, label):
                if f[f_index] == k:
                    sublabel.append(l)
            f_entropy += weight * self.targetEntropy(sublabel)
        return f_entropy

    def chooseBestFeature(self, train, label, used_feature):
        # choose the best feature which maximize entropy gain
        # used_feature is a list of bool of dimension of trainning set size

        # total dimension of feature
        n = len(train[0])
        # entropy under current label
        ent = self.targetEntropy(label)
        max = -1
        max_index = -1

        # find the largest gain
        for i in range(0, n):
            # if this feature is no longer available
            if used_feature[i]:
                continue

            # find largest gain
            f_entropy = self.featureEntropy(train, i, label)
            gain = ent - f_entropy
            if gain < -1e-10:
                print "Big error, gain smaller than 0"
                print gain
                exit()

            #print "%d feature gain is %.8f" %(i,gain)
            if gain > max:
                max = gain
                max_index = i

        #print "max gain is %.2f" %max
        return max_index

class Node:

    def __init__(self, f_index):
        self.f_index = f_index
        # child node for this node
        # dictionary for index and corresponding node
        self.child = {}
        # if this node is leaf node
        self.isleaf = False
        self.judgelabel = -1

    def setLeaf(self):
        self.isleaf = True

    def setLabel(self, label):
        self.judgelabel = label

    def setFeatureIndex(self, f_index):
        self.f_index = f_index

    def getFeatureIndex(self):
        return self.f_index

    def canJudge(self):
        if self.isleaf:
            return True
        else:
            return False

    def predictLabel(self):
        if self.judgelabel != 0 and self.judgelabel != 1:
            print "The label is strange!"

        return self.judgelabel

    def getNext(self, value):
        '''
        Given value, find correspoding child node, and return it
        :param value: value of the feature
        :return: return the child node corresponds to value
        '''
        goto_value = value
        while goto_value not in self.child:
            goto_value -= 1
            if goto_value == 0:
                break

        while goto_value not in self.child:
            goto_value += 1

        return self.child[goto_value]



    def addChild(self, child, value):
        '''
        Add a child tree to the root
        :param child: the child node to be added
        :param value:
        :return:
        '''

        if value not in self.child:
            self.child[value] = child
        else:
            print "Error, this value already has a child!"
            exit()