# Habitat Sol ComfyUI workflow manifest

## Validated environment

| Field | Value |
|---|---|
| Validation date | 2026-07-24 |
| ComfyUI | `0.28.0` |
| Frontend | `comfyui-frontend-package 1.47.10` |
| Templates | `comfyui-workflow-templates 0.11.15` |
| Runtime | local Git deployment, Python 3.14.4, PyTorch 2.13.0+cu130 |
| GPU | NVIDIA GeForce RTX 3090, 24 GB VRAM |
| ComfyUI base directory | `/home/baktakt/ai-lab/data/comfyui` |
| Models directory | `/home/baktakt/ai-lab/models/comfyui` |
| Output directory | `/home/baktakt/ai-lab/output/comfyui` |
| Active workflow user directory | `/home/baktakt/ai-lab/data/comfyui/user/default/workflows/habitat-sol/` |
| Repository mirror | `comfyui/workflows/` |

The server launch arguments establish the base/models/output directories. No `--user-directory` or multi-user username argument was present, so ComfyUI's active standard user is `default`.

## Selected production stack

| Component | Selected item | Why |
|---|---|---|
| Checkpoint | `N/intorealismUltra_v40.safetensors` | Exact preferred checkpoint was installed; used for all four SDXL workflows. |
| VAE | Checkpoint-bundled VAE | The checkpoint loader exposes a VAE output; no separate VAE is hard-coded. |
| Primary identity method | IPAdapter Plus Face for SDXL | Installed `ip-adapter-plus-face_sdxl_vit-h.safetensors` plus installed CLIP Vision, with separate reference conditioning for staged characters. |
| CLIP Vision | `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` | Installed and connected explicitly. |
| Pose/depth control | Union SDXL ControlNet | Installed `SDXL/controlnet-union-sdxl-1.0/diffusion_pytorch_model_promax.safetensors`; direct preprocessed maps only. |
| Face/detail repair | `04_repair_character_region.json` | Reliable mask-constrained identity-conditioned inpainting; the registered `FaceFixerOpenCV` class was excluded because its OpenCV dependency fails at execution. |
| Optional upscale | `4x-ClearRealityV1_Soft.pth` | Installed; selected to avoid the plastic sharpening tendency of UltraSharp. |

### Identity-method decision

PuLID was not present in `/object_info`. `IPAdapterUnifiedLoaderFaceID` was registered, but the installed IPAdapter model list did **not** include an SDXL FaceID/FaceID Plus v2 weight and `/models/insightface` was unavailable. Therefore the delivered system uses the next available proven option: **IPAdapter Plus Face SDXL**, with one to three approved reference images for a single-character scene and separate staged inpaint passes for two-character scenes. No character LoRA is required.

## Required registered node packages / classes

The active `/object_info` advertised the following classes used by these graphs:

- Core ComfyUI: `CheckpointLoaderSimple`, `CLIPTextEncode`, `EmptyLatentImage`, `KSampler`, `VAEDecode`, `LoadImage`, `LoadImageMask`, `ImageBatch`, `ConditioningCombine`, `SaveImage`, `ControlNetLoader`, `ControlNetApplyAdvanced`, `InpaintModelConditioning`, `ImageUpscaleWithModel`, `UpscaleModelLoader`.
- IPAdapter integration: `IPAdapterModelLoader`, `IPAdapterAdvanced`, `CLIPVisionLoader`.
- Installed custom utilities: `GrowMaskWithBlur`, `FaceFixerOpenCV`.

No new custom-node package or model was installed by this change.

## Workflow files

| UI workflow | Installed workflow path | Repository mirror |
|---|---|---|
| `01_character_forge.json` | `user/default/workflows/habitat-sol/01_character_forge.json` | `comfyui/workflows/01_character_forge.json` |
| `02_episode_single_character.json` | `user/default/workflows/habitat-sol/02_episode_single_character.json` | `comfyui/workflows/02_episode_single_character.json` |
| `03_episode_multi_character_inpaint.json` | `user/default/workflows/habitat-sol/03_episode_multi_character_inpaint.json` | `comfyui/workflows/03_episode_multi_character_inpaint.json` |
| `04_repair_character_region.json` | `user/default/workflows/habitat-sol/04_repair_character_region.json` | `comfyui/workflows/04_repair_character_region.json` |
| `06_transparent_wardrobe_asset_api.json` | API template; store alongside the workflow browser copy when installed | `comfyui/workflows/06_transparent_wardrobe_asset_api.json` |
| `07_wardrobe_to_episode_api.json` | API template; store alongside the workflow browser copy when installed | `comfyui/workflows/07_wardrobe_to_episode_api.json` |

## Validation record

- JSON parsing: every delivered UI workflow parses successfully.
- UI graph structure: unique IDs, links, node ports, group metadata, and widget values are checked by the repository validator.
- Live node validation: each referenced node class was found in the live `1749`-node `/object_info` catalog.
- Model validation: checkpoint, IPAdapter, CLIP Vision, ControlNet, and upscaler names were checked against the active server's model endpoints.
- Installation validation: installed copies are byte-identical to repository mirrors and are listed through ComfyUI userdata workflow browsing after refresh.
- Execution validation: `01_character_forge` generation path completed at 512×512 / 8 steps and wrote `habitat-sol/smoke/01_character_forge_00001_.png`. The four delivered UI graphs were node/model/link validated live; full identity/inpaint runs still require deliberate uploaded canonical references and painted masks, which were not fabricated for smoke testing.

## Limitations and future enhancements

1. **No raw-pose preprocessing node was installed.** Use a preprocessed OpenPose/DWPose/depth image with the Union ControlNet branch, or install a compatible preprocessor only after approval.
2. **No validated PuLID or SDXL FaceID Plus v2 weight was available.** IPAdapter Plus Face SDXL is the current identity fallback.
3. **Face repair is optional and conservative.** It should be bypassed if it makes a selected image less faithful; regional workflow 04 is the primary targeted repair mechanism.
4. **The optional 4× upscaler can create very large output.** Use it selectively or resize the result in a downstream approved process.
5. **Workflow graphs are designed for reference-conditioning, not basic img2img.** This is deliberate: episode camera, pose, setting, and clothing may change independently of an approved portrait.
