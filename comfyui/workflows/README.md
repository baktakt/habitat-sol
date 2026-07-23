# Habitat Sol ComfyUI workflows

## `habitat_sol_all_core_characters_api.json`

API-format ComfyUI workflow that contains all eight current core character portrait branches:

1. Amara Okonkwo
2. Elena Reyes
3. Nico Okonkwo-Reyes
4. Safi Okonkwo-Reyes
5. Mira Varga
6. Kenji Sato
7. Lina Sato-Varga
8. Tomas Sato-Varga

Each branch has its own detailed positive/negative prompt and its own LoRA strengths. Adults use the full Habitat Sol realism/portrait/concept stack. Minors use reduced style strength. Tomas disables the portrait/concept LoRAs by default because they tended to push him toward toddler/headgear imagery.

Base checkpoint: `FLUX1/flux1-dev-fp8.safetensors`

Default LoRAs:

- `Krea2-realism-V1.safetensors`
- `HabitatSol/Portrait-Engine-FLUX-v1.safetensors`
- `HabitatSol/ck-Sommo-Concept-Art-FLUX.safetensors`

Prompt manifest: `habitat_sol_core_character_prompts.json`

## Qwen text encoder note

The local ComfyUI has `qwen_3_8b.safetensors` in `models/text_encoders`. I tested it as the second encoder in a Flux-style `DualCLIPLoader` probe for Lina using `flux1-dev.safetensors` + `clip_l.safetensors` + `qwen_3_8b.safetensors`; the run completed but decoded to a near-black failed image. For the current `FLUX1/flux1-dev-fp8.safetensors` character workflow, Qwen is therefore **not better** than the proven Flux CLIP/T5 encoding path. If a true Qwen Image / Flux-2 character workflow becomes the preferred base, port these prompts into that graph and compare outputs again.
