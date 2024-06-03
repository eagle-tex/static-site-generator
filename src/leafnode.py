from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes require a value")
        if self.tag is None:
            return self.value

        props_value = self.props_to_html()
        # print(f"props = {props_value}")
        str = f"<{self.tag}{props_value}>{self.value}</{self.tag}>"
        return str
