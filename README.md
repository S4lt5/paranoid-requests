[![Tests](https://github.com/Yablargo/paranoid-requests/actions/workflows/test.yml/badge.svg)](https://github.com/Yablargo/paranoid-requests/actions/workflows/pylint_and_test.yml)
[![Public Lists Online and Updated](https://github.com/Yablargo/paranoid-requests/actions/workflows/public_sources.yml/badge.svg)](https://github.com/Yablargo/paranoid-requests/actions/workflows/public_sources.yml)
# paranoid-requests
Paranoid wrapper around requests and aiohttp to automatically impersonate users and use randomized proxies.

This project is designed to help those performing web-based pen testing, analytics, scraping, or other potentially
risky activities a degree of both safety and scalability.

It provides wrappers around [requests](https://github.com/psf/requests) and [aiohttp](https://github.com/aio-libs/aiohttp)
that can be used interchangably with the original modules, so that the 'paranoid' version may be dropped in without otherwise 
altering the source tool or script.


Http(s) provided by https://github.com/monosans/proxy-list/ and served through jsdeliver.

User Agents provided by https://github.com/Kikobeats/top-user-agents and served through jsdeliver.

## Do no harm

I ask that anyone reading this to take a moment to digest the following statement:

>This is released to enable pen testers do their jobs in good faith. Please try to make today's world 1% better than yesterday's.

## Note on dangers (and horriffic performance) of using public proxies

Please assume any of the public proxies queried by the PublicProxyList class have malicious intent. These are completely free and anonymous services that will try to sniff your SSL traffic, trick you, or otherwise compromise you.

* Don't pass credentials that are not public
* Don't put anything through these you don't want released to the world

For improved safety, you can use the ProxyList class and pass in your own list of proxy strings.

## Usage

```python
import paranoid_requests.requests_wrapper as noided_requests
import requests

# First, get my IP from ifconfig.co
host_addr = "http://ifconfig.co"

resp = requests.get(host_addr,headers={"Accept": "application/json"})
print("Default:\n\t",resp.json()['ip'])

#By default, paranoid proxy/user agents are only set when creating a new session
resp = noided_requests.get(host_addr,headers={"Accept": "application/json"})
print("Paranoid without session:\n\t",resp.json()['ip'])

http_proxies = ["http://95.216.136.105:8888","http://135.181.254.248:8888"]
https_proxies = ["https://95.216.136.105:8888","https://135.181.254.248:8888"]
noided_requests.configure(new_identity_per_request=False,http_proxy_list=http_proxies,https_proxy_list=https_proxies)
sess = noided_requests.Session()
resp = sess.get(host_addr,headers={"Accept": "application/json"})
print("Paranoid WITH session:\n\t",resp.json()['ip'])

#You can manually specify here, or automatically crawl public proxies (not a great idea if you care about speed/security)
http_proxies = ["http://95.216.136.105:8888","http://135.181.254.248:8888"]
https_proxies = ["https://95.216.136.105:8888","https://135.181.254.248:8888"]
noided_requests.configure(new_identity_per_request=True,http_proxy_list=http_proxies,https_proxy_list=https_proxies)
print("Paranoid Auto Session:\n")
for x in range(2):
    resp = noided_requests.get(host_addr,headers={"Accept": "application/json"})    
    print("\t",resp.json()['ip'])

#We can try completely automatic setup and try our luck against the public proxy list
noided_requests.configure(new_identity_per_request=True)
print("Paranoid Auto Session with public proxy list:\n")
for x in range(2):
    resp = noided_requests.get(host_addr,headers={"Accept": "application/json"})    
    print("\t",resp.json()['ip'])
```

Will produce output something like (arbitrary proxy addresses are used below):


```console
 ❯ python simple_requests_example.py
Default:
     YOUR-IP
Paranoid without session:
     YOUR-IP
Paranoid WITH session:
     207.204.229.66
Paranoid Auto Session:
     209.107.196.142
     216.131.75.35
Paranoid Auto Session with public proxy list:
     207.204.229.66
     209.107.196.142
```
