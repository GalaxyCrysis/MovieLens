from PyQt4 import QtCore
import html_parser
from urllib.request import urlopen
from PyQt4.QtCore import SIGNAL


class Worker(QtCore.QThread):
    def __init__(self, movie,parent = None):
        QtCore.QThread.__init__(self,parent)
        self.movie = movie
        self.existing = False
        self.data = ""
        self.pic_url = ""



    """
    main work: The workers will gain access to the website of wikipedia and get the hmtl. Then initialize the html parser
    and feed it witht he hmtl. After that they will have the link for the movie wikipedia page. They will do the same
    but this time they will get al ink for an image of the movie and some information about the movie. The workers
    will download the movie and finally create the widget.
    After everything is done the scroll area will add the widget
    """

    def run(self):
        print("started")
        if ", The" in self.movie:
            self.movie = self.movie.replace(", The", "")
        search_url = "https://en.wikipedia.org/w/index.php?search="
        url = "https://en.wikipedia.org"
        string = self.movie.split(" ")
        for i in range(0, len(string)):
            if i == len(string) - 1:
                search_url += string[i]
            else:
                search_url += string[i] + "+"

        wiki_url = self.gather_link(search_url, "wikipedia_url", self.movie)
        if wiki_url != "":
            wiki_url = "https://en.wikipedia.org" + wiki_url
            wiki_pic_url = self.gather_link(wiki_url, "wikipedia_pic_url", "")
            if wiki_pic_url != None and wiki_pic_url != "":
                wiki_pic_url = url + wiki_pic_url
            self.pic_url = self.gather_link(wiki_pic_url, "wikipedia_pic", "")
            if self.pic_url =="":
                self.pic_url = "none"

            self.data = self.gather_link(wiki_url, "wikipedia_data", "")
            if self.data == "":
                self.data = "none"
        else:
            self.data = "none"
            self.pic_url = "none"

        self.emit(SIGNAL("output(QString, QString)"), self.pic_url, self.data)








    def __del__(self):
        self.existing = True
        self.wait()

    def gather_link(self, page_url, method, movie):
        html_string = ""
        try:
            response = urlopen(page_url)
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")


        except:
            print("Error: Cannot crawl page")
            return ""

        if method == "wikipedia_url":
            return html_parser.getData(html_string, "wikipedia_url", movie)
        elif method == "wikipedia_pic":
            return html_parser.getData(html_string, "wikipedia_pic","")
        elif method == "wikipedia_pic_url":
            return html_parser.getData(html_string, "wikipedia_pic_url", "")
        elif method == "wikipedia_data":
            return html_parser.getData(html_string, "wikipedia_data", "")



