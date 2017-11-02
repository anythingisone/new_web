# -*- coding: utf-8 -*-
import scrapy
import time
import requests
import json,jsonpath
class LgSpider(scrapy.Spider):
    name = 'lg'
    # allowed_domains = ['lagou.com/jobs/']
    #start_urls = ['https://www.lagou.com/jobs/list_?px=new&city=%E5%8C%97%E4%BA%AC&district=%E6%B5%B7%E6%B7%80%E5%8C%BA#filterBox']
    headers = {
        'Host':'www.lagou.com',
        'Referer':'https://www.lagou.com/jobs/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    cookies = {
        'user_trace_token':'20171011163246-c1dd3b91-ae5e-11e7-89c7-525400f775ce',
        'LGUID':'20171011163246-c1dd4198-ae5e-11e7-89c7-525400f775ce',
        'index_location_city':'%E5%8C%97%E4%BA%AC',
        'JSESSIONID':'ABAAABAABEEAAJA568D25F9F0F0626C2614F21D49D62FA8',
        'X_HTTP_TOKEN':'28f5a91fa07f9095e3f87837a5ecc230',
        'TG-TRACK-CODE':'search_code',
        '_gid':'GA1.2.82748944.1508725396',
        'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6':'1508831703,1508831708,1508832552,1508891681',
        'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6':'1508898094',
        '_ga':'GA1.2.530919440.1507710766',
        'LGSID':'20171025091304-a7047e6f-b921-11e7-9613-5254005c3644',
        'LGRID':'20171025102138-3b5e76b4-b92b-11e7-9613-5254005c3644',
        'SEARCH_ID':'812abb174f484d99a37679f1af0b606f',
   }

    # def start_requests(self):
    #     # 起始url
    #     start_url = 'https://www.lagou.com/zhaopin/?labelWords=label&city=北京&district=海淀区&gj=3年及以下&bizArea=%E8%A5%BF%E4%B8%89%E6%97%97#filterBox'
    #     yield scrapy.Request(url=start_url,headers=self.headers,callback=self.parse)
    #
    # def afterparse(self,response):
    #         # 提取列表页信息
    #         position_list = response.xpath('//div[@id="s_position_list"]/ul/li')
    #         if position_list:
    #             for position in position_list:
    #                 print '职位名称：',position.xpath('.//h3/text()').extract()[0].encode('utf-8')
    #                 print '工作地点：',position.xpath('.//em/text()').extract()[0].encode('utf-8')
    #                 print 'url：',position.xpath('.//a/@href').extract()[0].encode('utf-8')
    #                 print '薪资：',position.xpath('.//span[@class="money"]/text()').extract()[0].encode('utf-8')
    #                 print '经验：',position.xpath('.//div[@class="li_b_l"]/text()').extract()[2].encode('utf-8').split(' / ')[0]
    #                 print '学历：',position.xpath('.//div[@class="li_b_l"]/text()').extract()[2].encode('utf-8').split(' / ')[1]
    #         else:
    #             print '暂时没有符合该搜索条件的职位'
    #
    #
    # def parse(self, response):
    #     position_list = response.xpath('//div[@id="s_position_list"]/ul/li')
    #     yx = response.xpath('//div[@class="selectUI-text text"]/ul/li')
    #     #yx = ['5k-10k','10k-15k','15k-25k','25k-50k','50k以上']
    #     gj = ['应届毕业生','3年及以下','3-5年','5-10年','10年以上']
    #     next_url= 'https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0'
    #     data= {
    #         'pn':'2'
    #     }
    #     # 下一页不能被点击
    #     next_page = response.xpath('//div[@class="pager_container"]/a[@class="page_no pager_next_disabled"]')
    #     if next_page:
    #         # 若是最后一页
    #         # 循环修改条件
    #         for yxfw in yx:
    #             xz = yxfw.xpath('./a/text()').extract()[0].encode('utf-8')
    #             for jy in gj:
    #                 burl = 'https://www.lagou.com/zhaopin/?labelWords=label&city=北京&gj='+ jy + '&yx=' + xz + '#filterBox'
    #                 yield scrapy.Request(url = burl,headers = self.headers,callback = self.afterparse,cookies = self.cookies)
    #                 time.sleep(0.5)
    #     else:
    #         for position in position_list:
    #             print '职位名称：',position.xpath('.//h3/text()').extract()[0].encode('utf-8')
    #             print '工作地点：',position.xpath('.//em/text()').extract()[0].encode('utf-8')
    #             print 'url：',position.xpath('.//a/@href').extract()[0].encode('utf-8')
    #             print '薪资：',position.xpath('.//span[@class="money"]/text()').extract()[0].encode('utf-8')
    #             print '经验：',position.xpath('.//div[@class="li_b_l"]/text()').extract()[2].encode('utf-8').split(' / ')[0]
    #             print '学历：',position.xpath('.//div[@class="li_b_l"]/text()').extract()[2].encode('utf-8').split(' / ')[1]
    #         # 下一页url
    #         next_url = response.xpath('//div[@class="pager_container"]/a[@class="page_no"]/@href').extract()[-1]
    #         print next_url
    #         yield scrapy.Request(url=next_url,headers=self.headers,callback=self.parse,cookies=self.cookies)


    def start_requests(self):
        allcity_url = 'https://www.lagou.com/jobs/allCity.html?px=new&gj=3%E5%B9%B4%E5%8F%8A%E4%BB%A5%E4%B8%8B&city=%E5%8C%97%E4%BA%AC&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&positionNum=500+&companyNum=0&isCompanySelected=false&labelWords='
        yield scrapy.Request(url=allcity_url,headers=self.headers,callback=self.allparse)
    # 所有城市url
    def allparse(self,response):
        city_list = response.xpath('//ul[@class="city_list"]/li/a')
        for city in city_list:
            #print city.xpath('./@href').extract().encode('utf-8')
            #print 'aaaaaaaaaaaaaaa'
            city = city.xpath('./text()').extract()[0].encode('utf-8')
            city_url = 'https://www.lagou.com/zhaopin/?labelWords=label&city='+city+'&gj=不限#filterBox'
            # print city_url.strip()
            yield scrapy.Request(url=city_url.strip(),headers=self.headers,callback=self.cityurl_parse,cookies=self.cookies)
            # time.sleep(1)

    # 所有区url
    def cityurl_parse(self,response):
        qu_list = response.xpath('//li[@class="detail-district-area"]/a')
        city = response.xpath('//div[@class="current-handle-position"]/a[@class="current_city current"]').xpath('./text()').extract()[0].encode('utf-8')
        for qu in qu_list:
            qu = qu.xpath('./text()').extract()[0].encode('utf-8')
            if qu == '不限':
                pass
            else:
                qu_url = 'https://www.lagou.com/jobs/list_?city='+city+'&district='+qu+'&gj=不限#filterBox'
                yield scrapy.Request(url=qu_url,headers=self.headers,callback=self.shopqu_parse,cookies=self.cookies)
    # list页面
    def lglist_parse(self,response):
        #提取列表页信息
        url_list = response.url.split('?')
        url = url_list[0][:-5] +'positionAjax.json'+'?px=new&'+url_list[1]+'&needAddtionalResult=false&isSchoolJob=0'
        referer = url_list[0][:-5]+'list_?px=new&'+url_list[1]
        print '11111111111111111'
        print url
        print referer
        i = 1
        datafalg = ''
        headers = {
            'Host':'www.lagou.com',
            'Referer':referer,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'X-Anit-Forge-Code':'0',
            'X-Anit-Forge-Token':'None',
            'X-Requested-With':'XMLHttpRequest',
         }
        f = open('./job.txt','a')
        while True:
            if i == 1:
                data = {
                    'first':'true',
                    'pn':i,
                    'kd':' '
                }
            else:
                data = {
                    'first':'false',
                    'pn':i,
                    'kd':' '
                }
            try:
                response = requests.post(url, headers=headers,cookies=self.cookies,data=data)
                htmls = json.loads(response.content, encoding="utf-8")
                data_list = jsonpath.jsonpath(htmls,'$..result.*')
                #page = data_list.xpath('//div[@class="pager_container"]')
                # https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E7%A6%8F%E5%B7%9E&district=%E4%BB%93%E5%B1%B1%E5%8C%BA&bizArea=%E4%B8%8A%E4%B8%89%E8%B7%AF&needAddtionalResult=false&isSchoolJob=0
                if type(data_list)==type(False):
                    print '无工作'
                    f.close()
                    break
                else:
                    if datafalg==data_list:
                        f.close()
                        break
                    else:
                        for data in data_list:
                            print '城市:',data['city']
                            print '职位名:',data['positionName']
                            print '公司名:',data['companyShortName']
                            print '学历:',data['education']
                            print '================'
                            f.write('城市:'+data['city'].encode('utf-8')+'\n')
                            f.write('职位名:'+data['positionName'].encode('utf-8')+'\n')
                            f.write('公司名:'+data['companyShortName'].encode('utf-8')+'\n')
                            f.write('学历:'+data['education'].encode('utf-8')+'\n')
                            f.write('=========================\n')
                        datafalg=data_list
                        print '===========第'+str(i)+'页=============='
                        f.write('url:'+referer+'\n')
                        f.write('===========第'+str(i)+'页==============\n')
                        i+=1
            except:
                time.sleep(1000)

        # f = open('./job.txt','a')
        # position_list = response.xpath('//div[@id="s_position_list"]/ul/li')
        # city = response.xpath('//div[@class="current-handle-position"]/a[@class="current_city current"]').xpath('./text()').extract()[0].encode('utf-8')
        # qu = response.xpath('//div[@class="current-handle-position"]/a[@class="current_district current"]').xpath('./text()').extract()[0].encode('utf-8')
        # if position_list:
        #     for position in position_list:
        #         print '职位名称：',position.xpath('.//h3/text()').extract()[0].encode('utf-8')
        #         print '工作地点：',position.xpath('.//em/text()').extract()[0].encode('utf-8')
        #         print 'url：',position.xpath('.//a/@href').extract()[0].encode('utf-8')
        #         print '薪资：',position.xpath('.//span[@class="money"]/text()').extract()[0].encode('utf-8')
        #         print '经验：',position.xpath('.//div[@class="li_b_l"]/text()').extract()[2].encode('utf-8').split(' / ')[0]
        #         print '学历：',position.xpath('.//div[@class="li_b_l"]/text()').extract()[2].encode('utf-8').split(' / ')[1]
        # else:
        #     print '暂时没有符合该搜索条件的职位3'


    def shopqu_parse(self,response):
        shopqu_list = response.xpath('//li[@class="detail-bizArea-area"]/a/text()')
        city = response.xpath('//div[@class="current-handle-position"]/a[@class="current_city current"]').xpath('./text()').extract()[0].encode('utf-8')
        qu = response.xpath('//div[@class="current-handle-position"]/a[@class="current_district current"]').xpath('./text()').extract()[0].encode('utf-8')
        yx = ['2k以下','2k-5k','5k-10k','10k-15k','15k-25k','25k-50k','50k以上']
        jy_list = response.xpath('//a[@data-lg-tj-id="8r00"]')
        position_list = response.xpath('//div[@id="s_position_list"]/ul/li')
        if len(shopqu_list)==1:
            for xz in yx:
                for jy in jy_list:
                    if jy == '不限':
                        pass
                    else:
                        jy = jy.xpath('./text()').extract()[0].encode('utf-8')
                        jy = jy.strip()
                        list_url = 'https://www.lagou.com/jobs/list_?city='+city+'&district='+qu+'&gj='+jy+'&yx='+xz+'#filterBox'
                        yield scrapy.Request(url=list_url,headers=self.headers,callback=self.lglist_parse,cookies=self.cookies)
        else:
            for shopqu in shopqu_list:
                shopqu = shopqu.extract().encode('utf-8')
                if '不限' in shopqu:
                    pass
                else:
                    for xz in yx:
                        for jy in jy_list:
                            if jy == '不限':
                                pass
                            else:
                                jy = jy.xpath('./text()').extract()[0].encode('utf-8')
                                jy = jy.strip()
                                list_url = 'https://www.lagou.com/jobs/list_?city='+city+'&district='+qu+'&gj='+jy+'&yx='+xz+'&bizArea=shopqu#filterBox'
                                yield scrapy.Request(url=list_url,headers=self.headers,callback=self.lglist_parse,cookies=self.cookies)



#https://www.lagou.com/jobs/positionAjax.json?gj=3%E5%B9%B4%E5%8F%8A%E4%BB%A5%E4%B8%8B&px=new&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0





