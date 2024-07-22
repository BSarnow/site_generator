import unittest
from functions import extract_markdown_links, extract_markdown_images, split_nodes_links, split_nodes_image, Text_to_textnodes, block_to_blocktyp, markdown_to_htmlNode
from textnode import TextNode, text_type_bold, text_type_code, text_type_image, text_type_italic, text_type_link, text_type_text

class Test_for_extraction(unittest.TestCase):
    def test_extract_markdown_links(self):
        print("test_extract_markdown_link")
        test_text = "Links sind die mit den [eckigen Klammern](Ohne !)"
        excepted_output = [("eckigen Klammern", "Ohne !")]
        self.assertEqual(extract_markdown_links(test_text), excepted_output)

    def test_extract_markdown_images(self):
        print("test_extract_markdown_images")
        test_text = "Images sind die mit den ![eckigen Klammern](und einem !)"
        excepted_output = [("eckigen Klammern", "und einem !")]
        self.assertEqual(extract_markdown_images(test_text), excepted_output)

    def test_raises_from_extract(self):
        print("test_raises_from_extract")
        with self.assertRaises(Exception) as context:
            test_text = "Das wird nun ein Text ohne Links und Images"
            extract_markdown_images(test_text)
        self.assertTrue("No images found" in str(context.exception))

    def test_with_many_links(self):
        print("test_with_many_links")
        test_text = "Nun [1. Klammer](2.Klammer) es spannend. wir haben [3.Klammer](4.Klammer) 2 links in diesem Text"
        excepted_output = [("1. Klammer", "2.Klammer"), ("3.Klammer", "4.Klammer")]
        self.assertEqual(extract_markdown_links(test_text), excepted_output)

class Test_for_splitting(unittest.TestCase):
    def test_split_image(self):
        print("test_split_image")
        test_list_of_Nodes = [TextNode("![Image 1](Link for the image) Image 1 at the beginning.", text_type_text), TextNode("Zwei Images in ![Image 2](Link for the image) der Mitte und am Ende ![Image 3](Link for the image)", text_type_text), TextNode("Node mit einem falschen Typ", text_type_code), TextNode("[Link 1](Link for the link) Link 1 at the beginning", text_type_text), TextNode("Node mit zwei Links [Link 2](Link for the link) in der Mitte und am Ende [Link 3](Link for the link)", text_type_text)]
        excepted_output = [TextNode("Image 1", text_type_image, "Link for the image"), TextNode(" Image 1 at the beginning.", text_type_text), TextNode("Zwei Images in ", text_type_text), TextNode("Image 2", text_type_image, "Link for the image"), TextNode(" der Mitte und am Ende ", text_type_text), TextNode("Image 3", text_type_image, "Link for the image"), TextNode("Node mit einem falschen Typ", text_type_code), TextNode("[Link 1](Link for the link) Link 1 at the beginning", text_type_text), TextNode("Node mit zwei Links [Link 2](Link for the link) in der Mitte und am Ende [Link 3](Link for the link)", text_type_text)]
        self.assertEqual(split_nodes_image(test_list_of_Nodes), excepted_output)

    def test_split_links(self):
        print("test_split_links")
        test_list_of_Nodes = [TextNode("![Image 1](Link for the image) Image 1 at the beginning.", text_type_text), TextNode("Zwei Images in ![Image 2](Link for the image) der Mitte und am Ende ![Image 3](Link for the image)", text_type_text), TextNode("Node mit einem falschen Typ", text_type_code), TextNode("[Link 1](Link for the link) Link 1 at the beginning", text_type_text), TextNode("Node mit zwei Links [Link 2](Link for the link) in der Mitte und am Ende [Link 3](Link for the link)", text_type_text)]
        excepted_output = [TextNode("![Image 1](Link for the image) Image 1 at the beginning.", text_type_text), TextNode("Zwei Images in ![Image 2](Link for the image) der Mitte und am Ende ![Image 3](Link for the image)", text_type_text), TextNode("Node mit einem falschen Typ", text_type_code), TextNode("Link 1", text_type_link, "Link for the link"), TextNode(" Link 1 at the beginning", text_type_text), TextNode("Node mit zwei Links ", text_type_text), TextNode("Link 2", text_type_link, "Link for the link"), TextNode(" in der Mitte und am Ende ", text_type_text), TextNode("Link 3", text_type_link, "Link for the link")]
        self.assertEqual(split_nodes_links(test_list_of_Nodes), excepted_output)

class Test_for_text_to_textnodes(unittest.TestCase):
    def test_to_textnodes(self):
        print("test_to_textnodes")
        test_text = "Keine Ahnung, was ich schreiben soll [frag google](www.google.de)"
        excepted_output = [TextNode("Keine Ahnung, was ich schreiben soll ", text_type_text), TextNode("frag google", text_type_link, "www.google.de")]
        self.assertEqual(Text_to_textnodes(test_text), excepted_output)

    def test_chaotic_text_to_textnodes(self):
        print("test_chaotic_text_to_textnodes")
        test_text = "Nun machen **wir** mal etwas *verrücktes* ![Bild von verrücktem Clown](www.fake-site.de) und `mischen wilde` Formate **völlig** *durcheinander* [Link zu Chaosportal](www.fake-chaos.de) und `ich will` noch ein Bild ![Katzenbabys](www.katzenbilder.de) von *süßen* **Katzen**"
        excepted_output = [TextNode("Nun machen ", text_type_text), TextNode("wir", text_type_bold), TextNode(" mal etwas ", text_type_text), TextNode("verrücktes", text_type_italic), TextNode(" ", text_type_text), TextNode("Bild von verrücktem Clown", text_type_image, "www.fake-site.de"), TextNode(" und ", text_type_text), TextNode("mischen wilde", text_type_code), TextNode(" Formate ", text_type_text), TextNode("völlig", text_type_bold),TextNode(" ", text_type_text), TextNode("durcheinander", text_type_italic),TextNode(" ", text_type_text), TextNode("Link zu Chaosportal", text_type_link, "www.fake-chaos.de"), TextNode(" und ", text_type_text), TextNode("ich will", text_type_code), TextNode(" noch ein Bild ", text_type_text), TextNode("Katzenbabys", text_type_image, "www.katzenbilder.de"), TextNode(" von ", text_type_text), TextNode("süßen", text_type_italic), TextNode(" ", text_type_text), TextNode("Katzen", text_type_bold)]
        self.assertEqual(Text_to_textnodes(test_text), excepted_output)

class Test_for_block_to_blocktype(unittest.TestCase):
    def test_headline(self):
        print("test for headlines")
        test_block = """## Testheadline"""
        excepted_output = "headline"
        self.assertEqual(block_to_blocktyp(test_block), excepted_output)

    def test_code(self):
        print("test for code")
        test_block = """```Testblock for code. just for the
        fun we write a little bit more this time```"""
        excepted_output = "code"
        self.assertEqual(block_to_blocktyp(test_block), excepted_output)
    
    def test_unorderd_list(self):
        print("test for unorderd_list")
        test_block = """
* one sentence
- more sentence
* that will be enough sentences"""
        excepted_output = "unorderd_list"
        self.assertEqual(block_to_blocktyp(test_block), excepted_output)
    
    def test_quote(self):
        print("test for quote")
        test_block = """> i have a dream
> that one day
> lego will be eatable"""
        excepted_output = "quote"
        self.assertEqual(block_to_blocktyp(test_block), excepted_output)
    
    def test_orderd_list(self):
        print("test for orderd_list")
        test_block = """1. tigers
2. lions
3. snowleopards
4. lynxs
5. panthers"""
        excepted_output = "orderd_list"
        self.assertEqual(block_to_blocktyp(test_block), excepted_output)
    
    def test_paragraphs(self):
        print("test for paragraph")
        test_block = """##123 Testheadline
        > chaotic block
        1. should
        2. not.
        3. work
        * and a ```code block at the end```"""
        excepted_output = "paragraph"
        self.assertEqual(block_to_blocktyp(test_block), excepted_output)

class test_markdown_to_html_node(unittest.TestCase):
    def test_hole_document(self):
        print("test for hole document to htmlnode")
        test_document = """
#### This is the **headline** of the document

thinks we need:

1. an unorderd list
2. a `code`
3. a paragraph
4. a orderd list
5. a headline
6. a quote

> "We need a quote"
> "we need a list"
> "we need **more** then one quote"

```This should be enough for a code block```

Thinks we have:

* a **headline**
* a paragraph
* an orderd list
* a quote
* a code
- a paragraph
* an unorderd list


"""
        excepted_output = '<div><h4> This is the <b>headline</b> of the document</h4><p>thinks we need:</p><ol><li>1. an unorderd list</li><li>2. a <code>code</code></li><li>3. a paragraph</li><li>4. a orderd list</li><li>5. a headline</li><li>6. a quote</li></ol><blockquote>> "We need a quote"> "we need a list"> "we need <b>more</b> then one quote"</blockquote><pre><code>This should be enough for a code block</code></pre><p>Thinks we have:</p><ul><li>* a <b>headline</b></li><li>* a paragraph</li><li>* an orderd list</li><li>* a quote</li><li>* a code</li><li>- a paragraph</li><li>* an unorderd list</li></ul></div>'
        self.assertEqual(markdown_to_htmlNode(test_document).to_html(), excepted_output)
    