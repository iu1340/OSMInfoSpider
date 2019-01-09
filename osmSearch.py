"""A Python module that provides the API client component for the open street map(OSM).
    Additional resources:
    * https://nominatim.openstreetmap.org/
    * https://wiki.openstreetmap.org/
    * https://www.openstreetmap.org/
    """

# 添加查询条件
class OsmSearch():
    # static variables
    __base_url = u'https://nominatim.openstreetmap.org/search.php'

    def __init__(self,query,polygon_geojson):
        """Initializes a search object with a query and target index."""
        self.query = query
        self.polygon_geojson = polygon_geojson
        self._uri = self.__base_url + "?q="+self.query+"&polygon_geojson="+str(self.polygon_geojson)+"&format=json"

    # properties
    @property
    def query(self):
        """Gets the search query"""
        return self._query

    @query.setter
    def query(self, query):
        """Sets the search query"""
        self._query = query

    @property
    def polygon_geojson(self):
        """Gets the label of the index targeted by the search"""
        return self._polygon_geojson

    @polygon_geojson.setter
    def polygon_geojson(self, polygon_geojson):
        self._polygon_geojson = polygon_geojson
        """Sets the label of the index targeted by the search"""

    @property
    def results(self):
        """Gets the results for the search"""
        return self._results

    @property
    def tot_num_res(self):
        """Gets the total number of results that exist in the index for
            this query. This number might be larger than can be retrieved
            and stored in a single ElsSearch object (i.e. 5,000)."""
        return self._tot_num_res
    
    def execute(self, osm_client = None):
        api_response = osm_client.exec_request(self._uri)
        self._results = api_response
        if(type(self._results).__name__ == "list" ):
            self._tot_num_res = len(self._results)
        elif(type(self._results).__name__ == "dict"):   
            self._tot_num_res = 1     
            