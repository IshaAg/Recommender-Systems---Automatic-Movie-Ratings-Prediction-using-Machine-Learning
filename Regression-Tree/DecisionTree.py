from dataset_movielens import dataset
from math import *


from LocationData import Movie_Location

from DirectorData import Movie_Director

from GenreData import Movie_Genre

from ActorData import Movie_Actor

from dataset_movielens_movienames import dataset_movie_name

from operator import itemgetter

from sklearn import tree
length={}

#Calculating Length for user

for user in dataset:
    ll=0
    for movie in dataset[user]:
        try:
            x=Movie_Director[movie]
            y=Movie_Location[movie]
            ll=ll+(len(Movie_Genre[movie])*len(Movie_Actor[movie]))
        except:
            continue
        
    length[user]=ll
    

#recommendation to user

def recommend(user):
    
    X=[]
    Y=[]
    for movie in dataset[user]:
        
        try:                                        # Only those movies for which Genre , Actor , Director , Location exist
            for genre in Movie_Genre[movie]:
                for actor in Movie_Actor[movie]:
                     x=Movie_Director[movie]
                     y=Movie_Location[movie]
                     L=[x,y,genre,actor]
                     X.append(L)
                     Y.append(dataset[user][movie])
        except:
            continue

    # Using Scikit Classifier
    clf=tree.DecisionTreeClassifier()
    clf=clf.fit(X,Y)

    PredictedList=[]
    j=0
    
    for movie in dataset_movie_name:
        print(j)
        j=j+1
        if movie in dataset[user]:
            continue
        Attributes=[]
        Prating=0.0
        length=0
        try:
            for genre in Movie_Genre[movie]:
                for actor in Movie_Actor[movie]:
                     x=Movie_Director[movie]
                     y=Movie_Location[movie]
                     Attributes=[x,y,genre,actor]
                     rating=clf.predict([Attributes])[0]
                     length=length+1
                     Prating=Prating+rating
            Prating=Prating/length
            PredictedList.append((movie,Prating))
        except:
            continue
        
    PredictedList=sorted(PredictedList,key=itemgetter(1))
    PredictedList.reverse()
    for i in range(0,10):
        print(list(dataset_movie_name[PredictedList[i][0]])[0])
    return


recommend('75')

def accuracy(user):
    Train=[]
    TrainValues=[]
    Test=[]
    TestValues=[]
    LL=length[user]
    i=0
    for movie in dataset[user]:
        
        try:
            
            for genre in Movie_Genre[movie]:
                for actor in Movie_Actor[movie]:
                    
                     x=Movie_Director[movie]
                     y=Movie_Location[movie]
                     L=[x,y,genre,actor]
                     i=i+1
                     if(i<floor(LL/4)):
                        Test.append(L)
                        TestValues.append(dataset[user][movie])
                     else:
                        Train.append(L)
                        TrainValues.append(dataset[user][movie])
        except:
            continue
    from sklearn import tree
    clf=tree.DecisionTreeClassifier()
    clf=clf.fit(Train,TrainValues)
    
       #accuracy
    ans = 0.0
    for i in range(len(Test)):
        ele=clf.predict([Test[i]])[0]
        ans = ans+ abs(ele-TestValues[i])
        Total_ans=Total_ans + abs(ele-TestValues[i])
    Total_Length= Total_Length + len(Test)
    print(ans/len(Test))

    return

recommend('75')                  
                
            






