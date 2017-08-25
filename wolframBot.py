import wolframalpha, re

TOKEN = "9HL4GP-LLTREW7G52"


def ask(text):
    text = re.sub("/ask ", "", text, count=1)
    try:
        client = wolframalpha.Client(TOKEN)
        res = client.query(text)
    except Exception:
        return "Could not connect to wolframAlpha to find the answer to: '" + text + "'"
    answer = ""
    try:
        for pod in res.pods:
            answer += str(pod.text) + "\n"
    except Exception:
        return "Could not find the answer to: '" + text + "'"
    return answer
