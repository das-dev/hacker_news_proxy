from urllib.parse import urljoin

from services import patch_html
from settings import PROXY_HOST, HACKER_NEWS_HOST

TM_HTML_ENTITY = '&#8482;'


def _ascii(unicode):
    return unicode.strip().encode('utf8')


def test_link_replace():
    source_url = urljoin(HACKER_NEWS_HOST, '/about')
    target_url = urljoin(PROXY_HOST, '/about')
    html_source = _ascii(f'<head></head><a href="{source_url}">Anchor</a>')
    target = _ascii(f'a href="{target_url}">Anchor{TM_HTML_ENTITY}</a>')
    assert target in patch_html(html_source, HACKER_NEWS_HOST)


def test_token_patching():
    html_source = _ascii(f'<head></head><span>Hacker News</span>'.strip())
    target = _ascii(f'<span>Hacker{TM_HTML_ENTITY} News</span>')
    assert target in patch_html(html_source, HACKER_NEWS_HOST)


def test_title_patching():
    html_source = _ascii(
        '''
        <html>
            <head><title>Hacker News</title></head>
            <body></body>
        </html>
        '''
    )
    target = _ascii(f'<title>Hacker{TM_HTML_ENTITY} News</title>')
    assert target in patch_html(html_source, HACKER_NEWS_HOST)
