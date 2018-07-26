#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import json
import requests
import pandas
from collections import OrderedDict
from pyquery import PyQuery as pq

keyword = '日本水母面膜'
## 这是淘宝搜索列表的url前面的相同部分，q=''代表搜索的关键词
## s=''代表第几页，s=0为第1页s=44为第二页，以此类推
search_url_prefix = 'https://s.taobao.com/search?q=' + keyword + '&s='
detail_url_prefix = 'https://store.taobao.com/shop/view_shop.htm?user_number_id='
## 鼠标悬停到查询结果的店铺名元素上时, 会查询此店铺的等级和徽章等信息
## sid的值应该为掌柜的user_id, callback值为jsonp形式的函数名, 去掉它才能得到正常的json数据
## rank_api_url = 'https://s.taobao.com/api?sid=%s&callback=shopcard&app=api&m=get_shop_card'
rank_api_url = 'https://s.taobao.com/api?sid=%s&app=api&m=get_shop_card'
rank_map = {
    'icon-supple-level-xin': '红心',
    'icon-supple-level-zuan': '蓝钻',
    'icon-supple-level-guan': '蓝色皇冠',
    'icon-supple-level-jinguan': '金色皇冠',
}


def getShopRank(user_ids):
    '''
    获取店铺等级
    '''
    shop_rank_list = []
    for user_id in user_ids:
        res = requests.get(rank_api_url % user_id).text
        rankInfo = json.loads(res)
        ## 貌似不会存在那种, 蓝钻 x 2 + 红心 x 1的情况, 简单了很多
        ## [{'levelClass': 'icon-supple-level-zuan'}, {'levelClass': 'icon-supple-level-zuan'}]
        levelClasses = rankInfo['levelClasses']
        levelClass = rank_map[levelClasses[0]['levelClass']]
        shop_rank_list.append(levelClass + ' x ' + str(len(levelClasses)))
    return shop_rank_list

def getShopDetail(user_ids):
    shop_link_list = []
    shop_name_list = []
    for index, user_id in enumerate(user_ids):
        print('当前序号: %d' % index)
        res = requests.get(detail_url_prefix + user_id)
        ## ...重定向, 但是没有Location响应头, 不过url-hash也可以
        shop_link_url = res.headers.get('url-hash')
        print(shop_link_url)
        page = requests.get(shop_link_url).text
        root = pq(page)

        ## a标签下有个J_TEnterShop标签, 内容为'进入店铺', 我们需要把这个先移除
        shop_name = root('.shop-name a').remove('#J_TEnterShop').text()
        ## 有些店铺名称较长, 可能会被截断, 可以通过a标签的title属性获得完整名称
        ## shop_name = root('.shop-name a').attr('title')
        print(shop_name)
        shop_link_list.append(shop_link_url)
        shop_name_list.append(shop_name)
    return shop_link_list, shop_name_list

def getList(startpage, endpage):
    #如果需要爬取具体的商品详情，页数过多可能会出现异常，此函数可以用来控制一次爬取的页数

    url_list = [search_url_prefix + str(i * 44) for i in range(startpage - 1, endpage)]  #生成需要爬取的商品列表url
 
    #定义存储商品列表数据数据的列表
    nid_list=[]
    raw_title_list=[]
    view_price_list=[]
    view_sales_list=[]
    item_loc_list=[]
    nick_list=[]

    shop_name_list = []
    shop_link_list = []
    shop_rank_list = []

    for url in url_list:
        resp = requests.get(url)
        print(resp.url)
        # 商品id, 唯一, 可以此跳转到其商品详情页面，然后进行其他信息的抓取
        nid         = re.findall(pattern='"nid":"(.*?)"',string = resp.text)
        #商品名称
        raw_title   = re.findall(pattern='"raw_title":"(.*?)"',string = resp.text)
        #商品价格
        view_price  = re.findall(pattern='"view_price":"(.*?)"',string = resp.text)
        #商品销量
        view_sale_full_strs = re.findall(pattern='"view_sales":"(.*?)"',string = resp.text)
        view_sales = []
        for i in view_sale_full_strs:
            j = re.findall('\d+', i)
            view_sales = view_sales + j
        #发货地址
        item_loc = re.findall(pattern='"item_loc":"(.*?)"',string = resp.text)
        #掌柜名
        nick0 = re.findall(pattern='"nick":"(.*?)"',string = resp.text)
        nick = [i for i in nick0 if i!=''] 
        #user_id
        user_id  = re.findall(pattern='"user_id":"(.*?)"',string = resp.text)

        ## 获取店铺信息
        shop_link, shop_name = getShopDetail(user_id)
        shop_rank = getShopRank(user_id)

        #逐个存储
        nid_list.extend(nid)
        raw_title_list.extend(raw_title)
        view_price_list.extend(view_price)
        view_sales_list.extend(view_sales)
        item_loc_list.extend(item_loc)
        shop_link_list.extend(shop_link)
        shop_name_list.extend(shop_name)
        shop_rank_list.extend(shop_rank)

        if nick is not '':
            nick_list.extend(nick)

    #生成数据框
    dt = {
        '商品id':       nid_list,
        '商品名称':      raw_title_list,
        '商品价格':      view_price_list,
        '商品销量':      view_sales_list,
        '商品发货地址':   item_loc_list,
        '店铺名称': shop_name_list,
        '店铺等级': shop_rank_list,
        '店铺链接': shop_link_list,
        '掌柜名':        nick_list
    }

    df = pandas.DataFrame(dt)  #根据字典生成数据框
    #写入Excel
    file = pandas.ExcelWriter("taobao_details.xlsx")  #新建一个空白Excel工作簿
    df.to_excel(file, "Sheet1")  #将df写入Sheet1工作表
    file.save()

getList(1, 9)