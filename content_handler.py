import lxml.html


def parse_html(html):
    tree = lxml.html.fromstring(html)
    return lxml.html.tostring(tree)


def patch_html(html):
    return parse_html(html)
