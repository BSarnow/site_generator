import unittest

from htmlnode import HTMLNode

class Test_HTML(unittest.TestCase):
    def test_probs_to_html(self):
        node = HTMLNode("The real Node", "Maybe we should write something", None, {"href": "https://www.google.com", "target": "_blank"})
        exepted_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.probs_to_html(),exepted_output)

    def test_probs_to_html2(self):
        node = HTMLNode("The real Node", "Maybe we should write something", None, {"href": "https://www.google.com", "target": "_blank"})
        exepted_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.probs_to_html(),exepted_output)
    
from htmlnode import LeafNode

class Test_LeafNode(unittest.TestCase):
    def test_no_value(self):
        with self.assertRaises(ValueError) as context:
            node = LeafNode("p", None)
            node.to_html()
        self.assertTrue("LeafNodes need a value" in str(context.exception))

    def test_only_value(self):
        node = LeafNode(None, "Some Text!")
        excepted_output = "Some Text!"
        self.assertEqual(node.to_html(), excepted_output)

    def test_html_p(self):
        node = LeafNode("p","Some Text!")
        excepted_output = "<p>Some Text!</p>"
        self.assertEqual(node.to_html(), excepted_output)

    def test_html_a(self):
        node = LeafNode("a", "Click here!",{"herf": "www.google.com"})
        exepted_output = '<a herf="www.google.com">Click here!</a>'
        self.assertEqual(node.to_html(), exepted_output)

from htmlnode import ParentNode

class Test_Parentnode(unittest.TestCase):
    def test_no_children(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode("p", None)
            node.to_html()
        self.assertTrue("No children was given" in str(context.exception))

    def test_no_tag(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, [LeafNode(None,"Test 1"), LeafNode("b", "Test 2"), ParentNode("a", [LeafNode("N", "Test Parentnode")])])
            node.to_html()
        self.assertTrue("No tag was given" in str(context.exception))

    def test_children_in_children(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode("p", [LeafNode(None,"Test 1"), LeafNode("b", "Test 2"), ParentNode("a", None)])
            node.to_html()
        self.assertTrue("No children was given" in str(context.exception))

    def test_right_output(self):
        node = ParentNode("p",[LeafNode(None,"Test 1"), LeafNode("b", "Test 2"), ParentNode("a", [LeafNode("N", "Test Parentnode")])])
        excepted_output = "<p>Test 1<b>Test 2</b><a><N>Test Parentnode</N></a></p>"
        self.assertEqual(node.to_html(), excepted_output)

if __name__=="__main__":
    unittest.main()