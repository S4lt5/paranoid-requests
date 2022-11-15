import datetime
import requests
from github import Github
from paranoid_requests.paranoid_core import ProxyListLoader

class TestPublicLists:
    """
    Test public lists that we pull for up-to-date information
    """

    def test_http_proxies_list_exists_and_is_up_to_date(self):
        """Test that the public HTTP proxy list exists, and is no more than 7d old"""
        response = requests.get(ProxyListLoader.public_http_proxies_url,timeout=20)
        assert response.status_code == 200

        repo = Github().get_repo("TheSpeedX/PROXY-List")
        print(repo.name)
        assert repo.name == "PROXY-List"
        contents = repo.get_contents('http.txt')
        #Format is in: Tue, 15 Nov 2022 12:49:49 GMT

        #Check to see if it has been modified in the past week
        last_modified_date = datetime.datetime.strptime(contents.last_modified, "%a, %d %b %Y %H:%M:%S %Z")
        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        assert last_modified_date > last_week
        #and the last modified date is less than right now, as a basic sanity check
        assert last_modified_date < datetime.datetime.utcnow()
