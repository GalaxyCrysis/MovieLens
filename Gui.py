from PyQt4 import QtGui,QtCore,uic
import MovieLens
import numpy as np
from PIL import Image,ImageQt
from io import BytesIO
import requests
from Worker import Worker
from PyQt4.QtCore import SIGNAL




class mainWindow(QtGui.QMainWindow):
    #init main window
    def __init__(self):
        super(mainWindow,self).__init__()
        uic.loadUi("gui.ui",self)
        self.setWindowTitle("MovieLens")
        self.rating_list = ""
        self.dataframe = ""
        self.movies =""

        self.threadList = list()
        self.pic_list = list()
        self.data_list = list()

        self.dataframe,self.movies,self.rating_list = MovieLens.getDataframes()


        #add signal to return pressed search line edit
        self.searchEdit.returnPressed.connect(self.initRecommendation)
        #auto complete signal
        self.searchEdit.textChanged.connect(self.autocomplete)
        self.searchView.hide()
        #item clicked list widget signal
        self.searchView.itemClicked.connect(self.insertText)
        self.widget = QtGui.QWidget()
        self.layout = QtGui.QVBoxLayout()
        self.show()

    """
        auto complete function for search edit. It starts at atleast 5 characters input and searches for movies
        which contain the string the user has inserted.Finally show the listview
    """
    def autocomplete(self):
        text = self.searchEdit.text()
        self.searchView.clear()
        if len(text) >=5:

            for i in range(0,len(self.movies)):
                if text in self.movies[i]:
                    item = QtGui.QListWidgetItem(self.movies[i])
                    self.searchView.addItem(item)

        if self.searchView.count() > 0:
            self.searchView.show()
        else:
            self.searchView.hide()


    #list widget item selected event for auto completing. Inserts the text selected into the search edit
    def insertText(self):
        items = self.searchView.selectedItems()
        for item in items:
            self.searchEdit.setText(item.text())
        self.searchView.hide()




    """
    init recommendation function: We get the text from searchLineedit, transform it and compare it with the dataframe
    we transform the dataframe into a correlation matrix to get the best possible results for recommendations
    After that we get the list of movie recommendations and print it on the scroll area
    """

    def initRecommendation(self):
        searchedMovie = self.searchEdit.text()
        self.threadList.clear()
        self.data_list.clear()
        self.pic_list.clear()

        #get movie index
        favoured_movie_index = list(self.movies).index(searchedMovie)

        #create correlation matrix
        correlation_matrix = np.corrcoef(self.dataframe)
        coeff = correlation_matrix[favoured_movie_index]

        #delete all widgets from layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widget)
            widget.setParent(None)

        #we now have a list. We need a correlation of 0,97 to 1 for best recommendations
        self.job_list = self.movies[(coeff > 0.97)& (coeff < 1.0)]
        #create thread workers and save them in a list and start them
        for job in self.job_list:
            thread = Worker(job)
            self.connect(thread, SIGNAL("output(QString, QString)"), self.updateSrollArea)
            self.threadList.append(thread)


        for thread in self.threadList:
            thread.start()


    """
    in a for loop we get the data from the lists. We create labels for movie_name, movie_rating, the movie_image and the movie data
    We get the movie images via getPixmap method. Finally we update the scrollarea
    """
    def updateSrollArea(self,pic_url,data):
        self.pic_list.append(pic_url)
        self.data_list.append(data)
        if len(self.pic_list) == len(self.job_list):
            for i in range(0, len(self.job_list)):
                # create labels
                movie_label = QtGui.QLabel(self.job_list[i])
                font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
                movie_label.setFont(font)
                rating_label = QtGui.QLabel(
                    "Rating: " + str(self.rating_list[list(self.movies).index(self.job_list[i])]) + "/5.0")

                image_label = QtGui.QLabel("")
                if self.pic_list[i] == "none" or self.pic_list[i] == "":
                    self.pic_list[i] = "http://englishwithatwist.com/wp-content/uploads/2014/02/Blog_The-Movies.jpg"
                pixmap = self.getPixmap(self.pic_list[i]).scaled(250,150)
                image_label.setPixmap(pixmap)


                text_browser = QtGui.QTextBrowser()
                if self.data_list[i]!= "" or self.data_list[i]!= "none":
                    text_browser.setText(self.data_list[i])


                # create layout
                namebox = QtGui.QHBoxLayout()
                namebox.addWidget(movie_label)
                namebox.addWidget(rating_label)

                databox = QtGui.QHBoxLayout()
                #databox.addWidget(image_label)
                databox.addWidget(text_browser)
                self.layout.addItem(databox)



                self.layout.addItem(namebox)

            self.widget.setLayout(self.layout)
            self.scrollArea.setWidget(self.widget)





    """
    get the pic from web via the page_url, convert it to a Qt Pixmap and return it
    """
    def getPixmap(self,page_url):
        try:
            response = requests.get(page_url)
            img = Image.open(BytesIO(response.content))
            qtImage = ImageQt.ImageQt(img)
            qImage = QtGui.QImage(qtImage)
            pixmap = QtGui.QPixmap.fromImage(qImage)
            return pixmap
        except:
            return ""





















