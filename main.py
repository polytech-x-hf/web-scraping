from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve

def GetImageFromLink(link, imageClass, imageName, savePath):#OK
    tmp = requests.get(link)
    html_doc = tmp.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    a = soup.find_all('a', class_ = imageClass, limit=1)#a = soup.find_all('a', id = targetedID)
    imgLinks = []
    for link in a:
        imgLinks.append(link.get('href'))
    if(len(imgLinks) >= 1):
        urlretrieve(imgLinks[0], savePath + "/" + imageName)

#renvoie les nom des perso et le lien de la page des persos
def GetCharactersLinks(pageLink, charsListLink, charactersClass):
    charsNames = []
    charsLinks = []
    tmp = requests.get(charsListLink)
    html_doc = tmp.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    a = soup.find_all('a', class_ = charactersClass)
    for link in a:
        linkSuffixe = link.get('href')
        if ("Category:" in linkSuffixe):#la fameuse syntaxe atroce
            (tmpNames, tmpLinks) = GetCharactersLinks(pageLink, charsListLink + linkSuffixe, charactersClass)
            if(len(tmpNames) == len(tmpLinks) and len(tmpNames) != 0):
                for i in range(0, len(tmpNames)):
                    charsLinks.append(tmpLinks[i])
                    charsNames.append(tmpNames[i])
            else:
                if(len(tmpNames) != len(tmpLinks)):
                    varUseless1 = "nique l'indentation de python"
                    #print("debug pls")
                else:
                    varUseless1 = "nique l'indentation de python"
                    #print("No item in this category : " + charsListLink + linkSuffixe)
        else:
            charsLinks.append(pageLink + linkSuffixe)
            charsNames.append(link.get('title'))

    return (charsNames, charsLinks)

pageLink = "https://jojo.fandom.com/"
charsListLink = "https://jojo.fandom.com/wiki/Category:Characters"
charactersClass = "category-page__member-link"
targetedClass = "image image-thumbnail"

def SaveAllImagesAndNamesWithLink(mainPageLink, charsListLink, charactersClass, imageClass, imagesName, imageExtension, fileTextName, path):

    (charsName, charLinks) = GetCharactersLinks(mainPageLink, charsListLink, charactersClass)
    if(len(charLinks) != len(charsName)):
        print("charsListLink and charsName doesn't have the same len")
        return
    file = open(path + "/" + fileTextName, "a")
    for i in range(0, len(charLinks)):
        GetImageFromLink(charLinks[i], imageClass, imagesName + str(i) + imageExtension, path)
        file.write(charsName[i] + "\n")
    file.close()

SaveAllImagesAndNamesWithLink(pageLink, charsListLink, charactersClass, targetedClass, "Jojos image", ".jpg", "Jojos Characters Names.txt", "./CharsImages")
