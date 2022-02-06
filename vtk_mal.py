# -*- coding: utf-8 -*-

import numpy as np 

class FileVTK:

    def __init__(self, FileName, Comment):
        self.F=open(FileName+".vtk",'w')
        self.F.write(Comment)


    def SavePoints(self, PointList):

        self.F.write('\nPOINTS '+str(len(PointList))+str(type(PointList[0][0])))
        for i in range(len(PointList)):
            self.F.write('\n')
            for j in range(len(PointList[i])):
                self.F.write('  '+str(PointList[i][j]))
        

    def SaveConnectivity(self, Connectivity):
        n=0
        for i in range(len(Connectivity)):
            n+=len(Connectivity[i])
        self.F.write('\nCELLS '+str(len(Connectivity))+' '+str(n))
        for i in range(len(Connectivity)):
            h=len(Connectivity[i])-1
            self.F.write('\n '+str(h))
            for j in range(1,len(Connectivity[i])):
                self.F.write('  '+str(Connectivity[i][j]))
        self.F.write('\nCELL_TYPES '+str(len(Connectivity)))
        for i in range(len(Connectivity)):
            l=len(Connectivity[i])-1
            if Connectivity[i][0]=='3D':
                if l==4:
                    t=10
                elif l==8:
                    t=12
            elif Connectivity[i][0]=='2D':
                if l==2:
                    t=3
                elif l==3:
                    t=5
                elif l==4:
                    t=9
            self.F.write('\n  '+str(t))

        
    def CreatePointScalarSection(self,Points):
        print ('FileVTK.CreatePointScalarSection function to be coded')
        self.F.write('POINT_DATA' + str(len(Points)) + '\n')
    def SavePointScalar(self, Label, Values):
        self.F.write('SCALARS ' + Label + ' float \n')
        self.F.write('LOOKUP_TABLE default \n')
        for value in Values:
            self.F.write('  ' + str(value) + '\n')
    def close(self):
        self.F.close()

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
    Connectivity.append(["3D", 0, 1, 2, 3, 4, 5, 6 ,7])    # a hexahedron  
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

