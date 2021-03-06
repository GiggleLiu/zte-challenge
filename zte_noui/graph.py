#import numpy as np
import poor_mans_numpy as np

__all__=['MyGraph','random_graph','save_graph','load_graph']

class MyGraph(object):
    '''
    Attributes:
        :connections: list, i,j,weight.
        :node_positions: 2darray, the positions of graph nodes.
        :must_nodes: list, nodes must be passed.
    '''
    def __init__(self,connections,node_positions,must_nodes=None,must_connections=None):
        self.connections=connections
        self.node_positions=np.asarray(node_positions)
        self.must_nodes=must_nodes if must_nodes is not None else []
        self.must_connections=must_connections if must_connections is not None else []
        il,jl,wl=zip(*self.connections)
        num_nodes=int(max(max(il),max(jl))+1)
        if num_nodes!=np.shape(self.node_positions)[0] or np.shape(self.node_positions)[1]!=2:
            raise ValueError()

        #initialize matrices.
        il,jl,weights=zip(*self.connections)
        il,jl=np.concatenate([il,jl]),np.concatenate([jl,il])
        weights=np.concatenate([weights,weights])
        self.dense_matrix=np.zeros([num_nodes]*2)
        for i,j,w in zip(il,jl,weights):
            self.dense_matrix[i][j]=w

    def __str__(self):
        return 'Graph(%s nodes, %s legs)\n  %s\n  must nodes: %s\n  must paths: %s'%(self.num_nodes,self.num_paths,\
                ', '.join(str(con) for con in self.connections),self.must_nodes,np.take(self.connections,self.must_connections))

    @property
    def num_nodes(self):
        '''Number of nodes'''
        return np.shape(self.dense_matrix)[0]

    @property
    def num_paths(self):
        '''Number of paths'''
        return len(self.connections)

    def get_cost(self,path):
        '''Calculate the cost for given path.'''
        il,jl=path[:-1],path[1:]
        diss=[self.dense_matrix[i][j] for i,j in zip(il,jl)]
        if not np.all(diss): raise ValueError('Invalid Path!')
        return np.sum(diss)

def save_graph(graph_prefix,graph):
    np.savetxt(graph_prefix+'.nod.dat',np.concatenate([graph.node_positions,[[1] if i in graph.must_nodes else [0] for i in xrange(graph.num_nodes)]],axis=1))
    np.savetxt(graph_prefix+'.con.dat',np.concatenate([graph.connections,[[1] if i in graph.must_connections else [0] for i in xrange(len(graph.connections))]],axis=1))

def load_graph(graph_prefix):
    #load nodes
    pos_data=np.loadtxt(graph_prefix+'.nod.dat')
    must_nodes=[i for i in xrange(len(pos_data)) if pos_data[i][-1]>0]
    node_positions=np.take(pos_data,[0,1],axis=1)
    #load connections
    con_data=np.loadtxt(graph_prefix+'.con.dat')
    connections=[(int(data[0]),int(data[1]),data[2]) for data in con_data]
    must_connections=[i for i in xrange(len(con_data)) if con_data[i][-1]>0]
    g=MyGraph(connections,node_positions,must_nodes=must_nodes,must_connections=must_connections)
    return g

def random_graph(num_nodes,density=1):
    m=np.random.random([num_nodes]*2)*3
    m[np.random.random([num_nodes]*2)>density]=0
    np.fill_diagonal(m,0)
    il,jl=np.where(m)
    weights=m[il,jl]
    return MyGraph(zip(il,jl,weights),node_positions=(np.random.random([num_nodes,2])-0.5)*num_nodes)

