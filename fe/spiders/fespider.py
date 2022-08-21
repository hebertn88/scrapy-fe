import scrapy


class FespiderSpider(scrapy.Spider):
    name = 'fespider'
    allowed_domains = ['fundsexpolorer.com.br']
    start_urls = ['https://www.fundsexplorer.com.br/ranking']

    def parse(self, response):
        response = response.replace(body=response.body.replace(b'<br>', b' '))
        table = response.xpath('//*[@id="table-ranking"]')
        collumn_names = table.xpath('//thead/tr/th/text()')
#//*[@id="table-ranking"]/thead/tr/th[1]
        print('\n\n----------------\n', collumn_names.getall(), '\n----------------\n',len(collumn_names.getall()),'\n',)

