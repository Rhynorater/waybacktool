# Wayback-Tool
A tool to fetch and verify the existence of endpoints from the Wayback Machine API.

### Features
* Pull urls from Wayback Machine
* Check those urls and provide url, status code, response length, content-type, and redirect url 
* Multithreaded
* Load and output to/from file
* Accepts stdin as input
* Optimizations made around old domains and timeouts


### Usage:
Fetch urls:
```
$ python waybacktool.py pull --host example.com  
http://example.com/example.html  
https://example.com/testing.js  
https://example.com/test.css  
```

Check urls:
```
$ python waybacktool.py pull --host example.com | python waybacktool.py check 
http://example.com/example.html, 200, 1024, text/html
https://example.com/testing.js, 301, 58, text/plain; charset=utf-8, https://example.com/testing1234.js
https://example.com/test.css, 403, 103, text/html
```

The reason this was designed in two pieces is that you can apply grep transformations to the output of the fetch urls. For example, the following is a valid use:
```
$ python waybacktool.py pull --host example.com | grep html | python waybacktool.py check 
http://example.com/example.html, 200, 1024, text/html
```

Hope you all can use this!

### Example Use Case

Let's say you're a security researcher and you want to find all the javascript files on a domain and its subdomains. You can use waybacktool to do this.

First, you would pull all the urls from the Wayback Machine for the domain and its subdomains:
```
$ python waybacktool.py pull --host example.com --with-subs yes > example.com.urls
```

This will create a file called `example.com.urls` with all the urls from the Wayback Machine for `example.com` and its subdomains.

Next, you can use `grep` to filter for javascript files:
```
$ cat example.com.urls | grep .js > example.com.js.urls
```

Finally, you can use waybacktool to check the status of these javascript files:
```
$ cat example.com.js.urls | python waybacktool.py check
```

This will output the status code, content length, and content type for each javascript file. You can then use this information to determine which files are interesting for further analysis.
