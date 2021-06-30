"""
Author: Samantha Gregoryk
Assignment: PA1
Class: CPTS 315
Section: 01
Date: September 27th, 2020
"""

from itertools import combinations
from itertools import chain

def frequent_lists(candidate, s):
    
    # create frequency list
    L = {}
    
    # items() returns the list with all dictionary keys with values
    for (k, v) in candidate.items():
        # support threshold 
        if v >= s:
            # list of all values equal to or above s
            L[k] = v
     
    # return frequency list 
    return L

def apriori_1(C1, s):
    
    # find candidate itemsets in C1
    candidate = {}
    
    # rows in data
    for row in C1:
        # items in rows
        for item in row:
            
            # make dictionary for each item in each row
            dictionary = candidate.get(item)
            
            if dictionary:
                # items that have matches, add 1 to the value
                candidate[item] += 1
           
            else:
                # items that dont have any matches
                candidate[item] =  1
    
    # save the number of matched items to a frequency list
    return frequent_lists(candidate, s)

def combination(L, n):
    
    # freuquent items and length (pair or triple)
    combo = list(combinations(L, n))
    
    return combo

def apriori_2(C2, L1, s):
    
    #empty list
    candidate = {}
    
    # find candidate itemsets in C2 from frequent itemsets in L1
    for row in C2:
        # pairs list
        for c in combination(L1, 2):
           
            # {0, 1} for each row in the frequent list
            if c[0] in row and c[1] in row:
             
              # make dictionary for each pair 
              dictionary = candidate.get(c)
                
              if dictionary:
                  # if pairs match each other, add one to the value
                  candidate[c] += 1
                   
              else:
                  # if pairs dont have any matches
                  candidate[c] = 1
    
    # create a new list to keep the frequent pairs in 
    return frequent_lists(candidate, s)
    
def apriori_3(C3, L2, s):
    
    # do the same as apriori_2() but with triples
    
    # empty list
    candidate = {}
    
    # find candidate itemsets in C2 from frequent itemsets in L1
    for row in C3:
        # triple list
        for c in combination(L2, 3):
            
            # {0, 1, 2} for each row in the frequent list
            if c[0] in row and c[1] in row and c[2] in row:
              
                # make dictionary for each triple
                dictionary = candidate.get(c)
                
                if dictionary:
                  # if triples match each other, add one to the value
                  candidate[c] += 1
                   
                else:
                  # if triples dont have any matches
                  candidate[c] = 1
                  
    # create a new list to keep the frequent triples in 
    return frequent_lists(candidate, s)
        
def sort(x):
    
    # sorted function
    s = sorted(x.items(), key=lambda k: k[1])
    # desecding order
    s.reverse()
    
    # return s
    return s
   
def confidence_pairs(a1, a2):
    
    # empty list 
    confidence = {}
    
    # a is each item for the list of keys in the dictionary
    for a in a2.keys():
        
        # {X} -> {Y}
        confidence[(a[0], a[1])] = a2[a] / a1[a[0]]
        
        # {Y} -> {x}
        confidence[(a[1], a[0])] = a2[a] / a1[a[1]]

    # return sort function
    return sort(confidence)

def confidence_triples(a2, a3):
    
    # empty list
    confidence = {}
    
    # a is each item for the list of keys in the dictionary
    for a in a3.keys():
        
        # if the first is true first, or the second is true first
        
        # {X, Y} or {Y, X}
        d1 = (a2.get((a[0], a[1])) or a2.get((a[1], a[0])))
        # {X, Z} or {Z, X}
        d2 = (a2.get((a[0], a[2])) or a2.get((a[2], a[0])))
        # {Y, Z} or {Z, Y}
        d3 = (a2.get((a[1], a[2])) or a2.get((a[2], a[1])))

        # {X, Y} -> {Z}
        confidence[(a[0], a[1], a[2])] = a3[a] / d1
        
        # {X, Z} -> {Y}
        confidence[(a[0], a[2], a[1])] = a3[a] / d2
        
        # {Y, Z} -> {X}
        confidence[(a[1], a[2], a[0])] = a3[a] / d3

    # return sort function
    return sort(confidence)

print("Inputting Data...")
# read in browsing-data.txt
with open('C:/Users/Samgr/OneDrive/Desktop/CPTS315/Homework/PA1/browsing-data-3000.txt', "r") as r:
    # returns a list containing each line in the file as a list item
    data = r.readlines()

print("Creating Buckets...")
buckets = [[items for items in line.split()] for line in data]

print("Running Apriori Pass 1...")
a1 = apriori_1(buckets, 100)

# turn the dictionary into a list
L1 = list(a1.keys())
    
print("Running Apriori Pass 2...")
a2 = apriori_2(buckets, L1, 100)

# turn dictionary into a set to finds common elements between the sets
L2 = set(chain.from_iterable(a2))

print("Running Apriori Pass 3...")
a3 = apriori_3(buckets, L2, 100)

print("Running Top 5 Confidence Scores for Pairs...")
c_p = confidence_pairs(a1, a2)
top5_pairs = c_p[:5]

print("Running Top 5 Confidence Scores for Triples...")
c_t = confidence_triples(a2, a3)
top5_triples = c_t[:5]

print("Top 5 Pairs and Triples saved in output.txt...")
# write into output.txt
with open('C:/Users/Samgr/OneDrive/Desktop/CPTS315/Homework/PA1/output.txt', "w") as w:
    
    # Output A in .txt
    w.write("OUTPUT A\n")
        
    # output: <i1>,<i2>,<confidence>\n
    for p in top5_pairs:
        w.write(p[0][0] + " " + p[0][1] + " " + str(p[1]) + "\n")

    # Output B in .txt
    w.write("OUTPUT B\n")
        
       # output: <i1>,<i2>,<i3>,<confidence>\n
    for t in top5_triples:
        w.write(t[0][0] + " " + t[0][1] + " " + t[0][2] + " " + str(t[1]) + "\n")
