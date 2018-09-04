from django.shortcuts import render
from backup_web.models import MongodbInfo
from django.core.paginator import Paginator
import datetime
import time
import mongoengine
from mongoengine import *

a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
b = time.strftime("%Y-%m-%d", time.localtime())

# Create your views here.
status_choices = (('complete',u"已完成"),
                  ('unfinshed',u"未完成"),
                 )

def colored_status(self):
    if self.status == "complete":  # 如果状态时publish的让其闪显示
        format_td = format_html('<span style="padding:2px;background-color:blue;color:white">已完成</span>')
        # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
    elif self.status == "unfinshed":
        format_td = format_html('<span style="padding:2px;background-color:red;color:white">未完成</span>')

    return format_td

colored_status.short_description = 'status'  # 将colored_status改名成status

def topx(date1,date2,hosts,limit):

    options = {
        'chart'     : {'zoomType':'xy'},
        'title'      : {'text':'备份主机名称数量类目'},
        'subtitle' : {'text':'数据图表'},
        'yAxis'     : {'title':{'text':'数量'}},
    }

    pipeline = [
        {'$match': {'$and': [{'data_now': {'$gte': date1, '$lte': date2}}, {'host': hosts}, {'status':'complete'}]}},
        # {'$group':{'_id':{'$slice':['$cates',2,1]},'counts':{'$sum':1}}},
        {'$group': {'_id': {'name': '$name'}, 'counts': {'$sum': 1}}},
        {'$limit':limit},
        {'$sort':{'counts':-1}}
    ]

    for i in MongodbInfo._get_collection().aggregate(pipeline):
        data = {
            #'name': i['_id'],
            'name': i['_id']['name'],
            'data': [i['counts']],
            'type': 'column'
        }
        yield data

# 从chart_data函数调取此处全局变量传入topx函数
series_MG1 = [i for i in topx('2018-01-01', '2019-12-30', 'ALLWEB-160-22', 20)]
series_MG2 = [i for i in topx('2018-01-01', '2019-12-30', 'zabbix_prd01-3-201', 20)]
series_MG3 = [i for i in topx('2018-01-01', '2019-12-30', 'elk01-3-201', 20)]
series_MG4 = [i for i in topx('2018-01-01', '2019-12-30', 'guanwu-161-78', 20)]
series_MG5 = [i for i in topx('2018-01-01', '2019-12-30', 'piwik_db01-02-17', 20)]
series_MG6 = [i for i in topx('2018-01-01', '2019-12-30', 'redmine-161-63', 20)]
series_MG7 = [i for i in topx('2018-01-01', '2019-12-30', 'db01-012_mysql3306', 20)]

#取得数据中所有按name分类的总量柱状图
def total_post():
    pipeline = [
        {'$group': {'_id': {'name': '$name'}, 'counts': {'$sum': 1}}},
    ]

    for i in MongodbInfo._get_collection().aggregate(pipeline):
        print(i)
        data = {
            'name': i['_id']['name'],
            'y':i['counts']
        }
        yield data

series_post = [i for i in total_post()]

def all_day_deal_name():
    pipeline = [
        {'$match': {'$and': [{'data_now': {'$gte': '2018-01-01', '$lte': '2019-12-30'}},{'status': 'complete'}]}},
        # {'$group':{'_id':{'$slice':['$cates',2,1]},'counts':{'$sum':1}}},
        {'$group': {'_id': {'name': '$name'}, 'counts': {'$sum': 1}}},
        #{'$limit': limit},
        {'$sort': {'counts': 1}}
    ]

    for i in MongodbInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id']['name'],
            'y':i['counts']
        }
        yield data

pie_data = [i for i in all_day_deal_name()]

def index(request):
    limit = 4
    mongodb_info = MongodbInfo.objects[:20]
    paginatior = Paginator(mongodb_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
#    context = {
#        'host': mongodb_info[0].host,
#        'name': mongodb_info[0].name,
#        'size': mongodb_info[0].size
#    }
    context = {
        'MongodbInfo':loaded
    }
    return render(request,'index.html',context)

def web_mongo(request):
    limit = 32
    mongodb_info = MongodbInfo.objects
    mongodb_info01 = MongodbInfo.objects(data_now__contains=b)
    mongodb_info02 = MongodbInfo.objects(Q(data_now__icontains=b) & Q(status__icontains="complete"))
    #count01=mongodb_info01.count()
    #print(count01)
    #count02=mongodb_info02.count()
    #print(count02)
    paginatior = Paginator(mongodb_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
    context = {
        'MongodbInfo':loaded,
        'count01': mongodb_info01.count(),
        'count02': mongodb_info02.count(),
        #'last_time': mongodb_info.order_by('-data_now').limit(1),
    }
    return render(request,'web_mongo.html',context)

def web_mongo_elk(request):
    limit = 4
    mongodb_info = MongodbInfo.objects(host='elk01-3-201')
    mongodb_info01 = MongodbInfo.objects(Q(data_now__contains=b) & Q(host='elk01-3-201'))
    mongodb_info02 = MongodbInfo.objects(Q(data_now__icontains=b) & Q(status__icontains="complete") & Q(host='elk01-3-201'))
    paginatior = Paginator(mongodb_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
    context = {
        'MongodbInfo':loaded,
        'count01': mongodb_info01.count(),
        'count02': mongodb_info02.count(),
    }
    return render(request,'web_mongo_elk.html',context)

def web_mongo_allweb(request):
    limit = 9
    mongodb_info = MongodbInfo.objects(host='ALLWEB-160-22')
    mongodb_info01 = MongodbInfo.objects(Q(data_now__contains=b) & Q(host='ALLWEB-160-22'))
    mongodb_info02 = MongodbInfo.objects(Q(data_now__icontains=b) & Q(status__icontains="complete") & Q(host='ALLWEB-160-22'))
    paginatior = Paginator(mongodb_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
    context = {
        'MongodbInfo':loaded,
        'count01': mongodb_info01.count(),
        'count02': mongodb_info02.count(),
    }
    return render(request,'web_mongo_allweb.html',context)

def web_mongo_zabbix(request):
    limit = 2
    mongodb_info = MongodbInfo.objects(host='zabbix_prd01-3-201')
    mongodb_info01 = MongodbInfo.objects(Q(data_now__contains=b) & Q(host='zabbix_prd01-3-201'))
    mongodb_info02 = MongodbInfo.objects(Q(data_now__icontains=b) & Q(status__icontains="complete") & Q(host='zabbix_prd01-3-201'))
    paginatior = Paginator(mongodb_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
    context = {
        'MongodbInfo':loaded,
        'count01': mongodb_info01.count(),
        'count02': mongodb_info02.count(),
    }
    return render(request,'web_mongo_zabbix.html',context)

def web_mongo_guanwu(request):
    limit = 6
    mongodb_info = MongodbInfo.objects(host='guanwu-161-78')
    mongodb_info01 = MongodbInfo.objects(Q(data_now__contains=b) & Q(host='guanwu-161-78'))
    mongodb_info02 = MongodbInfo.objects(Q(data_now__icontains=b) & Q(status__icontains="complete") & Q(host='guanwu-161-78'))
    paginatior = Paginator(mongodb_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
    context = {
        'MongodbInfo':loaded,
        'count01': mongodb_info01.count(),
        'count02': mongodb_info02.count(),
    }
    return render(request,'web_mongo_guanwu.html',context)

def web_mongo_redmine(request):
    limit = 2
    mongodb_info = MongodbInfo.objects(host='redmine-161-63')
    mongodb_info01 = MongodbInfo.objects(Q(data_now__contains=b) & Q(host='redmine-161-63'))
    mongodb_info02 = MongodbInfo.objects(Q(data_now__icontains=b) & Q(status__icontains="complete") & Q(host='redmine-161-63'))
    paginatior = Paginator(mongodb_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
    context = {
        'MongodbInfo':loaded,
        'count01': mongodb_info01.count(),
        'count02': mongodb_info02.count(),
    }
    return render(request,'web_mongo_redmine.html',context)

def web_mongo_pike(request):
    limit = 2
    mongodb_info = MongodbInfo.objects(host='piwik_db01-02-17')
    mongodb_info01 = MongodbInfo.objects(Q(data_now__contains=b) & Q(host='piwik_db01-02-17'))
    mongodb_info02 = MongodbInfo.objects(Q(data_now__icontains=b) & Q(status__icontains="complete") & Q(host='piwik_db01-02-17'))
    paginatior = Paginator(mongodb_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
    context = {
        'MongodbInfo':loaded,
        'count01': mongodb_info01.count(),
        'count02': mongodb_info02.count(),
    }
    return render(request,'web_mongo_pike.html',context)

def web_mongo_db(request):
    limit = 1
    mongodb_info = MongodbInfo.objects(host='db01-012_mysql3306')
    mongodb_info01 = MongodbInfo.objects(Q(data_now__contains=b) & Q(host='db01-012_mysql3306'))
    mongodb_info02 = MongodbInfo.objects(Q(data_now__icontains=b) & Q(status__icontains="complete") & Q(host='db01-012_mysql3306'))
    paginatior = Paginator(mongodb_info,limit)
    page = request.GET.get('page',1)
    loaded = paginatior.page(page)
    context = {
        'MongodbInfo':loaded,
        'count01': mongodb_info01.count(),
        'count02': mongodb_info02.count(),
    }
    return render(request,'web_mongo_db.html',context)

def chart_data(request):
    context = {
        'chart_MG1': series_MG1,
        'chart_MG2': series_MG2,
        'chart_MG3': series_MG3,
        'chart_MG4': series_MG4,
        'chart_MG5': series_MG5,
        'chart_MG6': series_MG6,
        'chart_MG7': series_MG7,
        'series_post': series_post,
        'pie_data':  pie_data
    }
    return render(request,'chart_data.html',context)