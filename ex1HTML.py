__author__ = 'JOKAZ'

from ex1 import *

# Replaces the entity characters (not sure if we will ever need but..)
def ReplaceEntityNamesByCharacter(string):
    entityCharacters = [
        "'",
        " ", "¡", "¢", "£", "¤", "¥", "¦", "§",
        "¨", "©", "ª", "«", "¬", "­", "®", "¯", "°", "±", "²", "³", "´",
        "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿", "×", "÷",
        "À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì",
        "Í", "Î", "Ï", "Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "Ø", "Ù", "Ú",
        "Û", "Ü", "Ý", "Þ", "ß", "à", "á", "â", "ã", "ä", "å", "æ", "ç",
        "è", "é", "ê", "ë", "ì", "í", "î", "ï", "ð", "ñ", "ò", "ó", "ô",
        "õ", "ö", "ø", "ù", "ú", "û", "ü", "ý", "þ", "ÿ", "—", "&#8211", "&#8217", "&#8216", "'", "\"", "&"]

    entityNames = [
        "&apos;",
        "&nbsp;", "&iexcl;",
        "&cent;", "&pound;", "&curren;", "&yen;", "&brvbar;", "&sect;", "&uml;",
        "&copy;", "&ordf;", "&laquo;", "&not;", "&shy;", "&reg;", "&macr;",
        "&deg;", "&plusmn;", "&sup2;", "&sup3;", "&acute;", "&micro;", "&para;",
        "&middot;", "&cedil;", "&sup1;", "&ordm;", "&raquo;", "&frac14;", "&frac12;",
        "&frac34;", "&iquest;", "&times;", "&divide;", "&Agrave;", "&Aacute;", "&Acirc;",
        "&Atilde;", "&Auml;", "&Aring;", "&AElig;", "&Ccedil;", "&Egrave;", "&Eacute;",
        "&Ecirc;", "&Euml;", "&Igrave;", "&Iacute;", "&Icirc;", "&Iuml;", "&ETH;",
        "&Ntilde;", "&Ograve;", "&Oacute;", "&Ocirc;", "&Otilde;", "&Ouml;", "&Oslash;",
        "&Ugrave;", "&Uacute;", "&Ucirc;", "&Uuml;", "&Yacute;", "&THORN;", "&szlig;",
        "&agrave;", "&aacute;", "&acirc;", "&atilde;", "&auml;", "&aring;", "&aelig;",
        "&ccedil;", "&egrave;", "&eacute;", "&ecirc;", "&euml;", "&igrave;", "&iacute;",
        "&icirc;", "&iuml;", "&eth;", "&ntilde;", "&ograve;", "&oacute;", "&ocirc;",
        "&otilde;", "&ouml;", "&oslash;", "&ugrave;", "&uacute;", "&ucirc;", "&uuml;",
        "&yacute;", "&thorn;", "&yuml;", "&mdash", "&ndash", "&rsquo;", "&lsquo", "&#39;", "&quot;", "&amp;"]

    i = 0
    while i < len(entityCharacters):
        string = string.replace(entityNames[i], entityCharacters[i])
        i += 1

    return string

# Downloads each page and saves it in a file
def downloadpages(pages):
    i = 0
    named = "page_%d"
    for v in pages:
        # urllib.urlretrieve(v, named.replace("%d", str(i)))
        try:
            # THIS WILL HANDLE REDIRECTS
            thing = urllib2.HTTPRedirectHandler()
            thing2 = urllib2.HTTPCookieProcessor()
            opener = urllib2.build_opener(thing, thing2)

            page = opener.open(v)
            dv = page.read()

            f = open(named.replace("%d", str(i)), 'w')
            f.write(dv)
            f.close()

            i += 1
        except urllib2.URLError as e:
            print e.reason


def decode_html(filename):
    html_string = file(filename).read()
    converted = BeautifulSoup.UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        return ''
    # print converted.originalEncoding

    return converted.unicode
    # return html_string


# Receives the soop and parses all the google results
def parseGoogle(soup):
    a = []
    d = []

    for li in soup.findAll('li', attrs={'class': 'g'}):  # iterates trought each <li class="g">
        sLink = li.find('a')  # gets the <a> atg
        a.append(sLink['href'])  # saves it
    return a

# This function just checks if it can find the headers of each page with BeautifulSoup
def checkSoupHeaders(soup, i):
    print "Document " + str(i)

    res = soup.xpath('//*[@id="root"]/body/div[2]/div[3]/article/div/div')

    if res is not None:
        header = soup.xpath('//*[@id="root"]/body/div[2]/div[3]/article/header/h1/span')

        if len(header) is not 0:
            return header[0].text
        else:
            return -1
    else:
        return -1