import scrapy
from scrapy_playwright.page import PageMethod
from ..items import RecruitmentCrawlItem


class TopcvSpider(scrapy.Spider):
    name = "topcv"
    allowed_domains = ["www.topcv.vn"]
    start_urls = [
        # "https://www.topcv.vn/tim-viec-lam-it-phan-mem-c10026",
        "https://www.topcv.vn/viec-lam/chuyen-vien-kinh-doanh-sales-khong-yeu-cau-kinh-nghiem-nghi-t7-cn-ngoai-hinh-sang/1496848.html?ta_source=JobSearchList_LinkDetail&u_sr_id=bWNFMYeOX3MdKcCE7WjjGznZZiGLhILmN6FN1Cwz_1728846335"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,
                                 meta=dict(playwright=True,
                                           playwright_include_page=True,
                                           playwright_page_methods=[
                                               PageMethod("wait_for_timeout", 4000),
                                               PageMethod("wait_for_load_state", "networkile"),
                                               PageMethod("wait_for_timeout", 4000),
                                               PageMethod("evaluate", "window.scrollBy(0, 1800)"),
                                               PageMethod("wait_for_selector",
                                                          "#box-job-information-detail", timeout=5000),
                                               PageMethod("wait_for_time_out", 4000),
                                               PageMethod("evaluate", "window.scrollBy(0, 1800)"),
                                               PageMethod("wait_for_selector",
                                                          ".job-detail__company", timeout=5000),
                                           ]
                                           ),
                                 callback=self.parse_job_posting)

    def parse(self, response):
        job_links = response.css(".job-item-search-result.bg-highlight.job-ta .avatar a::attr(href)").getall()
        for job_link in job_links:
            yield scrapy.Request(job_link,
                                 meta=dict(job_link=job_link,
                                           playwright=True,
                                           playwright_include_page=True,
                                           playwright_page_methods=[
                                               # Đợi thêm 8 giây để đảm bảo trang đã tải xong
                                               PageMethod("wait_for_selector", ".job-description__item", timeout=8000)
                                           ]
                                           ),
                                 callback=self.parse_job_posting
                                 )
            # yield {
            #     "link": job_link
            # }

    async def parse_job_posting(self, response):
        page = response.meta["playwright_page"]
        job_tmp = RecruitmentCrawlItem()
        # Lấy thông tin công việc
        # Get job title
        job_title = {}
        section_job_title = await page.query_selector('.job-detail__info--title')
        main_job_title = await section_job_title.query_selector('.h1')
        main_job_title_text = await main_job_title.inner_text()
        additional_job_title = await section_job_title.query_selector('.h1 .a')
        additional_job_title_text = await additional_job_title.inner_text()
        real_job_title = main_job_title_text + additional_job_title_text
        job_tmp["job_title"] = real_job_title

        job_info = {}
        job_info_sections = await page.query_selector_all('.job-description__item')
        for job_info_section in job_info_sections:
            job_section_title = await job_info_section.query_selector('h3')
            job_section_content = await job_section_title.query_selector('job-description__item--content')
            # If there are p tags in the section
            job_section_content_ps = job_section_content.query_selector_all('p')
            full_p = []
            if job_section_content_ps:
                p_content = [await paragraph.inner_text() for paragraph in job_section_content_ps]
                full_p = '\n'.join(p_content)
            # If there are ul and li tags
            ul = job_section_content.query_selector('ul')
            li_texts = []
            if ul:
                # Extract all li elements inside the ul
                lis = await ul.query_selector_all("li")
                li_texts = [await li.inner_text() for li in lis]

            section_combined_content = f"Title: {job_section_title}\n{full_p}\n" + "\n".join(li_texts)
            # Lưu vào job_info
            job_info[job_section_title] = section_combined_content

        job_salary = response.css(".job-detail__info--section-content-value::text").get()
        job_location = response.css(".company-address .company-value::text").get()
        job_yoe = response.css("#job-detail-info-experience .job-detail__info--section-content-value::text").get()
        job_schedule = "khongcodata"
        job_link = response.meta["job_link"]
        job_company = response.css(".company-name-label a::attr::text").get()
        job_expire_date = response.css(".job-detail__info--deadline::text").get()
        # Gán dữ liệu vào item
        job_tmp["job_title"] = job_title
        job_tmp["job_description"] = job_info
        job_tmp["job_salary"] = job_salary
        job_tmp["job_location"] = job_location
        job_tmp["job_yoe"] = job_yoe
        job_tmp["job_schedule"] = job_schedule
        job_tmp["job_link"] = job_link
        job_tmp["job_company"] = job_company
        job_tmp["job_expire_date"] = job_expire_date
        yield job_tmp

        await page.close()
