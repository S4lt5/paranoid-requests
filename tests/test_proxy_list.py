from paranoid_requests.paranoid_core import ProxyList,MissingProxyListError, InvalidProxyError
import pytest

class TestProxyList:
    """
    Test basic ProxyList functionality
    """
    def test_bad_list_fails(self):
        
        with pytest.raises(MissingProxyListError):
            ProxyList(proxies=None)

        with pytest.raises(MissingProxyListError):
            ProxyList([])

        with pytest.raises(MissingProxyListError):
            ProxyList({})

    def test_invalid_object_string_fails(self):
        # a string is a collection, but does not have the right tuples inside
        with pytest.raises(InvalidProxyError):
            ProxyList("foo")
        
        with pytest.raises(InvalidProxyError):
            ProxyList([(1,2,3)])
        
        #this should throw no exception...
        ProxyList([(1,2)])
        # but we add an invalid item to the list and it should now.
        with pytest.raises(InvalidProxyError):
            ProxyList([(1,2),None])

    
