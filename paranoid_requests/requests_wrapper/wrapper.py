from paranoid_core import UserAgentLoader, ProxyListLoader, ProxyList
import requests
import random

#If True, each request will get a new session, and thus a new user agent and proxy


class ParanoidConfig:
    """Contains configuration of which proxies to use, and when to use a new identity"""
    configuration = None
    @classmethod
    def get_config(cls):
        """Get the ParanoidConfig, or create a new one if it does not exist"""
        if cls.configuration is None:
            configure()

        return cls.configuration

    def __init__(self,new_identity_per_request=False,http_proxy_list=None,https_proxy_list=None,user_agent_list=None):
        self.new_identity_per_request=new_identity_per_request

        # Use public defaults for HTTP proxy list if none provided
        if http_proxy_list is None:
            self.http_proxy_list = ProxyListLoader.from_default_public_proxy_list(proxy_type='http')
        else:
            self.http_proxy_list = ProxyList(http_proxy_list)

        if https_proxy_list is None:
            self.https_proxy_list = ProxyListLoader.from_default_public_proxy_list(proxy_type='https')
        else:
            self.https_proxy_list = ProxyList(http_proxy_list)


        # use public defaults for useragent list if none provided
        if user_agent_list is None:
            self.user_agent_list = UserAgentLoader.from_default_public_user_agent_list()
        else:
            self.user_agent_list = user_agent_list







def configure(new_identity_per_request=False,http_proxy_list=None,https_proxy_list=None,user_agent_list=None):
    """Change Paranoid Requests Wrapper Config"""
    ParanoidConfig.configuration = ParanoidConfig(new_identity_per_request=new_identity_per_request,
                                        http_proxy_list=http_proxy_list,
                                        https_proxy_list=https_proxy_list,
                                        user_agent_list=user_agent_list)



def delete(url, params=None,**kwargs):
    """Wrapper for the requests function of the same name"""
    if ParanoidConfig.get_config().new_identity_per_request:
        return Session().delete(url, params=params,**kwargs)

    return requests.delete(url,params=params,**kwargs)

def get(url,params=None,**kwargs):
    """Wrapper for the requests function of the same name"""
    if ParanoidConfig.get_config().new_identity_per_request:
        return Session().get(url, params=params,**kwargs)

    return requests.get(url,params=params,**kwargs)

def head(url, params=None,**kwargs):
    """Wrapper for the requests function of the same name"""
    if ParanoidConfig.get_config().new_identity_per_request:
        return Session().head(url, params=params,**kwargs)

    return requests.head(url,params=params,**kwargs)

def options(url, params=None,**kwargs):
    """Wrapper for the requests function of the same name"""
    if ParanoidConfig.get_config().new_identity_per_request:
        return Session().options(url, params=params,**kwargs)

    return requests.options(url,params=params,**kwargs)

def patch(url, params=None,**kwargs):
    """Wrapper for the requests function of the same name"""
    if ParanoidConfig.get_config().new_identity_per_request:
        return Session().patch(url, params=params,**kwargs)

    return requests.patch(url,params=params,**kwargs)

def post(url, params=None,**kwargs):
    """Wrapper for the requests function of the same name"""
    if ParanoidConfig.get_config().new_identity_per_request:
        return Session().post(url, params=params,**kwargs)

    return requests.post(url,params=params,**kwargs)

def put(url, params=None,**kwargs):
    """Wrapper for the requests function of the same name"""
    if ParanoidConfig.get_config().new_identity_per_request:
        return Session().put(url, params=params,**kwargs)

    return requests.put(url,params=params,**kwargs)

def request(url, params=None,**kwargs):
    """Wrapper for the requests function of the same name"""
    if ParanoidConfig.get_config().new_identity_per_request:
        return Session().request(url, params=params,**kwargs)

    return requests.request(url,params=params,**kwargs)

class Session(requests.Session):
    """Wrapper for requests.session that injects user agent and proxy values"""
    def __init__(self) -> None:
        super().__init__()

        # if no config exists, create one, or get the one that exists
        config = ParanoidConfig.get_config()

        # add http/s proxies
        http_proxy = config.http_proxy_list.get_next_proxy()
        https_proxy = config.https_proxy_list.get_next_proxy()
        self.override_proxies = {
            "http": http_proxy,
            "https": https_proxy
        }
        # add user agent
        self.headers.update({'User-Agent': config.user_agent_list.get_next_user_agent()})

      
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
