import json
import copy
from flask import Flask, request, jsonify
from flask_api import status
from flask_restful import Resource, Api
from json import dumps
from BehaviourBasedRecommendation import BehaviourBasedRecommendation
from GenreBasedRecommendation import GenreBasedRecommendation
from ProfileBasedRecommendation import ProfileBasedRecommendation
from VideoSimilarityBasedRecommendation import VideoBasedRecommendation

app = Flask(__name__)
api = Api(app)

film_rec = VideoBasedRecommendation()
profile_rec = ProfileBasedRecommendation()
genre_rec = GenreBasedRecommendation()
behaviour_rec = BehaviourBasedRecommendation()
@app.route("/r", methods=['GET'])
def index():
    with open("input.txt") as f:
        content = f.readlines()
    user_id = int(content[0])
    user_id1 = user_id
    user_id2 = copy.copy(user_id1)
    user_id3 = copy.copy(user_id1)
    user_id4 = copy.copy(user_id1)

    viewed = film_rec.get_viewed_items(user_id1)
    out = film_rec.recommend(user_id1, viewed)  # film
    out1 = profile_rec.recommend(user_id2, viewed)  # profile
    out2 = genre_rec.recommend(user_id3, viewed)  # genre
    out3 = behaviour_rec.recommend(user_id4, viewed)  # behaviour

    for elmt in out2:
        if not (elmt in out3):
            out3.append(elmt)

    for elmt in out1:
        if not (elmt in out3):
            out3.append(elmt)

    for elmt in out:
        if not (elmt in out3):
            out3.append(elmt)

    key = []
    for i in range(len(out3)):
        key.append(i)
    res = {str(key[i]): str(out3[i]) for i in range(len(out3))}
    # print(key)
    # print(out3)
    return json.dumps(res), status.HTTP_200_OK

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=20000)