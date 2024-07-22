class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def probs_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __eq__(self, other):
        if isinstance(other, LeafNode):
            return (self.tag == other.tag and
                    self.value == other.value and
                    self.props == other.props)
        return False
        
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, probs=None):
        super().__init__(tag, value,None, probs)    
        
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNodes need a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.probs_to_html()}>{self.value}</{self.tag}>"
    
    

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        test_string = ""
        if self.tag == None:
            raise ValueError("No tag was given")
        if self.children == None:
            raise ValueError("No children was given")
        for children in self.children:
            if children == LeafNode:
                if children.tag != None:
                    test_string += f"<{children.tag}>{children.value}</{children.tag}>"
                else:
                    test_string += f"{children.value}"
            else:
                test_string += children.to_html()
        return f"<{self.tag}>{test_string}</{self.tag}>"
    
