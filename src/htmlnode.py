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
        if self.props:
            for k, v in self.props.items():
                stripped_k = k.strip('"')
                res = res + " " + f'{stripped_k}="{v}"'
        return res

    def __repr__(self):
        SELF_CLOSING_TAGS = ["img", "input"]

        def disp_node(node, level=1):
            lines = []

            if isinstance(node, HTMLNode):
                root_node_info = get_node_info(node)
                props = node.props_to_html() if node else ""

                tag = root_node_info[0]
                if tag in SELF_CLOSING_TAGS:
                    opening_tag = pad_str(f"<{tag}{props}/>", level - 1)
                else:
                    opening_tag = pad_str(f"<{root_node_info[0]}{props}>", level - 1)
                lines.append(opening_tag)

                value = root_node_info[1]
                if value:
                    value = pad_str(value, level)
                    lines.append(value)

                if isinstance(node.children, list):
                    for node_child_el in node.children:
                        lines.extend(disp_node(node_child_el, level + 1))
                elif node.children is None:
                    pass

                if tag not in SELF_CLOSING_TAGS:
                    closing_tag = pad_str(f"</{root_node_info[0]}>", level - 1)
                    lines.append(closing_tag)

            # if the node is not an HTMLNode
            else:
                raise Exception("The argument of disp_node MUST be of type 'HTMLNode'")

            return lines

        return "\n".join(disp_node(self, level=1))


def get_node_info(html_node):
    if isinstance(html_node, HTMLNode):
        tag = f"{html_node.tag}"
        value = f"{html_node.value}" if html_node.value else ""
        props = f"{html_node.props}" if html_node.props else ""

        return tag, value, props
    raise Exception("get_node_info argument must be of type HTMLNode")


def pad_str(str, level=1):
    leading_spaces = " " * 2 * level
    return leading_spaces + str
