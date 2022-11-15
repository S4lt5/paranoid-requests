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
