#! python 3.6.8
# -*- coding: utf-8 -*-
import numpy as np 
import pandas as pd
import os
from pandas import DataFrame, read_csv
import pygraphviz as pgv
from PIL import Image
import statistics as st
#from graphviz import Digraph


df = pd.read_csv('./avila/avila-ts.txt')

#df.info()
aux = df.values.tolist()
aux2 = aux[0:100]
test = aux[100:101]
heads = ["intercolumnar distance","upper margin","lower margin","exploitation","row number","modular ratio","interlinear spacing","weight,peak number","modular ratio/ interlinear spacing","clase"]

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def media(datos):
    if len(datos) % 2 == 0:
        n = len(datos)
        mediana = (datos[n // 2 - 1] + datos[n // 2]) / 2
    else:
        mediana = datos[len(datos) // 2]

    return mediana

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
    median = len(pointList)//2
    vecino = find_nearest(np.array(pointList)[:,0],median)
    #min(np.array(pointList)[0,:], key=lambda x:abs(x-median))
    #len(pointList)//2 # choose median
    print("median : "+str(median))
    for v in vecino:
        print("vecino : ",str(v))
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

#print(tree.__dict__)
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

def reescritura(tree,test):
    count=0
    for elem in test:
        print(elem)
        if acierto(tree,elem):
            count = count + 1
    return count*100/len(test)


def acierto(tree,node,depth=0):
    if tree is not None:
        if node is not None:
            #print(tree.__dict__)
            if hasattr(tree,'pointList')==False:
                if hasattr(tree, 'head'):
                    print(tree.head)
                    treeData = tree.head.split('<=')
                    if node[getAtribute(treeData[0])] <= float(treeData[1]):
                        print("TRUE")
                        acierto(tree.leftChild,node,depth+1)
                    else:
                        print("FALSE")
                        acierto(tree.rightChild,node,depth+1)
                if hasattr(tree.leftChild, 'head')==False and hasattr(tree.rightChild, 'head')==False:
                    print(node[10], tree.location[10])
                    if node[10]==tree.location[10]:
                        print("TRUE")
                        return 1
                    else:
                        print("FALSE")
                        return 0

def getAtribute(atri):
    i=0
    for atribute in heads:
        if atribute==atri:
            #print(atri)
            return i
        else:
            i=i+1

#acierto(tree,(0.759828,-1.304042,-0.023991,-0.973663,-0.006417,-0.681707,-1.138838,-1.404259,-0.060642,0.168869,'I'))
re = reescritura(tree,test)
print("Porcentaje de acierto : ",re)