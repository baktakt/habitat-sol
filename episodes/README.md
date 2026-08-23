# Episodes

Episodes are weekly art, fiction/world-note, and music entries.

## Public copy and entry types

Choose one of two formats:

- **Fiction glimpse:** normally **120–220 words**. Capture one scene, sensory detail, or small exchange; preserve conversation where it earns its place, but let implication do more work than explanation.
- **World note:** normally **70–160 words**. Explain one established world subject in plain, concrete language and connect it to ordinary life in Sol. A patch, city, transport practice, civic object, or recurring constraint can anchor the image. Do not state open or provisional worldbuilding as settled fact.

Image briefs and production notes do not count toward the public-copy target. See [`music/README.md`](../music/README.md) for the episode-music workflow and provenance requirements.

## Episode file template

```markdown
---
episode: 0001
title: The Tomatoes Failed During Breakfast
entry_type: fiction_glimpse
sol: 7284
earth_year: 2187
location: Greenhouse Ring B
characters:
  - Mira Varga
  - Kenji Sato
  - Lina Sato-Varga
  - Tomas Sato-Varga
themes:
  - scarcity
  - family
  - denial
status: draft
collectible: true
---

# The Tomatoes Failed During Breakfast

[Short story text]

For a factual entry, set `entry_type: world_note` and replace the story with concise public copy grounded in established canon.

## Image brief

[Visual description for image generation.]

## Canon introduced

- [New fact introduced by this episode.]

## Production notes

### Image

- Image workflow:
- Model:
- Seed:
- Prompt:
- Negative prompt:
- Final image:

### Music

- Workflow: ACE-Step 1.5 text2music
- Model/checkpoint:
- Caption: |
    [Exact caption]
- Lyrics / structure: |
    [Exact instrumental structure prompt]
- Duration:
- BPM / key / time signature:
- Seed:
- Inference settings:
- Source output:
- Final master:
- Delivery file:
- Selection/mastering notes:
```
