import os
import pytest
from paranoid_requests.paranoid_core import ProxyListLoader, InvalidProxyError,ProxyListDownloadError





class TestProxyListLoader:
    """
    Test proxylist loader
    """
    artifacts_path = os.path.join(os.path.dirname(__file__),'artifacts')
    empty_path = os.path.join(artifacts_path,'test_proxies_empty.txt')
    bad_path = os.path.join(artifacts_path,'test_proxies_bad.txt')
    good_path = os.path.join(artifacts_path,'test_proxies_good.txt')

    def test_bad_proxy_list_fails(self):
        """Test that invalid files or paths fail. Test that a good file loads successfully and can
        infinitely generate proxies from said list"""
        assert os.path.exists(TestProxyListLoader.empty_path)
        with pytest.raises(InvalidProxyError):
            ProxyListLoader.from_text_file(TestProxyListLoader.empty_path)

        assert os.path.exists(TestProxyListLoader.bad_path)
        with pytest.raises(InvalidProxyError):
            ProxyListLoader.from_text_file(TestProxyListLoader.bad_path)

        assert os.path.exists(TestProxyListLoader.good_path)
        proxy_list = ProxyListLoader.from_text_file(TestProxyListLoader.good_path)


        assert len(proxy_list.proxies) == 10

        assert ('156.239.55.107',3128) in proxy_list.proxies
        assert ('85.159.214.61',1080) in proxy_list.proxies
        assert ('138.0.207.18',38328) in proxy_list.proxies
        assert ('200.202.223.42',8080) in proxy_list.proxies
        assert ('150.109.32.166',80) in proxy_list.proxies
        assert ('47.74.152.29',8888) in proxy_list.proxies
        assert ('177.93.50.234',999) in proxy_list.proxies
        assert ('124.13.181.7',80) in proxy_list.proxies
        assert ('155.4.244.218',80) in proxy_list.proxies
        assert ('94.231.216.241',8085) in proxy_list.proxies


        # assert I can read far more than 10 out of the generator, try to read len * 2
        for ctr in range(20):
            proxy_list.get_next_proxy()

    def test_url_loader(self):
        """Tests for the url-based proxylist loader"""


        proxy_list = ProxyListLoader.from_url("https://raw.githubusercontent.com/Yablargo/paranoid-requests/main/tests/artifacts/test_proxies_good.txt")
        assert len(proxy_list.proxies) == 10

        assert ('156.239.55.107',3128) in proxy_list.proxies
        assert ('85.159.214.61',1080) in proxy_list.proxies
        assert ('138.0.207.18',38328) in proxy_list.proxies
        assert ('200.202.223.42',8080) in proxy_list.proxies
        assert ('150.109.32.166',80) in proxy_list.proxies
        assert ('47.74.152.29',8888) in proxy_list.proxies
        assert ('177.93.50.234',999) in proxy_list.proxies
        assert ('124.13.181.7',80) in proxy_list.proxies
        assert ('155.4.244.218',80) in proxy_list.proxies
        assert ('94.231.216.241',8085) in proxy_list.proxies



        with pytest.raises(ProxyListDownloadError):
            proxy_list = ProxyListLoader.from_url("https://raw.githubusercontent.com/Yablargo/paranoid-requests/main/tests/artifacts/test_proxies_nonexistant.txt")

        with pytest.raises(InvalidProxyError):
            ProxyListLoader.from_url("https://raw.githubusercontent.com/Yablargo/paranoid-requests/main/tests/artifacts/test_proxies_bad.txt")


    def test_public_loader(self):
        """Test the default public HTTP proxy list loader"""
        proxy_list = ProxyListLoader.from_default_public_proxy_list()

        assert len(proxy_list.proxies) > 10
