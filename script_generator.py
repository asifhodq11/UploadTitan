import random
from topic_research import get_trending_topic
from job_logger import log_event

# Add personalities
PERSONALITY_TONES = {
    "funny": {
        "openings": [
            "Okay, this will blow your mind: {topic}.",
            "So I was today years old when I found out {topic}...",
            "Let me meme it for you — {topic} is wild!"
        ],
        "closings": [
            "And now you're smarter than 90% of the internet 😂",
            "Follow me before your brain melts 🧠🔥"
        ]
    },
    "sarcastic": {
        "openings": [
            "Oh great, another day, another {topic} moment...",
            "Because obviously, the world needed more {topic}.",
            "Imagine not knowing this about {topic} 🙄"
        ],
        "closings": [
            "Congrats, you just wasted 40 seconds wisely.",
            "And no, I’m not making this up. Or am I?"
        ]
    },
    "luxury": {
        "openings": [
            "Want to feel elite? Understand {topic}.",
            "This is what the top 1% know about {topic}.",
            "Luxury isn’t just money — it’s {topic}."
        ],
        "closings": [
            "Now that’s what I call a rich move 💼",
            "Save this for your millionaire mindset."
        ]
    }
}

# Prewritten script bodies, < 30 seconds
SCRIPT_LINES = [
    "Step 1: Understand the basics.",
    "Step 2: Apply this small trick smartly.",
    "Step 3: Most ignore this — don’t be them.",
    "Step 4: Repeat until results show up.",
    "Pro Tip: Simplicity beats complexity.",
    "Bonus: Do it for 7 days — you'll thank me later."
]

def generate_script():
    topic = get_trending_topic()
    personality = random.choice(list(PERSONALITY_TONES.keys()))
    tone = PERSONALITY_TONES[personality]

    intro = random.choice(tone["openings"]).format(topic=topic)
    outro = random.choice(tone["closings"])

    # Keep max 3 lines to stay under 40 sec
    middle = "\n".join(random.sample(SCRIPT_LINES, 2 + random.randint(0, 1)))

    script = f"{intro}\n\n{middle}\n\n{outro}"
    log_event("Generated Script", script[:100] + f"... [{personality}]")
    return script
