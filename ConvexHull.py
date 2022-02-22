import numpy as np
import math

def aConvexHull(bucket):
    # Cari index ujung kiri dan ujung kanan titik
    x = bucket[:,0]
    idx_minx = np.argmin(x)
    idx_maxx = np.argmax(x)


    # value dari index ujung kiri dan ujung kanan titik
    # point_1 = bucket[idx_minx]
    # point_2 = bucket[idx_maxx]
    # bucket = np.delete(bucket, [idx_minx,idx_maxx], 0)
    
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

    final_Hull = np.array([int(idx_minx)])
    for i in Hull1:
        final_Hull = np.append(final_Hull,int(i))
    final_Hull = np.append(final_Hull, [int(idx_maxx)])
    for i in Hull2:
        final_Hull = np.append(final_Hull,int(i))

    export_Hull = np.array([[]])
    for i in range(final_Hull.shape[0]):
        if i != final_Hull.shape[0]-1:
            export_Hull = np.append(export_Hull, [final_Hull[i], final_Hull[i+1]])
        else:
            export_Hull = np.append(export_Hull, [final_Hull[i], final_Hull[0]])
    
    export_Hull = np.reshape(export_Hull, (-1, 2))
    export_Hull = export_Hull.astype(int)
    
    return export_Hull

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


array = np.array([[1.0,2.0],[8.0,2.0],[4.0,-1.0], [5.0,1.0], [7.0,1.0], [4.0,9.0], [6.0,7.0], [2.0,8.0], [4.0,4.0]])
aConvexHull(array)