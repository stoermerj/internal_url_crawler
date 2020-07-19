# internal_url_crawler

This is a crawler for small sites to find all the URLs, which are part of the site

The following inputs have to be made:
#Arg 1: String - The URL to be crawled
#Arg 2: Int - The repitions new URLs should be crawled without finding new hrefs not already in list
#Arg 3: Int - 0 or 1. if 0 then the internal link is http(s) if 1 then it is /
#Arg 4: Int - The maximum URLs to be crawl before script should stop
#Arg 4: String - As many arguments as needed. Any parts of the site which should be not crawled. 
