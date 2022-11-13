""" Module containing basic proxy list functionality, used by both paranoid implementations"""
import os, re, itertools 

class MissingProxyListError(Exception):
    """
    Used when ProxyList is called, but no or empty list of proxy servers is 
    """
    pass



class ProxyListDownloadError(Exception):
    """
    Used when the public proxy service cannot be queried
    """
    pass

class InvalidProxyError(Exception):
    """
    Thrown when we can obviously see that the passed object is not a (addr,port) tuple
    """




class ProxyList:

    def __init__(self, proxies):
        """
        Take the passed proxy list, or create a blank one

        Proxy is a list of tuples: [('address','port'),...]
        """
        if not proxies or not hasattr(proxies, '__len__') or len(proxies) < 1:
            raise MissingProxyListError("A non empty proxylist must be provided to ProxyList()")
        
        for p in proxies:
            if not p or not hasattr(proxies,'__len__') or len(p) != 2:
                raise InvalidProxyError("Each proxy must be a two-value tuple containing the address and port")


        # do I really need this?
        self.proxies = proxies
        #Create an infinite iterator that cycles through all of the proxies
        self.generator = itertools.cycle(proxies)
    
    def GetNextProxy(self):
        return next(self.generator)
                

#for determining if a host is valid
PROXY_REGEX=re.compile("^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\\-]*[A-Za-z0-9]):([\\d]+)$")

class ProxyListLoader:
    def fromTextFile(input_path):
        """Load a proxy list from a multiline text file with the format address:port, one per line."""

        if not os.path.exists(input_path) or not os.path.isfile(input_path):
            raise FileNotFoundError(f"The input file {input_path} does not exist.")   
        
        proxies = []
        with open(input_path,'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                proxy = ProxyListLoader.parseProxyEntry(line)
                proxies.append(proxy)                
        
        return ProxyList(proxies=proxies)


    def parseProxyEntry(line):
        """Validate a line of text iput that will be turned into a proxy entry, then return a tuple of host,port"""                
        match = PROXY_REGEX.search(line)
        if match is None:
            raise InvalidProxyError(f"The proxy entry {line} is not in the correct format of 'host:port'")
        
        #match 1 is the host, match 2 is the port
        return (match[1],match[2])
        
    