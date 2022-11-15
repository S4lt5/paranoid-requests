"""Tests for basic proxylist functionality"""
import pytest
from paranoid_requests.paranoid_core import MissingProxyListError,InvalidProxyError, ProxyList

class TestProxyList:
    """
    Test basic ProxyList functionality
    """
    def test_bad_list_fails(self):
        """Test that missing or invalid proxy list throws an error"""

        with pytest.raises(MissingProxyListError):
            ProxyList(proxies=None)

        with pytest.raises(MissingProxyListError):
            ProxyList([])

        with pytest.raises(MissingProxyListError):
            ProxyList({})

    def test_invalid_object_string_fails(self):
        """Test that bad values for an individual proxy line throw an error """
        # a string is a collection, but does not have the right tuples inside
        with pytest.raises(InvalidProxyError):
            ProxyList("foo")

        with pytest.raises(InvalidProxyError):
            ProxyList([(1,2,3)])

        #this should throw an invalid proxy exception...
        with pytest.raises(InvalidProxyError):
            ProxyList([(1,2)])
        # but we add an invalid item to the list and it should now.
        with pytest.raises(InvalidProxyError):
            ProxyList(["ssh://www.fubar.bazinga",None])

    def test_round_robin_generator(self):
        """Test that I can load a valid proxy from a list, and that the generator gives
        expected results"""

        proxies = [
        'http://156.239.55.107:3128',
        'http://85.159.214.61:1080',
        'http://138.0.207.18:38328',
        'http://200.202.223.42:8080',
        'http://150.109.32.166:80',
        'http://47.74.152.29:8888',
        'http://177.93.50.234:999',
        'http://124.13.181.7:80',
        'http://155.4.244.218:80',
        'http://94.231.216.241:8085']

        proxy_list = ProxyList(proxies=proxies)

        # make sure we actually get what we put in
        
        assert 'http://156.239.55.107:3128' in proxy_list.proxies
        assert 'http://85.159.214.61:1080' in proxy_list.proxies
        assert 'http://138.0.207.18:38328' in proxy_list.proxies
        assert 'http://200.202.223.42:8080' in proxy_list.proxies
        assert 'http://150.109.32.166:80' in proxy_list.proxies
        assert 'http://47.74.152.29:8888' in proxy_list.proxies
        assert 'http://177.93.50.234:999' in proxy_list.proxies
        assert 'http://124.13.181.7:80' in proxy_list.proxies
        assert 'http://155.4.244.218:80' in proxy_list.proxies
        assert 'http://94.231.216.241:8085' in proxy_list.proxies

        # now, we should be able to pull round robin and get them in order
        # loop through some number of times and we should get the proxies in order
        for x in range(20):
            assert 'http://156.239.55.107:3128' == proxy_list.get_next_proxy()
            assert 'http://85.159.214.61:1080' == proxy_list.get_next_proxy()
            assert 'http://138.0.207.18:38328' == proxy_list.get_next_proxy()
            assert 'http://200.202.223.42:8080' == proxy_list.get_next_proxy()
            assert 'http://150.109.32.166:80' == proxy_list.get_next_proxy()
            assert 'http://47.74.152.29:8888' == proxy_list.get_next_proxy()
            assert 'http://177.93.50.234:999' == proxy_list.get_next_proxy()
            assert 'http://124.13.181.7:80' == proxy_list.get_next_proxy()
            assert 'http://155.4.244.218:80' == proxy_list.get_next_proxy()
            assert 'http://94.231.216.241:8085' == proxy_list.get_next_proxy()

      