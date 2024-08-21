""" All the http request functionality

This file can also be imported as service and contains the following functionality
    * get_request - http get call with all functionality
    * post_request - http post call with all functionality

Author
----------
name: Bola
email: prasad.kumara@blackswan-technologies.com
"""
import requests

from app.config.logging_config import get_logger

logger = get_logger(class_name=__name__)


class HttpService:
    @classmethod
    def get_request(cls, url: str, query_params: dict = None, headers: dict = None, auth_enable=False):
        """ Http get call with all functionality
        Parameters
        ----------
        url: str
            Http get call url
        query_params: dict
            Get call query parameters
        headers: dict
            Get call headers
        auth_enable: bool
            JWT authentication enable or disable status

        Returns
        ----------
        tuple:
            Response object as JSON object, Http status

        Author
        ----------
        name: Bola
        email: prasad.kumara@blackswan-technologies.com

        Developers
        ----------
        - name: Bola
          email: prasad.kumara@blackswan-technologies.com
        """
        logger.info("Http Get Request Started")
        logger.debug(f"URL: {url}, Params: {query_params}, Headers: {headers}")
        response = requests.get(url=url, params=query_params, headers=headers)
        logger.debug(f"Response Code: {response.status_code}, Response Payload: {response.text}")
        logger.info("Http Get Request End")
        return response.json(), response.status_code

    @classmethod
    def post_request(cls, url: str, query_params: dict = None, payload: any = None, headers: dict = None,
                     auth_enable=False):
        """ Http post call with all functionality
        Parameters
        ----------
        url: str
            Http get call url
        query_params: dict
            Get call query parameters
        payload: any
            Post call request body
        headers: dict
            Get call headers
        auth_enable: bool
            JWT authentication enable or disable status

        Returns
        ----------
        tuple:
            Response object as JSON object, Http status

        Author
        ----------
        name: Bola
        email: prasad.kumara@blackswan-technologies.com

        Developers
        ----------
        - name: Bola
          email: prasad.kumara@blackswan-technologies.com
        """
        logger.info("Http Post Request Started")
        logger.debug(f"URL: {url}, Params: {query_params}, Headers: {headers}")
        response = requests.post(url=url, params=query_params, json=payload, headers=headers)
        logger.debug(f"Response Code: {response.status_code}, Response Payload: {response.text}")
        logger.info("Http Post Request End")
        return response.json(), response.status_code

    @classmethod
    def put_request(cls, url: str, query_params: dict = None, payload: any = None, headers: dict = None,
                    auth_enable=False):
        """HTTP PUT call with all functionality.

        Parameters
        ----------
        url : str
            The URL for the HTTP PUT call.
        query_params : dict, optional
            The query parameters for the HTTP PUT call (default is None).
        payload : any, optional
            The request body for the HTTP PUT call (default is None).
        headers : dict, optional
            The headers for the HTTP PUT call (default is None).
        auth_enable : bool, optional
            The JWT authentication enable or disable status (default is False).

        Returns
        -------
        tuple
            A tuple containing the response object as a JSON object and the HTTP status code.

        Author
        ------
        Name: Anuka
        Email: karunanayaka@focalid.tech

        Developers
        ----------
        - Name: Anuka
          Email: karunanayaka@focalid.tech
        """
        logger.info("Http Put Request Started")
        logger.debug(f"URL: {url}, Params: {query_params}, Headers: {headers}")
        response = requests.put(url=url, params=query_params, json=payload, headers=headers)
        logger.debug(f"Response Code: {response.status_code}, Response Payload: {response.text}")
        logger.info("Http Put Request End")
        return response.json(), response.status_code

    @classmethod
    def delete_request(cls, url: str, query_params: dict = None, headers: dict = None, auth_enable=False):
        """HTTP DELETE call with all functionality.

        Parameters
        ----------
        url : str
            The URL for the HTTP DELETE call.
        query_params : dict, optional
            The query parameters for the HTTP DELETE call (default is None).
        headers : dict, optional
            The headers for the HTTP DELETE call (default is None).
        auth_enable : bool, optional
            The JWT authentication enable or disable status (default is False).

        Returns
        -------
        tuple
            A tuple containing the response object as a JSON object and the HTTP status code.

        Author
        ------
        Name: Anuka
        Email: karunanayaka@focalid.tech

        Developers
        ----------
        - Name: Anuka
          Email: karunanayaka@focalid.tech
        """
        logger.info("Http Delete Request Started")
        logger.debug(f"URL: {url}, Params: {query_params}, Headers: {headers}")
        response = requests.delete(url=url, params=query_params, headers=headers)
        logger.debug(f"Response Code: {response.status_code}, Response Payload: {response.text}")
        logger.info("Http Delete Request End")
        return response.json(), response.status_code
