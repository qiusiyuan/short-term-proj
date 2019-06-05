import scrapy
from urllib.parse import urlparse
from urllib.parse import unquote

class dilidili(scrapy.Spider):
  name = "dilidili"
  domain = 'http://www.dilidili.wang'
  start_urls = ['http://www.dilidili.wang/watch3/62997/']
  src_xpath = ".//iframe/@src"
  title_xpath = ".//div[@class='num con24 clear']/a[@href='{link}']/@title"
  text_xpath = ".//div[@class='num con24 clear']/a[@href='{link}']/text()"
  def parse(self, response):
    link_xpath = ".//div[@class='num con24 clear']/a/@href"
    all_links = response.xpath(link_xpath).extract()
    for link in all_links:
      if self.domain in link:
        yield scrapy.Request(url=link, callback=self.search_mp4_downloader, errback=self._handle_error)

  def search_mp4_downloader(self, response):
    src = response.xpath(self.src_xpath).extract_first()
    title =response.xpath(self.title_xpath.format(link=response.url)).extract_first()
    num = response.xpath(self.text_xpath.format(link=response.url)).extract_first()
    src_parse =  urlparse(src)
    video_src = src_parse.query.split("=")[1]
    if self.is_mp4(src):
      yield({"src":video_src, "title":num + '-'+ title})
    else:
      yield({"warn": " is not mp4", "src":src, "title":num + '-'+ title})
  
  def _handle_error(self, error):
    print(error)

  def is_mp4(self, src_text):
    return src_text.endswith(".mp4")