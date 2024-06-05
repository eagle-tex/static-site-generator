from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None or self.value == "":
            raise ValueError("All leaf nodes require a value")
        if self.tag is None or self.tag == "":
            return self.value

        props_value = self.props_to_html()
        str = f"<{self.tag}{props_value}>{self.value}</{self.tag}>"
        return str
