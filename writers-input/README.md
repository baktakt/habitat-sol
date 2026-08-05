# Writers’ Input

This directory contains the human creative direction for Habitat Sol.

It is not intended to describe the entire universe. Its purpose is to preserve the creator’s taste, intentions, observations, boundaries, and important decisions while allowing AI writers to invent supporting details.

## Core principle

Human input should be used where authorship matters most:

- what the series is really about;
- what emotional truths it should explore;
- how the central characters should change;
- what feels distinctive to Habitat Sol;
- what the project should avoid;
- which important world decisions become canon.

AI may freely invent low-risk supporting details unless they contradict established canon or the creative direction contained here.

## Priority order

When generating or reviewing a story, use sources in this order:

1. `01-north-star.md`
2. `02-human-truths.md`
3. established character and world canon
4. `03-character-pressure.md`
5. `04-world-decisions.md`
6. `05-observation-bank.md`
7. `06-story-seeds.md`
8. AI invention

When two sources conflict, the higher source wins.

## Canon levels

Every piece of information should be understood as one of four levels:

### Locked

A defining fact that should not change without an explicit decision.

Examples:

- the thematic purpose of the series;
- central family relationships;
- major historical events;
- the fundamental character of Habitat Sol.

### Established

A fact already used in a published episode. It should normally be preserved, but may be clarified without changing its meaning.

### Provisional

A useful working idea that the AI may develop, reinterpret, or replace before publication.

### Open

Deliberately undefined. The AI may propose details when a story requires them.

Do not convert provisional or open material into locked canon merely because an AI generated it.

## Just-in-time worldbuilding

Do not attempt to complete the entire world in advance.

Develop a subject when:

- an upcoming story needs it;
- it affects several recurring characters;
- inconsistency would damage the series;
- it reveals something important about human life on Mars.

Otherwise, leave it open.

## Daily workflow

The creator should spend approximately ten minutes per day adding one small piece of input.

Possible contributions include:

- one emotional observation;
- one decision between alternatives;
- one character complication;
- one memory from real life;
- one image or sensory detail;
- one story seed;
- one reaction to generated material;
- one thing that feels wrong for Habitat Sol.

Fragments are welcome. Polished writing is not required.

The AI is responsible for organizing useful fragments, proposing consequences, identifying contradictions, and turning selected material into stories.

## Inbox curation automation

`inbox.md` is intentionally unstructured creator input. The daily canon-curation agent uses `../scripts/collect_inbox_items.py` and the tracked `.inbox-state.json` ledger to process only notes it has not handled before.

- The collector normalizes and fingerprints each non-empty bullet under `## Notes`.
- A recorded fingerprint is not reconsidered on later runs; a materially edited note has a new fingerprint and is eligible again.
- Each recorded entry preserves its disposition, destination, timestamp, and rationale, including `needs-creator` and `duplicate/no-change` outcomes.
- Do not delete the state file to force reprocessing. Revise/resubmit the note, or make an explicit reviewed state change instead.

Run the pending-only collector locally:

```bash
python3 scripts/collect_inbox_items.py --repo .
```

The curator records a final disposition only after it finishes any content edits:

```bash
python3 scripts/collect_inbox_items.py --repo . --mark-processed \
  --fingerprint <fingerprint> \
  --disposition story-seed \
  --destination writers-input/06-story-seeds.md \
  --rationale "Converted the creator's situation into a seed."
```

## AI writing rule

## Episode scale: glimpses, not full short stories

Habitat Sol entries are written for an Instagram post. They should feel like a **glimpse**: one charged moment, one small exchange, one image that lingers, and some room for the reader to infer the larger life around it.

- Aim for **120–220 words of story prose**; go beyond that only when the creator explicitly asks for a longer piece.
- Center one immediate action, observation, or turn. Do not try to establish every character, the town's entire pressure, or a complete plot in one entry.
- Keep dialogue when it reveals a relationship, but use only the lines the moment needs.
- Let an object, gesture, interruption, or withheld response imply the wider story instead of explaining it.
- End on an image, a changed look, or an unanswered feeling—not a summary, moral, or explanatory paragraph.
- The image brief and production record are not part of the public story-word target.

Across multiple entries, small glimpses should accumulate into a larger life.

The AI should not ask the creator to define every missing detail.

When information is missing:

1. check whether the decision would materially affect theme, character identity, long-term continuity, or the uniqueness of Habitat Sol;
2. if not, make a plausible invention;
3. mark consequential new inventions as provisional;
4. avoid contradicting locked or established facts;
5. prefer intimate, concrete details over encyclopedic explanation.

The goal is not to document Mars comprehensively.

The goal is to tell truthful stories about people who happen to live there.
