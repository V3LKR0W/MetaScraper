**MetaScraper**

Retreives Title, Description and OpenGraph images and returns back the data so it can be embeded as a preview in your web application.


**Module Dependacny**

pip install requests 

pip install bs4

pip install lxml


**Logic**

![Logic](https://github.com/V3LKR0W/MetaScraper/blob/master/Logic.png)


**Documentation**

MetaScraper.get_preview('https://example.com',useragent='MyUserAgent')
The useragent can also be None which then will use the default, figured it would be good to make it