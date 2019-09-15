#! python 3.6.8
# -*- coding: utf-8 -*-
import numpy as np 
import pandas as pd
import os
from pandas import DataFrame, read_csv
import pygraphviz as pgv
from PIL import Image
#from graphviz import Digraph


df = pd.read_csv('./avila/avila-ts.txt')
#df.info()
aux = df.values.tolist()
aux2 = aux[0:200]
heads = ["intercolumnar distance","upper margin","lower margin","exploitation","row number","modular ratio","interlinear spacing","weight,peak number","modular ratio/ interlinear spacing","clase"]

class Node:pass

def kdtree(pointList, depth=0):
    if not pointList:
        return
    #print("-------------------------------")
    #for i in range(len(pointList)):
    #    print(pointList[i])
    #print("-------------------------------")
    auxpointList = np.array(pointList)
    clasification = auxpointList[:,10]
    #print('clasification: ',clasification,depth)
    if len(clasification)==1:
        #print('tree point: ')
        node = Node()
        node.pointList = pointList
        return node
    # Select axis based on depth so that axis cycles through all valid values
    k = len(pointList[0]) - 1# assumes all points have the same dimension and dont have last column
    #print('k: ',k)
    axis = depth % k
    #print('axis: ',axis)
    # Sort point list and choose median as pivot element
    pointList.sort(key=lambda x:x[axis])
    #print("///////////////////"+"/n"+str(pointList[0][0]))
    median = len(pointList)//2 # choose median
    #print("median : "+str(median))
    # Create node and construct subtrees
    node = Node()
    valueInAxis = pointList[median][axis]
    node.head = heads[axis]+ '<=' + str(valueInAxis)
    node.location = pointList[median]
    node.leftChild = kdtree(pointList[0:median], depth+1)
    node.rightChild = kdtree(pointList[median+1:], depth+1)
    return node

#tree = kdtree(aux)
tree = kdtree(aux2)
#tree = kdtree(points)

#print(tree.location)
#print(tree.head)

g = pgv.AGraph(strict = True, directed = False)
g.node_attr['shape']='box'

def grafTree(tree,depth=0,id='root'):
    if tree is not None:
        if hasattr(tree, 'pointList'):
            leaf = np.array(tree.pointList)[:,10]
            #print(('-' * depth) + '>', 'depth', depth, 'leaf', leaf)
            #print(leaf[0])
            #print(tree.__dict__)
        else:
            #print(tree.__dict__)
            idLeft = id + 'L'
            idRight = id + 'R'
            idFinal = id + 'F'
            if id == 'root':
                g.add_node(id, label=tree.head)
            if hasattr(tree.leftChild, 'head'):
                g.add_node(idLeft, label=tree.leftChild.head)
                g.add_edge(id, idLeft, label='left(yes)')
            if hasattr(tree.rightChild, 'head'):
                g.add_node(idRight, label=tree.rightChild.head)
                g.add_edge(id, idRight, label='right(no)')
            if hasattr(tree.leftChild, 'head')==False and hasattr(tree.rightChild, 'head')==False:
                #print(tree.location)
                g.add_node(idFinal, label=tree.location[10])
                g.add_edge(id,idFinal, label='is')
            grafTree(tree.leftChild, depth + 1, idLeft)
            grafTree(tree.rightChild, depth + 1, idRight)
            #print(tree.__dict__)
    else:
        # print(str(depth))
        return

grafTree(tree)
g.write("./avila.dot")
g.layout(prog = 'dot')
g.draw('./avila.png')
