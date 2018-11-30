# Crawler
pyhon爬虫  

## Scrapy框架使用流程：  
scrapy startproject xxx  
scrapy genspider xxx "http://www.xxx.com"  
编写items.py，明确需要爬取的数据  
编写spiders/xxx.py，编写爬虫文件，处理请求和相应，以及提取数据（yield item）  
编写pipelines.py，编写管道文件，处理spider返回的item数据，比如本地持久化存储等  
编写setting.py,启动管道文件，以及其他相关设置  
启动爬虫  

## 报错解决：
1.TypeError: Object of type 'bytes' is not JSON serializable  
解决办法：可以自己写一个编码类
`  
import json  
 
 
class MyEncoder(json.JSONEncoder):  
 
    def default(self, obj):  
        """  
        只要检查到了是bytes类型的数据就把它转为str类型  
        :param obj:  
        :return: 
        """  
        if isinstance(obj, bytes):  
            return str(obj, encoding='utf-8')  
        return json.JSONEncoder.default(self, obj)    
 `  
 2.代码运行环境用的pycahrm，但是在成功爬虫后，tecent.json用pycahrm打开却是乱码  
 解决办法：  
 （1）改变pycharm对于该文件的编码，改为“GBK”  
 （2）换一个编辑器打开，如notepad
 

