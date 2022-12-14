import scrapy
import pandas as pd

def tofloat(num):
    try:
        num = float(num)
        return num
    except ValueError:
        return num

class FespiderSpider(scrapy.Spider):
    name = 'fespider'
    allowed_domains = ['fundsexpolorer.com.br']
    start_urls = ['https://www.fundsexplorer.com.br/ranking']

    def parse(self, response):
        response = response.replace(body=response.body.replace(b'<br>', b' '))

        table = response.xpath('//*[@id="table-ranking"]')

        collumn_names = table.xpath('//thead/tr/th/text()').getall()

        dataset = {}
        for col in collumn_names:
            dataset[col] = []

        for row in table.xpath('//tbody/tr'):
            for index, col in enumerate(row.xpath('td')):
                if col.xpath('a/text()').get():
                    a = col.xpath('a/text()').get()
                    link = 'https://www.fundsexplorer.com.br'
                    link += col.xpath('a/@href').get()
                    #'=HYPERLINK("https://www.tutorialexample.com"，"www.tutorialexample.com")'
                    cel = f'=HYPERLINK("{link}","{a}")' 
                else:
                    cel = col.xpath('text()').get()
                    if cel:
                        cel = cel.replace('R$ ','')
                        cel = cel.replace('N/A','')
                        cel = cel.replace('.','')
                        cel = cel.replace(',','.')
                        cel = cel.replace('%','').strip()
                        cel = tofloat(cel)
                        if index == 3 and tofloat(cel):
                            cel = cel / 10

                #print(type(cel), cel)
                dataset[collumn_names[index]].append(cel)
            #break

        df = pd.DataFrame(dataset)
        print(df.info())
        with pd.ExcelWriter(
            "data.xlsx",
            engine='xlsxwriter'
        ) as writer:
            df.to_excel(writer)
            