"""Used to generate user agents from a list of choices"""
import itertools
import json
import os
import requests


class MissingUserAgentListError(Exception):
    """
    Used when UserAgentList is called, but no or empty list of user agents is provided
    """



class UserAgentListDownloadError(Exception):
    """
    Used when the public user agent URL cannot be queried
    """

class InvalidUserAgentError(Exception):
    """
    Thrown when the passed object is not a non-empty string
    """



class UserAgentList:
    """A list of user agents, to be used in creating a round-robin generator
    exposed via the get_next_user_agent() method"""
    def __init__(self, user_agents):
        """
        Take the passed user-agent list, or create a blank one

        A user agent is a one-line string such as:
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        """
        if not user_agents or not hasattr(user_agents, '__len__') or len(user_agents) < 1:
            raise MissingUserAgentListError("A non empty proxylist must be provided to UserAgentList()")

        for agent in user_agents:
            if not agent or agent == "":
                raise InvalidUserAgentError("An empty user agent was passed to UserAgentList")


        # do I really need this?
        self.user_agents = user_agents
        #Create an infinite iterator that cycles through all of the proxies
        self.generator = itertools.cycle(user_agents)

    def get_next_user_agent(self):
        """Return the next user agent string to be used"""
        return next(self.generator)




class UserAgentLoader:
    """A file-based proxy list loader that reads one entry per line in host:port format"""
    @staticmethod
    def from_json_file(input_path):
        """Load a proxy list from a JSON file containing a list of user agent strings"""

        if not os.path.exists(input_path) or not os.path.isfile(input_path):
            raise FileNotFoundError(f"The input file {input_path} does not exist.")


        with open(input_path,'r') as file:
            content = file.read()
            return UserAgentLoader.from_string(content)

    @staticmethod
    def from_string(useragent_list_contents):
        """Read a proxy list from a string, one proxy per line in host:port format"""
        user_agents = []
        try:
            user_agents = json.loads(useragent_list_contents)
        except:
            raise UserAgentListDownloadError("Could not parse JSON from the user agent list")

        if len(user_agents) < 1:
            raise UserAgentListDownloadError("A user agent list with no entries was encountered.")

        for agent in user_agents:
            agent = agent.strip()
            UserAgentLoader.validate_user_agent_entry(agent)
            user_agents.append(agent)

        return UserAgentList(user_agents=user_agents)

    @staticmethod
    def from_url(url):
        """Load a proxy list from a URL, the url must have text content with the format addresS:port, one per line."""
        resp = requests.get(url,timeout=20)

        if resp.status_code != 200:
            raise UserAgentListDownloadError(f"Can't download the user agent list from {url}")

        return UserAgentLoader.from_string(resp.text)



    public_user_agents_url = "https://cdn.jsdelivr.net/gh/Kikobeats/top-user-agents@master/index.json"
    @staticmethod
    def from_default_public_user_agent_list():
        """Load a proxy list from Kikobeats' list of public user agents
        See https://github.com/Kikobeats/top-user-agents for up to date licensing info."""

        return UserAgentLoader.from_url(UserAgentLoader.public_user_agents_url)


    @staticmethod
    def validate_user_agent_entry(user_agent):
        """Validate a a user_agent is a non empty string"""
        if user_agent is None or user_agent == "":
            raise InvalidUserAgentError("A user agent must be a non-empty string")
