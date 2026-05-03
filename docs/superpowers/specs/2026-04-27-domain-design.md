# CELPIP Learner — Domain Design

**Date:** 2026-04-27
**Scope:** Domain model, study modes, evaluation skill architecture, and question generation layer. DB schema and answer structure details are deferred pending further research on CELPIP sample answers.

---

## Goals

Solve 4 pain points that existing CELPIP writing tools share:

1. **Evaluation consistency** — LLMs score the same writing differently across sessions. Solved by: per-criterion evaluation skills anchored to a curated reference example library.
2. **Feedback loop too long** — Holistic essay feedback is slow. Solved by: sub-passage practice modes (sentence, word/phrase) that give instant targeted feedback.
3. **Can't drill by criterion** — No tool isolates one rubric criterion. Solved by: each study mode fires only the criteria relevant to its granularity.
4. **Limited questions** — Fixed question banks run dry. Solved by: LLM question generation with a randomised strategy pool and full tagging.

---

## Architecture: Mode-Centric

The 4+1 study modes are the primary objects. Each mode knows which evaluation criteria apply to it and which question generation strategies it can use. The content library and evaluation skills are services the modes call.

```
Study Mode
  ├── calls → Question Generator (random strategy)
  ├── calls → Evaluation Skills (subset per mode)
  └── reads/writes → Content Library (DB)
```

---

## Study Modes

### 1. Whole Article
User writes a complete response to a generated CELPIP prompt (Task 1: email, Task 2: opinion essay).
- Evaluation: all 4 criteria (Coherence, Vocabulary, Readability, Task Fulfilment)
- Output: per-criterion band scores (1–12) + written feedback per criterion

### 2. Sentence Rewrite
Given a sentence with a known CELPIP band score, the user rewrites it to reach a higher target band.
- Evaluation: Vocabulary, Readability
- Output: new band score + diff of what improved

### 3. Sentence Write
User writes a sentence given a topic/context or fills in a missing sentence in a paragraph.
- Evaluation: Vocabulary, Readability
- Output: band score + feedback

### 4. Word/Phrase Fill
A sentence is shown with one word or phrase blanked out. User supplies just that word/phrase.
- Evaluation: Vocabulary only
- Output: correctness + explanation of why the chosen word works or doesn't

### 5. Mistake Revision
Spaced-repetition drill targeting mistakes the user has made in previous sessions.

**Flow per revision session:**
1. Show the user's original sentence containing the mistake → user corrects it
2. Agent generates a fresh targeted exercise for the same error pattern → user drills it
3. SM-2 algorithm schedules next review: day 1 → 3 → 7 → 14 → 30 (resets on failure, interval doubles on success)

**SM-2 fields per mistake item:** `interval`, `easiness_factor`, `repetitions`, `next_review_at`

- Evaluation: depends on the mistake's criterion (grammar → Readability, vocab → Vocabulary)
- Mistake types stored: grammar error, incorrect vocab usage

---

## Question Generation Layer

Used by all modes. A pool of generator strategies — the system randomly picks one per session to keep practice varied.

**Available strategies:**
| Strategy | Description |
|---|---|
| Topic-based generation | Given topic + audience + tone tags, generate a prompt |
| Fill-in-blank (sentence) | Generate a paragraph with one sentence removed |
| Fill-in-blank (word/phrase) | Generate a sentence with one word/phrase blanked |
| Spot-and-correct | Generate a sentence with a deliberate error; user finds and fixes it |
| Show-original-mistake | Pull a stored user mistake; ask user to correct their own sentence |
| Rewrite-to-band | Generate or select a sentence at band N; ask user to reach band N+1 |

**Question tags** (applied to every generated question):
- `task_type`: task_1_email | task_2_essay
- `topic_type`: complaint | proposal | opinion | request | suggestion | ...
- `audience`: residents_manager | city_council | friend | coworker | ...
- `tone`: formal | semi_formal | informal

---

## Evaluation Skills

One skill per CELPIP criterion. Each skill:
1. Loads the criterion rubric (what each band level looks like)
2. Retrieves calibration reference examples from DB (answers with known band scores for that criterion)
3. Compares user input against rubric + references
4. Returns: band score (1–12) + written feedback

| Skill | Scope | Applies to modes |
|---|---|---|
| **Coherence** | Article-level only | Whole Article |
| **Vocabulary** | Article + Sentence + Word/Phrase | All modes |
| **Readability** | Article + Sentence | Whole Article, Sentence Rewrite, Sentence Write, Mistake Revision |
| **Task Fulfilment** | Article-level only | Whole Article |

---

## Core Domain Entities (High-Level)

Detailed DB schema and field-level design are deferred. These are the key objects and relationships:

```
Question
  - task_type, topic_type, audience, tone (tags)
  - generated_by: strategy name

Answer
  - belongs to: Question
  - band scores per criterion
  - split into: Sentence[]

Sentence
  - belongs to: Answer
  - answer_part: which structural part of the answer it belongs to
    (e.g. "introduction", "body_1", "closing")
  - criterion tags: e.g. marks a sentence as a good Vocabulary example
  ⚠️ Answer structure (which parts exist per task type) is deferred —
     requires study of sample CELPIP answers before finalising

ReferenceExample
  - criterion: which of the 4 skills it calibrates
  - band_score: known CELPIP band
  - text: the reference answer/sentence

Mistake
  - user_id, criterion, error_pattern, original_sentence_text

RevisionItem (SM-2 schedule per Mistake)
  - interval, easiness_factor, repetitions, next_review_at

VocabPhrase
  - text, tags, source_sentence_id
```

---

## Out of Scope (This Phase)

- Detailed PostgreSQL schema and migrations
- Answer structure per task type (pending sample answer research)
- Frontend UI for any mode
- User authentication and session management
- API endpoints
