import random
from storage import read, write

class DSAEngine:
    def get_random(self):
        questions = read("dsa")
        return random.choice(questions)

    def check(self, q, user):
        ans = q["answer"].strip().lower()
        user = user.strip().lower()

        if q["type"] == "mcq":
            return user == ans or user == q["options"].get(ans,"").lower()

        # short answer check = keyword match
        score = sum(1 for k in ans.split() if k in user)
        return score >= max(1, len(ans.split()) // 2)
