scrape replacementdocs.com
----------------------------

Simple spider for scrapy in order to download the pdfs from replacementdocs.com


replacementdocs.com is a great resource for downloading manuals for consoles, unfortunately the page has been broken for a while(april 2018) with no fix in the pipeline

As Im very worried that the site may go down at any given moment due to their issues, I rather have a local copy of all the manuals in case it goes down (plus Im a bit of a data hoarder)


TODO
-----

 * Do not redownload the same pdf
 * Save the pdfs to a different folder based on their source system
 


Usage
-----

 * `pipenv install`
 * `pipenv run scrapy crawl rpd`

Caveats
-------

Take into account that replacementdocs provides a free service so dont go download the whole thing for no good reason as its over 9000 manuals and around 25Gb total.
If you need the whole pack I can provide a torrent for it as to alleviate the bandwith that would be incurred by multiple users downloading all the manuals.  