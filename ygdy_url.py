# 阳光电影网站爬虫demo

#  lxml是python的一个解析库，支持HTML和XML的解析，支持XPath解析方式，而且解析效率非常高
from lxml import etree
import requests

# －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
# 一、xpath过滤标签练习
# 学完视频将阳光电影网首页导航栏前9个菜单url抓取,输出结果为可以正常访问的url, 并过滤掉"经典影片"的菜单url
'''
<li>
    <a href="/html/gndy/dyzz/index.html"></a>   最新
</li>
<li>
    <a href="/html/gndy/index.html"></a>        经典
</li>
            /html/gndy/china/index.html         国内
    
https://www.ygdy8.com/html/gndy/oumei/index.html
'''

url='http://www.ygdy8.com'
url_list=[]

req=requests.get(url)
req.encoding='gb2312'
# 以文本形式打印网页源码
html=req.text


selector=etree.HTML(html)
'''
//*[@id="menu"]/div/ul//li[position()<10]/a
匹配当前节点下所有id="menu"的标签下的直接子节点div下的直接子节点ul，其下的子孙节点前九个li下的a标签
'''
infos=selector.xpath('//*[@id="menu"]/div/ul//li[position()<10]/a')
# infos=selector.xpath('//*[@id="menu"]/div/ul/li[position()<10]/a')
for info in infos:
        menus_text=info.xpath('text()')  #最新电影，国内电影，欧美电影，日韩电影等
        # print("menus_text[0]",menus_text[0])   最新电影，国内电影，欧美电影，日韩电影等
        menus_href=info.xpath('@href')   #获取链接标签
        if len(menus_text[0])>0 and menus_text[0]!='经典影片':
                menu_text=menus_text[0]
                menu_href=url+menus_href[0]  #menus_href[0]:/html/gndy/dyzz/index.html，所以需要拼接
                print(menu_text,menu_href)

                # 运行结果
                # 最新影片 http: // www.ygdy8.com / html / gndy / dyzz / index.html
                # 国内电影 http: // www.ygdy8.com / html / gndy / china / index.html
                # 欧美电影 http: // www.ygdy8.com / html / gndy / oumei / index.html
                # 日韩电影 http: // www.ygdy8.com / html / gndy / rihan / index.html
                # 华语电视 http: // www.ygdy8.com / html / tv / hytv / index.html
                # 日韩电视 http: // www.ygdy8.com / html / tv / rihantv / index.html
                # 欧美电视 http: // www.ygdy8.com / html / tv / oumeitv / index.html
                # 最新综艺 http: // www.ygdy8.com / html / zongyi2013 / index.html

                # ------------------------------------------------------------------------------------------------------------------
                # 二、循环内请求解析
                # 对第一题解析出来的url进行请求,解析出每个菜单的分页总数,每个菜单的id,并构造出全部的菜单分页请求url,全部存进一个url_list变量,url_list变量为列表
                req2=requests.get(menu_href)
                req2.encoding='gb2312'
                html2=req2.text
                selector2=etree.HTML(html2)

                # print("selector2.xpath",selector2.xpath('//div[@class="x"]//text()'))
                # selector2.xpath('//div[@class="x"]//text()获取的是div class="x"下的所有text，包括换行符
                # 共171页 / 4260条记录   首页
                # 1

                page_info=selector2.xpath('//div[@class="x"]//text()')[1].split('/')[0].replace('共','').replace('页','').strip()

                list_id=selector2.xpath('//div[@class="x"]//a/@href')[0].split('.')[0].split('_')[1]
                print(menu_text,menu_href,'TotalPage:',page_info,'list_id:',list_id)
                for ipage in range(int(page_info)):
                        page_url=menu_href.replace('index.html','')+'list_'+list_id+'_'+str(ipage+1)+'.html'
                        url_list.append(page_url)


                # 运行结果
                # 最新影片 http://www.ygdy8.com/html/gndy/dyzz/index.html TotalPage: 168 list_id: 23
                # 国内电影 http://www.ygdy8.com/html/gndy/china/index.html TotalPage: 97 list_id: 4
                # 欧美电影 http://www.ygdy8.com/html/gndy/oumei/index.html TotalPage: 179 list_id: 7
                # 日韩电影 http://www.ygdy8.com/html/gndy/rihan/index.html TotalPage: 29 list_id: 6
                # 华语电视 http://www.ygdy8.com/html/tv/hytv/index.html TotalPage: 18 list_id: 71
                # 日韩电视 http://www.ygdy8.com/html/tv/rihantv/index.html TotalPage: 36 list_id: 8
                # 欧美电视 http://www.ygdy8.com/html/tv/oumeitv/index.html TotalPage: 14 list_id: 9
                # 最新综艺 http://www.ygdy8.com/html/zongyi2013/index.html TotalPage: 135 list_id: 99
