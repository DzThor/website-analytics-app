from followerwonk import FollowerWonk

#FollowerWonk Freemium API Access


'''Returns "Social Authority Level"

Social Authority helps you find, optimize, and engage your Twitter audience. It's a 1 to 100
point scale that measures a user's influential content on Twitter.

More than just another self-focused metric, Social Authority helps you discover influential tweeters.'''

user = FollowerWonk.social_authority("Google")
print(user)