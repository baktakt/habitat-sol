# Habitat Sol ComfyUI workflow manifest

## Validated environment

| Field | Value |
|---|---|
| Validation date | 2026-07-27 |
| ComfyUI | `0.28.0` |
| Runtime | local Git deployment, Python 3.14.4, PyTorch 2.13.0+cu130 |
| GPU | NVIDIA GeForce RTX 3090, 24 GB VRAM |
| ComfyUI base directory | `/home/baktakt/ai-lab/data/comfyui` |
| Models directory | `/home/baktakt/ai-lab/models/comfyui` |
| Output directory | `/home/baktakt/ai-lab/output/comfyui` |
| Active workflow user directory | `/home/baktakt/ai-lab/data/comfyui/user/default/workflows/habitat-sol/` |
| Repository mirror | `comfyui/workflows/` |

## Active production stack

| Component | Selected item | Use |
|---|---|---|
| Qwen Image diffusion model | `qwen_image_2512_fp8_e4m3fn.safetensors` | Character forge, patch forge, and transparent garment generation. |
| Qwen Image Edit diffusion model | `qwen_image_edit_fp8_e4m3fn.safetensors` | Identity-preserving person + garment + scene composition. |
| Text encoder | `qwen_2.5_vl_7b_fp8_scaled.safetensors`, `type: qwen_image` | Used with both Qwen Image and Qwen-Image-Edit. |
| VAE | `qwen_image_vae.safetensors` | Used with both active diffusion models. |
| Qwen Image baseline | 1104×1472 (or 1152×1536 full body), Euler/simple, 50 steps, CFG 4.0, denoise 1.0 | Production candidate settings for Qwen Image 2512. |
| Qwen Image Edit baseline | 1152×1536, Euler/simple, 50 steps, CFG 4.0, denoise 1.0 | Production candidate settings for the identity-preserving edit path. |

The active Habitat Sol workflow family does **not** use `N/intorealismUltra_v40.safetensors`, SDXL, IPAdapter, CLIP Vision, Union ControlNet, or a 4× upscaler. Those belonged to a superseded workflow design and must not be treated as a production dependency.

## Registered node classes used by active graphs

- Qwen generation: `UNETLoader`, `CLIPLoader`, `VAELoader`, `CLIPTextEncode`, `EmptyLatentImage`, `KSampler`, `VAEDecode`, `SaveImage`.
- Qwen image edit: `LoadImage`, `ImageScale`, `ImageBatch`, `TextEncodeQwenImageEdit`, plus the Qwen generation classes above.
- Transparent garments: `ImageColorToMask`, `InvertMask`, `SaveImageWithAlpha`.

## Tracked workflow files

| File | Format | Model path | Purpose |
|---|---|---|---|
| `01_character_forge.json` | ComfyUI UI graph | Qwen Image 2512 | Five canonical character-reference views. |
| `05_habitat_patch_forge.json` | ComfyUI UI graph | Qwen Image 2512 | Text-free standalone habitat patch references. |
| `06_transparent_wardrobe_asset_api.json` | API graph | Qwen Image 2512 | One single-garment RGBA PNG asset on a removable chroma-green background. |
| `07_wardrobe_to_episode_api.json` | API graph | Qwen-Image-Edit | Compose canonical person identity, approved garment, and scene reference into an episode candidate. |
| `habitat_sol_patch_forge_api.json` | API graph | Qwen Image 2512 | Script/API counterpart of the patch forge. |

`habitat_sol_all_core_characters_api.json` and `habitat_sol_core_character_prompts.json` are retained historical Flux/LoRA prompt material. They are excluded from the active model stack and should not be updated for Qwen production.

## Validation record

- All current Qwen workflow JSON files parse successfully.
- The live `/object_info` catalog confirmed every class used by workflows 06 and 07, including `TextEncodeQwenImageEdit`, `ImageColorToMask`, `InvertMask`, and `SaveImageWithAlpha`.
- The exact active Qwen Image, Qwen-Image-Edit, text-encoder, and VAE filenames were confirmed in the live loader selectors.
- Workflow 06 executed as a 512×768 / 4-step smoke test and produced an RGBA PNG with both transparent and opaque pixels.
- Workflow 07 executed as a 512×768 / 4-step smoke test with canonical person, transparent garment, and scene inputs. This validates the graph path only; it is not an approved production image.

## Selection and limitations

1. Small 4-step smoke tests validate execution, not visual quality or wardrobe fidelity. Use the documented Qwen production settings before selecting an asset.
2. Qwen-Image-Edit may drift from an input garment at weak settings. Reject a result that changes the intended garment colour, silhouette, age, person identity, or scene facts; do not make a prompt-only correction canonical.
3. Transparent asset generation can leave green fringe or imperfect mask edges. Inspect alpha and pixels, then regenerate or use a narrow edge-repair pass before approval.
4. Keep identity reference, garment asset, scene reference, and selected episode frame as separate versioned assets.
5. Do not install or reintroduce SDXL/IPAdapter/ControlNet components merely to satisfy this workflow family; Qwen is the current source of truth.
