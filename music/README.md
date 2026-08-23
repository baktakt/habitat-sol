# Episode music

Each Habitat Sol episode may include an original instrumental cue generated locally with the MIT-licensed [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) model. The cue is part of the episode's storytelling: it should extend the scene's emotional movement without competing with the prose or turning an intimate moment into a trailer.

Use the upstream [ACE-Step 1.5 tutorial](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/Tutorial.md) for installation, model selection, interface details, and current parameter guidance. This document defines the Habitat Sol creative and archival workflow.

## Recommended local model

For the project's RTX 3090 (24 GB), use **ACE-Step 1.5 XL SFT** with the official ComfyUI split files and the 1.7B planner:

- `diffusion_models/acestep_v1.5_xl_sft_bf16.safetensors`
- `text_encoders/qwen_0.6b_ace15.safetensors`
- `text_encoders/qwen_1.7b_ace15.safetensors`
- `vae/ace_1.5_vae.safetensors`

XL SFT is the quality-first choice for finished episode cues: 50-step inference, tunable CFG, stronger detail and prompt adherence. The 1.7B planner is the upstream recommendation for 20–24 GB cards and leaves safer headroom than the 4B planner on this RTX 3090/16 GB host. Use the existing `ace_step_1.5_turbo_aio.safetensors` only for faster drafts. The installed editor workflow is `habitat-sol/music/01_habitat_sol_ace_step_1_5_xl_sft_quality.json`; the version-controlled UI and API graphs are under `music/workflows/`.

Start with batch size 1, 90–120 seconds, Euler/simple, 50 steps, CFG 7, and sampling shift 3. Generate several seeds rather than increasing batch size on a nearly full 24 GB card.

## Creative direction

Write the cue from the finished episode, not from a generic series prompt.

1. Identify the episode's emotional starting point, turn, climax, and aftertaste.
2. Choose a restrained palette of instruments and textures that supports that arc.
3. Keep the music cinematic but human-scale. Prefer atmosphere, tension, warmth, melancholy, or unresolved hope over spectacle, bombast, or generic space-opera grandeur.
4. Let recurring characters and locations develop recognizable musical colors over time, but do not force a leitmotif into every episode.
5. Unless an episode explicitly calls for a song, generate an instrumental cue with no sung or spoken words.

## ACE-Step prompt format

ACE-Step separates the overall musical identity from its development over time:

- **Caption** describes the whole cue: genre, mood, instruments, timbre, production character, space, and dynamics.
- **Lyrics / structure** acts as a temporal script. For instrumental cues, use short bracketed sections such as `[Intro - Sparse, atmospheric]`; do not write lyric text. Keep these directions consistent with the caption and avoid stacking too many instructions into one tag.

A useful starting template is:

### Caption

```text
[genre and function], [core instruments], [texture], [emotional qualities], [spatial/production qualities], [dynamic restraint]
```

### Lyrics / structure

```text
[Intro - opening texture and energy]

[Theme - principal instrument or motif]

[Development - how pulse, harmony, or orchestration changes]

[Interlude - contrast or reflection]

[Build - controlled rise in intensity]

[Climax - emotional high point]

[Outro - final texture and degree of resolution]
```

The section names are guides, not a mandatory form. Shorter episodes may only need three or four sections. Caption and structure must tell the same musical story—for example, do not request sparse piano in the caption and a distorted guitar climax in the structure unless that transition is deliberate.

## Generation and selection workflow

1. Finish the episode text and summarize its emotional arc in one sentence.
2. Draft the Caption and Lyrics / structure fields separately.
3. In ACE-Step, use `text2music`. Set an appropriate duration, and set BPM, key, and time signature only when the episode needs that control; otherwise allow the model to infer them.
4. Generate several candidates with different seeds. Batch generation is encouraged when VRAM allows.
5. Listen against the episode rather than judging the cue in isolation. Reject results that overwhelm the scene, introduce accidental vocals, or resolve an intentionally unresolved ending.
6. When tuning one parameter, hold the seed fixed so the comparison is meaningful. When exploring compositions, vary the seed.
7. Select a final candidate, export a lossless master and the delivery format needed by the publishing platform, then normalize/master conservatively without crushing the cue's dynamics.
8. Record enough information in the episode file to reproduce or audit the result.

## Episode production record

Under `## Production notes`, keep image and music records separate. Record:

```markdown
### Music

- Workflow: ACE-Step 1.5 text2music
- Model/checkpoint:
- Caption: |
    [exact caption]
- Lyrics / structure: |
    [exact structure prompt]
- Duration:
- BPM / key / time signature:
- Seed:
- Inference settings:
- Source output:
- Final master:
- Delivery file:
- Selection/mastering notes:
```

Do not replace exact prompts with summaries. Record the seed, checkpoint, duration, and non-default settings once a cue is selected. Generated audio files may be stored outside Git when they are too large; use stable paths or release/asset links rather than committing temporary renders.

## Episode 0001 prompt example

The first episode, **A New Day Dawns**, uses this starting prompt:

### Caption

```text
cinematic sci-fi ambient, deep pulsing synths, warm evolving strings, sparse piano, organ-like textures, intimate, atmospheric, melancholic, hopeful, spacious, restrained, futuristic
```

### Lyrics / structure

```text
[Intro - Sparse, atmospheric]

[Theme - Gentle piano and warm synths]

[Development - Pulsing, slowly expanding]

[Interlude - Quiet, reflective]

[Build - Strings rising, increasing intensity]

[Climax - Full, emotional, expansive]

[Outro - Fading, spacious, unresolved]
```

Use this as a formatting example, not as a universal Habitat Sol sound. Each episode should earn its own emotional arc and instrumentation.

## Licensing and provenance

ACE-Step 1.5 is published as an open-source project; record the exact model/checkpoint and the license information that applied when the cue was generated. Keep third-party reference audio, copyrighted melodies, artist-name imitation, and unlicensed samples out of prompts and inputs unless their use and publication rights are explicitly documented. Model licensing and generated-output usage terms can change, so verify the upstream repository before public release.
