from html.parser import HTMLParser
from urllib import parse
import urllib.request
import re

class html_parser(HTMLParser):
    
    def __init__(self):
        super().__init__()
        self.link_set = set()
        self.print_p = False
    
    def __init__(self, link_set, print_p):
        super().__init__()
        self.link_set = link_set
        self.print_p = print_p
    
    def handle_starttag(self, tag, attrs):
        pattern = re.compile("technotes/")
        if tag == 'a':
            if attrs[0][0] == 'href':
                if pattern.match(attrs[0][1]):
                    self.link_set.add(attrs[0][1])
        if tag == 'p' and self.print_p:
            print(attrs)
    
    def handle_data(self, data):
        pass
    
    def error(self, message):
        pass
        




def dispGuide(url):
    html_doc_raw = urllib.request.urlopen(url)
    html_doc = html_doc_raw.read().decode("utf8")
    html_processor = html_parser(link_set=None, print_p=True)
    html_processor.feed(html_doc)

html_doc_raw = urllib.request.urlopen("https://docs.oracle.com/javase/8/docs/")
html_doc = html_doc_raw.read().decode("utf8")
link_set = set()
html_processor = html_parser(link_set, False)
html_processor.feed(html_doc)

#print(link_set)
requestedGuide = input("Search: ")
pattern = re.compile('technotes/guides/'+requestedGuide)

foundURL = False
for link in link_set:
    if pattern.match(link):
        newURL = "https://docs.oracle.com/javase/8/docs/"+link
        foundQ = input("Is this the right guide Y/N?\n"+newURL+"\n")
        if foundQ == "Y":
            foundURL = True
            break
if foundURL:
    dispGuide(newURL)
else:
    print("No doc found")

