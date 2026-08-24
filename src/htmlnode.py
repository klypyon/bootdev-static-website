import typing

class HTMLNode:
    def __init__(
            self, 
            tag : typing.Optional[str] = None, 
            value : typing.Optional[str] = None, 
            children: typing.Optional[typing.List['HTMLNode']] = None, 
            props: typing.Optional[typing.Dict[str, str]] = None
        ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def props_to_html(self):
        if self.props:
            return ' ' + ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        return ''

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"