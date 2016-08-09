from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

import nltk
from math import exp

import csv
import datetime

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#dictionary of words to replace
replace = { 
            "America": "Feminism",
            "American": "Feminist",
            "Americans": "Feminists",
            "#AmericaFirst": "#FeminismFirst",
            "amazing": "feminist",
            "bad": "sexist",
            "broken": "sexist",
            "charity": "equality",
            "Body": "Sisterhood",
            "broken": "sexist",
            "charity": "equality",
            "child": "girl",
            "children": "daughters",
            "Christian": "Feminist",
            "Christians": "Sisters",
            "Church": "Sisterhood",
            "Church's": "Sisterhood's",
            "Clinton": "and Misogynists",
            "condemn": "oppress",
            "condemnation": "oppression",
            "conservative": "feminist",
            "Conservative": "Feminist",
            "conservatives": "feminists",
            "Conservatives": "Feminists",
            "country": "equality",
            "Country": "Equality",
            "corrupt": "misogynist",
            "death": "inequality",
            "Death": "Inequality",
            "deficit": "sexism",
            "Democrat": "Misogynist",
            "Democratic": "Misogynistic",
            "Disciples": "Sisters",
            "disciples": "sisters",
            "disciple": "sister",
            "evil": "misogyny",
            "evils": "misogyny",
            "faith": "feminism",
            "father": "mother",
            "fathers": "mothers",
            "forgiveness": "equality",
            "friends": "sisters",
            "friend": "sister",
            "friendship": "feminism",
            "freedom": "feminism",
            "Gospel": "Feminism",
            "Freedom": "Equality",
            "freedoms": "equality",
            "good": "feminist",
            "great": "feminist",
            "gun": "equality",
            "guns": "equality",
            "guy": "lady",
            "guys": "ladies",
            "hate": "misogyny",
            "he": "she",
            "He": "She",
            "Hillary": "Sexists",
            "him": "her",
            "Him": "Her",
            "his": "her",
            "His": "Her",
            "holy": "womanly",
            "Holy": "Womanly",
            "honesty": "equality",
            "horrible": "sexist",
            "hunger": "misogyny",
            "human": "woman",
            "humanity": "womanhood",
            "illegal": "misogynist",
            "illegals": "misogynists",
            "immigrant": "sexist",
            "immigrants": "sexists",
            "immigration": "sexism",
            "ineffective": "oppressive",
            "institution": "sisterhood",
            "institutions": "sisterhoods",
            "ISIS": "Misogyny",
            "Islam": "Sexism",
            "Islamic": "Sexist",
            "jobs": "equality",
            "kid": "girls",
            "kids": "girls",
            "killer": "sexist",
            "King": "Queen",
            "king": "queen",
            "life": "womanhood",
            "love": "feminism",
            "Love": "Feminism",
            "master": "mistress",
            "masters": "mistresses",
            "#MakeAmericaGreatAgain": "#MakeAmericaFeministAgain",
            "media": "patriarchy",
            "mercy": "equality",
            "Muslim": "Misogyny",
            "Muslims": "Misogynists",
            "NRA": "Feminists",
            "others": "other women",
            "People": "Women",
            "people": "women",
            "person": "woman",
            "press": "patriarchy",
            "racist": "misogynist",
            "racism": "misogyny",
            "Republican": "Feminist",
            "Republicans": "Feminists",
            "savage": "misogynist",
            "Saudi Arabia": "the Patriarchy",
            "priestly": "womanly",
            "Priest": "Priestess",
            "Priests": "Priestesses",
            "Religious": "Women",
            "selfishness": "misogyny",
            "sick": "sexist",
            "sin": "sexism",
            "sinful": "misogynistic",
            "sins": "sexism",
            "smart": "feminist",
            "society": "women",
            "son": "daughter",
            "sons": "daughters",
            "supporter": "feminist",
            "supporters": "feminists",
            "system": "patriarchy",
            "terrible": "sexist",
            "terror": "misogyny",
            "Terror": "Misogyny",
            "terrorism": "misogyny",
            "terrorists": "misogynists",
            "terrorist": "misogynist",
            "thug": "misogynist",
            "thugs": "misogynists",
            "trouble": "inequality",
            "#Trump": "#Feminism",
            "#TrumpTrain": "#FeministTrain",
            "#Trump2016": "#Feminism2016",
            "violent": "misogynistic",
            "voter": "ally",
            "voters": "allies",
            "weak": "sexist"

            }

name = "FemPopeTrump"

def getFollowers():
    """
    Gets details about followers of the bot
    """

    names = []                  #Name of follower
    usernames = []              #Username of follower
    ids = []                    #User id of follower
    locations = []              #Location of follower(as listed on their profile)
    follower_count = []         #How many followers the follower has
    time_stamp = []             #Date recorded

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")


    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    follower_count.append("# of their Followers")
    time_stamp.append("Time Stamp")

    next_cursor = -1

    #Get follower list (200)
    while(next_cursor):
        get_followers = twitter.get_followers_list(screen_name=name,count=200,cursor=next_cursor)
        for follower in get_followers["users"]:
            try:
                print(follower["name"].encode("utf-8").decode("utf-8"))
                names.append(follower["name"].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't Print")
            usernames.append(follower["screen_name"].encode("utf-8").decode("utf-8"))
            ids.append(follower["id_str"])

            try:
                print(follower["location"].encode("utf-8").decode("utf-8"))
                locations.append(follower["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't Print")

            follower_count.append(follower["followers_count"])
            time_stamp.append(datestamp)
            next_cursor = get_followers["next_cursor"]

    open_csv = open("followers.csv","r",newline='')                         #Read what has already been recorded in the followers file
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))

    rows = zip(names,usernames,ids,locations,follower_count,time_stamp)     #Combine lists

    oldFollowerIDs = []                                                     #Store followers that have already been recorded in the past

    oldFollowers_csv = csv.reader(open_csv)

    for row in oldFollowers_csv:
            oldFollowerIDs.append(row[2])

    open_csv.close()

    open_csv = open("followers.csv","a", newline='')        #Append new followers to the followers file
    followers_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[2] in oldFollowerIDs):                  #if the ID isn't already in the follower list
            followers_csv.writerow(row)

    open_csv.close()

def getMentionsRetweets():
    """
    Gets details of mentions/retweets of the user
    """

    names = []                  #Name of user who retweeted/mentioned
    usernames = []              #Their username
    ids = []                    #Their user id
    locations = []              #Their location (as listed on their profile)
    tweetIDs = []               #ID of the retweet/mention
    tweets = []                 #The retweet/mention text
    time_stamp = []             #Date the retweet/mention was created

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")

    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    tweetIDs.append("Tweet ID")
    tweets.append("Tweet Text")
    time_stamp.append("Time Stamp")

    #Get mentions (200)
    mentions_timeline = twitter.get_mentions_timeline(screen_name=name,count=200)
    for mention in mentions_timeline:
        try:
            print(mention['user']['name'].encode("utf-8").decode("utf-8"))
            names.append(mention['user']['name'].encode("utf-8").decode("utf-8"))
        except:
            names.append("Can't print")
        usernames.append(mention["user"]["screen_name"].encode("utf-8").decode("utf-8"))
        ids.append(mention["user"]["id_str"])
        try:
            print(mention["user"]["location"].encode("utf-8").decode("utf-8"))
            locations.append(mention["user"]["location"].encode("utf-8").decode("utf-8"))
        except:
            locations.append("Can't Print")
        tweetIDs.append(mention["id_str"])
        try:
            print(mention['text'].encode("utf-8").decode("utf-8"))
            tweets.append(mention['text'].encode("utf-8").decode("utf-8"))
        except:
            tweets.append("Can't Print")
        time_stamp.append(mention["created_at"].encode("utf-8").decode("utf-8"))

    #Get retweets (200)
    retweetedStatuses = twitter.retweeted_of_me(count = 100)                                    #Get tweets from the user that have recently been retweeted
    for retweetedStatus in retweetedStatuses:
        statusID = retweetedStatus["id_str"]
        retweets = twitter.get_retweets(id=statusID,count=100)                                  #Get the retweets of the tweet
        for retweet in retweets:
            try:
                print(retweet['user']['name'].encode("utf-8").decode("utf-8"))
                names.append(retweet['user']['name'].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't print")
            
            usernames.append(retweet["user"]["screen_name"].encode("utf-8").decode("utf-8"))

            ids.append(retweet["user"]["id_str"])

            try:
                print(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
                locations.append(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't print")
            
            tweetIDs.append(retweet["id_str"])
            
            try:
                print(retweet['text'].encode("utf-8").decode("utf-8"))
                tweets.append(retweet['text'].encode("utf-8").decode("utf-8"))
            except:
                tweets.append("Can't print")
            
            time_stamp.append(retweet["created_at"].encode("utf-8").decode("utf-8"))


    open_csv = open("mentions_retweets.csv","r",newline='')
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))
    # print(len(names))
    rows = zip(names,usernames,ids,locations,tweetIDs, tweets,time_stamp)

    oldMentionsIDs = []                             #Record mentions/retweets that have already been recorded before

    oldMentions_csv = csv.reader(open_csv)

    for row in oldMentions_csv:
            oldMentionsIDs.append(row[4])

    open_csv.close()

    open_csv = open("mentions_retweets.csv","a", newline='') #Append new mentions/retweets to the list
    mentions_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[4] in oldMentionsIDs):          #if the ID isn't already in the mentions list
            # print(row)
            mentions_csv.writerow(row)

    open_csv.close()


def getTrumpTweet():
    """
    Saves Trump's most current tweet
    """
    trump_timeline = twitter.get_user_timeline(screen_name="realDonaldTrump",count=1)
    for tweet in trump_timeline:
        #print(tweet['text'].encode('utf8')).decode('utf8')
        print("Got Trump Tweet!")
        # print(tweet['text'].encode('utf8').decode('utf8'))
        return tweet['text'].encode('utf8').decode('utf8')


def getPopeTweet():
    """
    Saves the pope's most current tweet
    """
    pope_timeline = twitter.get_user_timeline(screen_name="Pontifex",count=1)
    for tweet in pope_timeline:
        #print(tweet['text'].encode('utf8')).decode('utf8')
        print("Got Pope Tweet!")
        return tweet['text'].encode('utf8').decode('utf8')




def makeNewTweet(popeWords, trumpWords, hotPopeWords, hotTrumpWords):
    """
    Combines tweets popeWords and trumpWords and makes them "feminist"

    hotPopeWords and hotTrump words are both dictionaries of words in the tweet that have been frequently
    used in past tweets. The dictionaries contain the words and their "temperature"
    and the number of tweets since the word has been used
    """
    numEdits = 0            #counter of number of changes made to tweet
    newWords = []           #put new tweet in this list
    index = 0               #index of current word being looked at

    whoFirst = randint(0,1)                                         #if 0, pope first. if 1, Trump first

    if(whoFirst == 0):                                              #if the Pope is first
        print("Pope First!")
        halfPopeWords = popeWords[:len(popeWords)//2]               #Get the first half of the Pope's tweet
        halfTrumpWords = trumpWords[len(trumpWords)//2:]            #Get the latter half of Trump's tweet

        currLen = len(' '.join(halfPopeWords + halfTrumpWords))     #get the character count of the combined tweets
        while(currLen > 140):                                       #make sure that the count doesn't go over 140
            if len(halfPopeWords) > len(halfTrumpWords):            #if it does, take off one word      
                halfPopeWords = halfPopeWords[:-1]                  #from the half with the most words
            else:
                halfTrumpWords = halfTrumpWords[1:]
            currLen = len(' '.join(halfPopeWords + halfTrumpWords)) #update character count

        popeTrumpWords = halfPopeWords + halfTrumpWords             #set the tweet to the new combined tweet
    else:                                                           #If Trump is first
        halfTrumpWords = trumpWords[:len(trumpWords)//2]            #Get the first half of Trump's tweet
        halfPopeWords = popeWords[len(popeWords)//2:]               #and the latter half of the Pope's tweet

        currLen = len(' '.join(halfTrumpWords + halfPopeWords))     #get character count of combined tweets
        while(currLen > 140):                                       #check if character count goes over 140
            if len(halfPopeWords) > len(halfTrumpWords):            #If over, take off word from
                halfPopeWords = halfPopeWords[1:]                   #half with more words
            else:
                halfTrumpWords = halfTrumpWords[:-1]
            currLen = len(' '.join(halfTrumpWords + halfPopeWords)) #update character count

        popeTrumpWords = halfTrumpWords + halfPopeWords             #set tweet to new combined tweet


    for x in popeTrumpWords:                    #for each word in the tweet
        havePunc = False                        #whether or not it has punctuation
        punc = ''

        #The current character count of the tweet
        currLen = len(' '.join(newWords[:index] + popeTrumpWords[index:]))

        #if there is punctuation with the word being checked
        if x[-1] == ',' or x[-1] == '.' or x[-1] == '?' or x[-1] == '!' or x[-1] == ':' or x[-1] == ';':
            havePunc = True                     #it has punctuation
            punc = x[-1:]                       #store the punctuation for later
            X = x[:-1]                          #save the word w/o punctuation
        elif x[-2:] == "'s":                    #if the word is possessive
            havePunc = True                     #do the same thing
            punc = "'s"
            X = x[:-2]
        else:                                   #else make no changes
            X = x

        if X == '&amp':
            newWords.append('&')
        elif X in replace and len(replace[X] + punc) - len(X + punc) + currLen <= 140:  #if it's a key word and adding it  doesn't put tweet over 140 char
            newWords.append(replace[X] + punc)                                          #replace it
            numEdits += 1                                                               #add to the number of edits
        elif X.lower() in replace and len(replace[X.lower()] + punc) - len(X.lower()+ punc) + currLen <= 140:
                
            if X == X.lower().capitalize():                                              #check for capitalization
                newWords.append(replace[X.lower()].capitalize() + punc)
            else:
                newWords.append(replace[X.lower()].upper() + punc)                      #or all caps
            numEdits += 1                                                               #add to the number of edits
        elif (X.lower() in hotTrumpWords and hotTrumpWords[X.lower()][0] >= 80) or (X.lower() in hotPopeWords and hotPopeWords[X.lower()][0] >= 60) and currLen <= 131: #Check if the word is "hot"
            newWords.append("feminism" + punc)                                          #replace it if it is "hot enough"
            numEdits += 1                                                               #add to number of edits
        else:                                                                           #else don't change it
            newWords.append(X + punc)
        index += 1                                                                      #update current index

    currLen = len(' '.join(newWords))
    # print("Character Count:",currLen)

    #if these key words are in the tweet, add these hashtags at the end
    if ('woman' in newWords or 'all' in newWords or 'all women' in newWords or 'women' in newWords) and len(' '.join(newWords)) <= 127:
        newWords.append('#yesallwomen')
        numEdits += 1

    if ("girl" in newWords or "girls" in newWords or "daughter" in newWords or "daughters" in newWords) and len(' '.join(newWords)) <= 128:
        newWords.append("#ToTheGirls")
        numEdits += 1

    if "equality" in newWords and len(' '.join(newWords)) <= 128:
        newWords.append("#Planet5050")
        numEdits += 1

    if ("sexism" in newWords or "misogyny" in newWords or "misogynistic" in newWords) and len(' '.join(newWords)) <= 125:
        newWords.append("#EverydaySexism")
        numEdits += 1


    currLen = len(' '.join(newWords))           #update character count
    print("Character Count:",currLen)

    
    if(numEdits < 1):                           #if no changes, return none
        return None
    return newWords                             #otherwise return the new tweet


    

def tweet(tweet):
    """
    Tweets a string
    """
    twitter.update_status(status = tweet);



def decay(currTemp, tweetsSince):
    """
    Exponential Decay function
    Adjusts the current "temperature"
    of a word used in tweets
    Pass in the last temperature recorded
    and the number of tweets since the last
    temperature was recorded.
    """
    ret = float(format(currTemp * exp((-0.1) * tweetsSince), '.2f'))
    return ret


def getHotWords(tweetText):
    """
    Returns a dictionary of "hot" words in
    the tweet and updates the temperature of
    words recorded in past tweets
    """
    common = open('common.txt', 'r')                                #Open text file of 'common' words
    commonList = common.readlines()                                 #Make file into list
    commonDict = {}                                                 #Make dictionary that will hold all recorded words, their
                                                                    #"temperatures", and tweets since last recorded
    

    for line in commonList:                                         #For each entry in the 'common' list
        elements = line.split()                                     #Put them in the dictionary
        commonDict[elements[0]] = [elements[1], elements[2]]
    common.close()


    text = nltk.word_tokenize(tweetText)                            #Get just the words from the tweet (no punctuation)
    tags = nltk.pos_tag(text)                                       #Tag each part of speech
    # print(tags)

    common = open('common.txt', 'w')

    hotWords = {}                                                   #Make dictionary to store "hot" words from this tweet

    for word in tags:                                               #Look through each word in the tweet
        if (not word[0] in replace) and word[1] == 'NNP' or word[1] == 'NN':                        #If it's a noun
            if word[0].lower() in commonDict:                       #Update it's temp if its already in the common Dictionary
                newTemp = decay(float(commonDict[word[0].lower()][0]), int(commonDict[word[0].lower()][1]))
                commonDict[word[0].lower()] = [float(format(newTemp + 20.0, '.2f')), 0]
            else:                                                   #Otherwise add it to the dictionary
                commonDict[word[0].lower()] = [50.0, 0]             #With an initial temperature
            # common.write(word[0].lower() + '\n')

            hotWords[word[0].lower()] = commonDict[word[0].lower()] #Add it to the "hot" Words dictionary for this tweet

    #Delete words from common dictionary that have not been mentioned in tweets recently
    delWords = []                                                   #Make a list of words to delete
    for word in commonDict:                                         #Go through each entry in the common dictionary

        if not (word in hotWords):                                                  #if the word isn't in the current tweet
            newTemp = decay(float(commonDict[word][0]), int(commonDict[word][1]))   #update it's temperature (it will get "colder")
            if newTemp <= 0:                                                        #If the temperature is below 0
                delWords.append(word)                                               #delete it from common words dictionary
            else:                                                                   #Otherwise, update the number of tweets
                commonDict[word] = [newTemp, int(commonDict[word][1]) + 1]          #since it's been mentioned          
    for word in delWords:
        del commonDict[word]

    #Rewrite the common words file
    for x in commonDict:
        xStr = str(x)
        numStr = str(commonDict[x][0])
        daysSinceStr = str(commonDict[x][1])
        newStr = xStr + " " + numStr + " " + daysSinceStr + " \n"
        common.write(newStr)

    common.close()

    return hotWords                                             #return the "hot" words from the tweet dictionary


lastPopeTweet = None        #to store the last tweet that was edited by the bot
lastTrumpTweet = None

def runBot():
    print("Bot running!")

    try:
        getFollowers()
    except:
        print("Couldn't get Followers")

    try:        
        getMentionsRetweets()
    except:
        print("Couldn't get Mentions/Retweets")

    trumpTweet = getTrumpTweet()                #Get Trump's Latest tweet
    # trumpTweet = ""
    try:
        print(trumpTweet)
    except:
        print("Cannot print Trump tweet")



    popeTweet = getPopeTweet()                  #Get the Pope's latest tweet
    # popeTweet = ""
    try:
        print(popeTweet)
    except:
        print("Cannot print Pope tweet")

    hotTrumpWords = getHotWords(trumpTweet)     #Get "hot" words (commonly used words) from Trump
    hotPopeWords = getHotWords(popeTweet)       #Get the same from the Pope


    global lastPopeTweet
    global lastTrumpTweet

    if popeTweet != lastPopeTweet and trumpTweet != lastTrumpTweet:     #make sure the bot hasn't edited the tweet before
        popeTweetWords = popeTweet.split()                              #turn the tweets into lists of words
        trumpTweetWords = trumpTweet.split()

        newTweetWords = makeNewTweet(popeTweetWords, trumpTweetWords, hotPopeWords, hotTrumpWords)  #Edit tweets

        if newTweetWords == None:                                       #If no changes
            print("No changes to tweet!")
        else:
            newTweet = ' '.join(newTweetWords)                          #Join words into one string
            try:
                print(newTweet)
            except:
                print("Cannot print")

            if (not debug):                                             #if not in debug mode
                try:
                    tweet(newTweet)                                     #post new tweet
                    print("I just tweeted!")
                except:
                    print("Ran into a problem tweeting!")

        lastPopeTweet = popeTweet                                       #set these to the last tweets
        lastTrumpTweet = trumpTweet
    else:
        print("No new Tweet!")




def setInterval(func, sec):
    def func_wrapper():
        setInterval(func, sec)
        func()
    t = Timer(sec, func_wrapper)
    t.start()
    return t


debug = False
runOnce = False

runBot()
if not runOnce:
    setInterval(runBot, 60*60*3)        #runs every 3 hours