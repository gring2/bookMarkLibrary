from bs4 import BeautifulSoup, element
import requests
import traceback
import logging


def get_html_node(response, target_info, attr_name):
    try:

        soup = BeautifulSoup(response.text, 'html.parser')
        node = soup.find(**target_info)

        if meta_node_has_attri(node, attr_name) and len(node[attr_name]) > 1:
            return node

        return None

    except requests.exceptions.ConnectionError:
        logging.error(traceback.extract_stack())
        return None


def meta_node_has_attri(node, attr):
    return node is not None and node.has_attr(attr)
