# -*- coding: utf-8 -*-

import numpy as np 
#     class that defines a tree structure based on quad

class tree_amr:
#On a définit la class tree. Ça va consister en une fonction qui va recevoir comme variables
#quatre points differents en constituant un carré et une profondeur maximal. Aussi,
#la fonction va utiliser une autre variable "depth" laquelle va servir comme compteur de profondeur.
    def __init__(self, point_0, point_1, point_2, point_3, depth, depth_max):
#On définit une fonction récursive qui va prendre quatre points, et si la profondeur de division du carré est plus
#petite que la profondeur maximale, on va diviser le carré en quatre subcarrés et pour chaque subcarré, avec 
#ses quatre points respectives, on apliquera la class pour apliquer encore une fois la fonction init. Comme ça on va
#diviser l'espace jusqu'à une profondeur desirée.

    
        #first we suppose that when we create it, it is a leaf 
        self.branch = False

        #store the information locally in the memory for the leaf 
        self.point_0 = point_0
        self.point_1 = point_1
        self.point_2 = point_2
        self.point_3 = point_3
        
        if (depth < depth_max):

            #if the depth of the leaf is lower that the maximum depth 
            #then we check if we need to transform the leaf into a branch
            #We must transform the leaf into a branch 
            
            print ('depth < depth_max')
            self.branch = True
            #   creation points 4 to 8 that are used to create the new leaves 
            self.point_4 = np.asarray([(self.point_0[0] + self.point_1[0])/2,(self.point_0[1] + self.point_3[1])/2,0.0])
            self.point_5 = np.asarray([(self.point_0[0] + self.point_1[0])/2,(self.point_0[1] + self.point_1[1])/2,0.0])
            self.point_6 = np.asarray([(self.point_1[0] + self.point_2[0])/2,(self.point_1[1] + self.point_2[1])/2,0.0])
            self.point_7 = np.asarray([(self.point_2[0] + self.point_3[0])/2,(self.point_2[1] + self.point_3[1])/2,0.0])
            self.point_8 = np.asarray([(self.point_3[0] + self.point_0[0])/2,(self.point_3[1] + self.point_0[1])/2,0.0])            
            #   creation of the new leaves, this is the recursive part
            self.child_up_left    = tree_amr(self.point_8, self.point_4, self.point_7, self.point_3, depth + 1, depth_max)
            self.child_up_right   = tree_amr(self.point_4, self.point_6, self.point_2, self.point_7, depth + 1, depth_max)
            self.child_down_left  = tree_amr(self.point_0, self.point_5, self.point_4, self.point_8, depth + 1, depth_max)
            self.child_down_right = tree_amr(self.point_5, self.point_1, self.point_6, self.point_4, depth + 1, depth_max)

    def Create_Mesh_And_Connectivity_List(self, List_Of_Point, Connectivity):
        #avec cette fonction, on va amplier les listes des points et des conexions.

        #inputs:
        #        ListOfPoint : list that already includes points provided by
        #                      another routine
        #        Connectivity : connectivity list that already includes
        #                       information provided by other routines.On va l'utiliser
        #                       de manière que notre fichier vtk va créer un carré avec
        #                       ces points ici.

        #    outputs :
        #        ListOfPoint : you must add to this list the points related
        #                      to this leaf
        #        Connectivity : you must add to this list the connectivity that
        #                       describe your quad
        
        
        if self.branch:
            self.child_up_left.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
            self.child_up_right.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
            self.child_down_left.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
            self.child_down_right.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
        else:
            List_Of_Point.append(self.point_0)
            List_Of_Point.append(self.point_1)
            List_Of_Point.append(self.point_2)
            List_Of_Point.append(self.point_3)
            n = len(List_Of_Point)
            Connectivity.append(['2D',n - 4,n - 3,n - 2,n - 1])
        
          


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
    depth_max = 5
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
