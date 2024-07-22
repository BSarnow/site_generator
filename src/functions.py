from textnode import TextNode,text_type_bold, text_type_text,text_type_code, text_type_image, text_type_italic,text_type_link
from htmlnode import LeafNode, ParentNode
import re
# structur of a textNode:
# def __init__(self,Text,Text_type,url=None):
#        self.text = Text
#        self.text_type = Text_type
#        self.url = url

# structur of a LeafNode:
# def __init__(self, tag=None, value=None, probs=None):
#        super().__init__(tag, value,None, probs)   


def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b",text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i",text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code",text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a",text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img","",{"src" : text_node.url, "alt" : text_node.text})
    else:
        raise Exception("text_type is not supported")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            phrases = node.text.split(delimiter)
            if len(phrases) % 2 == 0:
                raise Exception("Invalid Markdowns")
            for i in range(len(phrases)):
                if phrases[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(phrases[i], text_type_text))
                else:
                    new_nodes.append(TextNode(phrases[i], text_type))

    return new_nodes
    
def extract_markdown_images(text):
    found_images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    if len(found_images) != 0:
        return found_images
    else:
        raise Exception("No images found")
    
def extract_markdown_links(text):
    new_text = text
    found_images = re.findall(r"!\[(.*?)\]\((.*?)\)", new_text)
    found_links = re.findall(r"\[(.*?)\]\((.*?)\)", new_text)
    for i in found_images:
        if i in found_links:
            found_links.remove(i)
    if len(found_links) != 0:
        return found_links
    else:
        raise Exception("No links found")
    
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        searching_text = node.text
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            while_loop_one= 0
            while while_loop_one == 0:
                found_image = re.findall(r"!\[(.*?)\]\((.*?)\)", searching_text)
                if len(found_image) != 0:
                    splitted_node = searching_text.split(f"![{found_image[0][0]}]({found_image[0][1]})")
                    if splitted_node[0] == "":
                        new_nodes.append(TextNode(found_image[0][0], text_type_image, found_image[0][1]))
                        searching_text = splitted_node[1]
                    else:
                        new_nodes.append(TextNode(splitted_node[0], text_type_text))
                        searching_text = splitted_node[1]
                        new_nodes.append(TextNode(found_image[0][0], text_type_image, found_image[0][1]))      
                else:
                    while_loop_one = 1
                    if searching_text != "":
                        new_nodes.append(TextNode(searching_text, text_type_text))                
    return new_nodes
        


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        searching_text = node.text
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            while_loop_one= 0
            while while_loop_one == 0:
                found_image = re.findall(r"!\[(.*?)\]\((.*?)\)", searching_text)
                found_links = re.findall(r"\[(.*?)\]\((.*?)\)", searching_text)
                for i in found_image:
                    if i in found_links:
                        found_links.remove(i)
                if len(found_links) != 0:
                    splitted_node = searching_text.split(f"[{found_links[0][0]}]({found_links[0][1]})")
                    if splitted_node[0] == "":
                        new_nodes.append(TextNode(found_links[0][0], text_type_link, found_links[0][1]))
                        searching_text = splitted_node[1]
                    else:
                        new_nodes.append(TextNode(splitted_node[0], text_type_text))
                        searching_text = splitted_node[1]
                        new_nodes.append(TextNode(found_links[0][0], text_type_link, found_links[0][1]))      
                else:
                    while_loop_one = 1
                    if searching_text != "":
                        new_nodes.append(TextNode(searching_text, text_type_text))                
    return new_nodes

def Text_to_textnodes(text):
    text_to_simplenode = [TextNode(text, text_type_text)]
    nodes_format_bold = split_nodes_delimiter(text_to_simplenode, "**", text_type_bold)
    nodes_format_italic = split_nodes_delimiter(nodes_format_bold, "*", text_type_italic)
    nodes_format_code = split_nodes_delimiter(nodes_format_italic, "`", text_type_code)
    nodes_format_image = split_nodes_image(nodes_format_code)
    nodes_format_link = split_nodes_links(nodes_format_image)
    return nodes_format_link

def markdown_to_block(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_blocktyp(block):
    splitted_block = block.split()
    splitted_line = block.split("\n")
    for line in splitted_line:
        if line == "":
            splitted_line.remove(line)
    if splitted_block[0] in ["#","##", "###", "####", "#####", "######"]:
        return "headline"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(line.startswith("> ")for line in splitted_line):
        return "quote"
    elif all(line.startswith("* ") or line.startswith("- ") for line in splitted_line):
        return "unorderd_list"
    elif all(splitted_line[i].startswith(f"{i+1}. ") for i in range(len(splitted_line))):
        return "orderd_list"
    else:
        return "paragraph"
    
def typ_to_tags(block,typ):
    if typ == "headline":
        splitted_block = block.split()
        return f"h{len(splitted_block[0])}"
    if typ == "code":
        return "pre","code"
    if typ == "quote":
        return "blockquote"
    if typ == "unorderd_list":
        return "ul", "li"
    if typ == "orderd_list":
        return "ol", "li"
    if typ == "paragraph":
        return "p"
    
def markdown_to_htmlNode(markdown):
    blocks = markdown_to_block(markdown)
    markdown_html_nodes = []
    for block in blocks:
        if block == "":
            blocks.remove(block)
        else:
            block_typ = block_to_blocktyp(block)
            tags = typ_to_tags(block, block_typ)
            if tags in ["h1","h2","h3","h4","h5","h6"]:
                striped_block = block.strip("#")
                blocked_textnode = Text_to_textnodes(striped_block)
                list_of_htmlnode = []
                for textnode in blocked_textnode:
                    list_of_htmlnode.append(text_node_to_html_node(textnode))
                HeadlineNode = ParentNode(tags,list_of_htmlnode)
                markdown_html_nodes.append(HeadlineNode) 
            if tags == "p":
                blocked_textnode = Text_to_textnodes(block)
                list_of_htmlnode = []
                for textnode in blocked_textnode:
                    list_of_htmlnode.append(text_node_to_html_node(textnode))
                paragraph_node = ParentNode(tags,list_of_htmlnode)
                markdown_html_nodes.append(paragraph_node)
            if tags == ("ul","li"):
                splitted_block = block.split("\n")
                list_of_textnodes = []
                for line in splitted_block:
                    children_of_listitem= []
                    text_listitem = str(line[1:])
                    list_symbol = TextNode(line[0],text_type_text)
                    children_of_listitem.append(text_node_to_html_node(list_symbol))
                    blocked_textnode = Text_to_textnodes(text_listitem)
                    for textnode in blocked_textnode:
                        children_of_listitem.append(text_node_to_html_node(textnode))
                    list_item = ParentNode(tags[1],children_of_listitem)
                    list_of_textnodes.append(list_item)
                unorderd_list_Node = ParentNode(tags[0],list_of_textnodes)
                markdown_html_nodes.append(unorderd_list_Node)
            if tags == ("ol","li"):
                splitted_block = block.split("\n")
                list_of_html_nodes = []
                for line in splitted_block:
                    textnodes = Text_to_textnodes(line)
                    children_of_listitem = []
                    for textnode in textnodes:
                        children_of_listitem.append(text_node_to_html_node(textnode))
                    list_item = ParentNode(tags[1],children_of_listitem)
                    list_of_html_nodes.append(list_item)
                orderd_list_node = ParentNode(tags[0],list_of_html_nodes)
                markdown_html_nodes.append(orderd_list_node)
            if tags == ("pre","code"):
                textnode_code = Text_to_textnodes(block)
                children_of_code_block = []
                for node in textnode_code:
                    children_of_code_block.append(text_node_to_html_node(node))
                code_block_node = ParentNode(tags[0],children_of_code_block)
                markdown_html_nodes.append(code_block_node)
            if tags == ("blockquote"):
                splitted_block = block.split("\n")
                children_of_the_quote = []
                for line in splitted_block:
                    textnodes = Text_to_textnodes(line)
                    for textnode in textnodes:
                        children_of_the_quote.append(text_node_to_html_node(textnode))
                Quote_node = ParentNode(tags,children_of_the_quote)
                markdown_html_nodes.append(Quote_node)
    final_node = ParentNode("div",markdown_html_nodes)
    return final_node
    
