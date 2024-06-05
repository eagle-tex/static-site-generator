class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        res = ""
        if self.props is not None:
            for k, v in self.props.items():
                stripped_k = k.strip('"')
                res = res + " " + f'{stripped_k}="{v}"'
        return res

    def __repr__(self):

        def disp_node(node, level=1):
            lines = []

            if isinstance(node, HTMLNode):
                root_node_info = get_node_info(node)
                r0 = pad_str(root_node_info[0], level - 1)
                r1 = pad_str(root_node_info[1], level - 1)
                r2 = pad_str(root_node_info[2], level - 1)
                r3 = pad_str(root_node_info[3], level - 1)
                lines.append(r0)
                lines.append(r1)
                lines.append(r2)
                lines.append(r3)

                if isinstance(node.children, list):
                    for index, node_child_el in enumerate(node.children):
                        lines.append(pad_str(f"Child #{index+1}", level - 1))
                        lines.extend(disp_node(node_child_el, level + 1))

                elif node.children is None:
                    children_msg = f"Children: {node.children}"
                    rc = pad_str(children_msg, level - 1)
                    lines.append(rc)

                r4 = pad_str(root_node_info[4], level - 1)
                r5 = pad_str(root_node_info[0], level - 1)
                lines.append(r4)
                lines.append(r5)

            # if the node is not an instance of HTMLNode
            else:
                raise Exception("The argument of disp_node MUST be of type 'HTMLNode'")

            return lines

        return "\n".join(disp_node(self, level=1))


def get_node_info(html_node):
    if isinstance(html_node, HTMLNode):
        delimiter = "--------------------"
        title = "HTMLNode"
        tag_msg = f"Tag: {html_node.tag}"
        value_msg = f"Value: {html_node.value}"
        props_msg = f"Props: {html_node.props}"
        return delimiter, title, tag_msg, value_msg, props_msg
    raise Exception("get_node_info argument must be of type HTMLNode")


def pad_str(str, level=1):
    leading_spaces = " " * 4 * level
    return leading_spaces + str
