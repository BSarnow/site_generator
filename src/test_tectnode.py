import unittest

from textnode import TextNode, text_type_bold, text_type_code, text_type_image, text_type_italic, text_type_link, text_type_text
from functions import text_node_to_html_node, split_nodes_delimiter
from htmlnode import HTMLNode, LeafNode
# To do
# text_type_text = "text"
# text_type_bold = "bold"
# text_type_italic = "italic"
# text_type_code = "code"
# text_type_link = "link"
# text_type_image = "image"
# none of them

text_type_false = "It is a fake type for the tests"

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_to_html(self):
        node_text = TextNode("Only Text", text_type_text)
        excepted_output = LeafNode(None,"Only Text")
        self.assertEqual(text_node_to_html_node(node_text), excepted_output)

    def test_bold_to_html(self):
        node_bold = TextNode("bold Text", text_type_bold)
        excepted_output = LeafNode("b","bold Text")
        self.assertEqual(text_node_to_html_node(node_bold), excepted_output)

    def test_italic_to_html(self):
        node_italic = TextNode("italic Text", text_type_italic)
        excepted_output = LeafNode("i","italic Text")
        self.assertEqual(text_node_to_html_node(node_italic), excepted_output)
    
    def test_code_to_html(self):
        node_code = TextNode("code Text", text_type_code)
        excepted_output = LeafNode("code","code Text")
        self.assertEqual(text_node_to_html_node(node_code), excepted_output)

    def test_link_to_html(self):
        node_link = TextNode("click here!", text_type_link, "www.google.de")
        excepted_output = LeafNode("a", "click here!", {"href": "www.google.de"})
        self.assertEqual(text_node_to_html_node(node_link), excepted_output)

    def test_image_to_html(self):
        node_image = TextNode("This is a picture",text_type_image, "fake-link for a picture")
        excepted_output = LeafNode("img","", {"src": "fake-link for a picture", "alt": "This is a picture"})
        self.assertEqual(text_node_to_html_node(node_image), excepted_output)

    def test_fake_to_html(self):
        with self.assertRaises(Exception) as context:
            node_fake = TextNode("Its fake", text_type_false)
            text_node_to_html_node(node_fake)
        self.assertTrue("text_type is not supported" in str(context.exception))

class Test_split_by_delimiter(unittest.TestCase):
    def test_bolt_markdowns(self):
        node_one = TextNode("The **middle** of this sentence should be bold", text_type_text)
        node_two = TextNode("This node should be unchanged", text_type_italic)
        node_three = TextNode("**Beginning** and the **end**", text_type_text)
        excepted_output = [TextNode("The ", text_type_text), TextNode("middle", text_type_bold), TextNode(" of this sentence should be bold", text_type_text), TextNode("This node should be unchanged", text_type_italic), TextNode("Beginning", text_type_bold), TextNode(" and the ", text_type_text), TextNode("end", text_type_bold)]
        self.assertEqual(split_nodes_delimiter([node_one, node_two, node_three], "**", text_type_bold), excepted_output)

    def test_invalid_markdown_test(self):
        with self.assertRaises(Exception) as context:
            node_one = TextNode("This Text has invalid **Markdowns", text_type_text)
            split_nodes_delimiter([node_one], "**", text_type_bold)
        self.assertTrue("Invalid Markdowns" in str(context.exception))
        

if __name__ == "__main__":
    unittest.main()
