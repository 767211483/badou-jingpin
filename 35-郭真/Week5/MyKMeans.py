import matplotlib.pyplot as plt
import numpy as np
import random
import sys

class MyKMeans:
    #聚类数量
    Num_Of_Class:int
    #中心点集
    Arr_Conter_Points = []
    #原始数据集
    Arr_Item = []
    #类内平均距离
    Arr_MeanDistance = []
    #聚类点集
    Arr_Points = []

    def __init__(self,NumOfClass,LitsItem):
        if(NumOfClass < 0):
            raise "Num of classical can not be 0"
        if(len(LitsItem) < 0):
            raise "list is null"
        self.Num_Of_Class = NumOfClass
        for i in range(self.Num_Of_Class):
            self.Arr_Points.append([])
        self.Arr_Item = LitsItem
        self.__random_start(self.Arr_Item)
        self.__calculate()

    def __random_start(self,List_Item):
        rand_index = random.sample([ i for i in range(len(List_Item))],self.Num_Of_Class)
        for item_index in rand_index:
            self.Arr_Conter_Points.append(List_Item[item_index])
        
    def distance_Euclidean(self,p1,p2):
        #欧拉距离
        temp = 0
        for i in range(len(p1)):
            temp += (p1[i]-p2[i])**2
        return pow(temp,0.5)

    def distance_Cosine(self,p1,p2):
        #余弦距离[0,2]
        a = 0
        p1_sum = 0
        p2_sum = 0
        for i in range(len(p1)):
            a += p1[i]*p2[i]
            p1_sum += p1[i]**2
            p2_sum += p2[i]**2
        return a/(pow(p1_sum,0.5)*pow(p2,0.5)) + 1

    def item_avg(self,List):
        #对位求平均
        sum = [0] * len(List[0])
        for item in List:
            for ax_index in range(len(item)):
                sum[ax_index] += item[ax_index]
        return [i/len(List) for i in sum]

    def center_avg_distance(self,itemlist,center):
        dis = 0
        item_count = 0
        for item in itemlist:
            dis += self.distance_Euclidean(item,center)
            item_count+=1
        return dis/item_count

    def __calculate(self):
        reslut = []
        for i in range(self.Num_Of_Class):
            reslut.append([])
        for item in self.Arr_Item:
            min_index = -1
            min_dis = sys.maxsize
            for center_index in range(len(self.Arr_Conter_Points)):
                dis = self.distance_Euclidean(item,self.Arr_Conter_Points[center_index])
                if(min_dis>dis):
                    min_index = center_index
                    min_dis = dis
            reslut[min_index].append(item)
        new_center = []
        for classical in reslut:
            avg_Center:list = self.item_avg(classical)
            new_center.append(avg_Center)
        end_flag = True
        for i in range(len(new_center)):
            end_flag = end_flag and (self.distance_Euclidean(new_center[i],self.Arr_Conter_Points[i])<0.001)
        if(end_flag):
            for index in range(len(reslut)):
                self.Arr_MeanDistance.append(self.center_avg_distance(reslut[index],new_center[index]))
                print("类内平均距离(相似度)",self.center_avg_distance(reslut[index],new_center[index]))
                print("Center:{",new_center[index],"}:",reslut[index])
            self.Arr_Points = reslut
            self.Arr_Conter_Points = new_center
            return 1
        self.Arr_Conter_Points = new_center
        self.__calculate()

x = np.random.rand(100, 2)
x.tolist()
a = MyKMeans(4,x.tolist())
x_coord_list = []
y_coord_list = []
colors = ['r', 'b', 'g', 'c', 'm']
for ps in a.Arr_Points:
    ps = np.array(ps)
    x_coord_list.append(ps[:, 0])
    y_coord_list.append(ps[:, 1])
for index in range(len(x_coord_list)):
    plt.scatter(x_coord_list[index],y_coord_list[index],color = colors[index%len(colors)])


plt.title("Scatter Plot of Multiple Points Sets")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.legend()


plt.show()
