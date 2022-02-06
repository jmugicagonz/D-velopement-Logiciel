# -*- coding: utf-8 -*-

import numpy as np 

#Dans ce programme, on va créer un fichier vtk pour le visualiser avec paraview. Le but va être de prendre 
#Comme entrée une liste de cellules (segments, quadrangles, triangles, tétraèdres et hexaèdres)
#Et après visualiser ces objets ainsi que le maillage au tour.

class FileVTK:
#Dans la class FileVTK, on trouve six fonctions. Elle va partir d'une fichier pour lire avec un commentaire au début.

    def __init__(self, FileName, Comment):
#Cette fonction ouvre le fichier et écrit quelques paramétres.
        self.fichier = open(FileName + '.vtk','w')
        self.fichier.write('# vtk DataFile Version 3.1\n')
        self.fichier.write(Comment + '\n')
        self.fichier.write('ASCII \n')
        self.fichier.write('DATASET UNSTRUCTURED_GRID \n')

    def SavePoints(self, PointList):
#Cette fonction prend une liste de points et les écrit dans le fichier.
        n = len(PointList)
        self.fichier.write('POINTS ' + str(n) + ' ' + 'FLOAT' + '\n')
        for point in PointList:
            self.fichier.write('  ')
            for coordonnee in point:
                self.fichier.write(str(coordonnee) + ' ')
            self.fichier.write('\n')   

    def SaveConnectivity(self, Connectivity):
#Cette fonction va prendre "Connectivitu", une liste des connections entre les points et va
#les écrire dans le fichier en les associant les figure aux lesquelles les points
#correspondent.
        n = len(Connectivity)
        m = sum([len(objet) - 1 for objet in Connectivity]) + n
        self.fichier.write('CELLS ' + str(n) + ' ' + str(m) + '\n')
        for objet in Connectivity:
            self.fichier.write('  ' + str(len(objet) - 1) + ' ')
            for point in objet[1:]:
                self.fichier.write(str(point) + ' ')
            self.fichier.write('\n')
        self.fichier.write('CELL_TYPES ' + str(len(Connectivity)) + '\n')
        for objet in Connectivity:
            self.fichier.write('  ')
            if objet[0] == '3D':
                if len(objet[1:]) == 4:
                    self.fichier.write('10 \n')
                else:
                    self.fichier.write('12 \n')
            else:
                if len(objet[1:]) == 4:
                    self.fichier.write('9 \n')
                elif len(objet[1:]) == 3:
                    self.fichier.write('5 \n')
                else:
                    self.fichier.write('3 \n')

    def CreatePointScalarSection(self,Points):
#Cette fonction écrit le nombre de points en consideration.
        self.fichier.write('POINT_DATA ' + str(len(Points)) + '\n')

    def SavePointScalar(self, Label, Values):
#Cette fonction va écrire la mesure consideré, donne dans "Label"
#et après va écrire les valeurs correspondants à cette mesure sur les points.
        self.fichier.write('SCALARS ' + Label + ' float \n')
        self.fichier.write('LOOKUP_TABLE default \n')
        for value in Values:
            self.fichier.write('  ' + str(value) + '\n')

    def close(self):
#Finalement, cette fonction va fermer le fichier VTK qu'on a crée.
        self.fichier.close()

#################################################################################################################
#
#    Part of the module dedicated to auto-validation 
#
#################################################################################################################

def test():
    MyVtkFile = FileVTK('test_file','first test')

    #     create the mesh point list

    Points =[]
    Points.append([0.0, 0.0, 0.0]) # 0
    Points.append([1.0, 0.0, 0.0]) # 1
    Points.append([1.0, 1.0, 0.0]) # 2
    Points.append([0.0, 1.0, 0.0]) # 3
    Points.append([0.0, 0.0, 1.0]) # 4
    Points.append([1.0, 0.0, 1.0]) # 5
    Points.append([1.0, 1.0, 1.0]) # 6
    Points.append([0.0, 1.0, 1.0]) # 7
    Points.append([2.0, 0.0, 0.0]) # 8
    Points.append([2.0, 1.0, 0.0]) # 9
    Points.append([2.0, 1.0, 1.0]) # 10 

    #          7---------------6---------------10
    #         /               /|               |
    #        /               / |               |
    #       4---------------5  |               |
    #       |               |  |               |
    #       |  3------------|--2---------------9    
    #       | /             | /               /
    #       |/              |/               /
    #       0---------------1---------------8
    
    MyVtkFile.SavePoints(Points)

    #     create the connectivity with:
    Connectivity = []
    Connectivity.append(["3D", 1, 8, 2, 5])             # a tetrahedron 
    Connectivity.append(["3D", 0, 1, 2, 3, 4, 5, 6 ,7]) # a hexahedron
    Connectivity.append(["2D", 2, 9, 10, 6])            # a quadrilateral
    Connectivity.append(["2D", 8, 9, 2])                # a triangle
    Connectivity.append(["2D", 5, 10])                  # a line 

    MyVtkFile.SaveConnectivity(Connectivity)

    #     create point scalar section

    MyVtkFile.CreatePointScalarSection(Points)

    #    create the data values: distance to point [0.0, 0.0, 0.0]
    Values = []
    for Point in Points:
        Values.append(np.sqrt(Point[0]**2 + Point[1]**2 + Point[2]**2))
    MyVtkFile.SavePointScalar("distance", Values)

    #    create the data values: distance to point [0.0, 0.0, 0.0] time 3.0
    Values = []
    for Point in Points:
        Values.append(3.0 * np.sqrt(Point[0]**2 + Point[1]**2 + Point[2]**2))
    MyVtkFile.SavePointScalar("distance_*_3", Values)

    MyVtkFile.close()

if __name__ == "__main__":
    test()

