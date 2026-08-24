import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_initialization(self):
        node = LeafNode(tag="div", value="Hello", props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, {"class": "my-class"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_props_to_html(self):
        node = LeafNode(tag="div", value="Hello", props={"class": "my-class", "id": "my-id"})
        expected_props_html = ' class="my-class" id="my-id"'
        self.assertEqual(node.props_to_html(), expected_props_html)

    def test_props_to_html_no_props(self):
        node = LeafNode(tag="div", value="Hello")
        self.assertEqual(node.props_to_html(), '')