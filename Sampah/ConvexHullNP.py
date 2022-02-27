import numpy as np
import math

class ConvexHull:
    def __init__(self, bucket):
        def getVertices(bucket):
            # Cari index ujung kiri dan ujung kanan titik
            x = bucket[:,0]
            idx_minx = np.argmin(x)
            idx_maxx = np.argmax(x)
            
            # inisiasi matrix untuk mencari determinan
            mat = np.full((3, 3), 1.0)
            mat[0,0] = bucket[idx_minx][0]
            mat[0,1] = bucket[idx_minx][1]
            mat[1,0] = bucket[idx_maxx][0]
            mat[1,1] = bucket[idx_maxx][1]

            # cek apakah titik lain termasuk s1 atau s2
            s1 = np.array([])
            s2 = np.array([])
        
            for i in range(bucket.shape[0]):
                mat[2,0] = bucket[i][0]
                mat[2,1] = bucket[i][1]
                det = np.linalg.det(mat)
                if (det > 0):
                    s1 = np.append(s1, i)
                elif (det < 0) :
                    s2 = np.append(s2, i)
            
            Hull1 = RecConvexHull(idx_minx,idx_maxx, s1, bucket, True)
            Hull2 = RecConvexHull(idx_minx,idx_maxx, s2, bucket, False)
            Hull2 = np.flipud(Hull2)

            vertices = np.array([int(idx_minx)])
            for i in Hull1:
                vertices = np.append(vertices,int(i))
            vertices = np.append(vertices, [int(idx_maxx)])
            for i in Hull2:
                vertices = np.append(vertices,int(i))
            return vertices.astype(int)

        def getSimplices(vertices):
            simplices = np.array([[]])
            for i in range(vertices.shape[0]):
                if i != vertices.shape[0]-1:
                    simplices = np.append(simplices, [vertices[i], vertices[i+1]])
                else:
                    simplices = np.append(simplices, [vertices[i], vertices[0]])
            
            simplices = np.reshape(simplices, (-1, 2))
            simplices = simplices.astype(int)
            
            return simplices
        
        def getPoint(vertices, bucket):
            point = np.array([])
            for i in vertices:
                point = np.append(point, bucket[i])
            point = np.reshape(point, (-1, 2))
            return point

        def DividePoint(idx1, idx2, si ,bucket, isLeft):
            # inisiasi matrix untuk mencari determinan
            mat = np.full((3, 3), 1.0)
            mat[0,0] = bucket[idx1][0]
            mat[0,1] = bucket[idx1][1]
            mat[1,0] = bucket[idx2][0]
            mat[1,1] = bucket[idx2][1]

            s = np.array([])
            if isLeft:
                for i in si:
                    mat[2,0] = bucket[int(i)][0]
                    mat[2,1] = bucket[int(i)][1]
                    det = np.linalg.det(mat)
                    if (det > 0):
                        s = np.append(s, i)
                return s   
            else:
                for i in si:
                    mat[2,0] = bucket[int(i)][0]
                    mat[2,1] = bucket[int(i)][1]
                    det = np.linalg.det(mat)
                    if (det < 0):
                        s = np.append(s, i)
                return s   

        def PointToLine(x1,x2,y1,y2):
            distx = x2 - x1
            disty = y2 - y1
            a = disty
            b = -distx
            c = (distx*y1) - (disty*x1)
            return (a,b,c)

        def Distance(x1, y1, Line):
            d = abs((Line[0] * x1 + Line[1] * y1 + Line[2])) / (math.sqrt(Line[0] * Line[0] + Line[1] * Line[1]))
            return d

        def RecConvexHull(idx1, idx2, s, bucket, isLeft):
            if s.size == 0:
                return np.array([])
            elif s.size == 1:
                return s
            else:
                max = 0
                Line = PointToLine(bucket[idx1][0],bucket[idx2][0],bucket[idx1][1],bucket[idx2][1])
                for i in s:
                    idx = int(i)
                    distance = Distance(bucket[idx][0], bucket[idx][1], Line)
                    if (max < distance):
                        max = distance
                        id = idx
            
                s1 = DividePoint(idx1, id, s, bucket, isLeft)
                arr1 = RecConvexHull(idx1, id, s1, bucket, isLeft)
                s2 = DividePoint(id, idx2, s, bucket, isLeft)
                arr2 = RecConvexHull(id, idx2, s2, bucket, isLeft)
                arr = np.append(arr1,id)
                arr = np.append(arr,arr2)

                return arr

        self.vertices = getVertices(bucket)
        self.simplices = getSimplices(self.vertices)
        self.point = getPoint(self.vertices, bucket)