# -*- coding: utf-8 -*-

import numpy as np 

import tetra as t
import vtk as vtk
#On va importer la class "tetra" pour créer et utiliser les fonctions correspondantes aux tétraèdres et "vtk" pour
#créer le fichier qu'on va répresenter avec ParaView.

class mesh:
#Comme dit dans l'énoncé, dans ce class on va créer un objet maillage qui contiendra la liste de
#l’ensemble des tétraèdres et qui aura une méthode permettant de tracer l’ensemble des tétraèdres
#ainsi qu’une méthode calculant la valeur de S pour n’importe quel point de l’espace. Pour initialiser
#cet objet on lui fournira comme entrée un fichier texte qui contiendra les informations suivantes :
#nombre de tétraèdres
#coordonnées du centre de la base du tétraèdre
#longueur du coté du triangle équilatéral servant de base
#hauteur du tétraèdre
#rotation du tétraèdre autour de sa hauteur

    def __init__ (self, DefenseFile):

        # input : 
        #    - DefenseFile, it is a text file that contains the description of
        #      all defense module
        # output : 
        #    - initialise the attribute self.List_Of_Module 
        f = open('defense_zone.txt','r')
        #On ouvre le fichier en mode lecture.
        
        self.List_Of_Modules = []
        j=0
        i=0
        #Ici, dans les variables "center", "baselength", "height" et "rotation" avec les boucles bien posés on va garder 
        #l'information des tétraèdres donnes.
        for line in f:
            if j>=1:
                if (j)%4==1:
                   lineprime = line.split(':')
                   #on utilise cette commande pour diviser la ligne qu'on lis dans deux parts quand on trouve le ":".
                   centerprime=lineprime[1].split()
                   center = np.asarray([float(centerprime[0]),float(centerprime[1]),float(centerprime[2])])
                elif (j-1-4*i)//2==0:
                   lineprime = line.split(':')
                   baselenght=float(lineprime[1])
                   
                elif (j-1-4*i)//3==0:
                   lineprime = line.split(':')
                   height=float(lineprime[1])
                   
                elif (j-1-4*i)//4==0:
                   lineprime = line.split(':')
                   rotation=float(lineprime[1])
                   rotation = rotation*(np.pi)/180
                   baselenght=baselenght*np.sin((np.pi)/3)
                   #Maintenant, avec l'information qu'on a déjà et quelques calculs on va obtenir les quatres points du tétraèdre.
                   point4=np.asarray([center[0],center[1], height])
                   point1=np.asarray([center[0]+(2/3)*baselenght*np.cos((np.pi)/2 + rotation),center[1]+(2/3)*baselenght*np.sin((np.pi)/2 + rotation),0])
                   point2=np.asarray([center[0]+(2/3)*baselenght*np.cos((np.pi)+(np.pi)/6 + rotation),center[1]+(2/3)*baselenght*np.sin((np.pi)+(np.pi)/6 + rotation),0])
                   point3=np.asarray([center[0]+(2/3)*baselenght*np.cos(-np.pi*1/6 + rotation),center[1]+(2/3)*baselenght*np.sin(-np.pi*1/6 + rotation),0])
                   #Ici on va créer le tratra à partir des points déjà calculés.
                   tet= t.tetra(point1,point2,point3,point4)
                   #Une fois crée, on le rajoute (les faces données par la class "tetra") dans "List_Of_Modules"
                   self.List_Of_Modules.append(tet)
                   i+=1
                   
                j+=1
            else:
                j+=1

 

    def Create_Mesh_And_Connectivity_List(self, List_Of_Point, Connectivity):
    #Avec cette fonction, pour chaque tetra dans "List_Of_Modules" on va utiliser la fonction "Create_Mesh_And_Connectivity_List"
    #de la class "tetra" pour ajouter les quatre sommets de chacun dans "List_Of_Point" et ses connexions correspondantes
    #dans "Connectivity".

        #     inputs :
        #        - List_Of_Point : list that already includes points provided
        #                          by another routine
        #        - Connectivity : connectivity list that already includes
        #                         information provided by other routines

        #    outputs :
        #        - List_Of_Point : you must add to this list the points
        #                          related to all the tetra of this mesh
        #        - Connectivity : you must add to this list the connectivity
        #                         that describe all the tetra of this mesh
        for tet in self.List_Of_Modules:
            tet.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)

    def Distance_Between_a_Point_and_the_Modules(self, p):
    #Ici on va utiliser une procédure similaire à quand on calculais la distance to a tetra mais on prendra la distance minimal
    #à chacun des tetras lasquelles on gardera dans "d_min" si le point n'est à l'intérieur d'auncun tetra. S'il est à l'intérieur
    #d'un tetra, "outside=False". La fonction retourne "outside" qui dit s'il est externe à tous les tetras et le vecteur "d_min".

        #    inputs : 
        #         - p it is a point
        #    output : [True/False, d_min]
        #         - False if the point is inside one of the defense module 
        #         - d_min = [] list of minimum distance from the point to the
        #                      each defense module
        outside = True
        i=0
        d_min=[]
        for tet in self.List_Of_Modules:
            d_min.append(tet.distance_to_a_point(p)[1])
            i+=1
            outside=outside and tet.distance_to_a_point(p)[0]

        
        return [outside, d_min] 

################################################################################
#
#    Part of the module dedicated to auto-validation 
#
################################################################################

def test_1():

    print ('Test 1 used to create the vtk file to plot the defense zone')

    defense_zone = mesh("defense_zone.txt")

    List_Of_Point = []
    Connectivity = []

    defense_zone.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
    MyVtkFile = vtk.FileVTK('defense_zone','all the tetra in your defense zone')
    MyVtkFile.SavePoints(List_Of_Point)
    MyVtkFile.SaveConnectivity(Connectivity)
    MyVtkFile.close()

def test_2():

    print ('Test 2 return all the distances from the tetras and a point')
    defense_zone = mesh("defense_zone.txt")

    p = np.asarray([0.0, 0.0, 0.0])

    [test, d_min] = defense_zone.Distance_Between_a_Point_and_the_Modules(p)

    print ('the point is outside the defense modules: '+str(test))
    print ('distance min: '+str(d_min))

if __name__ == "__main__":
    test_1()
    test_2()
