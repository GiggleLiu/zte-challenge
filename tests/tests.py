from numpy import *
from numpy.linalg import norm,svd
from copy import deepcopy
from numpy.testing import dec,assert_,assert_raises,assert_almost_equal,assert_allclose
from matplotlib.pyplot import *
import sys,pdb,time
from os import path
sys.path.insert(0,'../')

from testcases import *
from solvepath import find_shortest_path

random.seed(5)

def show_cases():
    plt.ion()
    fig=plt.figure(facecolor='w')
    plt.axis('equal')
    for ig,g in enumerate(Gs):
        plt.cla()
        plt.axis('off')
        visualize_graph(g)
        #visualize_path(g,g.solution)
        print 'The Cost is %s'%g.get_cost(g.solution)
        #animate_path(g,g.solution)#,filename='Ant-G%s'%ig)
        pdb.set_trace()

def test_shortest_path():
    from scipy.sparse.csgraph import shortest_path
    mat=G1.sparse_matrix
    dist_matrix=shortest_path(mat,method='D',directed=True)
    print 'The shortest distances between nodes are:\n%s'%dist_matrix

def test_g(g):
    solution,cost=find_shortest_path(g,max_num_nodes=8)
    print solution,cost
    ion()
    visualize_graph(g)
    visualize_path(g,solution)
    axis('equal')
    pdb.set_trace()
    assert_allclose(solution,g.solution)

if __name__=='__main__':
    test_g(G0)
    #test_shortest_path()
    #show_cases()
