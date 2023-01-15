Develop a small web proxy server which is able to cache web pages using python. It is a very
simple proxy server which only understands simple GET-requests, but is able to handle all kinds
of objects - not just HTML pages, but also images.

**Run webserver.py:
**
1. Start run the code. 2.Open a browser type server name "localhost", port number "8888", and corresponding name of HTML file in folder in this case "HelloWorld.html". For e.g. localhost:8888/HelloWorld.html

Run proxyserver.py:

1. Start run the code. 2.Open a browser, type server name "localhost", port number "8000" with your URL "www.google.com" next up press Enter,
   For e.g. localhost:8000/www.google.com. e.g. localhost:8000/gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html

For more information, when the code is deliberately terminated or shutted down, you need to wait about 15 seconds to restart the code. And also after browser send you response, you need to clear cache of the browser every time.

When we try to access localhost:8000/gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file5.html through "proxyserver", the server closed for some reason. Therefore when you use this given URL, restart the server.

![Screen Shot 2023-01-14 at 10 54 45 PM](https://user-images.githubusercontent.com/107897025/212522126-41459ed9-942c-44ca-8385-42d72979bf0a.png)
![Screen Shot 2023-01-14 at 10 55 00 PM](https://user-images.githubusercontent.com/107897025/212522127-7e1b5985-04c2-49f1-b00f-189fe766dcd1.png)
