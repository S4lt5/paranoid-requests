import os
import pytest
from paranoid_requests.paranoid_core import ProxyListLoader,MissingProxyListError, InvalidProxyError




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

        # assert I can read far more than 10 out of the generator, try to read len * 2
        for ctr in range(20):
            proxy_list.get_next_proxy()
