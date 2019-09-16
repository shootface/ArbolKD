from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.metrics import accuracy_score
from sklearn import tree
import pandas as pd
import numpy as np
import pygraphviz as pgv
"""
A: 4286
B: 5  
C: 103 
D: 352 
E: 1095 
F: 1961 
G: 446 
H: 519
I: 831
W: 44
X: 522 
Y: 266
""" 
heads = ["intercolumnar distance","upper margin","lower margin","exploitation","row number","modular ratio","interlinear spacing","weight,peak number","modular ratio/ interlinear spacing","clases"]
names = ['A','B','C','D','E','F','G','H','I','W','X','Y']
df = pd.read_csv('./avila/avila-ts.txt')
dt = pd.read_csv('./avila/avila-tr.txt')
df.clase = df.clase.replace({"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"W":10,"X":11,"Y":12})
dt.clase = dt.clase.replace({"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"W":10,"X":11,"Y":12})
dataSet = df.drop('clase',axis=1)
dataSetT = dt.drop('clase',axis=1)
clases = df['clase']
clasesT = dt['clase']
#print(df.head())
#df.info()
aux2 = df.values.tolist()
clf = tree.DecisionTreeClassifier().fit(dataSet,clases)
predict = clf.predict(dataSetT)
print(accuracy_score(clasesT,predict))
#print(predict[0])
#score = clf.score(dataSetT,dt)
#print('score : ',score)
#score = average_precision_score(dataSetT,clases) 
#print('Mean Accuracy: %.3f%%',score)
# Creates dot file named tree.dot
#dot_data = export_graphviz(
#            clf,
 #           out_file =  "./avilaDes.dot",
  #          feature_names=heads,
   #         class_names=names,
    #        filled= True,
     #       rounded= True)

#g = pgv.AGraph('./avilaDes.dot')
#g.layout(prog = 'dot')
#g.draw('./avila.svg')

#graph = graph_from_dot_data(dot_data)
#graph.write_png('./avilaDes.png')

## Create and fit a nearest-neighbor classifier

