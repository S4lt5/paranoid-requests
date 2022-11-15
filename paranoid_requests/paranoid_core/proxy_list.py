""" Module containing basic proxy list functionality, used by both paranoid implementations"""
import os
import itertools
import requests
import validators


class MissingProxyListError(Exception):
    """
    Used when ProxyList is called, but no or empty list of proxy servers is
    """



class ProxyListDownloadError(Exception):
    """
    Used when the public proxy service cannot be queried
    """

class InvalidProxyError(Exception):
    """
    Thrown when we can obviously see that the passed object is not valid URL
    """




class ProxyList:
    """A list of proxies, to be used in creating a round-robin generator
    exposed via the get_next_proxy() method"""
    def __init__(self, proxies=None):
        """
        Take the passed proxy list, or create a blank one

        Proxy is a list of urls e.g. http://192.168.2.55:8181
        """
        if not proxies or not hasattr(proxies, '__len__') or len(proxies) < 1:
            raise MissingProxyListError("A non empty proxylist must be provided to ProxyList()")

        for prox in proxies:
            if validators.url(str(prox)) is not True:
                raise InvalidProxyError("Each https proxy specified must be a valid url")


        # do I really need this?
        self.proxies = proxies

        #Create an infinite iterator that cycles through all of the proxies
        self.generator = itertools.cycle(self.proxies)

    def get_next_proxy(self):
        """Return the next proxy URL"""
        return next(self.generator)




class ProxyListLoader:
    """A file-based proxy list loader that reads one entry per line in host:port format"""
    @staticmethod
    def from_text_file(input_path):
        """Load a proxy list from a multiline text file with the format address:port, one per line."""

        if not os.path.exists(input_path) or not os.path.isfile(input_path):
            raise FileNotFoundError(f"The input file {input_path} does not exist.")


        with open(input_path,'r') as file:
            content = file.read()
            return ProxyListLoader.from_string(content)

    @staticmethod
    def from_string(proxylist_contents):
        """Read a proxy list from a string, one URL per line"""
        proxies = []
        for line in proxylist_contents.split("\n"):
            line = line.strip()
            proxy = ProxyListLoader.parse_proxy_entry(line)
            proxies.append(proxy)


        return ProxyList(proxies=proxies)

    @staticmethod
    def from_url(url):
        """Load a proxy list from a URL. The response must have one URL per line and contain valid URLs"""
        resp = requests.get(url,timeout=20)

        if resp.status_code != 200:
            raise ProxyListDownloadError(f"Can't download the proxy list from {url}")

        return ProxyListLoader.from_string(resp.text)



    public_http_proxies_url = "https://cdn.jsdelivr.net/gh/monosans/proxy-list@main/proxies_geolocation_anonymous/http.txt"
    @staticmethod
    def from_default_public_proxy_list(proxy_type="http"):
        """Load a proxy list from https://github.com/monosans/proxy-list/
        Check the source for up to date licensing info if you want to directly include this."""
        if proxy_type not in ("http","https"):
            raise ProxyListDownloadError("Must specify http or https for proxy type.")

        resp = requests.get(ProxyListLoader.public_http_proxies_url)

        if resp.status_code != 200:
            raise ProxyListDownloadError("Received an error when dowloading the default public proxy list")
        proxies = []
        for line in resp.text.split("\n"):
            items = line.split("|")
            if len(items) != 4:
                raise ProxyListDownloadError("The proxy list was not in the expected format.")
            if items[1] == "United States":
                #skip non-USA for performance and safety reasons
                proxies.append(f"{proxy_type}://{items[0]}")
        return ProxyList(proxies=proxies)



    @staticmethod
    def parse_proxy_entry(line):
        """Validate a line of text iput that will be turned into a proxy entry, then return URL"""
        url = str(line).strip()

        if validators.url(line) is True:
            return url

        raise InvalidProxyError(f"Proxy URL {url} is not valid")
