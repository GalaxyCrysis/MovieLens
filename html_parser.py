from bs4 import BeautifulSoup

"""
beautiful soup html parser: We search for links in the documents and return them
"""

def getData(html, method, movie):
    soup = BeautifulSoup(html, "html.parser")

    if method =="wikipedia_url":
        wiki_url = ""
        #search for all a tags in the html document
        short_movie = movie.split("(")
        for link in soup.find_all("a"):
            name = link.get("title")
            if name == movie or name == short_movie[0][:-1] or name == short_movie[0][:-1]+" (Movie)" or name == short_movie[0][:-1]+ " (American Film)":
                wiki_url = link.get("href")
        return wiki_url

    if method == "wikipedia_pic_url":
        wiki_url = ""
        for tag in soup.find_all("a"):
            if tag.has_attr("class"):
                for i in range(0,len(tag["class"])):
                    if tag["class"][i] == "image":
                        wiki_url = tag["href"]
                        return wiki_url

    if method == "wikipedia_pic":
        wiki_url = ""
        for tag in soup.find_all("img"):
            wiki_url = "https:"+tag.get("src")
            return wiki_url

    if method == "wikipedia_data":
        text = ""
        for tag in soup.find_all("p"):
            text = tag.get_text()
            break
        return text





















