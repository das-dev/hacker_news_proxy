import re
import lxml.html

from settings import PROXY_HOST

TOKEN_LENGTH_TO_PATCH = 6
RE_TARGET_TOKEN = fr'\b(?P<word>\w{{{TOKEN_LENGTH_TO_PATCH}}})\b'
RE_REPLACE = r'\g<word>™'


def patch_html(content: bytes, origin_host: str) -> bytes:
    tree: lxml.html.HtmlElement = lxml.html.fromstring(content.decode('utf8'))
    _patch_text(tree.head.find('title'))
    for node in tree.body.iterdescendants():
        _patch_text(node)
        _patch_link(node, origin_host)
    return lxml.html.tostring(tree)


def _patch_text(node: lxml.html.Element) -> None:
    if node is not None and node.text is not None:
        node.text = re.sub(RE_TARGET_TOKEN, RE_REPLACE, node.text)


def _patch_link(node: lxml.html.Element, origin_host: str) -> None:
    if node is not None and node.tag == 'a':
        href = node.get('href').replace(origin_host, PROXY_HOST)
        node.set('href', href)
