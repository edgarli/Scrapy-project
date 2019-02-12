from scrapy import Spider, Request
from visajob.items import VisajobItem
import re

class VisaJobSpider(Spider):
    name = 'visajob_spider'
    allowed_urls = ['https://www.myvisajobs.com/']
    start_urls = ['https://www.myvisajobs.com/Reports/2018-H1B-Visa-Sponsor.aspx']

    def parse(self, response):
        result_urls = ['https://www.myvisajobs.com/Reports/2018-H1B-Visa-Sponsor.aspx?P={}'.format(x) for x in range(1,5)]

        for url in result_urls:
            yield Request(url = url, callback = self.parse_result_page)

    def parse_result_page(self,response):
        company_url = response.xpath('//a[@target = "_blank"]/@href').extract()
        Number_of_Lca = response.xpath('//a[@rel = "nofollow"]/text()').extract()

        #print(len(Number_of_Lca))
        #print(Number_of_Lca)

        for url in company_url:
            if '/Visa-Sponsor' not in url:
                pass
            else:
                yield Request(url = 'https://www.myvisajobs.com/' + url, callback=self.parse_company_page)

        #print(company_url)

    def parse_company_page(self,response):
        Number_of_Lca = response.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent"]/table/tr[1]/td[1]/table/tr/td[1]/text()').extract_first()
        print(Number_of_Lca)

        Total_visa = re.findall('\d+',Number_of_Lca)[0]

        rows = response.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent"]/div/table/tr[3]/td/table//tr')
        company = response.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent"]/table/tr[1]/td[1]/table/tr/td[1]/span/text()').extract_first()
        #print(company)
        #print(len(rows))
        job_location = response.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent"]/div/table/tr[7]/td[2]/a/text()').extract()
        number_j_location = []
        job_location, number_j_location = self.extract_information(job_location, number_j_location)
        job_name = response.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent"]/div/table/tr[8]/td[2]/a/text()').extract()
        number_j_name = []
        job_name, number_j_name = self.extract_information(job_name,number_j_name)
        #print(gc_job_name)

        for i in range(1,len(rows)):
            if i == 4:
                break
            else:
                year = rows[i].xpath('./td/text()').extract_first()
                #print(year)
                salary = rows[i].xpath('./td[2]/a/text()').extract_first()
                #print(salary)
                certified = rows[i].xpath('./td[3]/a/text()').extract_first()
                c_withdraw = rows[i].xpath('./td[4]/a/text()').extract_first()
                denied =rows[i].xpath('./td[5]/a/text()').extract_first()
                withdraw = rows[i].xpath('./td[6]/a/text()').extract_first()
            item = VisajobItem()
            item['company'] = company
            item['certified'] = certified
            item['c_withdraw'] = c_withdraw
            item['denied'] = denied
            item['withdraw'] = withdraw
            item['year'] = year
            item['Total_visa'] = Total_visa
            item['job_location'] = job_location
            item['number_j_location'] = number_j_location
            item['job_name'] = job_name
            item['number_j_name'] = number_j_name
            item['salary'] = salary
            yield item


    def extract_information(self,lst_1,lst_2):
        for i in range(len(lst_1)):
            n = "".join(re.findall('\w\d+', lst_1[i]))
            lst_2.append(n)
            if ' ' in lst_1[i]:
                lst_1[i] = "".join(re.findall('[A-Za-z\s?]+', lst_1[i]))

            elif ',' in lst_1[i]:
                lst_1[i] = "".join(re.findall('[A-Za-z]+,[A-Za-z]+', lst_1[i]))
            else:
                lst_1[i] = "".join(re.findall('[A-Za-z\s?]+', lst_1[i]))

        return lst_1, lst_2

    #// *[ @ id = "ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent"] / div / table / tbody / tr[10]





