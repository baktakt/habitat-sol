# Habitat Sol ComfyUI workflow system

These are **ComfyUI UI workflow JSON files** for the Habitat Sol visual micro-series. They are version-controlled mirrors of the copies installed in ComfyUI's `workflows/habitat-sol/` browser folder.

## Visual contract

Every workflow carries the project rules in its visible group descriptions and default prompts:

- documentary, municipal-archive realism; intimate observation rather than heroic spectacle;
- a maintained, repaired, lived-in civilian town—not glossy sci-fi, luxury colonization, or military space opera;
- practical layered/repaired clothing, worn textiles, condensation, dust at thresholds, utility hardware, and abstract/unreadable labels;
- restrained practical light rather than extreme orange-and-teal grading;
- no generated readable text; faces and human situations outrank equipment;
- children and teenagers are always age-appropriate and non-sexualized.

Read `../../art-direction/visual-bible.md` and the named character sheet under `../../characters/` before replacing workflow prompt placeholders.

## Workflows

| File | Purpose | Normal starting point |
|---|---|---|
| `01_character_forge.json` | Build the approved canonical reference set for one recurring character. | Generate candidate batches, then select references deliberately. |
| `02_episode_single_character.json` | Place one approved character into a new episode scene using reference-image identity conditioning. | Use one to three approved references and a new story frame. |
| `03_episode_multi_character_inpaint.json` | Make a two-character scene in staged, separate identity-conditioned inpaint passes. | Start with an approved background/composition and non-overlapping masks. |
| `04_repair_character_region.json` | Correct one region in an approved image without regenerating the rest. | Load the approved source and paint only the failed region. |
| `06_transparent_wardrobe_asset_api.json` | Generate one transparent PNG garment asset from a manifest prompt. | Create and approve one garment before it is used on a character. |
| `07_wardrobe_to_episode_api.json` | Use a canonical person reference, transparent garment asset, and scene reference to generate an episode frame. | Preserve identity from image 1, clothing from image 2, and location/composition from image 3. |
## Open and save

1. In ComfyUI, refresh the workflow browser and open **`workflows/habitat-sol/`**.
2. Open the desired JSON. The coloured groups are intentionally numbered in production order.
3. Use the image widgets to upload/select references, base images, pose/depth maps, and masks. ComfyUI stores uploaded inputs in its input directory.
4. Change the `SaveImage` prefix before queuing. Never use the source image prefix for a repair.
5. Record the selected image's final prompt, reference names, seed, checkpoint, adapter strength, resolution, and output path in the episode's `## Production notes`.

## Canonical character references

Run `01_character_forge.json` for a single character and approve, at minimum:

1. front or near-front portrait;
2. three-quarter portrait;
3. full-body image;
4. neutral environmental image;
5. expression variation;
6. canonical outfit variation.

Save the selected images under the project's durable character-reference location, using clear names such as `characters/amara-okonkwo/reference-front.png`. Do not make a generated image canonical merely because it is attractive: compare it against the relevant character sheet first.

## Episode workflow: what to change

### Keep stable unless testing deliberately

- **Checkpoint:** `N/intorealismUltra_v40.safetensors`
- **Identity adapter:** installed `ip-adapter-plus-face_sdxl_vit-h.safetensors`
- **CLIP Vision:** installed `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors`
- **Sampling baseline:** 896 × 1152, DPM++ 2M SDE, Karras, 30 steps, CFG 4.5
- **IPAdapter reference strength:** start at 0.78; test roughly 0.65–0.85 before changing prompt wording

### Change per episode

- approved reference image(s), canonical identity anchors, and character-specific negative safeguards;
- one precise episode action/emotion; location/material details; camera/composition; practical light;
- seed and resolution when composition needs a different format;
- save prefix, e.g. `habitat-sol/episodes/0042`.

The episode workflow batches up to three approved images and averages their identity signal. This preserves the person while permitting a different pose, framing, clothing, location, and camera. It is not basic img2img.

### Pose and depth

`02_episode_single_character.json` has a Union SDXL ControlNet branch. Supply a **preprocessed** pose or depth map to its image input and set the node's control mode/strength for the map you supplied; disconnect that branch when not using composition guidance. No OpenPose/DWPose preprocessor was installed at validation time, so the workflow deliberately does not pretend to preprocess a raw photograph.

## Multi-character masks

`03_episode_multi_character_inpaint.json` avoids prompt-only group identity blending:

1. Load a base scene/background.
2. Paint/select **mask A**: white where Character A may change, black elsewhere.
3. Use Character A's reference, identity/action prompt, strength, and the conservative inpaint pass.
4. The decoded A result becomes the input for Character B.
5. Paint/select **mask B**; keep it separate from A where possible.
6. Use Character B's separate reference, prompt, and strength.
7. Inspect both faces/hands and use final repair only when it helps.

Defaults use expanded, feathered masks, noise masks, and 0.55 inpaint denoise. Start around 0.45 for a small correction, 0.55 for a normal replacement, and 0.65 only when the failed region needs a larger change.

## Region repair

`04_repair_character_region.json` is for face drift, hair/age mismatch, clothing inconsistency, bad hands, expression, accessories, or a signature detail. It preserves the rest of the approved image through a mask-constrained `InpaintModelConditioning` pass. Use a generous but not scene-wide mask, feather it, and save to `.../repaired`; it never overwrites a source.

## Later: character LoRAs

Reference conditioning is the initial system and should remain the baseline until a character has enough approved, varied references and recurring production reveals a measurable identity problem. Consider a character LoRA only when:

- the character recurs frequently;
- their approved reference set is stable and canon-reviewed;
- IPAdapter Plus repeatedly fails under the required poses/outfits/camera distances;
- training images and consent/provenance are documented; and
- the LoRA is tested against this baseline rather than silently replacing it.

The workflows use `CheckpointLoaderSimple`, so a later compatible `LoraLoader` can be placed between it and the generation/identity nodes without redesigning the workflow family.

## Reproducibility checklist

- exact workflow filename and graph revision;
- checkpoint, adapter, clip-vision model, ControlNet if used, and upscaler if used;
- character reference filenames and identity strength;
- prompt and negative prompt, unabridged;
- seed, resolution, sampler, scheduler, steps, CFG, denoise, and ControlNet strength;
- selected output path and publication status.
