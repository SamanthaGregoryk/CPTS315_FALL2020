# CPTS 315: Programming Assignment 1 (PA1) 

## Libraries:

from itertools import combinations
from itertools import chain

## Description: 

Load browsing_data.txt using the function input_data() that turns items in each row into lists. Then, create a dataframe from the lists using bucket_list().

For the first Aprori pass, use apriori_1() that inserts the dataframe with the support threshold. Then use apriori_2() for the second pass that uses the the same dataframe and support as the first pass but uses a list of all the freuquent items in the first pass to find the freuquent pairs. Then use apriori_3() for the third pass that uses the the same dataframe and support as the first pass but uses a list of all the freuquent items in the second pass to find the frequent triples.

To find the confidence scores for the freuqent pairs, use confidence_pairs() with the first and second apriori passes. Use top_5() to grab the first five freuquent pairs. To find the confidence scores for the freuqent triples, use confidence_pairs() with the second and third apriori passes. Use top_5() to grab the first five freuquent triples. 

Lastly, use output_data() to output the top five freuquent pairs and triple from the dataset with the following output below. 

## Output:

I could not get the entire dataset to run but a portion of the dataset runs as expected...
For now, I ran the first 5000 lines and my program worked fine. 

OUTPUT A
GRO85051 FRO40251 1.0
ELE88583 SNA24799 0.8125
ELE21353 DAI62779 0.7938931297709924
DAI85309 ELE99737 0.7213822894168467
SNA53220 SNA93860 0.7070707070707071
OUTPUT B
SNA80324 GRO85051 FRO40251 1.0
SNA93860 FRO19221 DAI62779 0.9193548387096774
SNA53220 FRO19221 DAI62779 0.8920863309352518
SNA53220 DAI62779 FRO19221 0.8920863309352518
SNA93860 FRO19221 SNA53220 0.8709677419354839
    
 
