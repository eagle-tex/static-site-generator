from typing import List
from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: List[HTMLNode], props: dict[str, str] | None = None
    ):
        if not isinstance(children, list):
            raise ValueError("<children> argument must be an array")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("A tag is required for a ParentNode")
        if self.children is None:
            raise ValueError("At least one child is required for a ParentNode")

        props_value = self.props_to_html()
        html = f"<{self.tag}{props_value}>"

        for child in self.children:
            html += child.to_html()

        # def convert(node):
        #     children_str = ""
        #     if node.tag is not None:
        #         children_str += f"<{node.tag}>"
        #     for ch in node.children:
        #         if isinstance(ch, LeafNode):
        #             children_str += ch.to_html()
        #         elif isinstance(ch, ParentNode):
        #             children_str += convert(ch)
        #         elif isinstance(ch, HTMLNode):
        #             raise Exception("A node of type 'HTMLNode' is not allowed as child")
        #     if node.tag is not None:
        #         children_str += f"</{node.tag}>"
        #     return children_str
        #
        # html = convert(self)

        html += f"</{self.tag}>"
        return html
