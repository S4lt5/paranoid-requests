from paranoid_requests.paranoid_core import UserAgentLoader, ProxyListLoader, ProxyList
import requests
import random

#If True, each request will get a new session, and thus a new user agent and proxy


class ParanoidConfig:
    configuration = None
    @classmethod
    def get_config(cls):
        if cls.configuration == None:
            configure()
        
        return cls.configuration

    def __init__(self,new_identity_per_request=False,proxy_list=None,user_agent_list=None):
        self.new_identity_per_request=new_identity_per_request

        # Use public defaults for proxy or useragent list if none provided
        if proxy_list is None:
            self.proxy_list = ProxyListLoader.from_default_public_proxy_list()                      
        else:
            self.proxy_list = ProxyList(proxy_list)
        
        if user_agent_list is None:
            self.user_agent_list = UserAgentLoader.from_default_public_user_agent_list()
        else:
            self.user_agent_list = user_agent_list
        






def configure(new_identity_per_request=False,proxy_list=None,user_agent_list=None):
    ParanoidConfig.configuration = ParanoidConfig(new_identity_per_request=new_identity_per_request,
                                        proxy_list=proxy_list,
                                        user_agent_list=user_agent_list)



def delete(url, params=None,**kwargs):      
    if ParanoidConfig.get_config().new_identity_per_request:
        s = Session()
        return s.delete(url, params=params,**kwargs)
    else:    
        return requests.delete(url,params=params,**kwargs)

def get(url,params=None,**kwargs):    
    if ParanoidConfig.get_config().new_identity_per_request:    
        s = Session()
        return s.get(url, params=params,**kwargs)
    else:    
        return requests.get(url,params=params,**kwargs)

def head(url, params=None,**kwargs):
    return requests.head(url,params=params,**kwargs)

def options(url, params=None,**kwargs):
    return requests.options(url,params=params,**kwargs)

def patch(url, params=None,**kwargs):
    return requests.patch(url,params=params,**kwargs)

def post(url, params=None,**kwargs):
    return requests.post(url,params=params,**kwargs)

def put(url, params=None,**kwargs):
    return requests.put(url,params=params,**kwargs)

def request(url, params=None,**kwargs):
    print("I GOT A REQUEST YO")
    return requests.request(url,params=params,**kwargs)

class Session(requests.Session):    
    """Wrapper for requests.session that injects user agent and proxy values"""
    def __init__(self) -> None:
        super().__init__()

        # if no config exists, create one        
        http_proxy = ParanoidConfig.get_config().proxy_list.get_next_proxy()
        address = http_proxy[0]
        port = http_proxy[1]
        self.override_proxies = {
            "http": f"http://{address}:{port}",
            "https": f"https://{address}:{port}"            
        }
            
    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None
    ): 
        return super().request(method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, self.override_proxies, hooks, stream, verify, cert, json)


def session():       
    
    return Session()

#Access wrapped module with requests member
requests = requests

