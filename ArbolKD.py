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
heads = ["intercolumnar distance","upper margin","lower margin","exploitation","row number","modular ratio","interlinear spacing","weight,peak number","modular ratio/ interlinear spacing","clase"]
points = [
(-3.498799,0.250492,0.23207,1.224178,-4.922215,1.145386,0.182426,-0.165983,-0.123005,1.087144,'W'),
(0.204355,-0.354049,0.32098,0.410166,-0.989576,-2.218127,0.220177,0.181844,2.090879,-2.009758,'A'),
(0.759828,-1.304042,-0.023991,-0.973663,-0.006417,-0.349509,-0.42158,-0.450127,0.469443,0.060952,'I'),
(-0.00549,0.360409,0.28186,-0.213479,-1.168333,-1.013906,-0.34608,1.176165,0.968347,-0.627999,'E'),
(0.080916,0.10132,0.10404,0.14049,0.261718,0.480988,0.710932,-0.25343,-0.497183,0.155681,'A'),
(0.068573,-0.181323,-3.210528,-0.294311,-1.168333,0.356414,-0.006326,-0.21955,0.126447,0.448186,'F'),
(-0.301743,-0.314793,0.399221,0.77052,0.708609,0.564038,-1.403091,-1.459107,-0.091823,1.62742,'Y'),
(0.031541,-0.118513,0.374326,-0.066706,0.261718,0.605563,0.55993,-0.258129,0.095265,0.344766,'A')]

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

tree = kdtree(aux)
#tree = kdtree(points)

print(tree.location)
print(tree.head)

g = pgv.AGraph(strict = True, directed = False)
g.node_attr['shape']='box'

def grafTree(tree,depth=0,id='root'):
    if tree is not None:
        if hasattr(tree, 'pointList'):
            leaf = np.array(tree.pointList)[:,10]
            print(('-' * depth) + '>', 'depth', depth, 'leaf', leaf)
            print(leaf[0])
        else:
            idLeft = id + 'L'
            idRight = id + 'R'
            maxDepth = 3
            if depth <= maxDepth:
                if id == 'root':
                    g.add_node(id, label=tree.head)
                if hasattr(tree.leftChild, 'head'):
                    g.add_node(idLeft, label=tree.leftChild.head)
                    g.add_edge(id, idLeft, label='left(yes)')
                    
                if hasattr(tree.rightChild, 'head'):
                    g.add_node(idRight, label=tree.rightChild.head)
                    g.add_edge(id, idRight, label='right(no)')
                    
            grafTree(tree.leftChild, depth + 1, idLeft)
            grafTree(tree.rightChild, depth + 1, idRight)
    else:
        # print(str(depth))
        return

grafTree(tree)
g.write("./avila.dot")
g.layout(prog = 'dot')
g.draw('./avila.png')
