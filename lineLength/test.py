from browser import document
from browser.widgets.dialog import InfoDialog
#from insert_returns import fixWebsiteText

def click(ev):
    InfoDialog("Hello", f"Hello, {document['inputText'].value} !")
    str = document["inputText"].value
    lineLimit = document["lineLimitInput"].value
    #InfoDialog("Hello", f"Hello, {document['lineLimitInput'].value} !")
    #ans = fixWebsiteText(str, lineLimit)
    #if ans == -1:
        #cause alert
    #else:

# bind event 'click' on button to function echo
document["fixButton"].bind("click", click)