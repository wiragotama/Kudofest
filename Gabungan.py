from BehaviourBasedRecommendation import BehaviourBasedRecommendation
from GenreBasedRecommendation import GenreBasedRecommendation
from ProfileBasedRecommendation import ProfileBasedRecommendation
from VideoSimilarityBasedRecommendation import VideoBasedRecommendation


user_id = 25
film_rec = VideoBasedRecommendation()
viewed = film_rec.get_viewed_items(user_id)
out = film_rec.recommend(user_id, viewed) # film

profile_rec = ProfileBasedRecommendation()
out1 = profile_rec.recommend(user_id, viewed)  # profile

genre_rec = GenreBasedRecommendation()
out2 = genre_rec.recommend(user_id, viewed)  # genre

behaviour_rec = BehaviourBasedRecommendation()
out3 = behaviour_rec.recommend(user_id, viewed)  # behaviour

for elmt in out2:
    if not (elmt in out3):
        out3.append(elmt)

for elmt in out1:
    if not (elmt in out3):
        out3.append(elmt)

for elmt in out:
    if not (elmt in out3):
        out3.append(elmt)

print(out)
print(out1)
print(out2)
print(out3)