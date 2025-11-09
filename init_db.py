
import sqlite3, json, os

DB = "questions.db"

DSA = [
    # MCQs
    ("mcq", "What is the time complexity of binary search on a sorted array?", 
     {"a":"O(log n)", "b":"O(n)", "c":"O(n log n)", "d":"O(1)"}, "a"),
    ("mcq", "Which data structure is best for implementing BFS?", 
     {"a":"Stack", "b":"Queue", "c":"Priority Queue", "d":"Set"}, "b"),
    ("mcq", "In a min-heap, the smallest element resides at:", 
     {"a":"Any leaf", "b":"The root", "c":"The deepest node", "d":"None of the above"}, "b"),
    # Short answers
    ("short", "Explain why quicksort has average O(n log n) time complexity.", None, 
     "partition divide-and-conquer average randomized expected n log n"),
    ("short", "What is the difference between a stable and unstable sorting algorithm?", None, 
     "stable keeps relative order equal keys unstable may reorder equal elements"),
    ("short", "What property of a binary search tree enables efficient search?", None, 
     "left subtree keys smaller right subtree keys larger order invariant")
]

SQL = [
    ("Return the second highest salary from table Employees(id, name, salary).",
     ["select", "salary", "from", "employees", "order by", "desc", "limit 1", "offset 1"]),
    ("Get department-wise average salary from Employees(name, salary, dept_id) joined with Departments(id, name).",
     ["select", "avg", "salary", "from", "employees", "join", "departments", "on", "dept_id", "id", "group by"]),
    ("Find users who never placed an order. Users(id, name), Orders(id, user_id).",
     ["select", "from", "users", "left join", "orders", "on", "users.id", "orders.user_id", "where", "orders.id", "is null"]),
]

def main():
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE dsa_questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qtype TEXT NOT NULL,
            question TEXT NOT NULL,
            options_json TEXT,
            answer TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE sql_questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            keywords_json TEXT NOT NULL
        )
    """)
    for qtype, question, options, answer in DSA:
        cur.execute("INSERT INTO dsa_questions(qtype, question, options_json, answer) VALUES(?,?,?,?)",
                    (qtype, question, json.dumps(options) if options else None, answer))
    for prompt, kw in SQL:
        cur.execute("INSERT INTO sql_questions(prompt, keywords_json) VALUES(?,?)",
                    (prompt, json.dumps(kw)))
    con.commit()
    con.close()
    print("Seeded DB at", DB)

if __name__ == "__main__":
    main()
