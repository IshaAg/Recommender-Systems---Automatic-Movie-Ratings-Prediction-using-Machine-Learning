from dataset_movielens import dataset
from math import *
from dataset_movielens_movienames import dataset_movie_name
from operator import itemgetter

MOVIE_SIZE=72000

Sigma={} #Standard deviation of each user
MatchDict={} # matching of user with other user (P(Ra true=Ri))


testData={}  # 25% of total users
trainData={} # 75% of total users

##totalUsers=len(dataset)
##print(totalUsers)
current=0
for user in dataset:
    current=current+1
    if(current<=1500):
        trainData[user]=dataset[user]
    else:
        testData[user]=dataset[user]

##print(len(trainData))
##print(len(testData))

#helper function to calculate standard deviation

def StdDev(i):
    L=[]
    n=len(trainData[i])
    for movie in trainData[i]:
        L.append(trainData[i][movie])
    mean=sum(L)/n

    #print(mean)
    
    Sigma_Sqr=(sum([pow(j-mean,2) for j in L]))/n
    deviation=sqrt(Sigma_Sqr)
    return deviation

#updating values of standard deviation for each user

for user in trainData:
    Sigma[user]=StdDev(user)


#guassion function  
def gaussian(x,y):
    return pow(x-y,2)

#matching function returns the dissimilarity between active user and ith user
def matching(active,i):
    sigma=Sigma[i]
    ans=0.0
    for movie in trainData[i]:
        if movie in testData[active]:
            ans+=gaussian(trainData[i][movie],testData[active][movie])
    ans/=2*pow(sigma,2)
    return ans

#storing the results of Matching between active and all other users

def MatchDictionary(active):
    MatchDict.clear()
    for user in trainData:
        MatchDict[user]=matching(active,user)

#predict the most probable rating for active user and movie {movie}
        
def predict(active,movie):
    L=[0]*10
    predicted_rating=0.0
    prob=0.0
    for i in range(0,10):
        r=(i+1)/2.0
        ans=0.0
        for user in trainData:
            temp=0.0
            
            if movie in trainData[user]:
                temp+=gaussian(r,trainData[user][movie])
                temp/=2*pow(Sigma[user],2)
                temp+=MatchDict[user]
                ans+=pow(e,-temp)
        L[i]=ans
        
        if ans>prob:
            prob=ans
            predicted_rating=r
            
    return predicted_rating

#recommend the most rated items to users

def recommend(user):
    MatchDictionary(user)
    L=[]
    i=0
    for i in range(0,MOVIE_SIZE):
        ##print(i)
        ##i=i+1
        movie=str(i)
        if movie in dataset[user]:
            continue
        L.append((movie,predict(user,movie)))
        
    L=sorted(L,key=itemgetter(1))

    L.reverse()
    
    for i in range(0,10):
        print(list(dataset_movie_name[L[i][0]])[0])
    
    return

def Analysis():
    actual_rating=0.0
    predicted_rating=0.0
    sq_sum=0.0
    n=0
    for user in testData:
        MatchDictionary(user)
        print("##############################################################################################################")
        for movie in testData[user]:
            actual_rating=testData[user][movie]
            predicted_rating=predict(user,movie)
            sq_sum+=pow(actual_rating-predicted_rating,2)
            print(actual_rating-predicted_rating)
            n=n+1
    sq_sum/=n
    sq_sum=sqrt(sq_sum)
    print sq_sum

##MatchDictionary('75')
##
##print(predict('75','32'))
##      
##for movie in dataset['75']:
##    print(movie)
##    print(predict('75',movie))
##
##recommend('75')

Analysis()



