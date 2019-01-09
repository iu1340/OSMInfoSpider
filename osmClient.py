"""A Python module that provides the API client component for the open street map(OSM).
    Additional resources:
    * https://nominatim.openstreetmap.org/
    * https://wiki.openstreetmap.org/
    * https://www.openstreetmap.org/
    """


import requests
import json
import time
import random
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
from osm.osmProxIp import OsmProxy


class OsmClent:
    """A class that implements a Python interface to nominatim.openstreetmap.org"""
    # class variables
    __url_base = "https://nominatim.openstreetmap.org/"  # Base URL for later use
    __min_req_interval = 1  # Min. request interval in sec
    __ts_last_req = time.time()  # Tracker for throttling

    # constructors
    def __init__(self, accept_launage="en", local_dir=None,user_agent = "",ip_list=[]):
        self.accept_launage = accept_launage
        if not local_dir:
            self.local_dir = pathlib.Path.cwd() / 'data'
        else:
            self.local_dir = pathlib.Path(local_dir)
        if not self.local_dir.exists():
            self.local_dir.mkdir()
        self.user_agent = user_agent
        self.ip_list = ip_list

    @property
    def accept_launage(self):
        """Gets the max. number of results to be used by the client instance"""
        return self._accept_launage

    @accept_launage.setter
    def accept_launage(self, accept_launage):
        """Sets the max. number of results to be used by the client instance"""
        self._accept_launage = accept_launage

    @property
    def user_agent(self):
        """Gets the max. number of results to be used by the client instance"""
        return self._user_agent

    @user_agent.setter
    def user_agent(self, user_agent):
        """Sets the max. number of results to be used by the client instance"""
        self._user_agent = user_agent

    @property
    def ip_list(self):
        """Gets the max. number of results to be used by the client instance"""
        return self._ip_list

    @ip_list.setter
    def ip_list(self, ip_list):
        """Sets the max. number of results to be used by the client instance"""
        self._ip_list = ip_list

    @property
    def local_dir(self):
        """Gets the currently configured local path to write data to."""
        return self._local_dir

    @property
    def req_status(self):
        '''Return the status of the request response, '''
        return {'status_code': self._status_code, 'status_msg': self._status_msg}

    @local_dir.setter
    def local_dir(self, path_str):
        """Sets the local path to write data to."""
        self._local_dir = pathlib.Path(path_str)

    # access functions
    def getBaseURL(self):
        """Returns the ELSAPI base URL currently configured for the client"""
        return self.__url_base

    

    def exec_request(self, URL):
        """Sends the actual request; returns response."""
        proxiesIp = OsmProxy(self.user_agent)
        
        if len(self.ip_list)>0:            
            proxies = proxiesIp.get_random_proxies(self.ip_list)
        else:
            proxies = None
        # print(proxies)
        # Throttle request, if need be
        interval = time.time() - self.__ts_last_req
        if (interval < self.__min_req_interval):
            time.sleep(self.__min_req_interval - interval)

        # Construct and execute request
        headers = {
            "Accept-Language": self.accept_launage,
            "User-Agent": self.user_agent,
            "Accept": 'application/json',
            'referer':self.__url_base
        }

        requests.adapters.DEFAULT_RETRIES = 5
        self._status_code = 500
        error_count = 0
        while (self._status_code != 200):
            # print(proxies)
            try:
                r = requests.get(
                    URL,
                    headers=headers,
                    proxies=proxies
                )
                self.__ts_last_req = time.time()
                self._status_code = r.status_code
                if r.status_code == 200:
                    self._status_msg = 'data retrieved'
                    text = json.loads(r.text)
                    r.close()
                    return text
                else:
                    
                    print(URL+" "+ str(error_count))
                    self._status_msg = "HTTP " + \
                        str(r.status_code) + " Error from " + URL + \
                        " and using headers " + str(headers) + ": " + r.text
                    raise requests.HTTPError("HTTP " + str(r.status_code) + " Error from " +
                                             URL + "\nand using headers " + str(headers) + ":\n" + r.text)
            except:
                error_count = error_count+1
                if (error_count%3==0):
                    if len(self.ip_list)>0:
                        proxies = proxiesIp.get_random_proxies(self.ip_list)
                if(error_count >= 10):
                    print("error query "+URL)
                    if (URL.find("reverse") >= 0):
                        return {}
                    return []
                time.sleep(1)
                continue
