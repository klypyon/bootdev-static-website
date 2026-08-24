from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be None for ParentNode.")

        if self.children is None:
            raise ValueError("Children cannot be None for ParentNode.")

        children_html = ''.join(child.to_html() for child in self.children) if self.children else ''
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})"