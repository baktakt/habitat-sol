#!/usr/bin/env python3
"""Build the single validated Habitat Sol character-reference forge UI workflow."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'comfyui' / 'workflows' / '01_character_forge.json'
CKPT='FLUX1/flux1-dev-fp8.safetensors'
LORAS=[('Krea2-realism-V1.safetensors',.35),('HabitatSol/Portrait-Engine-FLUX-v1.safetensors',.25),('HabitatSol/ck-Sommo-Concept-Art-FLUX.safetensors',.18)]
BASE='Amara Okonkwo, 39-year-old Black woman, Sol-born civic mediator and Habitat Council member; close natural hair or short practical coiled twists, warm brown skin, tired observant eyes, composed principled expression, ochre practical council jacket over dark thermal layers with repaired cuffs, subtle abstract civic pin; Habitat Sol municipal documentary photography, a maintained repaired aging civilian Mars town, soft practical light, realistic skin texture, no readable text, no fashion glamour.'
NEG='anime, cartoon, concept art, illustration, glossy generic science fiction, military space opera, fashion editorial, superhero pose, readable text, logo, watermark, plastic skin, deformed hands, extra fingers, duplicate person'
SHOTS=[
 ('01_front_portrait','front or near-front head-and-shoulders portrait, neutral expression, plain worn civic corridor background, both eyes clearly visible'),
 ('02_three_quarter_portrait','three-quarter portrait, seated at a mediation table, hands resting naturally on table edge, quiet attentive expression'),
 ('03_full_body','full body standing portrait from head to boots, relaxed poised posture, complete practical outfit visible, worn council corridor'),
 ('04_environment','medium environmental portrait in a lived-in council mediation room, one hand on a table, old notices and repaired panels blurred, no readable text'),
 ('05_expression','close portrait, a small private smile after difficult work, same canonical hair, clothing and age'),
 ('06_canonical_outfit','full body canonical outfit reference, ochre council jacket, dark thermal layers, repaired cuffs, soft indoor shoes, plain neutral habitat backdrop')]

nodes=[]; links=[]; groups=[]; nid=0; lid=0
def out(n,t): return {'name':n,'type':t,'links':[]}
def inp(n,t): return {'name':n,'type':t,'link':None}
def add(t,title,pos,w=None,ins=None,outs=None,size=(310,110)):
 global nid; nid+=1
 x={'id':nid,'type':t,'title':title,'pos':list(pos),'size':list(size),'flags':{},'order':nid-1,'mode':0,'inputs':ins or [],'outputs':outs or [],'properties':{'Node name for S&R':t}}
 if w is not None:x['widgets_values']=w
 nodes.append(x);return nid
def link(a,ao,b,bi,t):
 global lid;lid+=1;links.append([lid,a,ao,b,bi,t])
 for n in nodes:
  if n['id']==a:n['outputs'][ao]['links'].append(lid)
  if n['id']==b:n['inputs'][bi]['link']=lid

ck=add('CheckpointLoaderSimple','BASE MODEL — Flux Dev FP8 (tested)',(30,260),[CKPT],outs=[out('MODEL','MODEL'),out('CLIP','CLIP'),out('VAE','VAE')])
model,clip=ck,ck
for i,(name,strength) in enumerate(LORAS):
 n=add('LoraLoader',f'STYLE — {name}',(360+i*330,260),[name,strength,strength],ins=[inp('model','MODEL'),inp('clip','CLIP')],outs=[out('MODEL','MODEL'),out('CLIP','CLIP')]);link(model,0,n,0,'MODEL');link(clip,1,n,1,'CLIP');model=clip=n
for idx,(slug,shot) in enumerate(SHOTS):
 y=40+idx*260; x=1450
 p=add('CLIPTextEncodeFlux',f'{idx+1} — {slug}: edit identity and shot',(x,y),[BASE+' '+shot,BASE+' '+shot,3.5],ins=[inp('clip','CLIP')],outs=[out('CONDITIONING','CONDITIONING')],size=(450,170)); n=add('CLIPTextEncodeFlux',f'{idx+1} — NEGATIVE',(x,y+180),['',NEG,3.5],ins=[inp('clip','CLIP')],outs=[out('CONDITIONING','CONDITIONING')])
 ms=add('ModelSamplingFlux',f'{idx+1} — Flux canvas settings',(1940,y),[1.15,.5,832,1216],ins=[inp('model','MODEL')],outs=[out('MODEL','MODEL')]); latent=add('EmptyLatentImage',f'{idx+1} — 832×1216 reference frame',(1940,y+130),[832,1216,1],outs=[out('LATENT','LATENT')])
 ks=add('KSampler',f'{idx+1} — generate; change seed for alternate',(2280,y),[8291791398777243546+idx,'fixed',22,1.0,'euler','simple',1.0],ins=[inp('model','MODEL'),inp('positive','CONDITIONING'),inp('negative','CONDITIONING'),inp('latent_image','LATENT')],outs=[out('LATENT','LATENT')]); dec=add('VAEDecode',f'{idx+1} — decode',(2620,y),[],ins=[inp('samples','LATENT'),inp('vae','VAE')],outs=[out('IMAGE','IMAGE')]); save=add('SaveImage',f'{idx+1} — save approved candidate',(2960,y),[f'habitat-sol/characters/CHARACTER_NAME/references/{slug}'],ins=[inp('images','IMAGE')])
 for a,ao,b,bi,t in [(clip,1,p,0,'CLIP'),(clip,1,n,0,'CLIP'),(model,0,ms,0,'MODEL'),(p,0,ks,1,'CONDITIONING'),(n,0,ks,2,'CONDITIONING'),(ms,0,ks,0,'MODEL'),(latent,0,ks,3,'LATENT'),(ks,0,dec,0,'LATENT'),(ck,2,dec,1,'VAE'),(dec,0,save,0,'IMAGE')]:link(a,ao,b,bi,t)
groups=[{'title':'1 — Tested Flux character-reference forge','bounding':[10,0,1370,1780],'color':'#7a4a2b','font_size':24,'properties':{'description':'Use this workflow only to establish canonical references. The Flux Dev + realism/portrait LoRA stack was visually tested and is preferred over the rejected IntoRealism result.'}},{'title':'2 — Six required reference views; review before canonizing','bounding':[1410,0,1920,1780],'color':'#526d5d','font_size':24,'properties':{'description':'Generate front, 3/4, full body, environment, expression and outfit references. Do not promote an image with readable text, wrong age, glamour styling, or an unrecognizable face.'}}]
x={'last_node_id':nid,'last_link_id':lid,'nodes':nodes,'links':links,'groups':groups,'config':{},'extra':{'ds':{'scale':.65,'offset':[0,0]},'habitat_sol_notes':'Generate six deliberate reference views, manually select the canon set, then copy selected output files into characters/<slug>/references/ and commit them.'},'version':.4}
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(x,indent=2)+'\n');print(OUT)
