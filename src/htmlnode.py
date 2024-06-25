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
        SELF_CLOSING_TAGS = [
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "keygen",
            "link",
        ]
        MAX_LENGTH = 80  # maximum length of an element if displayed on one line

        def disp_node(node, level=1):
            lines = []

            if isinstance(node, HTMLNode):
                # get (tag, value, props) of current node
                root_node_info = get_node_info(node)
                props = node.props_to_html() if node else ""

                tag = root_node_info[0]
                if tag in SELF_CLOSING_TAGS:
                    opening_tag = pad_str(f"<{tag}{props}/>", level - 1)
                elif tag:  # tag is not empty nor None
                    opening_tag = pad_str(f"<{root_node_info[0]}{props}>", level - 1)
                else:  # tag is '' or None
                    opening_tag = ""

                value = root_node_info[1]
                if value:  # value != ''
                    if tag:  # tag != ''
                        value = pad_str(value, level)
                    else:  # tag is falsy ('' or None. '' in this case, since tag is a string)
                        value = pad_str(value, level - 1)

                if isinstance(node.children, list) and node.children:
                    if tag in SELF_CLOSING_TAGS:
                        raise Exception(f"<{tag}> tag cannot have children")
                    if opening_tag:  # opening_tag != ''
                        closing_tag = pad_str(f"</{root_node_info[0]}>", level - 1)
                        if len(opening_tag) + len(value.strip()) <= MAX_LENGTH - 7:
                            lines.append(f"{opening_tag}{value.strip()}")
                        else:
                            lines.append(opening_tag)
                            lines.append(value)
                    else:  # opening_tag == ''
                        lines.append(value)

                    for node_child_el in node.children:
                        # recursively extend the lines array with each child nested inside (hence: level+1)
                        lines.extend(disp_node(node_child_el, level + 1))

                    closing_tag = pad_str(f"</{root_node_info[0]}>", level - 1)
                    lines.append(closing_tag)
                else:  # node does not have any children (node.children == [] or None)
                    if opening_tag:  # opening_tag != ''
                        if tag not in SELF_CLOSING_TAGS:
                            closing_tag = pad_str(f"</{root_node_info[0]}>", level - 1)
                            if (
                                len(opening_tag)
                                + len(value.strip())
                                + len(closing_tag.strip())
                                <= MAX_LENGTH
                            ):
                                lines.append(
                                    f"{opening_tag}{value.strip()}{closing_tag.strip()}"
                                )  # all on one line
                            else:
                                # put opening_tag, value and closing_tag each on its line
                                lines.append(opening_tag)
                                lines.append(value)
                                lines.append(closing_tag)
                    else:  # opening_tag == ''
                        # there are no opening nor closing tags. just add a line with value.
                        lines.append(value)

            else:  # if the node is not an HTMLNode
                raise Exception("The argument of disp_node MUST be of type 'HTMLNode'")

            return lines

        return "\n".join(disp_node(self, level=1))


def get_node_info(html_node):
    if isinstance(html_node, HTMLNode):
        tag = f"{html_node.tag}" if html_node.tag else ""
        value = f"{html_node.value}" if html_node.value else ""
        props = f"{html_node.props}" if html_node.props else ""

        return tag, value, props
    raise Exception("get_node_info argument must be of type HTMLNode")


def pad_str(str, level=1):
    leading_spaces = " " * 2 * level
    return leading_spaces + str
