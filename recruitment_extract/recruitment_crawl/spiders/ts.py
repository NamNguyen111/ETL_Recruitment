import scrapy
from scrapy_playwright.page import PageMethod
from ..items import RecruitmentCrawlItem


class TsSpider(scrapy.Spider):
    name = "ts"
    allowed_domains = ["www.careerlink.vn"]
    start_urls = ["https://www.careerlink.vn/viec-lam/cntt-phan-mem/19?page=15"]

    def start_requests(self):
        # for i in range(1, 16):
        for url in self.start_urls:
            yield scrapy.Request(
                # url=self.start_urls[0] + "?page=" + str(i),
                callback=self.parse,
                url=url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "networkidle"),
                        PageMethod("wait_for_timeout", 5000),
                        PageMethod("wait_for_selector", "a.job-link.clickable-outside"),
                        PageMethod("evaluate", "window.scrollBy(0, 800)"),
                        PageMethod("wait_for_timeout", 3000),
                        PageMethod("evaluate", "window.scrollBy(0, 700)"),
                    ],
                },
            )

    def parse(self, response):
        jobs = response.css('a.job-link.clickable-outside::attr(href)').getall()
        for job in jobs:
            job_url = response.urljoin(job)
            yield scrapy.Request(
                url=job_url,
                callback=self.parse_detail,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "networkidle"),
                        PageMethod("wait_for_timeout", 5000),
                        PageMethod("evaluate", "window.scrollBy(0, 1800)"),
                        PageMethod("wait_for_timeout", 8000),
                        PageMethod("evaluate", "window.scrollBy(0, -350)"),
                        PageMethod("wait_for_selector", "#job-title"),
                    ],
                },
            )

    def parse_detail(self, response):
        item = RecruitmentCrawlItem()
        item['job_title'] = response.css('#job-title::text').get()

        # Job description
        job_description_section = response.css('#section-job-description')
        job_description_title = job_description_section.css('.job-section-title.mb-0::text').get(
            default="Mô tả công việc")
        job_description_ps = job_description_section.css('.my-3 .rich-text-content p')
        job_description_content = []
        for p in job_description_ps:
            # if_strong = p.css('strong').get()
            # if if_strong:
            #     job_description_content.append(str(p.css('strong::text').get))
            # else:
            #     job_description_content.append(str(p.css('::text').get))
            lines = p.css('::text, strong::text, br').getall()

            # Replace the <br> tag (which is returned as None or empty string) with a newline
            formatted_lines = [line if line.strip() else '\n' for line in lines]

            # Combine all the lines into a single string
            combined_text = ''.join(formatted_lines).strip()
            job_description_content.append(combined_text)
        combined_ps_desc_content = '\n'.join(job_description_content)
        desc_content = f"{job_description_title}\n{combined_ps_desc_content}"

        # Job skills
        job_skills_section = response.css('#section-job-skills')
        job_skills_title = job_skills_section.css('.job-section-title.mb-0::text').get(default="Yêu cầu công việc")

        job_skills_ps = job_skills_section.css('.raw-content.rich-text-content p')
        job_skills_content = []
        for p in job_skills_ps:
            # if_strong = p.css('strong').get()
            # if if_strong:
            #     job_skills_content.append(str(p.css('strong::text').get()))
            # else:
            #     job_skills_content.append(str(p.css('::text').get()))
            lines = p.css('::text, strong::text, br').getall()

            # Replace the <br> tag (which is returned as None or empty string) with a newline
            formatted_lines = [line if line.strip() else '\n' for line in lines]

            # Combine all the lines into a single string
            combined_text = ''.join(formatted_lines).strip()
            job_skills_content.append(combined_text)
        combined_ps_skill_content = '\n'.join(job_skills_content)
        skills_content = f"{job_skills_title}\n{combined_ps_skill_content}"

        item["job_description"] = f"{desc_content}\n\n\n{skills_content}"
        item["job_salary"] = response.css('#job-salary .text-primary::text').get()

        # Job location fix
        job_location_first = response.css('#job-location .mr-1::text').get(default="Unknown")
        job_location_second = response.css('#job-location .text-reset.font-weight-bold::text').get(default="nodata")
        job_location_combined = f"{job_location_first} {job_location_second}".strip()
        item["job_location"] = job_location_combined

        item["job_yoe"] = response.css('.cli-suitcase-simple+ span::text').get(default="Not specified")
        item["job_schedule"] = "nodata"  # Update this if needed
        item["job_link"] = response.url
        item["job_company"] = response.css('.org-name span::text').get()
        selector_job_expire_date = response.css('.day-expired.d-flex.align-items-center')
        item["job_expire_date"] = (str(selector_job_expire_date.css('span::text').get()) +
                                   str(selector_job_expire_date.css('b::text').get()))

        yield item
