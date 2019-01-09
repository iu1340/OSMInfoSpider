"""A Python module that provides the API client component for the open street map(OSM).
    Additional resources:
    * https://nominatim.openstreetmap.org/
    * https://wiki.openstreetmap.org/
    * https://www.openstreetmap.org/
    """

class OsmReverse:
    # static variables
    __base_url = u'https://nominatim.openstreetmap.org/reverse'

    def __init__(self,lat,lon,address_details):
        self.lat = lat
        self.lon = lon
        self.address_details = address_details
        self._uri = self.__base_url + "?lat="+self.lat+"&lon="+self.lon+"&addressdetails"+str(self.address_details)+"&format=json"

    # properties
    @property
    def lat(self):
        """Gets the search lat"""
        return self._lat

    @lat.setter
    def lat(self, lat):
        """Sets the search lat"""
        self._lat = lat

    @property
    def lon(self):
        """Gets the search lon"""
        return self._lon

    @lon.setter
    def lon(self, lon):
        """Sets the search lon"""
        self._lon = lon

    @property
    def address_details(self):
        """Gets the search address_details"""
        return self._address_details

    @address_details.setter
    def address_details(self, address_details):
        """Sets the search address_details"""
        self._address_details = address_details

    @property
    def results(self):
        """Gets the results for the search"""
        return self._results

    
    def execute(self, osm_client = None):
        api_response = osm_client.exec_request(self._uri)
        self._results = api_response  