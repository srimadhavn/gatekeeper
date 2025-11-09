import random
from storage import read

class SQLEngine:
    def get_random(self):
        return random.choice(read("sql"))

    def check(self, q, user_sql):
        text = user_sql.lower()
        return all(k in text for k in q["keywords"])
