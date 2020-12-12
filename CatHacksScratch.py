from html.parser import HTMLParser
from urllib import parse
import urllib.request
import re


#HTML parser for java docs
class html_parser_java(HTMLParser):
    
    def __init__(self):
        super().__init__()
        self.link_set = set()
        self.print_p = False
    
    def __init__(self, link_set, print_p, get_links):
        super().__init__()
        self.link_set = link_set
        self.print_p = print_p
        self.in_p_tag = False
        self.get_links = get_links
        self.in_header_tag = False
        self.buffer_string = ""
    
    #Handle open tags in HTML
    def handle_starttag(self, tag, attrs):
        pattern = re.compile("technotes/")
        if tag == 'a' and self.get_links:  #Handle links
            if attrs[0][0] == 'href':
               if pattern.match(attrs[0][1]):
                    self.link_set.add(attrs[0][1])
        if tag == 'p' and self.print_p: #Handle p's
            self.in_p_tag = True
        if tag == 'h1' and self.print_p:  #Handle Headers
            self.in_header_tag = True
            
    #Handle data inside of tags
    def handle_data(self, data):
        if self.in_p_tag or self.in_header_tag:   #If we are in a p or header tag...
            self.buffer_string += data.replace("\n"," ")   #Add the data to the buffer
    
    #Handle end tags in HTML
    def handle_endtag(self, tag):
        if tag == 'p':   #If closing p tag...
            self.in_p_tag = False   #Declare that we are out of a p tag
        if tag == 'h1':    #If closing header tag
            self.in_header_tag = False
            self.print_buffer()   #Empty contents of buffer and declare exit of header tag
    
    def error(self, message):
        pass
    
    #Print and empty the buffer
    def print_buffer(self):
        print(self.buffer_string)
        self.buffer_string = ""
        



    

#HTML parser for python docs
class html_parser_python(HTMLParser):
    
    def __init__(self):
        super().__init__()
        self.link_set = set()
        self.print_p = False
    
    def __init__(self, link_set, print_p, get_links):
        super().__init__()
        self.link_set = link_set
        self.print_p = print_p
        self.in_p_tag = False
        self.get_links = get_links
        self.in_header_tag = False
        self.buffer_string = ""
    
    #Handle open tags in HTML
    def handle_starttag(self, tag, attrs):
        pattern = re.compile("[a-zA-Z]+.html")
        if tag == 'a' and self.get_links:   #handle links
            if len(attrs) >= 2:
                if attrs[1][0] == 'href':
                    if pattern.match(attrs[1][1]):
                        self.link_set.add(attrs[1][1])
        if tag == 'p' and self.print_p:  #handle p's
            self.in_p_tag = True
        if (tag == 'h1' or tag == 'h2') and self.print_p:  #handle headers
            self.print_buffer()
            self.in_header_tag = True
            
    #Handle data in HTML
    def handle_data(self, data):
        if self.in_p_tag or self.in_header_tag:
            self.buffer_string += data.replace("\n"," ")
    
    #Handle end tags in HTML
    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p_tag = False
        if (tag == 'h1' or tag == 'h2') and self.print_p:
            self.in_header_tag = False
            print("------------------------------------")
            self.print_buffer()
            print("------------------------------------")
    
    def error(self, message):
        pass
    
    def print_buffer(self):
        print(self.buffer_string)
        self.buffer_string = ""
        


#Print out the guide for java doc sections
def dispGuideJava(url):
    html_doc_raw = urllib.request.urlopen(url)
    html_doc = html_doc_raw.read().decode("utf8")
    html_processor = html_parser_java(link_set=None, print_p=True, get_links=False)
    html_processor.feed(html_doc)
    html_processor.print_buffer()
 

 #Print out the guide for python doc sections
def dispGuidePython(url):
    html_doc_raw = urllib.request.urlopen(url)
    html_doc = html_doc_raw.read().decode("utf8")
    html_processor = html_parser_python(link_set=None, print_p=True, get_links=False)
    html_processor.feed(html_doc)
    html_processor.print_buffer()


#Determine which language to search
print()
language = input("Java or Python?\n")
print("\n")
#Get the HTML and process the index page
if language == "Java":
    url = "https://docs.oracle.com/javase/8/docs/"
    html_doc_raw = urllib.request.urlopen(url)
    html_doc = html_doc_raw.read().decode("utf8")
    link_set = set()
    html_processor = html_parser_java(link_set, False, True)
if language == "Python":
    url = "https://docs.python.org/3.9/reference/index.html"
    html_doc_raw = urllib.request.urlopen(url)
    html_doc = html_doc_raw.read().decode("utf8")
    link_set = set()
    html_processor = html_parser_python(link_set, False, True)
html_processor.feed(html_doc)

#Print out the table of links for reference
print("-----------Table of Contents------------")
for link in link_set:
    print(link)
print("\n")

#Get input for guide
requestedGuide = input("Search: ")

#Search for doc guide based on input
if language == "Java":
    pattern = re.compile('technotes/guides/'+requestedGuide)
else:
    pattern = re.compile(requestedGuide+'.html')
foundURL = False
for link in link_set:
    if pattern.match(link):
        if language == "Java":
            newURL = "https://docs.oracle.com/javase/8/docs/"+link
        else:
            newURL = "https://docs.python.org/3.9/reference/"+link
        foundQ = input("Is this the right guide Y/N?\n"+newURL+"\n")
        if foundQ == "Y":
            foundURL = True
            break

#If a guide was found, display it
if foundURL:
    if language == "Java":
        dispGuideJava(newURL)
    else:
        dispGuidePython(newURL)
else:
    print("No doc found")

