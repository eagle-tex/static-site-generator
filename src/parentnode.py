from typing import List
from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: List[HTMLNode], props: dict[str, str] | None = None
    ):
        if not isinstance(children, list):
            raise ValueError("<children> argument must be an array")
        # if children is None, "" or not a list
        if not children or not isinstance(children, list):
            children = []  # set children to an empty list
        # then call the constructor of the parent class
        super().__init__(tag, None, children, props)

    def __str__(self) -> str:
        return super().__str__()

    def to_html(self):
        if not self.tag:
            raise ValueError("A tag is required for a ParentNode")
        if self.children is None:
            raise ValueError("At least one child is required for a ParentNode")

        props_value = self.props_to_html()
        html = f"<{self.tag}{props_value}>\n"

        for child in self.children:
            if isinstance(child, ParentNode) or isinstance(child, LeafNode):
                html += child.to_html() + "\n"
            elif isinstance(child, HTMLNode):
                print(
                    "inside ParentNode.to_html() and this is an HTMLNode. Watch it!!!"
                )
                raise TypeError(
                    f'Child node "<{child.tag}>" is of type HTMLNode, which is prohibited.\
                    Must be ParentNode or LeafNode'
                )

        html += f"</{self.tag}>"
        return html
