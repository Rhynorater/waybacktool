# Wayback-Tool
A tool to fetch and verify the existence of endpoints from the Wayback Machine API.


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

The reason this was designed in two pieces is s that you can apply grep transformations to the output of the fetch urls. For example, the following is a valid use:
```
$ python waybacktool.py pull --host example.com | grep html > output.txt
$ python waybacktool.py check --loadfile output.txt
http://example.com/example.html, 200, 1024, text/html
```



Hope you all can use this!
