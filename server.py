from flask import Flask, jsonify
from flask import render_template
import requests
app = Flask(__name__)

# @app.route('/a'):
# def hello():
#   return 'hello'

# @app.route('/b'):
# def add():
#   x = 1
#   b = 2

#   return str(x + b)
def analyse(comment):
    with open("good_words.txt", "r") as f:
        good_words = f.readlines()

    with open("bad_words.txt", "r") as f:
        bad_words = f.readlines()
        bw = [x.strip() for x in bad_words]
        gw = [x.strip() for x in good_words]

    current_tweet = comment.split()
    gc = 0   
    bc = 0
    for j in range(0, len(current_tweet)):
        current_word = current_tweet[j].lower() 
        if current_word in gw:
            gc += 1
        elif current_word in bw:
            bc += 1
        if gc > bc:
            sentiment = 'good'
        elif gc < bc:
            sentiment = 'bad'
        else:
            sentiment = 'inconclusive'
    return sentiment

@app.route('/')
def mypage():

    response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')

    # Get top 10 ids
    top_ten_ids = response.json()[:10]

    # print('Top ten ids:', top_ten_ids)

    # an empty dictionary for now. looks like she changes it to a list or set
    # at bottom of this cell tho, but thats just temporarily so she can use
    # "append" on it.
    comments = {}
    # comments needs to be a dictionary so we can use the keys() method on it
    # Fetch top 10 stories

    stories = []
    for top_id in top_ten_ids:
        curr_story_api_url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(top_id)
        curr_story = requests.get(curr_story_api_url)
        stories.append(curr_story.json())

    # print(stories) #stories is a list, filled with dictionaries with key/value pairs and more lists(eg.kids ids,
    # it starts with "by:" "descendants:" "id:", then "kids:", "score:",
    # "title:" and so on. but no actual text

    for story in stories:
        if 'kids' in story:  # this makes sure that there is comments on the story
            # this accesses the first five comment ids of each story
            comment_ids = story['kids'][:10]
            title = story['title']  # accesses the title of the story
            # not sure what this line is doing yet. just remember that everywhere
            # u see this comments variable, she had put an [title] immediately
            # after it, with no quotes
            # {'comment': 'ewjlkarjlkewr', 'sentiment': asdlkfklsadf, 'random': 0}
            comments[title] = {}
            for comment_id in comment_ids:  # gets each comment id individually, from the 'kids' dict/list
                curr_comment_api_url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(comment_id)
                res = requests.get(curr_comment_api_url).json()
                if 'text' in res:
                    curr_comment = res['text']
                    comments[title]['comment'] = curr_comment

                    comments[title]['sentiment'] = analyse(curr_comment)
       
    return jsonify(comments) #remember jsonify can only return dictionaries




if __name__ == '__main__': 
  app.run()
