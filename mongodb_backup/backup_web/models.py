from django.db import models
import re
from mongoengine import *
from mongoengine import connect
connect('backup',host='10.10.3.202',port=27017,username='backup',password='Kjt@123')
# Create your models here.

class MongodbInfo(Document):
     data_now = StringField()
     host = StringField()
     size = StringField()
     status = StringField()
     path = StringField()
     name= StringField()
     type = StringField()
     env = StringField()
     file_create = ListField(StringField())

     meta = {
         'collection':'backup_info',
         'ordering': ['-data_now'],
     }

pipeline1 = [
    {'$match':{'$and':[{'data_now':{'$gte':'2018-01-01','$lte':'2018-12-30'}},{'host':'ALLWEB-160-22'}]}},
    #{'$group':{'_id':{'$slice':['$cates',2,1]},'counts':{'$sum':1}}},
    {'$group':{'_id':{'name':'$name'},'counts':{'$sum':1}}},
    #{'$limit':3}
]

for i in MongodbInfo._get_collection().aggregate(pipeline1):
    print(i)
#for i in MongodbInfo.objects(host='elk01-3-201'):
#    print(i.data_now,i.host,i.size,i.status,i.path,i.name,i.type,i.env,i.file_create)