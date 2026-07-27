# Habitat Sol wardrobe system

This folder is the canonical prompt library for **transparent PNG wardrobe assets**. It is not a fashion collection: every garment must belong to a maintained, repaired, civilian Mars town and support a character's story role.

## Production chain

```text
wardrobe prompt manifest
  → 06_transparent_wardrobe_asset_api.json
  → selected transparent PNG garment asset
  → 07_wardrobe_to_episode_api.json + canonical person reference + scene reference
  → selectable episode frame
```

`06_transparent_wardrobe_asset_api.json` generates one front-on garment on an exact chroma-green field, converts that field to a mask, inverts the mask, and writes a PNG with alpha through `SaveImageWithAlpha`. It deliberately creates a design asset—not a person wearing it.

`07_wardrobe_to_episode_api.json` provides Qwen-Image-Edit with three ordered references:

1. approved canonical character reference;
2. transparent garment asset;
3. scene/location reference.

It asks Qwen to preserve the first image's identity, use the second image's clothing design, and honour the third image's setting and composition. It is a **semantic clothing application**, not a naive flat PNG overlay: the model adapts fabric fit, folds, light, and pose to the person and scene.

## How to make a garment set

1. Open `wardrobe-prompt-manifest.json` and choose one character and one `wardrobes[]` entry.
2. In workflow 06, replace the default prompt with:

   ```text
   [identity_guard] [wardrobe.prompt] [global_asset_suffix]
   ```

   Keep the shared negative prompt unless an observed failure needs a narrow additional exclusion.
3. Change `CHARACTER_SLUG` and `ASSET_SLUG` in `SaveImageWithAlpha` to match the manifest. Generate candidates and reject any with green fringe, a non-transparent background, a cropped sleeve/hem, generated text, or a competing mark.
4. Copy the selected alpha PNG into a tracked canonical path, for example:

   ```text
   characters/varga-sato family/mira varga/wardrobes/greenhouse_jacket_v1.png
   ```

   Generated image files are intentionally not committed until they pass review.
5. For an episode, upload/select the canonical person reference, selected garment PNG, and scene reference in workflow 07. Replace its prompt only with the specific action, framing, and scene facts needed for the episode; retain its fixed image-role instructions.
6. Record the selected output under the episode's `## Production notes`: source person reference, wardrobe asset, scene reference, model filenames, seed, settings, full positive/negative prompts, workflow filename, output path, and selection status.

## Guardrails

- Garments are **plain and unmarked** by default. Do not ask the model to invent patches, labels, or readable signage. Approved patch masters are separate assets and should be composited/integrated in a later masked pass.
- The source garment must be read at thumbnail size before it is approved. A convincing episode frame does not repair an ambiguous clothing asset.
- Children and teenagers keep their explicit age safeguards in the manifest. Do not make them adult-coded, fashionable in an adult sense, glamorous, revealing, or military-styled.
- Keep the person identity, garment design, and scene reference as separately versioned assets. This makes clothing reusable across episodes without making any one generated scene canonical.

## Current set coverage

The manifest supplies three starting garments for each of the eight core characters: work/civic, everyday/school, and alternate shift or location-specific layers—**24 prompts in total**. Add a new garment only after it has a story use and an unambiguous owner.
