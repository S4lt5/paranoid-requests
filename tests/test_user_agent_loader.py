import os
import pytest
from json import JSONDecodeError
from paranoid_requests.paranoid_core import UserAgentLoader, InvalidUserAgentError,UserAgentListDownloadError,MissingUserAgentListError





class TestUserAgentLoader:
    """
    Test proxylist loader
    """
    artifacts_path = os.path.join(os.path.dirname(__file__),'artifacts')
    empty_path = os.path.join(artifacts_path,'test_empty_user_agents.txt')
    bad_txt_path = os.path.join(artifacts_path,'test_bad_user_agents.txt')
    bad_json_path = os.path.join(artifacts_path,'test_bad_user_agents.json')
    good_path = os.path.join(artifacts_path,'test_good_user_agents.json')

    def test_bad_user_agent_list_fails(self):
        """Test that invalid files or paths fail. Test that a good file loads successfully and can
        infinitely generate user agents from said list"""
        assert os.path.exists(TestUserAgentLoader.empty_path)
        
        with pytest.raises(JSONDecodeError):
            UserAgentLoader.from_json_file(TestUserAgentLoader.empty_path)

        assert os.path.exists(TestUserAgentLoader.bad_txt_path)
        with pytest.raises(JSONDecodeError):
            UserAgentLoader.from_json_file(TestUserAgentLoader.bad_txt_path)

        assert os.path.exists(TestUserAgentLoader.bad_json_path)
        with pytest.raises(InvalidUserAgentError):
            UserAgentLoader.from_json_file(TestUserAgentLoader.bad_json_path)

        assert os.path.exists(TestUserAgentLoader.good_path)
        agent_list = UserAgentLoader.from_json_file(TestUserAgentLoader.good_path)


        assert len(agent_list.user_agents) == 10
        assert "Mozilla/5.0 (Windows NT 10.0; rv:105.0) Gecko/20100101 Firefox/105.0" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26" in agent_list.user_agents
        assert "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.77" in agent_list.user_agents
        assert "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" in agent_list.user_agents
        # assert I can read far more than 10 out of the generator, try to read len * 2
        for ctr in range(20):
            agent_list.get_next_user_agent()

    def test_url_loader(self):
        """Tests for the url-based proxylist loader"""


        agent_list = UserAgentLoader.from_url("https://raw.githubusercontent.com/Yablargo/paranoid-requests/main/tests/artifacts/test_good_user_agents.json")
        assert len(agent_list.user_agents) == 10

        assert "Mozilla/5.0 (Windows NT 10.0; rv:105.0) Gecko/20100101 Firefox/105.0" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26" in agent_list.user_agents
        assert "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.77" in agent_list.user_agents
        assert "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0" in agent_list.user_agents
        assert "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" in agent_list.user_agents



        with pytest.raises(UserAgentListDownloadError):
            UserAgentLoader.from_url("https://raw.githubusercontent.com/Yablargo/paranoid-requests/main/tests/artifacts/test_agents_nonexistant.txt")

        with pytest.raises(InvalidUserAgentError):
            UserAgentLoader.from_url("https://raw.githubusercontent.com/Yablargo/paranoid-requests/main/tests/artifacts/test_bad_user_agents.json")


    def test_public_loader(self):
        """Test the default public HTTP proxy list loader"""
        user_agent_list = UserAgentLoader.from_default_public_user_agent_list()

        assert len(user_agent_list.user_agents) > 10

