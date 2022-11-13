from paranoid_requests.paranoid_core import ProxyListLoader,MissingProxyListError, InvalidProxyError
import pytest, os



class TestProxyListLoader:

    artifacts_path = os.path.join(os.path.dirname(__file__),'artifacts')
    empty_path = os.path.join(artifacts_path,'test_proxies_empty.txt')
    bad_path = os.path.join(artifacts_path,'test_proxies_bad.txt')
    good_path = os.path.join(artifacts_path,'test_proxies_good.txt')
    """
    Test proxylist loader
    """
    def test_bad_proxy_list_fails(self):                
        assert os.path.exists(TestProxyListLoader.empty_path)
        with pytest.raises(MissingProxyListError):
            ProxyListLoader.fromTextFile(TestProxyListLoader.empty_path)

        assert os.path.exists(TestProxyListLoader.bad_path)
        with pytest.raises(InvalidProxyError):
            ProxyListLoader.fromTextFile(TestProxyListLoader.bad_path)

        assert os.path.exists(TestProxyListLoader.good_path)        
        proxyList = ProxyListLoader.fromTextFile(TestProxyListLoader.good_path)

        
        assert len(proxyList.proxies) == 10

        # assert I can read far more than 10 out of the generator, try to read len * 2
        for x in range(20):
            proxyList.GetNextProxy()

    

        