# Habitat Sol ComfyUI workflow system

These version-controlled workflows support Habitat Sol's documentary visual-fiction production. **The active production stack is Qwen Image, not SDXL, Intorealism, IPAdapter, ControlNet, or Flux.**

Read `../../art-direction/visual-bible.md`, the relevant character sheet under `../../characters/`, and any episode image brief before changing prompts or references.

## Active Qwen stack

| Use | Diffusion model | Text encoder | VAE | Baseline |
|---|---|---|---|---|
| Character, location, patch, and transparent garment generation | `qwen_image_2512_fp8_e4m3fn.safetensors` | `qwen_2.5_vl_7b_fp8_scaled.safetensors` with `type: qwen_image` | `qwen_image_vae.safetensors` | 1104×1472 (or 1152×1536 for full body), Euler/simple, 50 steps, CFG 4.0, denoise 1.0 |
| Identity-preserving wardrobe-to-episode composition | `qwen_image_edit_fp8_e4m3fn.safetensors` | `qwen_2.5_vl_7b_fp8_scaled.safetensors` with `type: qwen_image` | `qwen_image_vae.safetensors` | 1152×1536, Euler/simple, 50 steps, CFG 4.0, denoise 1.0 |

Do not substitute an older SDXL/Intorealism/IPAdapter graph into this family. Qwen-Image-Edit is the identity-preserving edit route; text-only Qwen Image is for new reference, location, patch, and garment assets.

## Visual contract

Every workflow should preserve:

- municipal-archive/documentary realism rather than fashion editorial polish;
- a maintained, repaired, lived-in civilian town—not glossy sci-fi, luxury colonisation, or military space opera;
- practical layered/repaired clothes, worn textiles, condensation, dust at thresholds, utility hardware, and no generated readable text;
- subtle practical light and emotionally specific human situations;
- age-appropriate, non-sexualised depiction of children and teenagers.

## Current workflows

| File | Role | Start here |
|---|---|---|
| `01_character_forge.json` | UI workflow for a character's five canonical Qwen Image 2512 views. | Edit the identity prompt and preserve the 50-step / CFG 4.0 baseline. Approve portrait, three-quarter, profile, full body, and expression separately. |
| `05_habitat_patch_forge.json` | UI workflow for text-free, standalone habitat patch reference assets. | Generate the patch as a separate asset first; do not ask a character workflow to invent a canonical patch. |
| `06_transparent_wardrobe_asset_api.json` | API workflow for one transparent PNG garment asset. | Combine a character's `identity_guard`, wardrobe prompt, and the shared asset suffix from `../wardrobes/wardrobe-prompt-manifest.json`. |
| `07_wardrobe_to_episode_api.json` | API workflow for an episode image using person + garment + scene references. | Give inputs in fixed order: canonical person, approved transparent garment, scene/location reference. |
| `habitat_sol_patch_forge_api.json` | API-format counterpart for Qwen patch generation. | Use for scripted/API patch batches. |

`06` uses a temporary exact chroma-green background, `ImageColorToMask`, `InvertMask`, and `SaveImageWithAlpha` to produce a transparent RGBA garment PNG. The source garment must be checked for a real alpha channel, no green fringe, one complete silhouette, and no invented text/logos/patches before it becomes canonical.

`07` is a **semantic composition** workflow, not a flat overlay. Its Qwen-Image-Edit prompt assigns fixed roles to the batched images:

1. image 1 — canonical person identity;
2. image 2 — transparent wardrobe asset;
3. image 3 — scene/location reference.

It should preserve identity from image 1, garment silhouette/material/colour from image 2, and location/composition from image 3. Keep those assets separately versioned so an episode image never becomes the only source of truth for a person or garment.

## Legacy files

`habitat_sol_all_core_characters_api.json` and `habitat_sol_core_character_prompts.json` preserve an earlier Flux/LoRA character-prompt experiment. They are **not part of the active Qwen production path** and must not be used as the model/settings authority for new references or episodes.

## Running and selecting

1. In ComfyUI, open `workflows/habitat-sol/` and choose the relevant UI workflow, or run the API-format JSON through the ComfyUI API.
2. Use the Qwen baseline above for a production candidate. Small 4-step, 512×768 runs are execution smoke tests only—not art-selection candidates.
3. Review in this order: identity/age, subject count, garment accuracy, action/framing, Habitat Sol material evidence, then light/tone.
4. Reject drift rather than rationalising it: wrong age, extra/missing person, unreadable generated text, invented competing marks, glamour, generic space set, or a non-transparent garment background.
5. Save selected identity and garment assets to tracked character paths; keep transient candidates in ignored output paths.

## Reproducibility record

For every selected asset or episode image, capture:

- workflow filename and graph revision;
- exact Qwen model, text encoder, and VAE filenames;
- source person, garment, and scene-reference paths where applicable;
- complete positive and negative prompts;
- seed, resolution, sampler, scheduler, steps, CFG, and denoise;
- selected output path and publication status.
