#!/usr/bin/env python3
"""Build Habitat Sol ComfyUI UI workflow JSON files from the live node catalog.

The graphs intentionally use only node types confirmed by the active ComfyUI
server. They target the installed SDXL realism checkpoint and IPAdapter Plus
reference conditioning; no LoRA is required for identity.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "comfyui" / "workflows"
CKPT = "N/intorealismUltra_v40.safetensors"
IPADAPTER = "ip-adapter-plus-face_sdxl_vit-h.safetensors"
CLIP_VISION = "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"
CONTROLNET = "SDXL/controlnet-union-sdxl-1.0/diffusion_pytorch_model_promax.safetensors"
UPSCALER = "4x-ClearRealityV1_Soft.pth"

VISUAL_RULES = (
    "HABITAT SOL VISUAL RULES — documentary realism, not fashion photography; "
    "intimate and observational, never heroic; worn, maintained and repaired civilian "
    "habitats; used civic technology, not magical equipment; no glossy generic sci-fi, "
    "military space opera, superhero poses, orange/teal grading, or readable generated text; "
    "practical layered repaired clothing specific to the person; children and teenagers are "
    "always age-appropriate and non-sexualized; Mars is a lived-in town; faces and human "
    "situations matter more than equipment."
)
NEGATIVE = (
    "low quality, blurry, plastic skin, waxy skin, anime, cartoon, fashion editorial, "
    "glossy generic science-fiction, military space opera, superhero pose, spacesuit glamour, "
    "orange and teal color grade, readable text, logo, watermark, deformed hands, extra fingers, "
    "duplicate people, cropped face"
)

class Graph:
    def __init__(self, name: str):
        self.name = name
        self.nodes: list[dict] = []
        self.links: list[list] = []
        self.groups: list[dict] = []
        self._node = 0
        self._link = 0

    def node(self, typ: str, title: str, pos: tuple[int, int], widgets: list | None = None,
             size: tuple[int, int] = (315, 110), inputs: list | None = None,
             outputs: list | None = None) -> int:
        self._node += 1
        n = {
            "id": self._node, "type": typ, "title": title, "pos": list(pos), "size": list(size),
            "flags": {}, "order": self._node - 1, "mode": 0,
            "inputs": inputs or [], "outputs": outputs or [],
            "properties": {"Node name for S&R": typ},
        }
        if widgets is not None:
            n["widgets_values"] = widgets
        self.nodes.append(n)
        return self._node

    def link(self, src: int, src_slot: int, dst: int, dst_slot: int, typ: str) -> None:
        self._link += 1
        self.links.append([self._link, src, src_slot, dst, dst_slot, typ])
        for n in self.nodes:
            if n["id"] == src:
                n["outputs"][src_slot].setdefault("links", []).append(self._link)
            if n["id"] == dst:
                n["inputs"][dst_slot]["link"] = self._link

    def group(self, title: str, bbox: tuple[int, int, int, int], color: str, description: str = "") -> None:
        d = {"title": title, "bounding": list(bbox), "color": color, "font_size": 22}
        if description:
            d["properties"] = {"description": description}
        self.groups.append(d)

    def save(self, filename: str, description: str) -> None:
        x = {
            "last_node_id": self._node, "last_link_id": self._link, "nodes": self.nodes,
            "links": self.links, "groups": self.groups, "config": {},
            "extra": {"ds": {"scale": 0.8, "offset": [0, 0]}, "habitat_sol_notes": description},
            "version": 0.4,
        }
        (OUT / filename).write_text(json.dumps(x, indent=2) + "\n")

# Port helpers. Slot ordering follows the active server's /object_info.
def inp(name: str, typ: str) -> dict: return {"name": name, "type": typ, "link": None}
def out(name: str, typ: str) -> dict: return {"name": name, "type": typ, "links": []}
def checkpoint(g, p=(40, 250)):
    return g.node("CheckpointLoaderSimple", "MODEL — IntoRealism Ultra v4.0 (SDXL)", p, [CKPT], outputs=[out("MODEL", "MODEL"), out("CLIP", "CLIP"), out("VAE", "VAE")])
def text(g, title, p, value):
    return g.node("CLIPTextEncode", title, p, [value], inputs=[inp("clip", "CLIP")], outputs=[out("CONDITIONING", "CONDITIONING")])
def sampler(g, title, p, seed=2407187, steps=30, cfg=4.5, denoise=1.0):
    return g.node("KSampler", title, p, [seed, "fixed", steps, cfg, "dpmpp_2m_sde", "karras", denoise],
                  inputs=[inp("model", "MODEL"), inp("positive", "CONDITIONING"), inp("negative", "CONDITIONING"), inp("latent_image", "LATENT")], outputs=[out("LATENT", "LATENT")])
def loadimage(g, title, p, filename="Flux2-Klein_00005_.png"):
    return g.node("LoadImage", title, p, [filename], outputs=[out("IMAGE", "IMAGE"), out("MASK", "MASK")])
def maskload(g, title, p, filename="Flux2-Klein_00005_.png"):
    return g.node("LoadImageMask", title, p, [filename, "alpha"], outputs=[out("MASK", "MASK")])
def ipadapter(g, title, p):
    return g.node("IPAdapterModelLoader", title, p, [IPADAPTER], outputs=[out("IPADAPTER", "IPADAPTER")])
def clipvision(g, p):
    return g.node("CLIPVisionLoader", "CLIP VISION — installed ViT-H", p, [CLIP_VISION], outputs=[out("CLIP_VISION", "CLIP_VISION")])
def ipapply(g, title, p, weight=0.78):
    return g.node("IPAdapterAdvanced", title, p, [weight, "linear", "average", 0.0, 1.0, "V only"],
        inputs=[inp("model", "MODEL"), inp("ipadapter", "IPADAPTER"), inp("image", "IMAGE"), inp("image_negative", "IMAGE"), inp("attn_mask", "MASK"), inp("clip_vision", "CLIP_VISION")], outputs=[out("MODEL", "MODEL")])
def decode(g, p): return g.node("VAEDecode", "DECODE", p, [], inputs=[inp("samples", "LATENT"), inp("vae", "VAE")], outputs=[out("IMAGE", "IMAGE")])
def facefix(g, p, seed=2407187):
    return g.node("FaceFixerOpenCV", "FACE REPAIR — conservative; bypass if not needed", p,
        [seed, 1024, 32, 1.2, 8, 0.30, "combined", "dpmpp_2m_sde", "karras", 4.5, 18],
        inputs=[inp("image", "IMAGE"), inp("base_model", "MODEL"), inp("vae", "VAE"), inp("positive_cond_base", "CONDITIONING"), inp("negative_cond_base", "CONDITIONING")], outputs=[out("IMAGE", "IMAGE")])
def saveimage(g, title, p, prefix): return g.node("SaveImage", title, p, [prefix], inputs=[inp("images", "IMAGE")])

def character_forge():
    g = Graph("character forge")
    g.group("1 — Character Definition", (20, 20, 1010, 600), "#805c3b", "Edit the stable identity description and candidate count. " + VISUAL_RULES)
    g.group("2 — Model and Style", (20, 660, 900, 420), "#526d5d", "IntoRealism Ultra v4.0 SDXL defaults: 896×1152, 30 steps, DPM++ 2M SDE, Karras, CFG 4.5.")
    g.group("3 — Optional Pose", (970, 660, 350, 420), "#526d5d", "This first version is prompt-led. Use the episode workflow for supplied ControlNet pose/depth maps.")
    g.group("4 — Generation", (1370, 20, 900, 600), "#3e627c", "Batch size creates candidate variations. Keep the seed fixed while comparing prompt changes.")
    g.group("5 — Face Review", (2320, 20, 750, 600), "#8a5f52", "Review face, hands, hair and clothing at full size. Use 04_repair_character_region.json for a targeted identity-conditioned correction; automatic FaceFixerOpenCV is excluded because its live dependency is broken.")
    g.group("6 — Output", (3120, 20, 380, 600), "#6a6a6a", "Approve a front/near-front portrait, three-quarter portrait, full body, neutral environment, expression variation, and canonical outfit variation before episode production.")
    ck = checkpoint(g)
    ident = text(g, "CHARACTER DEFINITION — edit name, age, heritage, face, hair, body, wardrobe, anchors", (390, 90),
        "CHARACTER_NAME, [age], [heritage], [face shape and distinctive features], [hair], [body type], [practical canonical clothing and palette], [two visual anchors]; front or near-front full body documentary character reference in a quiet lived-in Habitat Sol interior; practical layered repaired clothing; emotionally neutral observant expression; " + VISUAL_RULES)
    neg = text(g, "NEGATIVE PROMPT", (390, 360), NEGATIVE)
    latent = g.node("EmptyLatentImage", "CANVAS — editable portrait/full-body resolution + candidates", (1010, 760), [896, 1152, 4], outputs=[out("LATENT", "LATENT")])
    ks = sampler(g, "GENERATION — seed / steps / CFG / sampler / scheduler / denoise", (1420, 250))
    dec = decode(g, (1880, 270))
    save = saveimage(g, "SAVE CANDIDATES — change CHARACTER_NAME", (3150, 260), "habitat-sol/characters/CHARACTER_NAME/candidates")
    for s,ss,d,ds,t in [(ck,1,ident,0,"CLIP"),(ck,1,neg,0,"CLIP"),(ck,0,ks,0,"MODEL"),(ident,0,ks,1,"CONDITIONING"),(neg,0,ks,2,"CONDITIONING"),(latent,0,ks,3,"LATENT"),(ks,0,dec,0,"LATENT"),(ck,2,dec,1,"VAE"),(dec,0,save,0,"IMAGE")]: g.link(s,ss,d,ds,t)
    g.save("01_character_forge.json", "Character-reference creation. " + VISUAL_RULES)

def episode_single():
    g = Graph("single character episode")
    g.group("1 — Episode Inputs", (20, 20, 1100, 620), "#805c3b", "Edit only the identity line, story frame, camera, seed, and save prefix per episode. " + VISUAL_RULES)
    g.group("2 — Character References", (20, 700, 1060, 430), "#526d5d", "Select one to three approved canonical reference images. Batch them; average preserves identity without copying their pose or framing.")
    g.group("3 — Identity Conditioning", (1150, 20, 980, 620), "#3e627c", "IPAdapter Plus Face SDXL. Identity strength 0.78 is an editable starting point; 0.65–0.85 usually preserves face while allowing a new scene.")
    g.group("4 — Pose and Composition", (1150, 700, 1280, 430), "#526d5d", "Optional inputs are direct, preprocessed pose/depth maps. Union SDXL ControlNet supports pose or depth but the map must match the selected union type. Disconnect to disable.")
    g.group("5 — Scene Generation", (2180, 20, 900, 620), "#6e5a7d", "Keep character identity concise; put the episode action, location, camera, and visual style in separate readable prompt nodes.")
    g.group("6 — Face Review", (3130, 20, 740, 620), "#8a5f52", "Inspect face/hands/clothing at full size; route a specific fault to 04_repair_character_region.json. The registered FaceFixerOpenCV node is not used because its live OpenCV dependency fails.")
    g.group("7 — Final Output", (3920, 20, 460, 620), "#6a6a6a", "Soft upscaler is optional. At four times, resize outside ComfyUI if the full 4× output is too large.")
    ck=checkpoint(g)
    identity=text(g,"CHARACTER IDENTITY",(390,70),"CHARACTER_NAME, concise canonical face/hair/age/body anchors, practical role-specific layered clothing; identity comes primarily from approved references, not repeated prompt prose.")
    action=text(g,"EPISODE ACTION AND EMOTION",(390,230),"one person, a specific small action at the emotional turn of this episode; quiet, intimate, observational body language")
    place=text(g,"LOCATION AND ENVIRONMENT",(390,390),"specific Habitat Sol location with condensation, dust at thresholds, repaired panels, worn textiles, hand-labelled equipment as abstract unreadable marks")
    camera=text(g,"CAMERA AND COMPOSITION + HABITAT SOL VISUAL STYLE",(390,540),"medium environmental documentary portrait, imperfect municipal archive composition, soft practical light, realistic skin, 85mm; "+VISUAL_RULES)
    neg=text(g,"NEGATIVE PROMPT",(390,900),NEGATIVE)
    r1=loadimage(g,"REFERENCE 1 — approved portrait",(60,770)); r2=loadimage(g,"REFERENCE 2 — three-quarter",(60,900)); r3=loadimage(g,"REFERENCE 3 — full body",(390,770))
    b12=g.node("ImageBatch","BATCH REFERENCES 1+2",(390,900),inputs=[inp("image1","IMAGE"),inp("image2","IMAGE")],outputs=[out("IMAGE","IMAGE")])
    b123=g.node("ImageBatch","BATCH REFERENCES +3",(720,840),inputs=[inp("image1","IMAGE"),inp("image2","IMAGE")],outputs=[out("IMAGE","IMAGE")])
    ipa=ipadapter(g,"IPADAPTER PLUS FACE — installed SDXL model",(1190,100)); cv=clipvision(g,(1190,280)); apply=ipapply(g,"IDENTITY STRENGTH — edit weight",(1530,110))
    pose=loadimage(g,"OPTIONAL PREPROCESSED POSE/DEPTH MAP",(1180,780)); cn=g.node("ControlNetLoader","UNION SDXL CONTROLNET",(1530,780),[CONTROLNET],outputs=[out("CONTROL_NET","CONTROL_NET")])
    combine1=g.node("ConditioningCombine","COMBINE — identity + action",(1880,80),inputs=[inp("conditioning_1","CONDITIONING"),inp("conditioning_2","CONDITIONING")],outputs=[out("CONDITIONING","CONDITIONING")])
    combine2=g.node("ConditioningCombine","COMBINE — + location",(1880,240),inputs=[inp("conditioning_1","CONDITIONING"),inp("conditioning_2","CONDITIONING")],outputs=[out("CONDITIONING","CONDITIONING")])
    combine3=g.node("ConditioningCombine","COMBINE — + camera/style",(1880,400),inputs=[inp("conditioning_1","CONDITIONING"),inp("conditioning_2","CONDITIONING")],outputs=[out("CONDITIONING","CONDITIONING")])
    cp=g.node("ControlNetApplyAdvanced","OPTIONAL CONTROLNET — set strength / disconnect if unused",(1880,780),[0.65,0.0,1.0],inputs=[inp("positive","CONDITIONING"),inp("negative","CONDITIONING"),inp("control_net","CONTROL_NET"),inp("image","IMAGE")],outputs=[out("CONDITIONING","CONDITIONING"),out("CONDITIONING","CONDITIONING")])
    latent=g.node("EmptyLatentImage","CANVAS — editable",(2220,410),[896,1152,1],outputs=[out("LATENT","LATENT")]); ks=sampler(g,"SCENE GENERATION",(2520,230)); dec=decode(g,(2890,250)); up=g.node("UpscaleModelLoader","OPTIONAL SOFT UPSCALER",(3930,160),[UPSCALER],outputs=[out("UPSCALE_MODEL","UPSCALE_MODEL")]); upscale=g.node("ImageUpscaleWithModel","FINAL UPSCALE — bypass if not wanted",(3930,310),inputs=[inp("upscale_model","UPSCALE_MODEL"),inp("image","IMAGE")],outputs=[out("IMAGE","IMAGE")]); save=saveimage(g,"SAVE — change EPISODE_ID",(3930,470),"habitat-sol/episodes/EPISODE_ID")
    for s,ss,d,ds,t in [(ck,1,identity,0,"CLIP"),(ck,1,action,0,"CLIP"),(ck,1,place,0,"CLIP"),(ck,1,camera,0,"CLIP"),(ck,1,neg,0,"CLIP"),(r1,0,b12,0,"IMAGE"),(r2,0,b12,1,"IMAGE"),(b12,0,b123,0,"IMAGE"),(r3,0,b123,1,"IMAGE"),(ck,0,apply,0,"MODEL"),(ipa,0,apply,1,"IPADAPTER"),(b123,0,apply,2,"IMAGE"),(cv,0,apply,5,"CLIP_VISION"),(identity,0,combine1,0,"CONDITIONING"),(action,0,combine1,1,"CONDITIONING"),(combine1,0,combine2,0,"CONDITIONING"),(place,0,combine2,1,"CONDITIONING"),(combine2,0,combine3,0,"CONDITIONING"),(camera,0,combine3,1,"CONDITIONING"),(combine3,0,cp,0,"CONDITIONING"),(neg,0,cp,1,"CONDITIONING"),(cn,0,cp,2,"CONTROL_NET"),(pose,0,cp,3,"IMAGE"),(apply,0,ks,0,"MODEL"),(cp,0,ks,1,"CONDITIONING"),(cp,1,ks,2,"CONDITIONING"),(latent,0,ks,3,"LATENT"),(ks,0,dec,0,"LATENT"),(ck,2,dec,1,"VAE"),(up,0,upscale,0,"UPSCALE_MODEL"),(dec,0,upscale,1,"IMAGE"),(upscale,0,save,0,"IMAGE")]: g.link(s,ss,d,ds,t)
    g.save("02_episode_single_character.json", "Single-character reference-conditioned episode workflow. " + VISUAL_RULES)

def multi_character():
    g=Graph("multi character inpaint")
    g.group("1 — Base Scene",(20,20,850,560),"#805c3b","Load or make a clean background/base scene. The two passes sample only in their feathered masks.")
    g.group("2 — Character A",(20,630,850,420),"#526d5d","Approved A reference + concise A identity. Keep identity strength separate from Character B.")
    g.group("3 — Character A Inpaint",(920,20,1030,560),"#3e627c","Conservative 0.55 denoise, noise mask enabled, expanded/feathered mask. A affects only A mask.")
    g.group("4 — Character B",(920,630,850,420),"#526d5d","Approved B reference + concise B identity. Do not put both people into one identity prompt.")
    g.group("5 — Character B Inpaint",(2000,20,1030,560),"#6e5a7d","B begins from A's decoded result and samples only B mask; it should not regenerate A/background.")
    g.group("6 — Final Review",(3080,20,700,560),"#8a5f52","Inspect at full size; use workflow 04 for face/detail correction. FaceFixerOpenCV is omitted because its registered node fails without OpenCV.")
    g.group("7 — Output",(3830,20,400,560),"#6a6a6a",VISUAL_RULES)
    ck=checkpoint(g)
    base=loadimage(g,"BASE SCENE — approved background/composition",(60,100)); ma=maskload(g,"MASK A — paint white over character A",(60,270)); mb=maskload(g,"MASK B — paint white over character B",(60,430))
    ra=loadimage(g,"CHARACTER A — approved reference",(50,750)); pa=text(g,"A IDENTITY + A ACTION",(380,700),"CHARACTER_A identity anchors; specific action and wardrobe for this scene; documentary Habitat Sol realism"); na=text(g,"A NEGATIVE",(380,890),NEGATIVE)
    growa=g.node("GrowMaskWithBlur","A MASK — expand + feather",(950,100),[12,0.0,True,False,10.0,1.0,1.0],inputs=[inp("mask","MASK")],outputs=[out("MASK","MASK")]); ipa=ipadapter(g,"A IPADAPTER PLUS FACE",(950,280)); cva=clipvision(g,(950,420)); ia=ipapply(g,"A IDENTITY STRENGTH",(1280,280)); inpa=g.node("InpaintModelConditioning","A INPAINT — noise mask enabled",(1280,100),[True],inputs=[inp("positive","CONDITIONING"),inp("negative","CONDITIONING"),inp("vae","VAE"),inp("pixels","IMAGE"),inp("mask","MASK")],outputs=[out("POSITIVE","CONDITIONING"),out("NEGATIVE","CONDITIONING"),out("LATENT","LATENT")]); ka=sampler(g,"A INPAINT — conservative denoise",(1640,180),denoise=0.55); da=decode(g,(1640,390))
    rb=loadimage(g,"CHARACTER B — approved reference",(970,750)); pb=text(g,"B IDENTITY + B ACTION",(1300,700),"CHARACTER_B identity anchors; specific action and wardrobe for this scene; documentary Habitat Sol realism"); nb=text(g,"B NEGATIVE",(1300,890),NEGATIVE)
    growb=g.node("GrowMaskWithBlur","B MASK — expand + feather",(2040,100),[12,0.0,True,False,10.0,1.0,1.0],inputs=[inp("mask","MASK")],outputs=[out("MASK","MASK")]); ipb=ipadapter(g,"B IPADAPTER PLUS FACE",(2040,280)); cvb=clipvision(g,(2040,420)); ib=ipapply(g,"B IDENTITY STRENGTH",(2370,280)); inpb=g.node("InpaintModelConditioning","B INPAINT — noise mask enabled",(2370,100),[True],inputs=[inp("positive","CONDITIONING"),inp("negative","CONDITIONING"),inp("vae","VAE"),inp("pixels","IMAGE"),inp("mask","MASK")],outputs=[out("POSITIVE","CONDITIONING"),out("NEGATIVE","CONDITIONING"),out("LATENT","LATENT")]); kb=sampler(g,"B INPAINT — conservative denoise",(2730,180),seed=2407188,denoise=0.55); db=decode(g,(2730,390))
    save=saveimage(g,"SAVE — change EPISODE_ID",(3850,260),"habitat-sol/episodes/EPISODE_ID/multi_character")
    for s,ss,d,ds,t in [(ck,1,pa,0,"CLIP"),(ck,1,na,0,"CLIP"),(ma,0,growa,0,"MASK"),(ck,0,ia,0,"MODEL"),(ipa,0,ia,1,"IPADAPTER"),(ra,0,ia,2,"IMAGE"),(cva,0,ia,5,"CLIP_VISION"),(pa,0,inpa,0,"CONDITIONING"),(na,0,inpa,1,"CONDITIONING"),(ck,2,inpa,2,"VAE"),(base,0,inpa,3,"IMAGE"),(growa,0,inpa,4,"MASK"),(ia,0,ka,0,"MODEL"),(inpa,0,ka,1,"CONDITIONING"),(inpa,1,ka,2,"CONDITIONING"),(inpa,2,ka,3,"LATENT"),(ka,0,da,0,"LATENT"),(ck,2,da,1,"VAE"),(ck,1,pb,0,"CLIP"),(ck,1,nb,0,"CLIP"),(mb,0,growb,0,"MASK"),(ck,0,ib,0,"MODEL"),(ipb,0,ib,1,"IPADAPTER"),(rb,0,ib,2,"IMAGE"),(cvb,0,ib,5,"CLIP_VISION"),(pb,0,inpb,0,"CONDITIONING"),(nb,0,inpb,1,"CONDITIONING"),(ck,2,inpb,2,"VAE"),(da,0,inpb,3,"IMAGE"),(growb,0,inpb,4,"MASK"),(ib,0,kb,0,"MODEL"),(inpb,0,kb,1,"CONDITIONING"),(inpb,1,kb,2,"CONDITIONING"),(inpb,2,kb,3,"LATENT"),(kb,0,db,0,"LATENT"),(ck,2,db,1,"VAE"),(db,0,save,0,"IMAGE")]: g.link(s,ss,d,ds,t)
    g.save("03_episode_multi_character_inpaint.json", "Two-character staged identity inpainting. " + VISUAL_RULES)

def repair_region():
    g=Graph("repair character region")
    g.group("1 — Approved Image + Mask",(20,20,900,560),"#805c3b","Load the approved episode image and a white-on-black region mask. Expand and feather the mask to avoid seams.")
    g.group("2 — Character References",(20,630,900,420),"#526d5d","Use one approved portrait and concise canonical anchors for face drift, hair, age, clothing, hands, expression, or accessories.")
    g.group("3 — Identity-conditioned Inpaint",(970,20,1160,560),"#3e627c","IPAdapter Plus Face SDXL + InpaintModelConditioning, noise mask enabled. Start 0.45–0.65 denoise; lower protects the approved composition.")
    g.group("4 — Detail Review",(2180,20,760,560),"#8a5f52","The masked identity-conditioned inpaint pass is the reliable face/detail repair. Inspect hands and face at full size; FaceFixerOpenCV is omitted because its live OpenCV dependency fails.")
    g.group("5 — Output",(2990,20,450,560),"#6a6a6a",VISUAL_RULES)
    ck=checkpoint(g)
    base=loadimage(g,"APPROVED EPISODE IMAGE — never overwritten",(50,120)); mask=maskload(g,"REGION MASK — paint white where repair is allowed",(50,340)); ref=loadimage(g,"CANONICAL CHARACTER REFERENCE",(50,750)); p=text(g,"REPAIR PROMPT — identity + exact correction",(390,710),"CHARACTER_NAME canonical identity anchors; repair only the masked region: correct hair, age, face, practical layered clothing, hands, expression or accessory; preserve the approved scene outside mask; Habitat Sol documentary realism") ; n=text(g,"NEGATIVE",(390,900),NEGATIVE)
    grow=g.node("GrowMaskWithBlur","MASK EXPANSION + FEATHER",(1000,100),[10,0.0,True,False,8.0,1.0,1.0],inputs=[inp("mask","MASK")],outputs=[out("MASK","MASK")]); ipa=ipadapter(g,"IPADAPTER PLUS FACE",(1000,280)); cv=clipvision(g,(1000,430)); apply=ipapply(g,"IDENTITY STRENGTH — edit",(1330,280)); inpnode=g.node("InpaintModelConditioning","INPAINT — noise mask enabled",(1330,100),[True],inputs=[inp("positive","CONDITIONING"),inp("negative","CONDITIONING"),inp("vae","VAE"),inp("pixels","IMAGE"),inp("mask","MASK")],outputs=[out("POSITIVE","CONDITIONING"),out("NEGATIVE","CONDITIONING"),out("LATENT","LATENT")]); ks=sampler(g,"REGION REPAIR — conservative denoise",(1720,180),denoise=0.52); dec=decode(g,(1720,400)); save=saveimage(g,"SAVE REPAIRED VERSION — never source prefix",(3020,250),"habitat-sol/episodes/EPISODE_ID/repaired")
    for s,ss,d,ds,t in [(ck,1,p,0,"CLIP"),(ck,1,n,0,"CLIP"),(mask,0,grow,0,"MASK"),(ck,0,apply,0,"MODEL"),(ipa,0,apply,1,"IPADAPTER"),(ref,0,apply,2,"IMAGE"),(cv,0,apply,5,"CLIP_VISION"),(p,0,inpnode,0,"CONDITIONING"),(n,0,inpnode,1,"CONDITIONING"),(ck,2,inpnode,2,"VAE"),(base,0,inpnode,3,"IMAGE"),(grow,0,inpnode,4,"MASK"),(apply,0,ks,0,"MODEL"),(inpnode,0,ks,1,"CONDITIONING"),(inpnode,1,ks,2,"CONDITIONING"),(inpnode,2,ks,3,"LATENT"),(ks,0,dec,0,"LATENT"),(ck,2,dec,1,"VAE"),(dec,0,save,0,"IMAGE")]: g.link(s,ss,d,ds,t)
    g.save("04_repair_character_region.json", "Targeted identity-conditioned region repair. " + VISUAL_RULES)

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    character_forge(); episode_single(); multi_character(); repair_region()
    print("Created", *sorted(p.name for p in OUT.glob("0*.json")), sep="\n- ")
