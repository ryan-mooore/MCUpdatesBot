import tweepy
import json
import time
from credentials import ApiKey, AccessToken
import training

def run():
    class StreamListener(tweepy.StreamListener):
        def on_status(self, status):
            print(status.author.name + ':', status.text)
            data = str(f'{status.entities["urls"] is not None} ' + 
            f'{status.user.id} ' + 
            f'{status.text} ' + 
            f'{status.in_reply_to_status_id is not None}')

            result = training.train(model, [data])[0]
            print("Result:", result)

            time.sleep(30)
            
            try:
                api.retweet(status.id)
            except Exception as e:
                print(e)
            
            print("----------------------")

        def on_error(self, e):
            print(e)

    
    key = ApiKey()
    token = AccessToken()

    auth = tweepy.OAuthHandler(key.public, key.secret)
    auth.set_access_token(token.public, token.secret)

    api = tweepy.API(auth)
    stream = tweepy.Stream(auth=api.auth, listener=StreamListener())
    
    model = training.get_model()

    stream.filter(follow=get_user_ids())

def load_following(api):
    friends = api.friends()
    following = []
    for user in friends:
        following.append({
            "id": user.id,
            "name": user.name
        })
    following_json = json.dumps(following)
    with open("bot/users.json", "w") as wfile:
        wfile.write(following_json)
        wfile.close

def target(api):
    with open("bot/users.json", "r") as wfile:
        users = wfile.read()
        users = json.loads(users)
        training_data = []
        obreak = False
        for user in users:
            timeline = api.user_timeline(user["id"], count=25, include_rts=False)
            for status in timeline:
                current_tweet = {
                    "training": {
                        "user": status.user.id,
                        "text": status.text,
                        "isReply": status.in_reply_to_status_id is not None,
                        "hasUrl": status.entities["urls"] is not None
                    }
                }
                print("User: ", api.get_user(current_tweet["training"]["user"]).name)
                print("------------------------")
                print("Tweet:", current_tweet["training"]["text"])
                print("------------------------")
                print("Is Reply:", current_tweet["training"]["isReply"])
                print("Has Image:", current_tweet["training"]["hasUrl"])
                reply = input("Relevant?")
                if reply.lower() in ["yes", "y", "t", "true"]:
                    current_tweet["target"] = True
                
                elif reply.lower() == "exit":
                    obreak = True
                    break
                
                else:
                    current_tweet["target"] = False
                training_data.append(current_tweet)
            
            if obreak: break
        
        with open("bot/training.json", "w") as wfile:
            wfile.write(json.dumps(training_data))
            wfile.close

def get_user_ids():
    with open("bot/users.json", "r") as wfile:
        users = wfile.read()
        users = json.loads(users)
        wfile.close()
    user_ids = []
    for user in users:
        user_ids.append(str(user["id"]))
    return user_ids
