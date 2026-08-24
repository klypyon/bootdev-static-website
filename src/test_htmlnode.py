import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "my-class"})

    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "my-class", "id": "my-id"})
        expected_props_html = ' class="my-class" id="my-id"'
        self.assertEqual(node.props_to_html(), expected_props_html)

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), '')