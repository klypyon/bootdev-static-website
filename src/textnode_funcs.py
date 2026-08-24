from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
import typing
import re

IMAGE_PATTERN = r"!\[([^\]]+)\]\(([^)]+)\)"
LINK_PATTERN = r"(?<!!)\[([^\]]+)\]\(([^)]+)\)"

def split_nodes_delimiter(old_nodes: typing.List[TextNode], delimiter: str, text_type: TextType) -> typing.List[TextNode]:
    new_nodes : typing.List[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Node text has an even number of delimiters '{delimiter}': {node.text}")

        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text: str) -> typing.List[typing.Tuple[str, str]]:
    """
    Takes raw markdown text and returns a list of tuples. Each tuple should 
    contain the alt text and the URL of any markdown images.

    For example:
        ```
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        print(extract_markdown_images(text))
        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        ```
    """
    matches = re.findall(IMAGE_PATTERN, text)
    return [(alt_text, url) for alt_text, url in matches]

def split_nodes_image(old_nodes: typing.List[TextNode]) -> typing.List[TextNode]:
    new_nodes : typing.List[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)

        if not matches:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for alt_text, image_link in matches:
            if not alt_text or not image_link:
                raise ValueError(f"Node text contains an invalid image pattern: {node.text}")

            markdown_image = f"![{alt_text}]({image_link})"

            before, after = remaining_text.split(markdown_image, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_link))

            remaining_text = after

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def extract_markdown_links(text: str) -> typing.List[typing.Tuple[str, str]]:
    """
    Takes raw markdown text and returns a list of tuples. Each tuple should 
    contain the anchor text and the URL of any markdown links.

    For example:
        ```
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        print(extract_markdown_links(text))
        # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        ```
    """
    matches = re.findall(LINK_PATTERN, text)
    return [(anchor_text, url) for anchor_text, url in matches]

def split_nodes_link(old_nodes: typing.List[TextNode]) -> typing.List[TextNode]:
    new_nodes : typing.List[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)

        if not matches:
            new_nodes.append(node)
            continue

        remaining_text = node.text

        for anchor_text, url in matches:
            if not anchor_text or not url:
                raise ValueError(f"Node text contains an invalid link pattern: {node.text}")

            markdown_link = f"[{anchor_text}]({url})"

            before, after = remaining_text.split(markdown_link, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            remaining_text = after

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text) -> typing.List[TextNode]:
    """
    Takes raw text and returns a list of TextNode objects, splitting the text into 
    different types based on markdown syntax for bold, italic, code, images, and links.

    For example:
        ```
        text = "This is **bold** text and *italic* text with `code`."
        print(text_to_textnodes(text))
        # [TextNode("This is ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text and ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" text with ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(".", TextType.TEXT)]
        ```
    """
    nodes = [TextNode(text, TextType.TEXT)]

    # Split by bold (**)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Split by italic (*)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    # Split by italic (_)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Split by code (`)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Split by images
    nodes = split_nodes_image(nodes)

    # Split by links
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown: str) -> typing.List[str]:
    return [line.strip() for line in markdown.split("\n\n") if line.strip() != ""]

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        print(f"Processing block: {block!r} as {block_type}", flush=True)

        if block_type == BlockType.PARAGRAPH:
            text_nodes = text_to_textnodes(block.replace("\n", " "))
            html_children = [text_node_to_html_node(node) for node in text_nodes]
            html_nodes.append(ParentNode("p", html_children))

        elif block_type == BlockType.HEADING:
            heading_level = len(re.match(r"^(#+)", block).group(1))
            heading_text = block[heading_level:].strip()
            text_nodes = text_to_textnodes(heading_text)
            html_children = [text_node_to_html_node(node) for node in text_nodes]
            html_nodes.append(ParentNode(f"h{heading_level}", html_children))

        elif block_type == BlockType.CODE:
            code_content = re.search(
                r"```(\n)(.*?)```", 
                block, 
                re.DOTALL
            ).group(2).rstrip("\n")
            html_nodes.append(ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)])]))

        elif block_type == BlockType.QUOTE:
            quote_lines = [line[1:].strip() for line in block.split("\n")]
            quote_text = "\n".join(quote_lines)
            text_nodes = text_to_textnodes(quote_text)
            html_children = [text_node_to_html_node(node) for node in text_nodes]
            html_nodes.append(ParentNode("blockquote", html_children))

        elif block_type == BlockType.UNORDERED_LIST:
            list_items = [line[1:].strip() for line in block.split("\n")]
            list_item_nodes = []
            for item in list_items:
                text_nodes = text_to_textnodes(item)
                html_children = [text_node_to_html_node(node) for node in text_nodes]
                list_item_nodes.append(ParentNode("li", html_children))
            html_nodes.append(ParentNode("ul", list_item_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            list_items = [line.split(". ", 1)[1].strip() for line in block.split("\n")]
            list_item_nodes = []
            for item in list_items:
                text_nodes = text_to_textnodes(item)
                html_children = [text_node_to_html_node(node) for node in text_nodes]
                list_item_nodes.append(ParentNode("li", html_children))
            html_nodes.append(ParentNode("ol", list_item_nodes))

    return ParentNode("div", html_nodes)