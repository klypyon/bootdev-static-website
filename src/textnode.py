from enum import Enum
from leafnode import LeafNode
import typing

class TextType(Enum):
    TEXT = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    """
    A class representing a text node in a static website.

    Attributes:
        text (str): The text content of the node.
        text_type (TextType): The type of the text (e.g., plain, bold, italic, code, link, image).
        url (str): The URL associated with the text node, if applicable (for links and images).
    """
    def __init__(self, text: str, text_type : TextType, url : typing.Optional[str] = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        return False

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type.value!r}, {self.url!r})"


def text_node_to_html_node(text_node: TextNode) -> 'LeafNode':
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
    raise ValueError(f"text_node is not a valid type: {text_node.text_type}")