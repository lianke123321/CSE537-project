# helper function for read in the data
def readData(trainf, trainl, testf, testl, fname):
    '''
    :param trainf: path for train set feature
    :param trainl: path for train set label
    :param testf:  path for test set feature
    :param testl:  path for test set label
    :param fname:  path for feature name
    :return:
    '''

    train_feature = []
    test_feature = []
    train_label = []
    test_label = []
    feature_name = []

    with open(trainf) as f:
        for line in f:
            feature_vector = [int(x) for x in line.rstrip('\n').split(' ')]
            train_feature.append(feature_vector[:])

    with open(testf) as f:
        for line in f:
            feature_vector = [int(x) for x in line.rstrip('\n').split(' ')]
            test_feature.append(feature_vector[:])

    with open(trainl) as f:
        for line in f:
            label = int(line.rstrip('\n'))
            train_label.append(label)

    with open(testl) as f:
        for line in f:
            label = int(line.rstrip('\n'))
            test_label.append(label)

    with open(fname) as f:
        for line in f:
            feature_name.append(filter(str.isalnum, line))

    return train_feature, train_label, test_feature, test_label,feature_name

if __name__ == "__main__":

    trainf = 'trainfeat.csv'
    testf  = 'testfeat.csv'
    trainl = 'trainlabs.csv'
    testl  = 'testlabs.csv'
    fname  = 'featnames.csv'

    train_feature, train_label, \
    test_feature,  test_label, \
    feature_name = readData(trainf, trainl, testf, testl, fname)

    num_pos = 0
    num_neg = 0

    for l in train_label:
        if l == 0:
            num_neg += 1
        else:
            num_pos += 1

    print num_pos
    print num_neg

    values = []
    for i in range(0, len(train_feature[0])):
        values.append(set())

    for feature in train_feature:
        for i, val in enumerate(feature):
            values[i].add(val)

    print values[0]
    print values[1]
    print "Having save the values"

    for feature in test_feature:
        for i, val in enumerate(feature):
            if val not in values[i]:
                print "column %d has value %d not in train" %(i, val)

    # test the max_value for every feature
    train_value_max = [0 for i in range(0, len(feature_name))]
    test_value_max = train_value_max[:]
    for sample in train_feature:
        for i, val in enumerate(sample):
            if val > train_value_max[i]:
                train_value_max[i] = val

    for sample in test_feature:
        for i, val in enumerate(sample):
            if val > test_value_max[i]:
                test_value_max[i] = val

    for (tr, te, n) in zip(train_value_max, test_value_max, feature_name):
        print "%s with train max: %d, test max: %d"%(n, tr, te)









