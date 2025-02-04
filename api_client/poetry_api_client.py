import requests
from urllib.parse import quote
from typing import List, Optional
from api_client.input_classes import _Input
from api_client.output_enum import Output

class PoetryApiClient:
    BASE_URL = "https://poetrydb.org"

    def call_api(self, inputs: List[_Input], outputs: Optional[List[Output]] = None,
                raw_text: bool = False) -> None:
        """
        Build the route from the inputs, then make a GET request to poetrydb.org.
        :param inputs: A list of _Input objects (e.g. [Author('Shakespeare'), LineCount('14')])
        :param outputs: A list of Output enums to filter the returned fields
        :param raw_text: If True, response is in json, if False it's in a raw text/string.
        :return: The response from the PoetryDB API. A Python dict/list if JSON, or a raw text/string if raw_text=True.
        """
        route = self._build_route(inputs, outputs, raw_text)
        url = f"{self.BASE_URL}{route}"
        return requests.get(url)

    def _build_route(self, inputs: List[_Input], outputs: Optional[List[Output]] = None,
                    raw_text: bool = False) -> str:
        
        if not inputs:
            return "/"
        
        # build <input field> components
        input_fields = ",".join(str(inp) for inp in inputs)

        # build <search term> components and URL-encode values allowing "," symbol
        search_terms = []
        for inp in inputs:
            term = quote(inp.value, safe=",")
            if inp.absolute:
                term += ":abs"
            search_terms.append(term)
        search_terms = ";".join(search_terms)

        # start building the route
        route = f"/{input_fields}/{search_terms}"

        # build <output field> components (optional)
        if outputs:
            output_fields = ",".join(output.value for output in outputs)
            route += f"/{output_fields}"

        # return in plain text instead of json (optional)
        if raw_text:
            route += ".text"

        return route
        
