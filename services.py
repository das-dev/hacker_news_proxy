import re
import lxml.html

LOCALHOST = 'https://127.0.0.1:8080/'
TOKEN_LENGTH_TO_PATCH = 6
RE_TARGET_TOKEN = r'\b(?P<word>\w{{{0}}})\b'.format(TOKEN_LENGTH_TO_PATCH)
RE_REPLACE = r'\g<word>™'


def patch_html(content: bin, origin_host: str) -> bin:
    tree = lxml.html.fromstring(content.decode('utf8'))
    _patch_node(tree.head.find('title'))
    for node in tree.body.iterdescendants():
        _patch_node(node, origin_host)
    return lxml.html.tostring(tree)


def _patch_node(node: lxml.html.Element,
                origin_host: str | None = None) -> None:
    if node is not None and node.text is not None:
        node.text = re.sub(RE_TARGET_TOKEN, RE_REPLACE, node.text)
        if node.tag == 'a':
            href = node.get('href').replace(origin_host, LOCALHOST)
            node.set('href', href)
