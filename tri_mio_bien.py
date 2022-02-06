# -*- coding: utf-8 -*-

import numpy as np 
import vtk   as vtk


class tri: 
    
    """
    A triangle is defined by three points and a normal
    
    The normal of the triangle face is defined by 
    N = P1P2 x P1P3 
    
    where x is the cross product and abs(N) = 1

    Attributes
    ----------
    points : nested list of the three triangle vertices 
            (cartesian coordinates)
        
    normal : normal of the triangle (vector components)       
    """

    def __init__(self, point1, point2, point3):

        """
        Create a triangle by computing the normal and by storing the three 
        vertices as attributes
    
        Inputs
        -----
        point1, point2, point3 : the three triangle vertices
                                (cartesian coordinates)
        """     
        self.points = np.asarray([point1,point2,point3])
        vector1 = np.asarray([point2[i]-point1[i] for i in range (3)])
        vector2 = np.asarray([point3[i]-point1[i] for i in range (3)])
        normal = 1/np.sqrt((vector1[1]*vector2[2]-vector1[2]*vector2[1])**2+(vector1[2]*vector2[0]-vector1[0]*vector2[2])**2+(vector1[0]*vector2[1]-vector1[1]*vector2[0])**2)*np.asarray([vector1[1]*vector2[2]-vector1[2]*vector2[1],vector1[2]*vector2[0]-vector1[0]*vector2[2],vector1[0]*vector2[1]-vector1[1]*vector2[0]])
        self.normal=normal
    def Create_Mesh_And_Connectivity_List(self, List_Of_Point, Connectivity):

        """
        The three vertices of the new triangle are stored in List_of_Point and 
        Connectivity
        
        Inputs/Outputs
        --------------
        List_Of_Point : nested list of points of triangles 
                        (cartesian coordinates)
        
        Connectivity  : nested list of connectivity indices over each triangle 
                        vertex (array indices)
        """
        List_Of_Point += [self.points[0],self.points[1],self.points[2]]
        n = len(List_Of_Point)
        Connectivity.append('2D',n-3,n-2,n-1)
        
        print ('tri.Create_Mesh_And_Connectivity_List to be coded')

    def Create_Tri_and_Normal_Mesh_Connectivity_List(self, List_Of_Point, 
                                                     Connectivity):

        """
        The three vertices of the new triangle and the two points used to
        plot the normal are stored in List_of_Point and Connectivity
        
        Inputs / Outputs
        ----------------

        List_Of_Point : nested list of points of triangles and their normals 
                        (cartesian coordinates)
        
        Connectivity  : nested list of connectivity indices of triangle vertex 
                        and their normals (array indices) 
        """
        List_Of_Point += [self.points[0],self.points[1],self.points[2],np.asarray([(self.points[0][0]+self.points[1][0]+self.points[2][0])/3,(self.points[0][1]+self.points[1][1]+self.points[2][1])/3,(self.points[0][2]+self.points[1][2]+self.points[2][2])/3]),np.asarray([(self.points[0][0]+self.points[1][0]+self.points[2][0])/3 + self.normal[0],(self.points[0][1]+self.points[1][1]+self.points[2][1])/3 + self.normal[1],(self.points[0][2]+self.points[1][2]+self.points[2][2])/3+self.normal[2]])]
        n = len(List_Of_Point)
        Connectivity.append(['2D',n-5,n-4,n-3])
        Connectivity.append(['2D',n-2,n-1])
        
        print ('tri.Create_Tri_and_Normal_Mesh_Connectivity_List to be coded')

     
    def distance_to_a_point(self, p):

        """
        Compute the minimum distance from a point to one of the triangle
        vertex.
        
        Input
        -----

        p : point (cartesian coordinates)

        Returns
        -------
        
        distance_to_a_point : list [True/False, d_min]
          - True only if the face is pointing in the direction of point 
          - d_min : minimum distance from the point to the face
        """

        # first we check if the face is pointing toward the point
        
        normal_side = False
        d_min = np.inf                   # Numpy Infinity
        
        if np.dot(self.normal,np.asarray([p[0] - self.points[0][0],p[1] - self.points[0][1], p[2] - self.points[0][2]])) < 0:
            return([normal_side,d_min])
        else:
            normal_side = True
            def pointTriangleDistance(TRI, P):
                # function [dist,PP0] = pointTriangleDistance(TRI,P)
                # calculate distance between a point and a triangle in 3D
                # SYNTAX
                #   dist = pointTriangleDistance(TRI,P)
                #   [dist,PP0] = pointTriangleDistance(TRI,P)
                #
                # DESCRIPTION
                #   Calculate the distance of a given point P from a triangle TRI.
                #   Point P is a row vector of the form 1x3. The triangle is a matrix
                #   formed by three rows of points TRI = [P1;P2;P3] each of size 1x3.
                #   dist = pointTriangleDistance(TRI,P) returns the distance of the point P
                #   to the triangle TRI.
                #   [dist,PP0] = pointTriangleDistance(TRI,P) additionally returns the
                #   closest point PP0 to P on the triangle TRI.
                #
                # Author: Gwolyn Fischer
                # Release: 1.0
                # Release date: 09/02/02
                # Release: 1.1 Fixed Bug because of normalization
                # Release: 1.2 Fixed Bug because of typo in region 5 20101013
                # Release: 1.3 Fixed Bug because of typo in region 2 20101014
            
                # Possible extention could be a version tailored not to return the distance
                # and additionally the closest point, but instead return only the closest
                # point. Could lead to a small speed gain.
            
                # Example:
                # %% The Problem
                # P0 = [0.5 -0.3 0.5]
                #
                # P1 = [0 -1 0]
                # P2 = [1  0 0]
                # P3 = [0  0 0]
                #
                # vertices = [P1; P2; P3]
                # faces = [1 2 3]
                #
                # %% The Engine
                # [dist,PP0] = pointTriangleDistance([P1;P2;P3],P0)
                #
                # %% Visualization
                # [x,y,z] = sphere(20)
                # x = dist*x+P0(1)
                # y = dist*y+P0(2)
                # z = dist*z+P0(3)
                #
                # figure
                # hold all
                # patch('Vertices',vertices,'Faces',faces,'FaceColor','r','FaceAlpha',0.8)
                # plot3(P0(1),P0(2),P0(3),'b*')
                # plot3(PP0(1),PP0(2),PP0(3),'*g')
                # surf(x,y,z,'FaceColor','b','FaceAlpha',0.3)
                # view(3)
            
                # The algorithm is based on
                # "David Eberly, 'Distance Between Point and Triangle in 3D',
                # Geometric Tools, LLC, (1999)"
                # http:\\www.geometrictools.com/Documentation/DistancePoint3Triangle3.pdf
                #
                #        ^t
                #  \     |
                #   \reg2|
                #    \   |
                #     \  |
                #      \ |
                #       \|
                #        *P2
                #        |\
                #        | \
                #  reg3  |  \ reg1
                #        |   \
                #        |reg0\
                #        |     \
                #        |      \ P1
                # -------*-------*------->s
                #        |P0      \
                #  reg4  | reg5    \ reg6
                # rewrite triangle in normal form
                B = TRI[0, :]
                E0 = TRI[1, :] - B
                # E0 = E0/sqrt(sum(E0.^2)); %normalize vector
                E1 = TRI[2, :] - B
                # E1 = E1/sqrt(sum(E1.^2)); %normalize vector
                D = B - P
                a = dot(E0, E0)
                b = dot(E0, E1)
                c = dot(E1, E1)
                d = dot(E0, D)
                e = dot(E1, D)
                f = dot(D, D)
            
                #print "{0} {1} {2} ".format(B,E1,E0)
                det = a * c - b * b
                s = b * e - c * d
                t = b * d - a * e
            
                # Terible tree of conditionals to determine in which region of the diagram
                # shown above the projection of the point into the triangle-plane lies.
                if (s + t) <= det:
                    if s < 0.0:
                        if t < 0.0:
                            # region4
                            if d < 0:
                                t = 0.0
                                if -d >= a:
                                    s = 1.0
                                    sqrdistance = a + 2.0 * d + f
                                else:
                                    s = -d / a
                                    sqrdistance = d * s + f
                            else:
                                s = 0.0
                                if e >= 0.0:
                                    t = 0.0
                                    sqrdistance = f
                                else:
                                    if -e >= c:
                                        t = 1.0
                                        sqrdistance = c + 2.0 * e + f
                                    else:
                                        t = -e / c
                                        sqrdistance = e * t + f
            
                                        # of region 4
                        else:
                            # region 3
                            s = 0
                            if e >= 0:
                                t = 0
                                sqrdistance = f
                            else:
                                if -e >= c:
                                    t = 1
                                    sqrdistance = c + 2.0 * e + f
                                else:
                                    t = -e / c
                                    sqrdistance = e * t + f
                                    # of region 3
                    else:
                        if t < 0:
                            # region 5
                            t = 0
                            if d >= 0:
                                s = 0
                                sqrdistance = f
                            else:
                                if -d >= a:
                                    s = 1
                                    sqrdistance = a + 2.0 * d + f;  # GF 20101013 fixed typo d*s ->2*d
                                else:
                                    s = -d / a
                                    sqrdistance = d * s + f
                        else:
                            # region 0
                            invDet = 1.0 / det
                            s = s * invDet
                            t = t * invDet
                            sqrdistance = s * (a * s + b * t + 2.0 * d) + t * (b * s + c * t + 2.0 * e) + f
                else:
                    if s < 0.0:
                        # region 2
                        tmp0 = b + d
                        tmp1 = c + e
                        if tmp1 > tmp0:  # minimum on edge s+t=1
                            numer = tmp1 - tmp0
                            denom = a - 2.0 * b + c
                            if numer >= denom:
                                s = 1.0
                                t = 0.0
                                sqrdistance = a + 2.0 * d + f;  # GF 20101014 fixed typo 2*b -> 2*d
                            else:
                                s = numer / denom
                                t = 1 - s
                                sqrdistance = s * (a * s + b * t + 2 * d) + t * (b * s + c * t + 2 * e) + f
            
                        else:  # minimum on edge s=0
                            s = 0.0
                            if tmp1 <= 0.0:
                                t = 1
                                sqrdistance = c + 2.0 * e + f
                            else:
                                if e >= 0.0:
                                    t = 0.0
                                    sqrdistance = f
                                else:
                                    t = -e / c
                                    sqrdistance = e * t + f
                                    # of region 2
                    else:
                        if t < 0.0:
                            # region6
                            tmp0 = b + e
                            tmp1 = a + d
                            if tmp1 > tmp0:
                                numer = tmp1 - tmp0
                                denom = a - 2.0 * b + c
                                if numer >= denom:
                                    t = 1.0
                                    s = 0
                                    sqrdistance = c + 2.0 * e + f
                                else:
                                    t = numer / denom
                                    s = 1 - t
                                    sqrdistance = s * (a * s + b * t + 2.0 * d) + t * (b * s + c * t + 2.0 * e) + f
            
                            else:
                                t = 0.0
                                if tmp1 <= 0.0:
                                    s = 1
                                    sqrdistance = a + 2.0 * d + f
                                else:
                                    if d >= 0.0:
                                        s = 0.0
                                        sqrdistance = f
                                    else:
                                        s = -d / a
                                        sqrdistance = d * s + f
                        else:
                            # region 1
                            numer = c + e - b - d
                            if numer <= 0:
                                s = 0.0
                                t = 1.0
                                sqrdistance = c + 2.0 * e + f
                            else:
                                denom = a - 2.0 * b + c
                                if numer >= denom:
                                    s = 1.0
                                    t = 0.0
                                    sqrdistance = a + 2.0 * d + f
                                else:
                                    s = numer / denom
                                    t = 1 - s
                                    sqrdistance = s * (a * s + b * t + 2.0 * d) + t * (b * s + c * t + 2.0 * e) + f
            
                # account for numerical round-off error
                if sqrdistance < 0:
                    sqrdistance = 0
            
                dist = sqrt(sqrdistance)
            
                PP0 = B + s * E0 + t * E1
                return dist, PP0
            
        d_min = pointTriangleDistance(self.points,p)[0]

        return [normal_side, d_min]


###############################################################################
#
#    Part of the module dedicated to auto-validation 
#
###############################################################################

def test_1(): 

    print ('\n First test used to plot the tri and its normal \n')
    # When a tri is defined like that, the normal should face toward Z > 0  
    p1 = np.asarray([0.0, 0.0, 0.0])
    p2 = np.asarray([1.0, 0.0, 0.0])
    p3 = np.asarray([0.0, 1.0, 0.0])
    my_tri = tri(p1, p2, p3)

    List_Of_Point = []
    Connectivity = []

    my_tri.Create_Tri_and_Normal_Mesh_Connectivity_List(List_Of_Point, 
                                                        Connectivity)

    MyVtkFile = vtk.FileVTK('tri',
                            'tri with its normal that should face toward Z>0')
    MyVtkFile.SavePoints(List_Of_Point)
    MyVtkFile.SaveConnectivity(Connectivity)
    MyVtkFile.close()

def test_2():
    
    print ('\n Second test used to check the distance' 
           'from a point to the tri ')
    # In this test case you will compute the distance min
    # between a point p and a triangle vertex
    p1 = np.asarray([0.0, 0.0, 0.0])
    p2 = np.asarray([1.0, 0.0, 0.0])
    p3 = np.asarray([0.0, 1.0, 0.0])
    my_tri = tri(p1, p2, p3)

    p = np.asarray([0.0, 0.0, 10.0])
    print ('test of point : '+str(p))
    [test, dist_min] = my_tri.distance_to_a_point(p)
    print ('test     : '+str(test))
    print ('dist_min : '+str(dist_min))
    print ('')

    p = np.asarray([0.0, 0.0, -10.0])
    print ('test of point : '+str(p))
    [test, dist_min] = my_tri.distance_to_a_point(p)
    print ('test     : '+str(test))
    print ('dist_min : '+str(dist_min))
    print ('')

if __name__ == "__main__":
    test_1()
    test_2()

