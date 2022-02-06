# -*- coding: utf-8 -*-

import numpy as np 
import vtk   as vtk 

#     class that defines a tree structure based on quad

class tree_amr:
    def __init__(self, point_0, point_1, point_2, point_3, depth, depth_max):

        #     creation of a branch or a leaf 

        #   Be carefull this a recursive function 

        #    inputs:
        #        point_0 : point 0 of the quad  
        #        point_1 : point 1 of the quad   
        #        point_2 : point 2 of the quad   
        #        point_3 : point 3 of the quad  
        #        depth   : depth of the local branch or leaf in the tree 
        #        depth_max : maximum depth allowed in this tree 

        #    quad point order : 

        #                     3-------2                      3---7---2
        #                     |       |                      |   |   |
        #  for a leaf       : |       |  for a branch     :  8---4---6
        #                     |       |                      |   |   |
        #                     0-------1                      0---5---1

        #     first we suppose that when we create it, it is a leaf 
        self.branch = False

        #    store the information locally in the memory for the leaf 
        self.point_0 = point_0
        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3
        
        if (depth < depth_max):

            #   if the depth of the leaf is lower that the maximum depth 
            #   then we check if we need to transform the leaf into a branch
            #   We must transform the leaf into a branch 
            self.branch = True
            print ('depth < depth_max')
                
            #   creation points 4 to 8 that are used to create the new leaves 
            
            #   creation of the new leaves, this is the recursive part
            # self.child_up_left    = 
            # self.child_up_right   = 
            # self.child_down_left  = 
            # self.child_down_right = 
            self.point_4=np.asarray([(self.point_0[0]+self.point_1[0])/2, (self.point_0[1]+self.point_3[1])/2, 0.0])
            self.point_5=np.asarray([(self.point_0[0]+self.point_1[0])/2, self.point_0[0], 0.0])
            self.point_6=np.asarray([self.point_1[0], (self.point_1[1]+self.point_2[1])/2, 0.0])
            self.point_7=np.asarray([(self.point_2[0]+self.point_3[0])/2, self.point_2[1], 0.0])
            self.point_8=np.asarray([self.point_0[0], (self.point_0[1]+self.point_3[1])/2, 0.0])
            self.child_up_left    = tree_amr(self.point_8, self.point_4, self.point_7, self.point_3, depth+1, depth_max)
            self.child_up_right   = tree_amr(self.point_4, self.point_6, self.point_2, self.point_7, depth+1, depth_max)
            self.child_down_left  = tree_amr(self.point_0, self.point_5, self.point_4, self.point_8, depth+1, depth_max)
            self.child_down_right = tree_amr(self.point_5, self.point_1, self.point_6, self.point_4, depth+1, depth_max)
            
            print ('tree_amr.init has already been coded')

    def Create_Mesh_And_Connectivity_List(self, List_Of_Point, Connectivity):

        #      inputs :
        #        ListOfPoint : list that already includes points provided by
        #                      another routine
        #        Connectivity : connectivity list that already includes
        #                       information provided by other routines

        #    outputs :
        #        ListOfPoint : you must add to this list the points related
        #                      to this leaf
        #        Connectivity : you must add to this list the connectivity that
        #                       describe your quad
        if self.branch == False:
            i = len(List_Of_Point)
            List_Of_Point.append(self.point_0)
            List_Of_Point.append(self.point_1)
            List_Of_Point.append(self.point_2)
            List_Of_Point.append(self.point_3)
            Connectivity.append(["2D", i, i+1, i+2, i+3])
        else:
        
            self.child_up_left.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
            self.child_up_right.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
            self.child_down_left.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
            self.child_down_right.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)

            
 

################################################################################
#
#    part of the module dedicated to check the routines
#
################################################################################

def test():
    point_1 = np.asarray([0.0, 0.0, 0.0])
    point_2 = np.asarray([1.0, 0.0, 0.0])
    point_3 = np.asarray([1.0, 1.0, 0.0])
    point_4 = np.asarray([0.0, 1.0, 0.0])
    depth_max = 2
    depth = 0 

    my_tree = tree_amr(point_1, point_2, point_3, point_4, depth, depth_max)
    
    List_Of_Point = []
    Connectivity = []
    my_tree.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)

    MyVtkFile = vtk.FileVTK('tree_amr_case_2',
                            'first time I can see my quadtree')
    MyVtkFile.SavePoints(List_Of_Point)
    MyVtkFile.SaveConnectivity(Connectivity)
    MyVtkFile.close()

if __name__ == "__main__":
    test()
