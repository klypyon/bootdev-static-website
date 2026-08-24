import unittest
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_initialization(self):
        child1 = ParentNode(tag="span", children=[], props={"class": "child1"})
        child2 = ParentNode(tag="span", children=[], props={"class": "child2"})
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "parent"})

        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child1, child2])
        self.assertEqual(parent.props, {"class": "parent"})

    def test_to_html(self):
        child1 = ParentNode(tag="span", children=[], props={"class": "child1"})
        child2 = ParentNode(tag="span", children=[], props={"class": "child2"})
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "parent"})

        expected_html = '<div class="parent"><span class="child1"></span><span class="child2"></span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_repr(self):
        child1 = ParentNode(tag="span", children=[], props={"class": "child1"})
        parent = ParentNode(tag="div", children=[child1], props={"class": "parent"})

        expected_repr = "ParentNode(tag='div', children=[ParentNode(tag='span', children=[], props={'class': 'child1'})], props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_to_html_no_children(self):
        parent = ParentNode(tag="div", children=[], props={"class": "parent"})
        expected_html = '<div class="parent"></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_none_children(self):
        parent = ParentNode(tag="div", children=None, props={"class": "parent"})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_none_tag(self):
        parent = ParentNode(tag=None, children=[], props={"class": "parent"})
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_repr_no_children(self):
        parent = ParentNode(tag="div", children=[], props={"class": "parent"})
        expected_repr = "ParentNode(tag='div', children=[], props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_none_children(self):
        parent = ParentNode(tag="div", children=None, props={"class": "parent"})
        expected_repr = "ParentNode(tag='div', children=None, props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_none_tag(self):
        parent = ParentNode(tag=None, children=[], props={"class": "parent"})
        expected_repr = "ParentNode(tag=None, children=[], props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_parent_with_parent(self):
        child1 = ParentNode(tag="span", children=[], props={"class": "child1"})
        child2 = ParentNode(tag="span", children=[], props={"class": "child2"})
        parent1 = ParentNode(tag="div", children=[child1, child2], props={"class": "parent1"})

        child3 = ParentNode(tag="p", children=[], props={"class": "child3"})
        parent2 = ParentNode(tag="section", children=[parent1, child3], props={"class": "parent2"})

        expected_html = '<section class="parent2"><div class="parent1"><span class="child1"></span><span class="child2"></span></div><p class="child3"></p></section>'
        self.assertEqual(parent2.to_html(), expected_html)

    def test_to_html_with_children(self):
        child1 = ParentNode(tag="span", children=[], props={"class": "child1"})
        child2 = ParentNode(tag="span", children=[], props={"class": "child2"})
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "parent"})

        expected_html = '<div class="parent"><span class="child1"></span><span class="child2"></span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_with_grandchildren(self):
        grandchild1 = ParentNode(tag="em", children=[], props={"class": "grandchild1"})
        grandchild2 = ParentNode(tag="strong", children=[], props={"class": "grandchild2"})
        child = ParentNode(tag="span", children=[grandchild1, grandchild2], props={"class": "child"})
        parent = ParentNode(tag="div", children=[child], props={"class": "parent"})

        expected_html = '<div class="parent"><span class="child"><em class="grandchild1"></em><strong class="grandchild2"></strong></span></div>'
        self.assertEqual(parent.to_html(), expected_html)   

    def test_repr_with_grandchildren(self):
        grandchild1 = ParentNode(tag="em", children=[], props={"class": "grandchild1"})
        grandchild2 = ParentNode(tag="strong", children=[], props={"class": "grandchild2"})
        child = ParentNode(tag="span", children=[grandchild1, grandchild2], props={"class": "child"})
        parent = ParentNode(tag="div", children=[child], props={"class": "parent"})

        expected_repr = "ParentNode(tag='div', children=[ParentNode(tag='span', children=[ParentNode(tag='em', children=[], props={'class': 'grandchild1'}), ParentNode(tag='strong', children=[], props={'class': 'grandchild2'})], props={'class': 'child'})], props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_with_multiple_children(self):
        child1 = ParentNode(tag="span", children=[], props={"class": "child1"})
        child2 = ParentNode(tag="span", children=[], props={"class": "child2"})
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "parent"})

        expected_repr = "ParentNode(tag='div', children=[ParentNode(tag='span', children=[], props={'class': 'child1'}), ParentNode(tag='span', children=[], props={'class': 'child2'})], props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_with_no_children(self):
        parent = ParentNode(tag="div", children=[], props={"class": "parent"})

        expected_repr = "ParentNode(tag='div', children=[], props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_with_none_children(self):
        parent = ParentNode(tag="div", children=None, props={"class": "parent"})

        expected_repr = "ParentNode(tag='div', children=None, props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_with_none_tag(self):
        parent = ParentNode(tag=None, children=[], props={"class": "parent"})

        expected_repr = "ParentNode(tag=None, children=[], props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_with_none_props(self):
        parent = ParentNode(tag="div", children=[], props=None)

        expected_repr = "ParentNode(tag='div', children=[], props=None)"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_with_none_tag_and_props(self):
        parent = ParentNode(tag=None, children=[], props=None)

        expected_repr = "ParentNode(tag=None, children=[], props=None)"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_with_none_children_and_props(self):
        parent = ParentNode(tag="div", children=None, props=None)

        expected_repr = "ParentNode(tag='div', children=None, props=None)"
        self.assertEqual(repr(parent), expected_repr)

    def test_repr_with_none_tag_and_children(self):
        parent = ParentNode(tag=None, children=None, props={"class": "parent"})

        expected_repr = "ParentNode(tag=None, children=None, props={'class': 'parent'})"
        self.assertEqual(repr(parent), expected_repr)