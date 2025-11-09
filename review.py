#!/usr/bin/env python3
import sys
from storage import read
from dsa_engine import DSAEngine

def review_topic(tag):
    answers = read("answers")
    wrong = [a for a in answers if (not a["correct"]) and tag in a["tags"]]

    if not wrong:
        print(f"No wrong answers found for topic '{tag}'. You're clean here!")
        return

    # pick the first wrong entry
    entry = wrong[0]

    # load matching question
    questions = read("dsa")  # Only DSA for now
    q = next((x for x in questions if x["id"] == entry["id"]), None)
    if not q:
        print("Question not found (data mismatch)")
        return

    print(f"\nReviewing topic: {tag}")
    print(f"Question: {q['question']}")

    if q["type"] == "mcq":
        for k,v in q["options"].items():
            print(f"{k}) {v}")

    user = input("\nYour answer: ").strip().lower()

    from dsa_engine import DSAEngine
    engine = DSAEngine()
    correct = engine.check(q, user)

    if correct:
        print("\n✅ Correct this time! Nice redemption.")
        # update answer history so next time it doesn't show
        entry["correct"] = True
        write_back = read("answers")
        for item in write_back:
            if item["id"] == entry["id"]:
                item["correct"] = True
        from storage import write
        write("answers", write_back)
    else:
        print("\n❌ Still incorrect — keep practicing.")


def main():
    if len(sys.argv) < 2:
        print("Usage: gatekeeper review <tag>")
        return
    
    tag = sys.argv[1]
    review_topic(tag)

if __name__ == "__main__":
    main()
