import csv
import pandas as pd
import numpy as np
from collections import Counter 
import math

import sys

def loadData(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        lines = []
        for row in reader: 
            lines.append(row) 
        return lines
    
def E(dfD):
    sum = 0
    y_values = dfD.iloc[:, -1].unique()
    for y_value in y_values: 
        sum += ((dfD.iloc[:, -1].value_counts()[y_value]/dfD.shape[0])* math.log2((dfD.iloc[:, -1].value_counts()[y_value]/dfD.shape[0])))
    return -sum


def IG(dfD, x):
    sum = 0
    for value in dfD[x].unique():
        sum += ((dfD[x].value_counts()[value] / dfD.shape[0]) * E(dfD[dfD[x]==value]))
    # print("IG({})={}".format(x, E(dfD) - sum))
    return E(dfD) - sum 


def the_most_discr(dfD, X):
    igs = {}
    for x in X: 
        igs[x] = IG(dfD,x)
    first_key, first_value = next(iter(igs.items()))
    list_of_max = list()
    list_of_max.append(first_key)
    max = first_value
    for key in igs:
        if igs[key] == max: 
            list_of_max.append(key)
        elif igs[key] > max:
            max = igs[key] 
            list_of_max.clear()
            list_of_max.append(key)   
    list_of_max.sort()
    return list_of_max[0]           
    #return max(igs, key= lambda k: (igs[k], k))
        
class Node:
    def __init__(self, x, subtrees, leaf): 
        self.x = x
        self.subtrees = subtrees #tuple of v,t
        self.leaf = leaf


def id3algorithm(D, Dparent, X, y, maxdepth): 
    
    if D is None: 
        counter = Counter(Dparent[y]) #v = class counts
        v_list = counter.most_common(5)
        list_new = []
        list_new.append(v_list[0][0])
        max = v_list[0][1]
        for m in v_list:
            if m[1]==max:
                list_new.append(m[0])
        list_new.sort()
        v = list_new[0]
        return Node(v, None, True)
    counter = Counter(D[y])
    v_list = counter.most_common(5)
    list_new = []
    list_new.append(v_list[0][0])
    max = v_list[0][1]
    for m in v_list:
        if m[1]==max:
            list_new.append(m[0])
    list_new.sort()
    v = list_new[0]


    Dyv = D[D[y]==v]

    if maxdepth!=None and maxdepth==0:
        return Node(v, None, True)

    if len(X)==0 or D.equals(Dyv):
        return Node(v, None, True)

    x = the_most_discr(D, X)

    subtrees = []

    all_values = list(set(D[x].tolist()))
    value_counts = Counter(all_values)

    sorted_values = sorted(all_values, key=lambda x: (value_counts[x], x), reverse=True)

    if maxdepth!=None:
        maxdepth-=1
    for v in sorted_values:
        X_copy = X.copy()
        X_copy.remove(x)
        t = id3algorithm(D[D[x]==v], D, X_copy, y, maxdepth)

        subtrees.append((v, t))
    return Node(x, subtrees, False)


def printTree(tree, k, string):
    if tree.leaf == True: 
        string += tree.x
        print(string)
        return
    k += 1
    string += str(k) + ":" + tree.x + "="

    for one_tree in tree.subtrees: 
        new_string = string + str(one_tree[0]) + " " 
        printTree(one_tree[1],k,new_string)

def test(test_data, tree):
    if tree.leaf == True:
        return tree.x
    feature = tree.x
    value = test_data[feature]
    for one_tree in tree.subtrees: 
        if one_tree[0] == value: 
            return test(test_data, one_tree[1])

    return test(test_data, tree.subtrees[0][1])       


def confusionMatrix(dataframe, predictions):
        key = dataframe.columns[-1]
        y = dataframe[key].unique()
        y = sorted(y)
        test_y = dataframe.iloc[:,-1].values
        output=""

        for t in y:
            matrix_row = ""
            for z in y:
                correct = 0
                for i, element in enumerate(predictions):
                    if element == z and test_y[i] == t:
                        correct = correct + 1           
                matrix_row = matrix_row + str(correct) + " "
            output+=matrix_row + "\n"
        output = output[:-1]
        print(output)
    
        return

class ID3:
    def __init__(self):
        self.tree = None

    def fit(self, dataset, maxdepth):
        self.dataset = dataset
        dataframe = pd.DataFrame(self.dataset)
        X = list(dataset[0].keys())
        y = X.pop() 
        self.tree = id3algorithm(dataframe, dataframe, X, y, maxdepth)

        print("[BRANCHES]: ")
        printTree(self.tree, 0, "")
        

    def predict(self, dataset):
        self.dataset = dataset
        dataframe = pd.DataFrame(self.dataset)
        string_result = "[PREDICTIONS]: "
        dataframe_trained = pd.DataFrame(columns=['y'])
        for idx, row in dataframe.iterrows(): 
            result = test(row[:-1], self.tree)
            dataframe_trained = pd.concat([dataframe_trained, pd.DataFrame({'y': [result]})], ignore_index=True)
            string_result += result + " "
        print(string_result)
        y_pred = dataframe_trained.values
        y_true = dataframe.iloc[:,-1].values
        total_samples = len(y_true)
        correct_predictions = sum(y_t == y_p for y_t, y_p in zip(y_true, y_pred))
        accuracy = correct_predictions[0] / total_samples
        print("[ACCURACY]: {:.5f}".format(accuracy))
        print("[CONFUSION_MATRIX]:")
        confusionMatrix(dataframe, y_pred)

def main():

    training_data_file = sys.argv[1]
    test_data_file = sys.argv[2]
    maxDepth=None
    if len(sys.argv) > 3:
        maxDepth = int(sys.argv[3])

    trainingData = loadData(training_data_file)
    model = ID3() 
    model.fit(trainingData, maxDepth)
    
    testData = loadData(test_data_file)

    model.predict(testData) 

    # trainingData = loadData("volleyball.csv")
    # maxdepth = 1
    # model = ID3() 
    # model.fit(trainingData, maxdepth)
    
    # testData = loadData("volleyball_test.csv")

    # predictions = model.predict(testData) 

    



if __name__ == "__main__":
    main()
