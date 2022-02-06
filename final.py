# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 13:56:26 2018

@author: Juan
"""

import numpy as np 
import vtk   as vtk
import mesh as m
import QuadTree3 as ta
#On va importer "vtk" pour genérer le fichier vtk et comme ça avoir la répresentation dans ParaView. "mesh" avec le but de lire et de créer les
#tetras, aussi calculer les distances des points à eux et finalement "QuadTree3" pour le maillage autour des tetras.


    
def compute_value(p, dico):
#Ici on va calculer le valeur de la signal en utilisant la fonction donné dans l'enoncé et aussi la fonciton "Distance_Between_a_Point_and_the_Modules"
#dans la class mesh. On done le point et le dictionaire dico définit dci-dessous et elle nous retourne le valeur de la signal.
    a = dico['distances'](p)[1]
    some=0
    for p in a:
        some += 1/(p+1e-14)
    if not (dico['distances'](p)[0]):
        return np.inf
    else:
        return (some)


def test_function(r0, r1, r2, r3, dico):
#Ici on redefinit la fonction test_function parce que laquelle on avait dans "QuadTree3" n'est pas adaptée au problème final.
#Cette fonction s'utilise pour savoir si on doit raffiner ou pas. Pour ça, on va voir si il y a au moins un point tu carré avec une 
#signal moins petit que notre valeur de la signal et un autre avec un valeur égal ou plus grande. Come ça, on va arriver à raffiner et
#avoir une isoligne parce que tous les carrés petits vont satisfaire cette condition-ci et ils ne seront plus raffinés à cause de la
#pronfondeur maximale qu'on va définir. C'est claire que si on cherche avoir des carrés petites et une ligne imaginaire qui les traverse
#ils doivent satisfaire la condition déjà exposé.
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
    #"r_target" va nous donner le valeur de la signal.
    if ((r0 <  r_target) | (r1 <  r_target) | (r2 <  r_target) | (r3 <  r_target)) \
     & ((r0 >= r_target) | (r1 >= r_target) | (r2 >= r_target) | (r3 >= r_target)): 
        return True 
    else: 
        return False
def test():
      #on fixe un carré initial qui va contenir tous le tetras (on est sure parce que j'ai regardé le fichier "defense_zone.txt")
      #on pourrait prendre un carré plu grand mais le programme prendrait encore plus de temps pour arriver à la solution.
      point1 = np.asarray([-15,-15,0.01])
      point2 = np.asarray([15,-15,0.01])
      point3 = np.asarray([15,15,0.01])
      point4 = np.asarray([-15,15,0.01])
      depth_max = 10
      depth = 0 
      List_Of_Point = []
      Connectivity = []
      #Maintenant on va lire le fichier et on va créer les tétraèdres avec la class "mesh". 
      mesh=m.mesh('defense_zone.txt')
      mesh.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
      #On va definir un dictionnaire pour avoir plus de facilité pour passer des fonctions et valeurs aux fonctions.
      dico = {}  #this dictionnary is used to send any structure to the quad_tree
      dico['eval_function'] = compute_value
      dico['refine_or_not'] = test_function
      dico['distances'] = mesh.Distance_Between_a_Point_and_the_Modules
      dico['r_target'] = 1
      dico['level_min']= 5
      #C'est important de mettre une profondeur minimal au moins de 5 parce que sinon le programme probablement s'arrêtera avant
      #de construire le maillage.
      #Maintenant on va créer le maillage.
      my_tree=ta.tree_amr(point1, point2, point3, point4, depth, depth_max,dico)
      my_tree.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
      #Grace à la class "vtk" on va créer le fichier vtk.
      MyVtkFile = vtk.FileVTK('maillage1','Premiere maillage')
      MyVtkFile.SavePoints(List_Of_Point)
      MyVtkFile.SaveConnectivity(Connectivity)
      MyVtkFile.close()
      #On répéte la procédure pour les autres maillages. 
      dico['r_target'] = 1.2
      dico['level_min']= 5
      my_tree=ta.tree_amr(point1, point2, point3, point4, depth, depth_max,dico)
      my_tree.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
      MyVtkFile = vtk.FileVTK('maillage2','Premiere maillage')
      MyVtkFile.SavePoints(List_Of_Point)
      MyVtkFile.SaveConnectivity(Connectivity)
      MyVtkFile.close()
      dico['r_target'] = 1.5
      dico['level_min']= 5
      my_tree=ta.tree_amr(point1, point2, point3, point4, depth, depth_max,dico)
      my_tree.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
      MyVtkFile = vtk.FileVTK('maillage3','Premiere maillage')
      MyVtkFile.SavePoints(List_Of_Point)
      MyVtkFile.SaveConnectivity(Connectivity)
      MyVtkFile.close()

#finalement on exécute le programme.
if __name__ == "__main__":
    test()