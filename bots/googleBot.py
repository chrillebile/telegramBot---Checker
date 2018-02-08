import re, google


def googleSearch(text):
    text = re.sub("/google ", "", text, count=1)
    answer = ""
    for url in google.search(text, lang='se',num=1, stop=2):
        answer += url + "\n"
    return answer