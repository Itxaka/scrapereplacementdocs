# -*- coding: utf-8 -*-
import scrapy
import os


class RpdSpider(scrapy.Spider):
    name = "rpd"
    base_url = "http://www.replacementdocs.com/"
    allowed_domains = ["replacementdocs.com"]
    start_urls = ["{}download.php".format(base_url)]
    custom_settings = {
        "LOG_LEVEL": "INFO",
        "ROBOTSTXT_OBEY": False
    }
    # replacementdocs downloads are currently broken so we use that to catch a 404 to fix the link
    handle_httpstatus_list = [404]
    download_dir = "downloads"

    def parse(self, response):
        """
        main list of the systems they have manuals for, no pagination
        """
        # for each section follow up and parse the page
        for section in response.xpath("//a[contains(@href, 'download.php?list')]"):
            self.logger.debug("Found section: {}".format(section.xpath("/text()").extract_first()))
            # TODO: use response.meta to pass system being parsed?
            url = section.xpath("@href").extract_first()
            yield response.follow(url, self.parse_manuals_page)

    def parse_manuals_page(self, response):
        """
        manuals page, its a list of manuals, can have pagination
        """
        page = response.xpath("//div[@class='nextprev']/select/option[@selected='selected']/text()").extract_first()
        self.logger.debug("Parsing manuals page number {} with url: {}".format(page, response.url))

        # manuals in this page
        for manual in response.xpath("//a[contains(@href, 'download.php?view')]/@href").extract():
            # TODO: use response.meta to include the manual name so we can log it?
            yield response.follow(manual, self.parse_individual_manual)

        # pagination
        next_page = response.xpath("//a[contains(@class, 'npbutton') and contains(text(), '>>')]").xpath("@href").extract_first()
        if next_page is not None:
            self.logger.debug("Found next page, following to page {}".format(int(page)+1))
            yield response.follow(next_page, self.parse_manuals_page)

    def parse_individual_manual(self, response):
        """
        individual page of a manual, should have download link
        """
        self.logger.debug("Parsing manual: {}".format(response.url))
        download_url = response.xpath("//a[contains(@href, 'request.php?')]/@href").extract_first()
        self.logger.debug("Got download url: {}".format(download_url))
        yield response.follow(download_url, self.fix_download_url)

    def fix_download_url(self, response):
        """
        fix the download url as its currently broken on the website
        """
        self.logger.debug("GOT LINK: {}".format(response.url))
        fixed_url = "{}{}".format("http://files.replacementdocs.com/", response.url.split("/")[-1])
        self.logger.debug("FIXED LINK: {}".format(fixed_url))
        yield response.follow(fixed_url, self.save_pdf)

    def save_pdf(self, response):
        """
        save the final pdf locally
        """

        path = response.url.split('/')[-1]
        self.logger.info("Saving PDF {}".format(path))
        if not os.path.exists(self.download_dir):
            os.mkdir(self.download_dir)
        path = os.path.join(self.download_dir, path)
        with open(path, 'wb') as f:
            f.write(response.body)

