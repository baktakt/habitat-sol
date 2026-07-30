# Martian Habitat Patch System

## Purpose

Generate **text-free fabric patch reference images** for clothing, bags, maintenance gear, civic uniforms, and props across the Martian settlement network. Habitat Sol uses a round civic badge; the othe...[truncated]

## Shared Martian red thread

Every habitat patch follows one family grammar:

- a tactile embroidered/chenille or woven-fabric badge, square format with softly rounded corners;
- **the fixed, non-negotiable frame palette on every patch:** outer border in oxidized Mars red `#9A3E2F`; inner containment ring in basalt navy `#162B3A`; stitch/edge marks in dust cream `#D6C6A6`; do not substitute a habitat-local colour in any of these three frame elements;
- one central environmental/civic motif, one orbit/route/seal geometry, and limited local palette;
- visible thread, slightly uneven stitching, practical field-issued construction, quiet use marks;
- **no typography, letters, numbers, words, logos, watermarks, flags, or pseudo-writing**;
- photographed/documented front-on on neutral worn canvas, not modelled on clothing, not a glossy product advert.

The red thread communicates a shared Martian ecosystem without making the habitats interchangeable: each patch balances the common border and ring with a distinct local material, colour accent, and motif.

## Prompt baseline

Append this to each habitat-specific prompt:

> square textile mission patch reference, front-on orthographic product-documentary view on worn neutral canvas; tactile embroidered thread and woven cloth, softly rounded corners; **identical standard frame across the entire Martian habitat series: outer border exactly oxidized Mars red #9A3E2F, inner containment ring exactly basalt navy #162B3A, stitch and edge marks exactly dust cream #D6C6A6; these frame colours never change and are not habitat palette accents**; practical field-issued construction, subtle wear, no readable text, no letters, no numbers, no words, no logo, no watermark, no pseudo-writing, no flags; physically plausible fabric and thread, no human, no clothing, no mockup, no glossy commercial product photography.

Use this negative prompt in the workflow:

> readable text, letters, typography, numbers, words, logo, watermark, signature, pseudo-writing, flag, QR code, person, face, hands, clothing mockup, mannequin, glossy product advertisement, plastic texture, chrome, generic spaceship, military insignia, anime, cartoon, low quality, blurry, distorted geometry.

## Habitat prompts

### 1. Habitat Sol — current render

**Feeling:** first civilian town; intimate, historic, maintained through care; civic memory under constraint.

> Habitat Sol patch: a **perfectly round** civic fabric badge with a continuous circular oxidized-red outer border, circular basalt-navy containment field, and circular dust-cream stitch ring; centered simplified flat greenhouse arch built from bold moss-green and muted-ochre stitched bands, sheltering one small stylized three-leaf sprout beneath a warm amber sun-disc; calm practical civic warmth, first civilian town, old Mars, collective care; clean intact patch field with **no repair seam, no cross-shaped patch, no lower-right-corner applique, and no extra geometric mark**; no square or rectangular patch geometry; **[append text/no-text constraints and fixed palette; do not append the square-format clause]**

### 2. Habitat Meridian — next render

**Feeling:** administrative and transport capital; efficient, cosmopolitan, controlled.

> Habitat Meridian patch: an abstract central transit interchange, three clean radial route lines joining a balanced meridian circle beneath a small rust-red horizon; slate blue, graphite, cool silver-grey, restrained teal and oxidized red; disciplined geometry, precise spacing, quiet institutional authority, transit and governance rather than military power; **[append Prompt baseline]**

### 3. Habitat Elysium

**Feeling:** largest, wealthiest city; health, beauty, biotech, media, status.

> Habitat Elysium patch: a stylized white greenhouse petal or medical bioform enclosing a polished water droplet, surrounded by a delicate orbital halo; bone white, pale aqua, soft lilac, pearl grey and a small oxidized-red edge; refined but not luxurious, medically advanced civic optimism, materially plausible embroidery; **[append Prompt baseline]**

### 4. Habitat Ferrum

**Feeling:** industrial powerhouse; labor, durability, unionized solidarity.

> Habitat Ferrum patch: a heavy forged hexagonal bolt framing a simple furnace glow and two interlocking structural beams; iron grey, burnt orange, charcoal, muted copper and oxidized red; thick thread, reinforced edges, useful and durable rather than aggressive; **[append Prompt baseline]**

### 5. Habitat Astra

**Feeling:** university and research city; youthful argument, knowledge, discovery.

> Habitat Astra patch: a compact observatory aperture with an abstract star field and a single measured trajectory line, nested in an open book-like geometric frame; midnight blue, chalk white, violet, cool cyan and oxidized red; curious, rigorous, lightly youthful, scholarly rather than mystical; **[append Prompt baseline]**

### 6. Habitat Arcadia

**Feeling:** agriculture, water, ice, ecology, self-sufficiency.

> Habitat Arcadia patch: a water droplet becoming an ice crystal and a green leaf within a terraced basin shape; deep algae green, ice blue, clear teal, clay brown and oxidized red; practical ecological stewardship, experimental but grounded; **[append Prompt baseline]**

## Production order

1. Generate four to eight candidates for Sol using `05_habitat_patch_forge.json`; select one for the visual system.
2. Duplicate the positive prompt into the workflow's visible prompt nodes and replace only the Sol-specific paragraph with Meridian’s paragraph. Keep the common grammar, sampler, resolution, and negative prompt stable.
3. Continue in canon order: Elysium, Ferrum, Astra, Arcadia. Change one habitat-specific motif/palette at a time, so every final selection remains visibly family-related.
4. Save selected source renders under `comfyui/patches/<habitat>/selected/` (or record an external Comfy output path) with the seed and full prompt. Treat them as references, not final production embroidery files.

## First render record — Habitat Sol

- Workflow: `comfyui/workflows/05_habitat_patch_forge.json` (UI) and `comfyui/workflows/habitat_sol_patch_forge_api.json` (single-candidate API run)
- Model: `qwen_image_2512_fp8_e4m3fn.safetensors` with `qwen_2.5_vl_7b_fp8_scaled.safetensors` and `qwen_image_vae.safetensors`
- Seed: `218700504`
- Resolution: `768 × 768`
- Sampling: Euler, simple scheduler, 30 steps, CFG 4.0
- Output: `comfyui/patch-sol-round-218700504.png` (replaces the previous squa...[truncated]

## Second render record — Habitat Meridian

- Workflow: `comfyui/workflows/habitat_sol_patch_forge_api.json`, with the habitat clause replaced by the Meridian prompt above.
- Seed: `218700601`; resolution: `768 × 768`; sampler: Euler/simple, 30 steps, CFG 4.0.
- Output: `comfyui/patch-meridian-candidate-218700601.png`
- Review: pass. It retains the red outer seam, dark basalt inner ring, cream routes, and visible thread of Sol’s family grammar, while shifting decisively to balanced slate/teal transit geometry and controlled civic authority. No text or pseudo-writing is present.

## Remaining render records

All use `comfyui/workflows/habitat_sol_patch_forge_api.json` with the corresponding prompt above, `768 × 768`, Euler/simple, 30 steps, CFG 4.0, and the shared negative prompt.

| Habitat | Seed | Selected reference | Review |
|---|---:|---|---|
| Elysium | `218700701` | `comfyui/patch-elysium-candidate-218700701.png` | **Pass** — text-free textile patch; pearl/aqua droplet, white bioform, lilac halo clearly convey refined health/biotech while retaining the shared red, cream and dark ring. |
| Ferrum | `218700801` | `comfyui/patch-ferrum-candidate-218700801.png` | **Pass** — text-free reinforced patch; forged hexagon, furnace glow, and crossed structural beams establish durable fabrication without military heraldry. |
| Astra | `218700901` | `comfyui/patch-astra-candidate-218700901.png` | **Pass** — text-free textile patch; open-book geometry, dark observatory ring, star field, and measured line make the research-city identity immediately legible. |
| Arcadia | `218701001` | `comfyui/patch-arcadia-candidate-218701001.png` | **Pass** — text-free textile patch; water basin, ice crystal, and leaf form a distinct practical ecology/water identity within the family border. |

## Selection checks

Reject a candidate if it contains accidental writing, a logo-like mark, legible numerals, militaristic heraldry, a glossy merch aesthetic, or loses the common red/basalt/cream grammar. Select only an image that reads clearly at both badge size and full resolution.
