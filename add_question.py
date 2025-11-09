#!/usr/bin/env python3
import json, os
from storage import read, write

def ask(prompt):
    return input(f"{prompt}: ").strip()

def add_dsa():
    qtype = ask("Question type (mcq/short)").lower()
    question = ask("Enter the question")
    tags = ask("Enter tags (comma separated)").lower().replace(" ","").split(",")

    if qtype == "mcq":
        options = {}
        for letter in ["a","b","c","d"]:
            opt = ask(f"Option {letter} (leave blank to stop)")
            if not opt: break
            options[letter] = opt
        answer = ask("Correct option letter (a/b/c/d)")
    else:
        options = None
        answer = ask("Expected keywords / answer essence")

    # Load existing questions
    data = read("dsa")
    new_id = (data[-1]["id"] + 1) if data else 1

    entry = {
        "id": new_id,
        "type": qtype,
        "question": question,
        "answer": answer,
        "tags": tags
    }

    if options:
        entry["options"] = options

    data.append(entry)
    write("dsa", data)
    print(f"\n✅ DSA question added (ID {new_id})")

def add_sql():
    prompt = ask("Enter SQL prompt")
    keywords = ask("Enter required keywords (comma separated)").lower().replace(" ","").split(",")
    tags = ask("Enter tags (comma separated)").lower().replace(" ","").split(",")

    data = read("sql")
    new_id = (data[-1]["id"] + 1) if data else 1

    entry = {
        "id": new_id,
        "prompt": prompt,
        "keywords": keywords,
        "tags": tags
    }

    data.append(entry)
    write("sql", data)
    print(f"\n✅ SQL question added (ID {new_id})")

if __name__ == "__main__":
    mode = ask("Add (dsa/sql)?").lower()
    if mode == "dsa":
        add_dsa()
    elif mode == "sql":
        add_sql()
    else:
        print("Invalid mode")
