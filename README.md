# paranoid-requests
Paranoid wrapper around requests and grequests to automatically impersonate users and use randomized proxies.

This project is designed to help those performing web-based pen testing, analytics, scraping, or other potentially
risky activities a degree of both safety and scalability.

It provides wrappers around [requests](https://github.com/psf/requests) and [aiohttp](https://github.com/aio-libs/aiohttp)
that can be used interchangably with the original modules, so that the 'paranoid' version may be dropped in without otherwise 
altering the source tool or script.

HTTP Proxies provided by https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt and served through jsdelivr! ❤️

User Agents provided by https://github.com/Kikobeats/top-user-agents and servd through jsdeliver! ❤️


## Note on dangers of using public proxies

Please assume any of the public proxies queried by the PublicProxyList class have malicious intent. These are completely free
and anonymous services that will try to sniff your SSL traffic. 

* Don't pass credentials that are not public
* Don't put anything through these you don't want released to the world

For improved safety, you can use the ProxyList class and pass in your own list of proxy strings.

## Usage
