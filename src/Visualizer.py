import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from myConvexHull import ConvexHull
from sklearn import datasets

def check_input_dataset(input):
    try:
        val = int(input)
        if (val >= 1 and val <=3):
            return True
        else:
            return False
    except ValueError:
        return False

def check_input_xy(x,y,length):
    try:
        valx = int(x)
        valy = int(y)
        if (valx >= 0 and valx <=length-1) and (valy >= 0 and valy <=length-1):
            return True
        else:
            return False
    except ValueError:
        return False

def visualisasi(data,x,y):
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['Target'] = pd.DataFrame(data.target)
    plt.figure(figsize = (10, 6))
    colors = ['b','r','g']
    string = data.feature_names[x] + ' vs ' + data.feature_names[y]
    plt.title(string)
    plt.xlabel(data.feature_names[x])
    plt.ylabel(data.feature_names[y])
    for i in range(len(data.target_names)):
        bucket = df[df['Target'] == i]
        bucket = bucket.iloc[:,[x,y]].values
        hull = ConvexHull(bucket) #bagian ini diganti dengan hasil implementasi ConvexHull Divide & Conquer
        plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
        for simplex in hull.simplices:
            plt.plot(bucket[simplex, 0], bucket[simplex, 1], colors[i])
    plt.legend()
    plt.show()


            
end = False
print("~~ Tucil 2 Convex Hull Visualizer ~~")
print()
print("~~ Dibuat oleh 13520136 ~~")

while(not end):

    valid = False

    while (not valid):
        print()
        print("Pilih dataset yang ingin dicari convex hull:")
        print("1. Iris")
        print("2. Wine")
        print("3. Breast Cancer")
        pilihan = input("Masukkan angka pilihan: ")
        valid = check_input_dataset(pilihan)
        if (not valid):
            print("input salah!")
            print()
    pilihan = int(pilihan)
    if pilihan == 1:
        data = datasets.load_iris()
    elif pilihan == 2:
        data = datasets.load_wine()
    elif pilihan == 3:
        data = datasets.load_breast_cancer()

    print()
    print("Atribut yang dimiliki tabel (<index>. <nama atribut>):")
    for i in range(len(data.feature_names)):
        print(i, end=". ")
        print(data.feature_names[i])

    valid2 = False
    while(not valid2):
        print()
        print("Pilih nilai x dan y yang ingin ditampilkan pada visualisasi convex hull (masukan indexnya):")
        x = input("Masukkan x: ")
        y = input("Masukkan y: ")
        valid2 = check_input_xy(x,y,len(data.feature_names))
        if (not valid2):
            print("input salah!")
    
    x = int(x)
    y = int(y)

    visualisasi(data,x,y)

    valid3 = False
    while (not valid3):
        print()
        pilihan = input("Ingin mencari convex hull untuk data yang lain? (y/n)? ")
        if pilihan.lower() == "n":
            valid3 = True
            end = True
        elif pilihan.lower() == "y":
            valid3 = True
        else:
            print("input salah!")