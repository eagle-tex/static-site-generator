from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == "" or self.tag is None:
            raise ValueError("A tag is required for a ParentNode")
        if self.children is None or (
            isinstance(self.children, list) and len(self.children) == 0
        ):
            raise ValueError("At least one child is required for a ParentNode")

        html = ""

        def convert(node):
            children_str = ""
            if node.tag is not None:
                children_str += f"<{node.tag}>"
            for ch in node.children:
                if isinstance(ch, LeafNode):
                    children_str += ch.to_html()
                elif isinstance(ch, ParentNode):
                    children_str += convert(ch)
                elif isinstance(ch, HTMLNode):
                    raise Exception("A node of type 'HTMLNode' is not allowed as child")
            if node.tag is not None:
                children_str += f"</{node.tag}>"
            return children_str

        html = convert(self)
        return html
