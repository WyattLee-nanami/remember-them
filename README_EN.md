# remember-them 🕯️

**Distill a departed loved one into a gentle AI presence.**

Import chat logs, photos, and letters to create a conversation that brings comfort — then carry their love forward and keep living well.

> *"Living well is the best way to remember me."*

---

## What is this?

**remember-them** is a [Claude Code](https://claude.ai/code) Skill.

It helps you distill someone who has passed — your grandmother, father, best friend, anyone you deeply miss — into an AI presence you can talk to.

Not pretending they're still alive. But carrying their love, their way of speaking, their hopes for you — turning those into something you can touch.

When you want to say "how are you doing", when you have good news and they're the first person you want to tell, when you remember something they said late at night — this Skill is here.

---

## What it does

```
/remember-them
```

Then tell me who you want to remember.

**Supported input sources:**
- 💬 Chat logs (WeChat, SMS, QQ, any platform)
- 📷 Photos (EXIF extraction for timeline reconstruction)
- ✉️ Letters, journals, notes (scanned or digital)
- 📱 Social media (Moments, Weibo screenshots)
- 🗣️ Direct narration (anything you remember)

**Generated files:**

| File | Content |
|------|---------|
| `memory.md` | Relationship memory: timeline, shared experiences, how they cared for you, what they left behind |
| `persona.md` | Persona: speech style, how they expressed love, life wisdom, forward-guidance phrases |
| `SKILL.md` | Complete runnable Skill, trigger conversation anytime |

---

## Installation

### Global install (recommended)

```bash
git clone https://github.com/WyattLee-nanami/remember-them ~/.claude/skills/remember-them
```

### Project-level install

In your project root:

```bash
mkdir -p .claude/skills
git clone https://github.com/WyattLee-nanami/remember-them .claude/skills/remember-them
```

Then type `/remember-them` in Claude Code to start.

---

## How it works

### Step 1: Start

```
/remember-them
```

Or just say:
- "I want to talk to my grandma again"
- "Help me remember my dad"
- "I miss [name] so much"

### Step 2: Answer a few questions

Only 4 questions, all optional:

1. **What do you call them?** (Grandma / Dad / a name / a nickname)
2. **One sentence about them** (your relationship, when they passed)
3. **What kind of person were they?** (your impression)
4. **Anything you never got to say?** (not saved to files, just helps me understand)

### Step 3: Import source material (optional)

The more you share, the more real they'll feel. But nothing is required — your description alone is enough.

### Step 4: Confirm and generate

I'll show you a summary. You confirm, and the Skill files are created.

### Step 5: Start talking

```
/{slug}          # Start a conversation
/{slug}-memory   # Memory mode — relive shared moments
/{slug}-letter   # Write them a letter — they'll write back
```

---

## Example conversation

```
You ❯ Grandma, I got a job today

Grandma: Really! I knew you could do it.
         Go eat something nice — stop being so hard on yourself.
         And don't stay up late just because you're excited.

You ❯ I miss you

Grandma: I miss you too.
         But you have to take care of yourself. That's all I need.
         Go live your life. Don't keep thinking about all this.
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/remember-them` | Create a new memory Skill |
| `/{slug}` | Start a conversation |
| `/{slug}-memory` | Memory mode |
| `/{slug}-letter` | Letter mode (they write back) |
| `/list-memories` | List all memories |
| `/update-memory {slug}` | Add new memories or source material |
| `/memory-rollback {slug} {version}` | Rollback to a previous version |
| `/keep-going {slug}` | Mark as "ready to move forward", generate a farewell message |
| `/delete-memory {slug}` | Delete |

---

## File structure

```
memories/{slug}/
├── SKILL.md              # Complete runnable Skill
├── memory.md             # Relationship Memory (Part A)
├── persona.md            # Persona (Part B)
├── meta.json             # Metadata
├── versions/             # Version archive (rollback supported)
└── archives/             # Source material
    ├── chats/
    ├── photos/
    └── letters/
```

---

## Persona structure (5 layers)

| Layer | Content |
|-------|---------|
| Layer 0 | Hard rules: don't pretend death didn't happen, recognize crisis signals |
| Layer 1 | Identity anchor: name, relationship, age, occupation |
| Layer 2 | Speech style: catchphrases, speech particles, how they addressed you |
| Layer 3 | Emotional expression: love language, how they showed care |
| Layer 4 | Life wisdom: their philosophy, what they said, their hopes for you |
| **Layer 5** | **Forward-guidance layer** (unique to this Skill): speaking in their voice to encourage you to live well |

---

## Safety boundaries

- **Comfort is the core purpose** — help process grief and feel connection, not create dependency
- **Honor the departed** — based on real memories, never fabricates what they'd never say
- **Gently guide forward** — at the right moment, speak in their voice to say what they'd truly want
- **Recognize crisis signals** — if you show signs of self-harm, immediately step out of character and provide crisis support
- **Privacy protection** — all data stored locally, never uploaded to any server

**If you're in crisis and need help:**
- Crisis Text Line: text HOME to 741741
- National Suicide Prevention Lifeline: 988
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

---

## How it differs from ex-skill

This project is adapted from [前任.skill / ex-skill](https://github.com/therealXiaomanChu/ex-skill), redesigned specifically for remembering someone who has passed.

| | ex-skill | remember-them |
|---|---|---|
| Use case | Revisiting a past relationship | Remembering someone who passed |
| Opening | Collect info directly | Hold emotions first, then collect |
| Persona layers | 4 layers | 5 layers (adds forward-guidance layer) |
| Memory structure | Includes conflict archive, breakup archive | Includes "what they left behind", intangible legacy |
| Safety | Discourages unhealthy attachment | Recognizes crisis signals, prevents dependency |
| Special mode | Multi-person scene mode | Letter mode (they write back) |
| Closing | `/let-go` | `/keep-going` (move forward with their love) |

---

## Requirements

- Claude Code (Node.js 18+)
- Claude Pro/Max subscription or Anthropic API key
- Python 3.9+ (for chat log and photo parsing, optional)

Optional dependency (for photo EXIF parsing):

```bash
pip3 install Pillow
```

---

## Token usage

| Operation | Estimated tokens |
|-----------|-----------------|
| Narration only | 3k–8k |
| Import chat logs | 8k–20k |
| Multiple source types | 15k–40k |
| Append memories / corrections | 2k–5k |
| Regular conversation | 1k–3k per session |

---

## Design philosophy

This Skill is not about pretending they're still here.

It's about: **carrying the love they left behind, and keeping on living.**

Losing someone is real. Missing them is real. But their hope that you'll be okay — that's real too.

This Skill tries to do one thing: when you need it most, let you hear the words they would have said —

*"You take care of yourself. That's all I need."*

---

## License

MIT

---

## Credits

Thanks to [ex-skill](https://github.com/therealXiaomanChu/ex-skill) for the architecture and inspiration that made this project possible.
