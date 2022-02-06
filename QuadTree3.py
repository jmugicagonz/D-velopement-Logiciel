# -*- coding: utf-8 -*-

import numpy as np 
import vtk   as vtk 
#on import le fichier vtk parce que on va l'utiliser pour créer un autre fichier vtx a fin de visualiser la 
#division du space qu'on va faire sur ParaView.

#class that defines a tree structure based on quad

class tree_amr:
 def __init__(self, point_0, point_1, point_2, point_3, depth, depth_max,
                 dico):
#On va faire un programme similaire à quadtree2 mais plus sofistiqué. On va introduire un dictionaire a fin de utiliser certaines fonctions
#dans "init" pour évaluer si on doit diviser l'espace ou non.
            #     creation of a branch or a leaf 
    
            #   Be carefull this a recursive function 
    
            #    inputs:
            #        point_0 : point 0 of the quad  
            #        point_1 : point 1 of the quad   
            #        point_2 : point 2 of the quad   
            #        point_3 : point 3 of the quad  
            #        depth   : depth of the local branch or leaf in the tree 
            #        depth_max : maximum depth allowed in this tree 
            #        dico : it is a dictionnary that includes at least :
            #        dico['eval_function'] : a function used to compute the
            #                                physical value value on a point
            #            inputs :
            #                point : the point of the quad
            #                dico  : the dictionnary that includes all what you need
            #            outputs :
            #                this function returns the physical value estimated at
            #                this point
            #        dico['refine_or_not'] : a function used to decide if the leaf
            #                                should be transformed in a branch
            #            inputs :
            #                value_0 : physical value at point_0 of the quad
            #                value_1 : physical value at point_1 of the quad
            #                value_2 : physical value at point_2 of the quad
            #                value_3 : physical value at point_3 of the quad
            #                dico  : the dictionnary that includes all what you need
            #            outputs :
            #                this function returns True or False 
            #        dico['level_min'] : you must refine at least up to this depth 
    
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
            
            #dans notre cas, 'eval function' va évaluer distance de chaque sommet au centre du carré original.
            self.value_0 = dico['eval_function'](self.point_0,dico)
            self.value_1 = dico['eval_function'](self.point_1,dico)
            self.value_2 = dico['eval_function'](self.point_2,dico)
            self.value_3 = dico['eval_function'](self.point_3,dico)

            #on évalue si on doit réfiner en fonction de les valeurs des signals de nos points mais aussi si la profondeur actuelle est
            #plus petite que la pronfondeur minimal qu'on cherche. Comme ça on peut assurer qu'on trouvera des points avec lesquelles
            #la fonction 'refine_or_not' va être 'TRUE' et on arrivera à une solution. Si on le fait pas, on risque que le programme s'arrête
            #sans avoir bien rafiné l'espace.
            if (((depth < depth_max) & dico['refine_or_not'](self.value_0,self.value_1,self.value_2,self.value_3,dico)) or depth<dico['level_min']):

                
                    #   We must transform the leaf into a branch 
                    #   creation of the new leaves, this is the recursive part
                    self.branch = True
                    #   creation points 4 to 8 that are used to create the new leaves 
                    self.point_4 = np.asarray([(self.point_0[0] + self.point_1[0])/2,(self.point_0[1] + self.point_3[1])/2,0.1])
                    self.point_5 = np.asarray([(self.point_0[0] + self.point_1[0])/2,(self.point_0[1] + self.point_1[1])/2,0.1])
                    self.point_6 = np.asarray([(self.point_1[0] + self.point_2[0])/2,(self.point_1[1] + self.point_2[1])/2,0.1])
                    self.point_7 = np.asarray([(self.point_2[0] + self.point_3[0])/2,(self.point_2[1] + self.point_3[1])/2,0.1])
                    self.point_8 = np.asarray([(self.point_3[0] + self.point_0[0])/2,(self.point_3[1] + self.point_0[1])/2,0.1])  
                    #   creation of the new leaves, this is the recursive part
                    self.child_up_left    = tree_amr(self.point_8, self.point_4, self.point_7, self.point_3, depth + 1, depth_max, dico)
                    self.child_up_right   = tree_amr(self.point_4, self.point_6, self.point_2, self.point_7, depth + 1, depth_max, dico)
                    self.child_down_left  = tree_amr(self.point_0, self.point_5, self.point_4, self.point_8, depth + 1, depth_max, dico)
                    self.child_down_right = tree_amr(self.point_5, self.point_1, self.point_6, self.point_4, depth + 1, depth_max, dico)

 def Create_Mesh_And_Connectivity_List(self, List_Of_Point, Connectivity):
#Avec cette fonction on va rajouter les nouveaux points "leaves" à "List_Of_Point" et aussi ses conexions à "Connectivity" pour pouvaoir
#après répresenter les carrés avec ParaView. Cette est une fonction récursive qui permet d'arriver aux "fils" rafinés qui nous interesent
#à l'interieur de notre carré original. De cette façon, si "self.branch=TRUE" ça veut dire qu'on veut continuer à rafiner le carré, donc
#on ajoute pas les sommets. Une fois que "self.branch=FALSE", ça veut dire soit qu'on veut pas continuer à rafiner là, soit qu'ont est arrivé
#à la profondeur maximal, et dans tous les deux cas, on ajoutera les sommets et sa  connexion "Connectivity" corréspondante.

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

        if self.branch:
        #Si le carré dans lequel on se trouve a été encore rafiné.
            self.child_up_left.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
            self.child_up_right.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
            self.child_down_left.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
            self.child_down_right.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
        else:
        #Si le carré dans lequel on se trouve n'est plus rafiné.
            List_Of_Point.append(self.point_0)
            List_Of_Point.append(self.point_1)
            List_Of_Point.append(self.point_2)
            List_Of_Point.append(self.point_3)
            n = len(List_Of_Point)
            Connectivity.append(['2D',n - 4,n - 3,n - 2,n - 1])


 def Get_values(self, List_Of_Values):
 #Cette fonction marche de manière pareil à "Create_Mesh_And_Connectivity_List". Si le carré dans lequel on se trouve a été rafiné,
 #"self.branch=TRUE" et on va apliquer une recursivité et on ne va pas ajouter les valeurs des sommets à "List_Of_Values". Une fois qu'on
 #arrive a un carré qui ne va pas être plus rafiné, on ajoute le valeur calculé par "dico['eval_function'](self.point_x,dico)" (dans
 #ce cas ici elle corresponde à la fonction "compute_value") pour les quatre sommets dans "List_Of_Values".
        if self.branch:
            self.child_up_left.Create_Mesh_And_Connectivity_List(List_Of_Values)
            self.child_up_right.Create_Mesh_And_Connectivity_List(List_Of_Values)
            self.child_down_left.Create_Mesh_And_Connectivity_List(List_Of_Values)
            self.child_down_right.Create_Mesh_And_Connectivity_List(List_Of_Values)
        else:
            List_Of_Values.append(self.value_0)
            List_Of_Values.append(self.value_1)
            List_Of_Values.append(self.value_2)
            List_Of_Values.append(self.value_3)



################################################################################
#
#    part of the module dedicated to check the routines
#
################################################################################

def compute_value(p, dico):
    #dans ce cas ici, conpute value va calculer la distance de notre point au centre du carré.
    center = dico['center']
    return np.sqrt((p[0] - center[0])**2 + (p[1] - center[1])**2 + (p[2] - center[2])**2)

def test_function(r0, r1, r2, r3, dico):
    # function to choose if the mesh needs to be refined
    # dico['refine_or_not'] : a function used to decide if the leaf should be
    #                         transformed in a branch
    #     inputs :
    #         value_0 : physical value at point_0 of the quad
    #         value_1 : physical value at point_1 of the quad
    #         value_2 : physical value at point_2 of the quad
    #         value_3 : physical value at point_3 of the quad
    #         dico    : the dictionnary that includes all what you need
    #     outputs :
    #         this function returns True or False 
    r_target = dico['r_target']

    if ((r0 <  r_target) | (r1 <  r_target) | (r2 <  r_target) | (r3 <  r_target)) \
     & ((r0 >= r_target) | (r1 >= r_target) | (r2 >= r_target) | (r3 >= r_target)):    
        return True 
    else: 
        return False


def test():
    point_1 = np.asarray([0.0, 0.0, 0.0])
    point_2 = np.asarray([1.0, 0.0, 0.0])
    point_3 = np.asarray([1.0, 1.0, 0.0])
    point_4 = np.asarray([0.0, 1.0, 0.0])
    depth_max = 10
    depth = 0 

    dico = {}  # this dictionnary is used to send any structure to the quad_tree
    dico['eval_function'] = compute_value
    dico['refine_or_not'] = test_function
    dico['center']        = [0.0 , 0.0, 0.0]
    dico['r_target']      = 0.3
    dico['level_min']     = 1

    my_tree = tree_amr(point_1, point_2, point_3, point_4, depth, depth_max,
                       dico)

    List_Of_Point = []
    Connectivity = []
    my_tree.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)

    MyVtkFile = vtk.FileVTK('tree_amr_case_3',
                            'quadtree refined using the target function')
    MyVtkFile.SavePoints(List_Of_Point)
    MyVtkFile.SaveConnectivity(Connectivity)
    MyVtkFile.close()

if __name__ == "__main__":
    test()
