# -*- coding: utf-8 -*-

import numpy as np

import tri as t
import vtk as vtk
#on va prendre la class "tri" laquelle on va utiliser pour construire le tétraèdre. Aussi la class "vtk" comme dans
#les autre modules pour la répresentation dans ParaView".

class tetra: 
#Pour la class "tetra" on va donner les quatre points du tétraèdre et elle, avec "tri", va créer le tetra. On toruve aussi 
#les fonctions "Create_Mesh_And_Connectivity_List", "Create_Mesh_And_Connectivity_List_From_Tri", et "distance_to_a_point"
#que j'expliquerai ci-dessous.
    """
    A tetrahedron is defined by four points and a four triangles
    the normal of each triangle face should point out of the tetrahedron

    Attributes
    ----------
    
    points : nested list of the 4 tetrahedron vertices 
            (cartesian coordinates)
    
    faces : nested list of the 4 faces
    """

    def __init__(self, point1, point2, point3, point4):
    #Init va prendre les quatre points et en appelant la class "tri" va créer le tetra en ajoutant les faces dans un vecteur".
        """
        Create a tetrahedron by storing his 4 vertices and his 4 faces
        
        Inputs
        ------
        
        point1, point2, point3, point4 : the 4 tetrahedron vertices
        """
        
        self.points = np.asarray([point1,point2,point3,point4])
        self.faces = [t.tri(point1,point2,point3),
                      t.tri(point1,point2,point4),
                      t.tri(point4,point2,point3),
                      t.tri(point1,point2,point4)]

 

    def Create_Mesh_And_Connectivity_List(self, List_Of_Point, Connectivity):
    #Cet fonction va amplier "List_Of_Points" avec les points du tetra et dans "Connectivity" on va la amplier
    #avec les connexion et le format corréspondant à un tetra pour l'utiliser après avec ParaView".
        """
        Inputs
        ------
        List_Of_Point : list that already includes points provided by another 
                        routine
        Connectivity  : connectivity list that already includes information 
                        provided by other routines

        Outputs
        -------
        List_Of_Point : you must add to this list the points related to this 
                        tetra
        Connectivity : you must add to this list the connectivity that describe
                       your tetra
        """
        List_Of_Point+=[self.points[i] for i in range(4)]
        n = len(List_Of_Point)
        Connectivity.append(["3D",n-4,n-3,n-2,n-1]) 

    def Create_Mesh_And_Connectivity_List_From_Tri(self, 
                                                   List_Of_Point, 
                                                   Connectivity):
    #Avec cette fonction on va la donner nos faces, lesquelles ont une class "tri". Donc, quand on appele la fonction
    #"Create_Mesh_And_Connectivity_List", on va prendre cette fonction tu fichier "tri.py" lequel on a importé dans notre
    #programme. Donc, notre fonction va rajouter dans "List_Of_Point" les differentes points des faces et dans
    #"Connectivity" les conexions entre les points d echaque face. Ça va nous permettre créer quatre faces en lieu de créer
    #directement le tetra avec les quatre sommets.
        """
        Inputs
        ------
        List_Of_Point : list that already includes points provided by another
                        routine
        Connectivity  : connectivity list that already includes information 
                        provided by other routines

        Outputs
        -------
        List_Of_Point : you must add to this list the points related to each
                        tri of this tetra
        Connectivity  : you must add to this list the connectivity that 
                        describes each tri of this tetra 
        """
        for face in self.faces:
          face.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)

    def distance_to_a_point(self, p):
    #Avec cette fonction, on va donner un point p comme input. On va utiliser la fonction "distance_to_a_point" dans la class tri
    #pour calculer la distance du point à chaque face du tetra et on prendra la distance minimal. Il faut voir si le point est en face
    #d'une des faces du tetra, parce que sinon ça veut dire qu'il est à l'interieur. Dans ce cas ici, on ne calculera pas la distance
    #et on donera "ouside=False" pour que les fonctions des modules postérieurs ne le prennent pas. La fonction va nous donner un array
    #avec deux valeurs. Le première nous dira si le point est à l'extérieur ou à l'intérieur. S'il est à l'intérieur,
    #"outside=False" et la distance minimal égal à l'infini. S'il est à l'extérieur, "outside=True" et la distance minimal
    #avec son valeur corréspondant.
        """
        Inputs
        ------
        p : it is a point
        
        Outputs
        -------
        [True/False, d_min]
        - True only if one of the face of the tetra is pointing in 
          the direction of point 
        - d_min (if True) minimum distance from the point to the tetra
        """
        outside = False 
        [b1,d1],[b2,d2],[b3,d3],[b4,d4]=self.faces[0].distance_to_a_point(p),\
                                        self.faces[1].distance_to_a_point(p),\
                                        self.faces[2].distance_to_a_point(p),\
                                        self.faces[3].distance_to_a_point(p)
        outside = (b1 or b2 or b3 or b4) > 0
        d_min = np.inf
        if outside:
           d_min = min(d1,d2,d3,d4)
        
        return [outside, d_min] 
        

###############################################################################
#
#    Part of the module dedicated to auto-validation 
#
###############################################################################


def test_1(): 

    print ('First test that create two vtk files ')
    print ('   - the first file allows to plot the Tetra')
    print ('   - the second file allows to plot the Tetra and all the normal')
    print ('   of its tri to check if they a pointing in the right direction')
    point1 = np.asarray([0.0, 0.0, 0.0])
    point2 = np.asarray([1.0, 0.0, 0.0])
    point3 = np.asarray([0.0, 1.0, 0.0])
    point4 = np.asarray([0.0, 0.0, 1.0])
    my_tetra = tetra(point1, point2, point3, point4)

    List_Of_Point = []
    Connectivity = []
    my_tetra.Create_Mesh_And_Connectivity_List(List_Of_Point, Connectivity)
    MyVtkFile = vtk.FileVTK('tetra','tetra')
    MyVtkFile.SavePoints(List_Of_Point)
    MyVtkFile.SaveConnectivity(Connectivity)
    MyVtkFile.close()

    List_Of_Point = []
    Connectivity = []
    my_tetra.Create_Mesh_And_Connectivity_List_From_Tri(List_Of_Point, 
                                                        Connectivity)
    MyVtkFile = vtk.FileVTK('tetra_from_tri',
                            'Tri from a tetra and the normal of each face')
    MyVtkFile.SavePoints(List_Of_Point)
    MyVtkFile.SaveConnectivity(Connectivity)
    MyVtkFile.close()

def test_2():

    print ('Second test used to compute the distance of a point from a tetra')
    point1 = np.asarray([0.0, 0.0, 0.0])
    point2 = np.asarray([1.0, 0.0, 0.0])
    point3 = np.asarray([0.0, 1.0, 0.0])
    point4 = np.asarray([0.0, 0.0, 1.0])
    my_tetra = tetra(point1, point2, point3, point4)

    p = np.asarray([0.01, 0.01, 0.01])
    [test, d_min] = my_tetra.distance_to_a_point(p)

    print ('the point is outside the tetra: '+str(test))
    print ('distance min: '+str(d_min))

if __name__ == "__main__":
    test_1()
    test_2()
