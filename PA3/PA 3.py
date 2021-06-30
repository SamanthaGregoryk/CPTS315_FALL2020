"""
Author: Samantha Gregoryk
Assignment: PA3
Class: CPTS 315
Section: 01
Date: Novemeber 9th, 2020
"""
import numpy as np

iterations = 20
n = 1

def read_file(file):
    
    # read in data
    with open(file, "r") as f:
       read_f = f.read().splitlines()

    return read_f

def alphabetic_order(training_data, stop_list):
    
    # the set is in a unordered list 
    
    # find set of words in fortune cookie list
    # that are not in stop words list
    vocab = sorted(list(set([i for sentence in training_data for i in sentence.split() if i not in stop_list])))

    # return the sorted vocabulary list (alphabetic order)
    return vocab

def create_vectors(training_data, vocab, stop_list):
    
    # first create seperate lists for each line from the training data 
    split_train_data = [line.split() for line in training_data]
    
    # create an empty list for all vectors
    empty_vectors = []
     
    # for each line in the split up training data
    for i in split_train_data:

        # this is the present vectors 
        vector = []
        
        # this will match the size of the vobaculary to the vector 
        for j in vocab:
            
            # if the present vector in the vocabulary is in the line of the training data
            ## e.g. [0, 0, 1, 0 ,0]

            # append the vector to 1 (class 1)
            if j in i:
                vector.append(1)
                
            # else append the vector to 0 (class 0)
            else:
                vector.append(0)
                        
        # append the single vectors to the empty vector list 
        empty_vectors.append(vector)

    # return the (not so) empty list of vectors
    return empty_vectors

def online_binary_classifier(vectors, training_labels, num_iterations):
    
    # initialize the '0' weight by the length of all '0' vectors  
    weight = [0] * len(vectors[0])
    
    # create an empty list to hold results in 
    result = {}
    
    # for each training iteration in the range {1,2,...,20} 
    for itr in range(num_iterations):
        
        # intialize variables
        correct = 0
        mistake = 0

        # for each training example in the (xt,yt) in the range of the length of the vectors 
        for tr_ex in list(range(len(vectors))):    
            
            # predict using current weight from the training labels 
            # y_t = sign(w * x)
            v = vectors[tr_ex]
            y_t = np.dot(v, weight) 
            correct = vectors[tr_ex]
            
            # if there is a mistake 
            if y_t > 0:
                y_t = 1

            else:
                y_t = 0

            # update the weight
            # w = w + n * yt * xt
            if int(y_t) != correct:
                mistake += 1
                weight = weight + n * v

            else:
                correct  += 1
                  
        # calculate accuracy
        accuracy = correct / (correct + mistake)

        # each itr is held in the results list
        result[itr] = {correct, mistake, accuracy}

    # return the results list
    return result

def perceptron(vectors, weight, testing_data, testing_labels):
    
    # initialze variables
    correct = 0
    mistake = 0

    # for each testing example in the (xt,yt) in the range of the length of the testing data 
    for t_ex in list(range(len(testing_data))):
        
        #initalize variable    
        s = 0
        
        # calculate the product 
        for i in range(len(vectors)):
            s = (weight[i] * vectors[i])

        if s <= 0:
            s = 0
        
        else:
            s = 1

        correct = int(testing_labels[t_ex])

        if s == correct:
            correct += 1
        
        else:
            mistake += 1
    
    # calculate accuracy
    accuracy = correct / (correct + mistake)

    # return the correct, mistake, and accuracy of the data
    return correct, mistake, accuracy


print("Reading In Training Data...")
training_data = read_file('C:/Users/Samgr/OneDrive/Desktop/CPTS315/Homework/PA3/fortune-cookie-data/traindata.txt')

print("Reading In Training Labels...")
training_labels = read_file('C:/Users/Samgr/OneDrive/Desktop/CPTS315/Homework/PA3/fortune-cookie-data/trainlabels.txt')

print("Reading In Testing Data...")
testing_data = read_file('C:/Users/Samgr/OneDrive/Desktop/CPTS315/Homework/PA3/fortune-cookie-data/testdata.txt')

print("Reading In Testing Labels...")
test_labels = read_file('C:/Users/Samgr/OneDrive/Desktop/CPTS315/Homework/PA3/fortune-cookie-data/testlabels.txt')

print("Reading In Stop List...")
stop_list = read_file('C:/Users/Samgr/OneDrive/Desktop/CPTS315/Homework/PA3/fortune-cookie-data/stoplist.txt')

print("Building Vocabulary...")
vocab = alphabetic_order(training_data, stop_list)

print("Creating Training Vectors...")
training_vectors = create_vectors(training_data, vocab, stop_list)

print("Creating Testing Vectors...")
testing_vectors = create_vectors(testing_data, vocab, stop_list)

print("Running Binary Classifier On Data...")
weight_vector, training_results = online_binary_classifier(training_vectors, training_labels, iterations)

print("Running Perceptron On Data...")
perceptron_testing = perceptron(training_vectors, weight_vector, testing_vectors, test_labels)

print("Results Are Saved In Saved In output.txt")

