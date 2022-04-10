from urllib.parse import urljoin

from services import patch_html, LOCALHOST

HACKER_NEWS_HOST = 'https://news.ycombinator.com/'
TM_HTML_ENTITY = '&#8482;'


def test_link_replace():
    source_url = urljoin(HACKER_NEWS_HOST, '/about')
    target_url = urljoin(LOCALHOST, '/about')
    html_source = f'<head></head><a href="{source_url}">Anchor</a>'.encode('utf8')
    target = f'a href="{target_url}">Anchor{TM_HTML_ENTITY}</a>'
    assert target in patch_html(html_source, HACKER_NEWS_HOST).decode('utf8')


def test_token_patching():
    html_source = f'<head></head><span>Hacker News</span>'.strip().encode('utf8')
    target = f'<span>Hacker{TM_HTML_ENTITY} News</span>'
    assert target in patch_html(html_source, HACKER_NEWS_HOST).decode('utf8')


def test_title_patching():
    html_source = '''
    <html>
        <head>
            <title>Hacker News</title>
        </head>
        <body></body>
    </html>
    '''.strip().encode('utf8')
    target = f'<title>Hacker{TM_HTML_ENTITY} News</title>'
    assert target in patch_html(html_source, HACKER_NEWS_HOST).decode('utf8')
