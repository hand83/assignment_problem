# -*- coding: utf-8 -*-
"""
Created on Sat May 26 2018
@author: Andras Horvath

Solution of assignment problem using the Hungarian (or Kuhn-Munkres) algorithm
"""
import numpy


def SubMin(M):
    # Initial step
    # Subtract row and column minimums from the matrix
    # Depending on the sum of the row or columnt minimum, the function starts 
    # with the larger wan in order to fastest convergence
    mins = [M.min(0), M.min(1)]
    rc = int(numpy.sum(mins[0], axis = 1) > numpy.sum(mins[1], axis = 0))
    M = M - numpy.concatenate(
        [mins[rc] for x in range(M.shape[rc])], 
         axis = rc)
    mins = M.min(1 - rc)
    return M - numpy.concatenate(
        [mins for x in range(M.shape[1 - rc])],
         axis = 1 - rc)



class Cluster:
    # Cluster object tracks the independent zeros in the matrix
    # provides methods to process further the optimization
    
    def __init__(self, Matrix):
        # input matrix
        self.Matrix = Matrix
        # groups of dependent zeros
        self.Groups = []
        # vertices covering the groups of dependent zeros
        self.Vertices = [[], []]
        # table of zero values
        Zpos = numpy.argwhere(Matrix == 0).tolist()
        # getting the dependent set of zeros
        ini_groups = [[Zpos[0]]]
        Zpos = Zpos[1:]
        for G in ini_groups:
            for e in G:
                to_delete = []
                for i in range(len(Zpos)):
                    if e[0] == Zpos[i][0] or e[1] == Zpos[i][1]:
                        G.append(Zpos[i])
                        to_delete.append(i)
                Zpos = [Zpos[x] for x in range(len(Zpos)) if x not in 
                        to_delete ]
            if len(Zpos) > 0:
                ini_groups.append([Zpos[0]])
                Zpos = Zpos[1:]
        # subsetting the groups in order to get:
        # minimum number of covering vertices
        # minimum number of subgroups that can be covered by the vertices
        for G in ini_groups:
            # all possible vertices
            hvVert = [list(set(map(lambda x: x[0], G))), 
                      list(set(map(lambda x: x[1], G)))]
            # direction of the vertices (vertical or horizontal)
            hvDir = [[ 0 for x in hvVert[0] ], 
                     [ 1 for x in hvVert[1] ]]
            # setting the order of the vertex list
            # among the horizontal and vertical vertex groups, the smallest 
            # one leads the concatenated list
            direction = len(hvVert[1]) < len(hvVert[0])
            DV = zip(hvDir[direction] + hvDir[1 - direction], 
                     hvVert[direction] + hvVert[1 - direction])            
            # creating all possible subgroups
            subGroups = []
            for v in DV:
                subGroups.append(filter(lambda x: x[v[0]] == v[1], G))
            # filtering subgroups
            # starting with the largest subgroup, members of the other 
            # subgroups are excluded if they match with any member of the
            # the current one
            while len(subGroups) > 0:
                # largest subgroup
                imax = max(range(len(subGroups)), 
                           key = lambda x: len(subGroups[x]))
                Gmax = subGroups.pop(imax)
                # covering vertex of the largest subgroup
                self.Vertices[DV[imax][0]].append(DV[imax][1])
                DV.pop(imax)
                self.Groups.append(Gmax)
                del_subgroups = []
                for i in range(len(subGroups)):
                    del_items = []
                    for j in range(len(subGroups[i])):
                        for e in Gmax:
                            if e == subGroups[i][j]:
                                del_items.append(j)
                    subGroups[i] = [ subGroups[i][x] for x in 
                                    range(len(subGroups[i])) if x not in 
                                    del_items]
                    if len(subGroups[i]) == 0:
                        del_subgroups.append(i)
                subGroups = [ subGroups[x] for x in 
                            range(len(subGroups)) if x not in del_subgroups ]
                DV = [ DV[x] for x in range(len(DV)) if x not in 
                    del_subgroups ]
        
        #print self.Matrix
        #print
        #print self.Vertices
        #print
        # check if the current solution is optimal
        self.Optimal = len(self.Groups) == len(Matrix)
        
    def Centers(self):
        # obtains the independent zeros from the groups of dependent zeros
        Centers = []
        Groups = self.Groups[:]
        # starting with the smallest group, we exclude the dependent zeros
        # from the other groups
        while len(Groups) > 0:
            # smallest group
            imin = min(range(len(Groups)), 
                       key = lambda x: (len(Groups[x]), Groups[x][0][1]))
            Gmin = Groups.pop(imin)
            # the first member of the smallest group is selected
            # this determines the solution choise if multiple exist
            # solutions nearest to the upper left and lower right corner
            # are preferred
            Centers.append(Gmin[0])
            del_groups = []
            for i in range(len(Groups)):
                del_items = []
                for j in range(len(Groups[i])):
                    if Gmin[0][1] == Groups[i][j][1] or \
                    Gmin[0][0] == Groups[i][j][0]:
                        del_items.append(j)
                Groups[i] = [ Groups[i][x] for x in 
                            range(len(Groups[i])) if x not in del_items ]
                if len(Groups[i]) == 0:
                    del_groups.append(i)
            Groups = [ Groups[x] for x in range(len(Groups)) if x not in 
                    del_groups ]

        return Centers

    def ReZero(self):
        # applying new weights on the matrix according to covering vertices
        # use only on matrices which are not optimized yet
        # values not covered by vertices: get the minimum of them and subtract        
        submask = numpy.ones((self.Matrix.shape[0], 
                              self.Matrix.shape[1]), numpy.bool)
        submask[self.Vertices[0], :] = False
        submask[:, self.Vertices[1]] = False
        decr = self.Matrix[submask].min()
        M = self.Matrix - submask * decr
        # values covered by to vertices: add the previously obtained minimum
        addmask = numpy.zeros((self.Matrix.shape[0], 
                               self.Matrix.shape[1]), numpy.bool)
        addmask[numpy.ix_(self.Vertices[0], self.Vertices[1])] = True
        M = M + addmask * decr
        return M
            
            

def OptimalAssignments(strArr):
    # main fuction
    # convert the input sting array to a matrix
    M = numpy.matrix(
        map(lambda x: x[1:-1].split(","), strArr)
    ).astype(int)
    # initial processing: subtracting row and column minimums
    M = SubMin(M)
    # clustering the zeros in the matrix
    C = Cluster(M)
#    step = 1
    # iterate until optimized
    while not C.Optimal:
        # apply new weights on the matrix
        M = C.ReZero()
        # re-clustering
        C = Cluster(M)
#        step += 1
#        if step == 4:
#            assert False, "stopped"
    # return solution in string format
    # the return string shows the row and column indices of the optimum 
    # positions
    return "".join(map(lambda z: "({0:d}-{1:d})".format(z[0] + 1, z[1] + 1), 
                       sorted(C.Centers(), key = lambda x: x[0])))


