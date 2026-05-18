def calculate_trust_score(user_profile):

    score = 50

    if user_profile["known_devices"] > 2:
        score += 10

    if user_profile["known_locations"] > 1:
        score += 5

    if user_profile["avg_transfer"] < 5000:
        score += 10

    return min(score, 100)
