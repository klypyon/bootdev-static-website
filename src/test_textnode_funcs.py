from unittest import TestCase

from textnode_funcs import (
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image, 
    split_nodes_link,
    text_to_textnodes
)
from textnode import TextNode, TextType

class TestTextNodeFuncs(TestCase):
    def test_split_nodes_bold_delimiter(self):
        old_nodes = [
            TextNode("Here is some **bold** text.", TextType.TEXT)
        ]
        delimiter = "**"
        text_type = TextType.BOLD
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Here is some ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT) 

    def test_split_nodes_italic_delimiter(self):
        old_nodes = [
            TextNode("Here is some *italic* text.", TextType.TEXT)
        ]
        delimiter = "*"
        text_type = TextType.ITALIC
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Here is some ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_code_delimiter(self):
        old_nodes = [
            TextNode("Here is some `code` text.", TextType.TEXT)
        ]
        delimiter = "`"
        text_type = TextType.CODE
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Here is some ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_extract_markdown_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(text)
        self.assertListEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_split_nodes_link(self):
        old_nodes = [
            TextNode("This is a [link](https://example.com) in the text.", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")
        self.assertEqual(new_nodes[2].text, " in the text.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_link_multiple_occurrences(self):
        old_nodes = [
            TextNode("This is a [link1](https://example.com/1) and another [link2](https://example.com/2).", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link1")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com/1")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "link2")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].url, "https://example.com/2")
        self.assertEqual(new_nodes[4].text, ".")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_split_nodes_image(self):
        old_nodes = [
            TextNode("This is an image ![alt text](https://example.com/image.png) in the text.", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is an image ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "alt text")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/image.png")
        self.assertEqual(new_nodes[2].text, " in the text.")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_image_multiple_occurrences(self):
        old_nodes = [
            TextNode("This is an image ![alt1](https://example.com/image1.png) and another ![alt2](https://example.com/image2.png).", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is an image ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "alt1")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/image1.png")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "alt2")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].url, "https://example.com/image2.png")
        self.assertEqual(new_nodes[4].text, ".")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_multiple_occurrences(self):
        old_nodes = [
            TextNode("This is a **test**, and this is another **test**.", TextType.TEXT)
        ]
        delimiter = "**"
        text_type = TextType.BOLD
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "test")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, ", and this is another ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "test")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, ".")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_empty_string(self):
        old_nodes = [
            TextNode("This is a test.", TextType.TEXT)
        ]
        delimiter = ""
        text_type = TextType.BOLD

        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_split_nodes_missing_end_delimiter(self):
        old_nodes = [
            TextNode("This is a **test with a missing delimiter.", TextType.TEXT)
        ]
        delimiter = "**"
        text_type = TextType.BOLD

        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_text_node_to_text_nodes(self):
        text_node = TextNode("This is a **bold**, `code`, and *italic* text with a [link](https://example.com) and an ![image](https://example.com/image.png).", TextType.TEXT)
        text_nodes = text_to_textnodes(text_node.text)

        self.assertEqual(len(text_nodes), 11)

        self.assertListEqual(
            [(node.text, node.text_type, node.url) for node in text_nodes],
            [
                ("This is a ", TextType.TEXT, None),
                ("bold", TextType.BOLD, None),
                (", ", TextType.TEXT, None),
                ("code", TextType.CODE, None),
                (", and ", TextType.TEXT, None),
                ("italic", TextType.ITALIC, None),
                (" text with a ", TextType.TEXT, None),
                ("link", TextType.LINK, "https://example.com"),
                (" and an ", TextType.TEXT, None),
                ("image", TextType.IMAGE, "https://example.com/image.png"),
                (".", TextType.TEXT, None)
            ]
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_lines(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])    

    def test_markdown_to_blocks_with_empty_lines(self):
        md = """
This is a paragraph with empty lines above and below.

Another paragraph follows.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with empty lines above and below.",
                "Another paragraph follows.",
            ],
        )   

    def test_markdown_to_blocks_with_only_empty_lines(self):
        md = """

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])    

class TestMarkdownToHTML(TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
        )

    def test_blockquote(self):
        md = """
> This is a blockquote with **bold** text and `code`.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with <b>bold</b> text and <code>code</code>.</blockquote></div>"
        )

    def test_multi_blockquote(self):
        md = """
> This is a blockquote with **bold** text and `code`.

> This is another blockquote with *italic* text.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with <b>bold</b> text and <code>code</code>.</blockquote><blockquote>This is another blockquote with <i>italic</i> text.</blockquote></div>"
        )

    def test_heading(self):
        md = """
# This is a heading with **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading with <b>bold</b> text</h1></div>"
        )

    def test_multi_heading(self):
        md = """
## This is a heading with **bold** text

### This is another heading with *italic* text

#### This is a third heading with `code` text

##### This is a fourth heading with a [link](https://example.com)

###### This is a fifth heading with an ![image](https://example.com/image.png)

####### This should not be a heading, but a paragraph with **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a heading with <b>bold</b> text</h2><h3>This is another heading with <i>italic</i> text</h3><h4>This is a third heading with <code>code</code> text</h4><h5>This is a fourth heading with a <a href=\"https://example.com\">link</a></h5><h6>This is a fifth heading with an <img src=\"https://example.com/image.png\" alt=\"image\"></img></h6><p>####### This should not be a heading, but a paragraph with <b>bold</b> text</p></div>"
        )

    def test_multi_block_types(self):
        md = """
# Heading 1

```
> Blockquote with **bold** text
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><pre><code>> Blockquote with **bold** text</code></pre></div>"
        )

    def test_multi_block_types_with_paragraphs(self):
        md = """
# Heading 1

```
> Blockquote with **bold** text
```

This is a paragraph with *italic* text.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><pre><code>> Blockquote with **bold** text</code></pre><p>This is a paragraph with <i>italic</i> text.</p></div>"
        )