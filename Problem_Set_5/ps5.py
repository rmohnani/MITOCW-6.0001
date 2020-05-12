# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
            # pubdate = pubdate.astimezone(pytz.timezone('EST'))
            # pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower().strip()

    def is_phrase_in(self, text):
        self.text = text.lower().strip()

        for char in self.text:
            if char in string.punctuation:
                self.text = self.text.replace(char, " ")

        ### My initial solution. Created a list to keep track of phrase word index positions in the text
        ### and compared these values to determine if words positions match that of the phrase.

        # text_list = self.text.split()
        # phrase_list = self.phrase.split()
        # word_indexes = []

        # for word in phrase_list:
        #     if word not in text_list:
        #         return False

        #     try:
        #         last_item = word_indexes[-1]
        #     except IndexError:
        #         last_item = -1

        #     if text_list.index(word) <= last_item or (text_list.index(word) > last_item + 1 and last_item != -1):
        #         return False
        #     word_indexes.append(text_list.index(word))
        # return True

        ### Smarter solution. Add spaces after and before both phrase and text and then 
        ### simply check whether phrase in text. Done to avoid problem of phrase being 
        ### contained inside other words.

        text = " " + " ".join(self.text.split()) + " "
        phrase = " " + self.phrase + " "
        if phrase in text:
            return True
        return False

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower().strip()
    
    def evaluate(self, story):
        if self.is_phrase_in(story.get_title()):
            return True
        else:
            return False
    
    def __str__(self):
        return self.phrase

# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower().strip()
    
    def evaluate(self, story):
        if self.is_phrase_in(story.get_description()):
            return True
        else:
            return False

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, date_string):
        date_format = "%d %b %Y %H:%M:%S"
        time = datetime.strptime(date_string, date_format)
        time = time.replace(tzinfo=pytz.timezone("EST"))
        self.time = time

### pubdate in GMT initially or no timezone specification, so we have to do the .replace(EST)
# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) < self.time:
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) > self.time:
            return True
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    triggered_stories = []
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story) and story not in triggered_stories:
                    triggered_stories.append(story)
    return triggered_stories 




#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    ### Important note: didn't initially understand the question being asked so after googling the question
    ### and seeing some guy's answer, I understood. But this is basically the same soln as his, cuz I would have done it same way.

    trigger_dict = {}
    trigger_list = []
    for command in lines:
        temp_list = [x for x in command.split(",")]
        if temp_list[1] == "TITLE":
            trigger_dict[temp_list[0]] = TitleTrigger(temp_list[2])
        elif temp_list[1] == "DESCRIPTION":
            trigger_dict[temp_list[0]] = DescriptionTrigger(temp_list[2])
        elif temp_list[1] == "AFTER":
            trigger_dict[temp_list[0]] = AfterTrigger(temp_list[2])
        elif temp_list[1] == "BEFORE":
            trigger_dict[temp_list[0]] = BeforeTrigger(temp_list[2])
        elif temp_list[1] == "NOT":
            trigger_dict[temp_list[0]] = NotTrigger(temp_list[2])
        elif temp_list[1] == "AND":
            trigger_dict[temp_list[0]] = AndTrigger(temp_list[2], temp_list[3])
        elif temp_list[1] == "OR":
            trigger_dict[temp_list[0]] = OrTrigger(temp_list[2], temp_list[3])
        elif temp_list[0] == "ADD":
            trigger_list.extend(temp_list[1:])
    return trigger_list

FILENAME = "Problem_Set_5/triggers.txt"

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("COVID-19")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Corona")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config(FILENAME)
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print("Exception:", e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

