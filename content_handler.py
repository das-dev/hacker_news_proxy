import re
import lxml.html


class HTMLHandler:
    def __init__(self, content):
        self.src = content.decode('utf8')
        self.tree = lxml.html.fromstring(self.src)

    def patch(self, node):
        if node is not None:
            node.text = re.sub(r'\b(?P<word>\w{6})\b', r'\g<word>™', node.text)

    def handle(self):
        self.patch(self.tree.head.find('title'))
        for node in self.tree.body.iterdescendants():
            self.patch(node)
        return lxml.html.tostring(self.tree)
