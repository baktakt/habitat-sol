#!/usr/bin/env python3
"""Build the two API-format wardrobe workflows mirrored in comfyui/workflows/."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "comfyui" / "workflows"

NEGATIVE = (
    "cartoon, anime, illustration, painting, fashion editorial, glamour photography, "
    "mannequin, person, face, hands, body, duplicate garment, clothing rack, hanger, "
    "floor, wall, studio set, background object, readable text, letters, numbers, logo, "
    "watermark, signature, badge, decal, insignia, patch, extra pocket, extra sleeve, "
    "extra garment, armor, military uniform, glossy generic sci-fi, plastic fabric, "
    "deformed garment, cropped garment"
)

ASSET_PROMPT = (
    "ONE standalone Habitat Sol wardrobe garment asset only, no person: Mira Varga greenhouse "
    "duty outer layer, olive-green hip-length work jacket with rolled sleeves, plain reinforced "
    "cuffs, shallow utility pockets, subtle visible mending, realistic worn canvas and soft "
    "thermal lining, no marks or graphics. Front-on orthographic product-documentary view, "
    "complete garment fully visible with generous empty margin on every side, symmetrical neutral "
    "lay-flat silhouette, sleeves slightly separated from torso, isolated against one perfectly "
    "flat pure chroma-green #00FF00 background, no ground plane, no shadow, no gradient, no prop, "
    "no hanger. The green background is temporary and will be converted to transparency. "
    "Habitat Sol civilian workwear: repairable, practical, modest, never fashion styling, "
    "natural fabric weave, no readable text."
)

EPISODE_PROMPT = (
    "The supplied images have fixed roles: image 1 is the approved canonical person identity; "
    "image 2 is a transparent wardrobe asset; image 3 is a scene/location reference. Preserve "
    "the exact recognisable facial identity, age, hair, body build, and age-appropriate presentation "
    "of image 1. Dress that same person in the exact garment silhouette, colour, material, and repair "
    "details from image 2, adapting folds and fit naturally to their pose. Place them in the practical "
    "Habitat Sol setting, composition, and light of image 3. Full-body environmental documentary frame, "
    "head to boots visible, natural stance and hands, maintained but aging civilian Mars town, worn textiles, "
    "quiet practical light. Do not add labels, letters, logos, badges, decals, extra garments, extra people, "
    "or fashion/editorial styling."
)


def ref(node: str, output: int = 0):
    return [node, output]


def make_asset_workflow() -> dict:
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE, "clip": ref("2")}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"text": ASSET_PROMPT, "clip": ref("2")}},
        "6": {"class_type": "EmptyLatentImage", "inputs": {"width": 1152, "height": 1536, "batch_size": 1}},
        "7": {"class_type": "KSampler", "inputs": {"seed": 6601210031, "control_after_generate": "increment", "steps": 50, "cfg": 4.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0, "model": ref("1"), "positive": ref("5"), "negative": ref("4"), "latent_image": ref("6")}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ref("7"), "vae": ref("3")}},
        "9": {"class_type": "ImageColorToMask", "inputs": {"image": ref("8"), "color": 65280}},
        "10": {"class_type": "InvertMask", "inputs": {"mask": ref("9")}},
        "11": {"class_type": "SaveImageWithAlpha", "inputs": {"images": ref("8"), "mask": ref("10"), "filename_prefix": "HabitatSol/wardrobe/CHARACTER_SLUG/ASSET_SLUG_v1"}},
    }


def make_episode_workflow() -> dict:
    return {
        "1": {"class_type": "LoadImage", "inputs": {"image": "canonical_person_reference.png"}},
        "2": {"class_type": "LoadImage", "inputs": {"image": "transparent_wardrobe_asset.png"}},
        "3": {"class_type": "LoadImage", "inputs": {"image": "scene_reference.png"}},
        "4": {"class_type": "ImageScale", "inputs": {"image": ref("1"), "upscale_method": "lanczos", "width": 1152, "height": 1536, "crop": "center"}},
        "5": {"class_type": "ImageScale", "inputs": {"image": ref("2"), "upscale_method": "lanczos", "width": 1152, "height": 1536, "crop": "center"}},
        "6": {"class_type": "ImageScale", "inputs": {"image": ref("3"), "upscale_method": "lanczos", "width": 1152, "height": 1536, "crop": "center"}},
        "7": {"class_type": "ImageBatch", "inputs": {"image1": ref("4"), "image2": ref("5")}},
        "8": {"class_type": "ImageBatch", "inputs": {"image1": ref("7"), "image2": ref("6")}},
        "9": {"class_type": "UNETLoader", "inputs": {"unet_name": "qwen_image_edit_fp8_e4m3fn.safetensors", "weight_dtype": "default"}},
        "10": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image", "device": "default"}},
        "11": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "12": {"class_type": "TextEncodeQwenImageEdit", "inputs": {"clip": ref("10"), "vae": ref("11"), "image": ref("8"), "prompt": EPISODE_PROMPT}},
        "13": {"class_type": "CLIPTextEncode", "inputs": {"text": "cartoon, anime, illustration, painting, glamour photography, fashion editorial, plastic skin, waxy skin, bad anatomy, deformed hands, extra fingers, duplicate person, duplicate face, extra person, readable text, letters, numbers, logo, watermark, armor, superhero, military sci-fi, glossy spaceship set", "clip": ref("10")}},
        "14": {"class_type": "EmptyLatentImage", "inputs": {"width": 1152, "height": 1536, "batch_size": 1}},
        "15": {"class_type": "KSampler", "inputs": {"seed": 6601210032, "control_after_generate": "increment", "steps": 50, "cfg": 4.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0, "model": ref("9"), "positive": ref("12"), "negative": ref("13"), "latent_image": ref("14")}},
        "16": {"class_type": "VAEDecode", "inputs": {"samples": ref("15"), "vae": ref("11")}},
        "17": {"class_type": "SaveImage", "inputs": {"filename_prefix": "HabitatSol/episodes/EPISODE_ID/CHARACTER_SLUG__WARDROBE_SLUG", "images": ref("16")}},
    }


for filename, payload in {
    "06_transparent_wardrobe_asset_api.json": make_asset_workflow(),
    "07_wardrobe_to_episode_api.json": make_episode_workflow(),
}.items():
    (OUT / filename).write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {OUT / filename}")
