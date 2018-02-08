import requests
import re
import time

# base url
base = 'http://www.paulgraham.com/'

# get the html
res = requests.get('{}articles.html'.format(base)).text
links = re.findall(
    r'<font size=2 face="verdana"><a href="([a-zA-Z0-9\-\.html]*)">',
    res
)

# get absolute links
links = ['{}{}'.format(base, link) for link in links]


# parse every link for text
for i, link in enumerate(links):
    
    # get the aricle html, without abusing the site
    time.sleep(0.1)
    res = requests.get(link).text
    
    # find the text
    article = re.findall(
        r'<font size=2 face="verdana">(.*)<br><br></font>',
        res, re.DOTALL
    )
    if len(article) == 0:
        article = re.findall(
            r'<font size=2 face="verdana">(.*)<br><br><br clear=all></font>',
            res, re.DOTALL
        )

    try:
        article = article[0].replace('<br>', '\n')
        article += '\n'
        
        # write retreived text in a file
        with open('paul_graham_essay.txt', 'a') as f:
            f.write(article)
        print(i+1, '. Text taken from: ', link)
    
    except IndexError:
        print(i+1, '. Could not get text from: ', link)

