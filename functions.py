from textblob import TextBlob
from googletrans import Translator
import json
import math
import random

#User Settings
destLang = "en"

# Translation
transl = Translator()


def detectLang(text):
    lang = TextBlob(text)
    return (lang.detect_language())


def translate(text, sourceLang, outLang):
    translatedText = transl.translate(text, src=sourceLang, dest=outLang)
    return (translatedText.text)


# CS term look up
def findSimilarity(word1, word2):
    JaroScore = None

    # Jaro Distance
    if (word1 == word2):
        JaroScore = 1.0

    if JaroScore != 1.0:
        maxDist = math.floor(max(len(word1), len(word2)) * 0.5) - 1
        match = 0
        hash1 = [0] * len(word1)
        hash2 = [0] * len(word2)
        for i in range(len(word1)):
            for j in range(max(0, i - maxDist), min(len(word2),
                                                    i + maxDist + 1)):
                if (word1[i] == word2[j] and hash2[j] == 0):
                    hash1[i] = 1
                    hash2[j] = 1
                    match += 1
                    break
        if (match == 0):
            JaroScore = 0.0

    if JaroScore != 0.0:
        t = 0
        point = 0
        for i in range(len(word1)):
            if (hash1[i]):
                while (hash2[point] == 0):
                    point += 1
                if (word1[i] != word2[point]):
                    point += 1
                    t += 1
        t = t // 2
        JaroScore = (match / len(word1) + match / len(word2) +
                     (match - t + 1) / match) / 3.0
    return JaroScore


def findWord(word, listOfWords):
    simis = []
    for i in listOfWords:
        simis.append(findSimilarity(word, i))
    wordIndex = (simis.index(max(simis)))
    return (listOfWords[wordIndex])


# Trivia
questionDict = {
    "In what country is it considered a compliment to slurp loudly while eating soup?":
    ["Japan", "Iceland", "Russia", "Brazil"],
    "You are in Amman, Jordan, and you are invited to go to the souk. Where will you be going?":
    ["Market", "Restroom", "Mosque", "Park"],
    "What is the most popular language in the world?":
    ["Chinese", "English", "Spanish", "Hindi"],
    "Which country is known as “the land of no rivers”?":
    ["Saudi Arabia", "Egypt", "Peru", "Chile"],
    "What’s the most linguistically diverse COUNTRY in the world?":
    ["Papua New Guinea", "America", "Malaysia", "Indonesia"],
    "What is the currency called in Spain?":
    ["Euro", "Spanish Dollar", "Peso", "Yuan"],
    "Which country has been labeled the most diverse?":
    ["India", "USA", "China", "Mexico"],
    "How many stars are there on the flag of China?": ["5", "3", "2", "1"],
    "Which country has more lakes than the rest of the world combined?":
    ["Canada", "Brazil", "Malaysia", "Australia"],
    "Which country has the world's highest waterfall?":
    ["Venezuela", "India", "USA", "China"],
    "Fortune cookies were first made in which country?":
    ["America", "France", "Italy", "Russia"]
}


def getTriviaQuestion():
    question = random.choice(list(questionDict.keys()))
    answers = questionDict[question]
    return ([question, answers])


# Economy System
def giveMoney(userID, amount):
    with open("pointLog.json", "r") as f:
        points = json.load(f)
        f.close()
    if userID not in list(points.keys()):
        points[userID] = amount
    else:
        points[userID] = points[userID] + amount

    with open("pointLog.json", "w") as f:
        json.dump(points, f)
        f.close()


def checkBalance(userID):
    with open("pointLog.json", "r") as f:
        points = json.load(f)
        f.close()
    return (points[str(userID)])
