import playwright
import scrapy
from scrapy_playwright.page import PageMethod
from ..items import RecruitmentCrawlItem


class VietnamworksSpider(scrapy.Spider):
    name = "vietnamworks"
    allowed_domains = ["www.vietnamworks.com"]
    start_urls = [
        "https://www.vietnamworks.com/viec-lam?g=5&page=7",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 meta=dict(
                                     playwright=True,
                                     playwright_include_page=True,
                                     playwright_page_methods=[
                                         PageMethod("wait_for_timeout", 8000),
                                         PageMethod("wait_for_load_state", "networkidle"),
                                         PageMethod("wait_for_timeout", 8000),
                                         PageMethod("evaluate", "window.scrollBy(0, 1800)"),
                                         PageMethod("wait_for_timeout", 9000),
                                         PageMethod("evaluate", "window.scrollBy(0, -350)"),
                                         PageMethod("wait_for_selector", ".gmxClk", timeout=10000),
                                     ]
                                 ),
                                 callback=self.parse)

    def parse(self, response):
        page = response.meta["playwright_page"]
        job_links = response.css(".sc-eBfVOF.bpNIXv a::attr(href)").getall()
        for job_link in job_links:
            if not job_link.startswith('http'):
                job_link = response.urljoin(job_link)
            # yield scrapy.Request(job_link,
            #                      meta=dict(
            #                          job_link=job_link,
            #                          playwright=True,
            #                          playwright_include_page=True,
            #                          playwright_page_methods=[
            #                              PageMethod("wait_for_load_state", "networkidle"),
            #                              PageMethod("wait_for_timeout", 6000),
            #                              PageMethod("evaluate", "window.scrollBy(0, 900)"),
            #                              PageMethod("wait_for_timeout", 6000),
            #                              PageMethod("evaluate", "window.scrollBy(0, 900)"),
            #                              PageMethod("wait_for_selector", ".jSVTbX", timeout=10000),
            #                          ]
            #                      ),
            #                      callback=self.parse_job_posting)
            yield {
                "duonglink" : job_link
            }
        # print("hello")

    async def parse_job_posting(self, response):
        page = response.meta["playwright_page"]
        button_selector = ".sc-6d845a53-0.dnzMim.btn-info.btn-md.sc-4913d170-2.jZDliU.clickable"
        button_exists = await page.query_selector(button_selector)
        if button_exists:
            await page.click(button_selector)
        job_tmp = RecruitmentCrawlItem()
        # Lấy thông tin công việc
        job_title = response.css(".bsKseP::text").get()




        job_info = {}
        sections = await page.query_selector_all('.sc-4913d170-4.jSVTbX')
        for section in sections:
            section_title = await section.query_selector('h2')
            section_title_text = await section_title.inner_text()

            content_div = await section.query_selector('.sc-4913d170-6.hlTVkb')
            paragraphs = await content_div.query_selector_all('p')
            content = [await paragraph.inner_text() for paragraph in paragraphs]

            full_content = '\n'.join(content)
            job_info[section_title_text] = full_content
        combined_info = f"Mô tả công việc:\n{job_info.get('Mô tả công việc', '')}\n\nYêu cầu công việc:\n{job_info.get('Yêu cầu công việc', '')}"





        job_salary = response.css(".iOaLcj::text").get()
        job_location = response.css("p.bgAmOO::text").get()
        job_yoe = response.css("#vnwLayout__col:nth-child(7) .ioTZSy::text").get()
        job_schedule = "khongcodata"
        job_link = response.meta["job_link"]
        job_company = response.css(".dIdfPh::text").get()
        job_expire_date = response.css("#vnwLayout__col:nth-child(1) .bgAmOO::text").get()
        # Gán dữ liệu vào item
        job_tmp["job_title"] = job_title
        job_tmp["job_description"] = combined_info
        job_tmp["job_salary"] = job_salary
        job_tmp["job_location"] = job_location
        job_tmp["job_yoe"] = job_yoe
        job_tmp["job_schedule"] = job_schedule
        job_tmp["job_link"] = job_link
        job_tmp["job_company"] = job_company
        job_tmp["job_expire_date"] = job_expire_date
        yield job_tmp

        await page.close()
