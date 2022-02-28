import math

class ConvexHull:
    def __init__(self, bucket):
        self.bucket = bucket.tolist()
        
        #Fungsi untuk mencari index titik yang merupakan convex hull
        def getVertices():

            #mencari index letak titik paling kiri dan paling kanan
            x = []
            for item in self.bucket:
                x.append(item[0])
            idx_min,idx_max = getMinMax(x)
            
            #membagi titik titik menjadi s1 dan s2
            matrix = [[1 for i in range(3)] for i in range(3)]
            matrix[0][0] = self.bucket[idx_min][0]
            matrix[0][1] = self.bucket[idx_min][1]
            matrix[1][0] = self.bucket[idx_max][0]
            matrix[1][1] = self.bucket[idx_max][1]

            s1 = []
            s2 = []
            for i in range(len(self.bucket)):
                matrix[2][0] = self.bucket[i][0]
                matrix[2][1] = self.bucket[i][1]
                det = getDeterminant(matrix)
                if (det > 0):
                    s1.append(i)
                elif (det < 0) :
                    s2.append(i)
            
            Hull1 = RecConvexHull(idx_min,idx_max, s1, True)
            Hull2 = RecConvexHull(idx_min,idx_max, s2, False)
            invertArray(Hull2)

            vertices = [idx_min]
            for item in Hull1:
                vertices.append(item)
            vertices.append(idx_max)
            for item in Hull2:
                vertices.append(item)

            return vertices
        
        # Fungsi untuk mendapatkan pasangan titik untuk divisualisasikan
        def getSimplices():
            simplices = []
            for i in range(len(self.vertices)):
                s = []
                if i != len(self.vertices)-1:
                    s.append(self.vertices[i])
                    s.append(self.vertices[i+1])
                else:
                    s.append(self.vertices[i])
                    s.append(self.vertices[0])
                simplices.append(s)
            
            return simplices
        
        def getPoint():
            container = []
            for i in self.vertices:
                container.append(self.bucket[i])

            return container

        #fungsi untuk membalikan urutan array
        def invertArray(array):
            for i in range(math.floor(len(array)/2)):
                temp = array[i]
                array[i] = array[len(array)-1-i]
                array[len(array)-1-i] = temp

        #fungsi untuk mencari index dengan nilai min dan max pada array
        def getMinMax(array):
            min = array[0]
            max = array[0]
            idx_min = 0
            idx_max = 0
            for i in range(1,len(array)):
                if array[i] < min:
                    min = array[i]
                    idx_min = i
                elif array[i] > max:
                    max = array[i]
                    idx_max = i
            return idx_min, idx_max
        
        #fungsi untuk mencari determinan dengan menggunakan expansi kofaktor
        def getDeterminant(matrix):
            if len(matrix) == 1:
                return matrix[0][0]
            elif len(matrix) > 1:
                sign = 1
                det = 0
                for i in range(len(matrix)):
                    a = matrix[i][0]
                    m = []
                    for j in range(len(matrix)):
                        m1 = []
                        for k in range(len(matrix[0])):
                            if j != i and k != 0:
                                m1.append(matrix[j][k])
                        if (len(m1) != 0):
                            m.append(m1)
                    det += sign * (a * getDeterminant(m))
                    sign *= -1
                return det

        # Fungsi untuk mencari titik yang berada di luar garis 
        # jika isLeft True maka fungsi mengembalikan titik-titik yang berada di kiri atas garis
        # jika isLeft False maka fungsi mengembalikan titik-titik yang berada di kanan bawah garis
        def DividePoint(idx1, idx2, si, isLeft):
            # inisiasi matrix untuk mencari determinan
            mat = [[1 for i in range(3)] for i in range(3)]
            mat[0][0] = self.bucket[idx1][0]
            mat[0][1] = self.bucket[idx1][1]
            mat[1][0] = self.bucket[idx2][0]
            mat[1][1] = self.bucket[idx2][1]

            s = []
            if isLeft:
                for i in si:
                    mat[2][0] = self.bucket[int(i)][0]
                    mat[2][1] = self.bucket[int(i)][1]
                    det = getDeterminant(mat)
                    if (det > 0):
                        s.append(i)
                return s   
            else:
                for i in si:
                    mat[2][0] = self.bucket[int(i)][0]
                    mat[2][1] = self.bucket[int(i)][1]
                    det = getDeterminant(mat)
                    if (det < 0):
                        s.append(i)
                return s   

        # Fungsi untuk mencari persamaan garis (ax + by + c = 0) antara 2 titik (x1,y1) dan (x2,y2)
        def PointToLine(x1,x2,y1,y2):
            distx = x2 - x1
            disty = y2 - y1
            a = disty
            b = -distx
            c = (distx*y1) - (disty*x1)
            return (a,b,c)

        # Fungsi untuk mencari titik terjauh dari garis
        def Distance(x1, y1, Line):
            d = abs((Line[0] * x1 + Line[1] * y1 + Line[2])) / (math.sqrt(Line[0] * Line[0] + Line[1] * Line[1]))
            return d

        # Fungsi Rekursif untuk mencari convex hull
        def RecConvexHull(idx1, idx2, s, isLeft):
            if len(s) == 0:
                return []
            elif len(s) == 1:
                return s
            else:
                max = 0
                id = -999
                Line = PointToLine(self.bucket[idx1][0],self.bucket[idx2][0],self.bucket[idx1][1],self.bucket[idx2][1])
                for i in s:
                    idx = int(i)
                    distance = Distance(self.bucket[idx][0], self.bucket[idx][1], Line)
                    if (max < distance):
                        max = distance
                        id = idx
                if (id != -999):
                    s1 = DividePoint(idx1, id, s, isLeft)
                    arr1 = RecConvexHull(idx1, id, s1, isLeft)
                    s2 = DividePoint(id, idx2, s, isLeft)
                    arr2 = RecConvexHull(id, idx2, s2, isLeft)

                    arr1.append(id)
                    for item in arr2:
                        arr1.append(item)

                    return arr1
                else:
                    return []

        self.vertices = getVertices()
        self.simplices = getSimplices()
        self.point = getPoint()