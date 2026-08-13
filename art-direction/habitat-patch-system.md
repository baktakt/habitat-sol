# Martian Habitat Patch System

## Purpose

Generate a coherent set of **text-free civic fabric patch reference images** for clothing, bags, maintenance gear, civic uniforms, and props across the Martian settlement network. Habitat Sol uses a round badge; the other habitats use softly rounded square badges.

These prompts are written as complete, ready-to-paste Qwen Image prompts. Do not concatenate prompt fragments at run time.

## Shared design grammar

Every habitat patch belongs to one visual family:

- tactile embroidered thread and woven cloth, made for repeated civilian use rather than ceremony;
- a fixed outer frame palette: oxidized Mars red (`#9A3E2F`), basalt navy (`#162B3A`), and dust cream (`#D6C6A6`);
- one bold civic or environmental motif with a limited habitat-specific accent palette;
- simple geometry that remains legible when the patch is small on clothing;
- visible thread, slightly uneven stitching, softened edges, and restrained use marks;
- no typography, letters, numbers, words, flags, commercial branding, or pseudo-writing;
- front-on isolation on a uniform pure-white background, not attached to clothing and not presented as glossy merchandise. Generate white rather than asking Qwen for transparency; remove the white background to alpha in post-production when a transparent asset is needed.

The frame colours provide the shared Martian identity. Habitat-specific colours belong inside the central motif and must not replace the oxidized-red outer border, basalt-navy containment field, or dust-cream stitch details.

## Qwen prompt format

Each positive prompt follows the same order:

1. image type and exact patch shape;
2. fixed family frame;
3. central motif and local palette;
4. material, condition, and construction;
5. pure-white isolation background, lighting, and composition;
6. explicit absence of recognizable text.

Use natural continuous prose and concrete visible relationships. Keep one main motif, state exact counts where they matter, and avoid abstract lore that cannot be rendered. Colour names carry the visual instruction; hex values are production references and may not be reproduced exactly by the model. A uniform pure-white background is the generation standard because it is more reliable than model-generated transparency and produces a clean source for later background removal.

## Negative-prompt strategy

Use **one shared negative prompt for every patch**, then append the short habitat-specific suffix listed below. This avoids six drifting copies of the same baseline while still blocking each motif's likely failure modes. Critical requirements also remain in the positive prompts because negative conditioning alone is not reliable enough to define identity.

### Shared negative prompt

> readable text, letters, typography, numbers, words, pseudo-writing, signature, QR code, flag, commercial brand logo, watermark, military heraldry, rank chevrons, weapon motif, person, face, body, hands, clothing, jacket, bag, mannequin, clothing mockup, multiple patches, duplicate patch, cropped patch, tilted product view, extreme perspective, folded patch, glossy merchandise advertisement, retail packaging, presentation box, plastic badge, metal badge, enamel pin, sticker, rubber patch, chrome, reflective foil, photoreal scene inside the emblem, generic spaceship, astronaut, canvas background, fabric background, textured background, grey background, colored background, gradient background, environmental scene, horizon, floor, tabletop, display stand, hard cast shadow, dramatic shadow, halo, vignette, transparent checkerboard pattern, fake transparency grid, heavy grime, heavy rust, burned fabric, torn motif, loose detached pieces, neon glow, hologram, anime, cartoon, distorted geometry, asymmetrical frame, unreadable motif, low resolution, low quality, blurry

## Ready-to-use habitat prompts

### 1. Habitat Sol

**Feeling:** first civilian town; intimate, historic, maintained through care; civic memory under constraint.

**Positive prompt**

> A single perfectly round Habitat Sol civic fabric badge, centered and fully visible in a square 1:1 reference image. Its fixed family frame has one continuous oxidized Mars-red outer border, a circular basalt-navy containment field, and one dust-cream stitch ring. At the center, a simplified greenhouse arch made from bold moss-green and muted-ochre embroidered bands shelters exactly one small three-leaf sprout beneath one warm amber sun-disc. The motif is flat, balanced, and readable at badge size, expressing civilian shelter, cultivation, and collective care without military symbolism. The badge is tactile woven cloth with dense embroidery, slightly uneven practical stitching, softly worn thread, and an intact field; there is no repair seam, added applique, cross-shaped insert, or extra geometric mark. It is isolated front-on against a seamless uniform pure-white background under soft even diffuse light, with only a faint tight grounding shadow directly beneath the edge. No clothing, hands, packaging, or recognizable text appears.

**Append to shared negative prompt**

> square patch, rectangular patch, shield shape, repair seam, cross-shaped insert, lower-right applique, extra symbol, multiple sprouts, multiple suns, missing greenhouse arch, dead plant, ruined greenhouse

### 2. Habitat Meridian

**Feeling:** administrative and transport capital; efficient, cosmopolitan, controlled.

**Positive prompt**

> A single softly rounded square Habitat Meridian civic fabric badge, centered and fully visible in a square 1:1 reference image. Its fixed family frame uses an oxidized Mars-red outer border, a basalt-navy inner containment ring, and dust-cream stitch and edge details. The center contains one precise abstract transit interchange: exactly three clean radial route lines meet one balanced meridian circle beneath one short rust-red horizon bar. Slate blue, graphite, cool silver-grey, and restrained teal appear only inside the central motif. The geometry is disciplined, evenly spaced, and legible at badge size, conveying civic transport and administration rather than military command. The badge is woven cloth with fine practical embroidery, firm reinforced edges, subtle thread texture, and restrained use marks. It is isolated front-on against a seamless uniform pure-white background under soft even diffuse light, with only a faint tight grounding shadow directly beneath the edge. No map labels, arrows, vehicles, clothing, hands, packaging, or recognizable text appears.

**Append to shared negative prompt**

> subway map, road map, map labels, arrows, compass rose, target reticle, radar screen, corporate transit logo, more than three route lines, extra circles, chaotic routes

### 3. Habitat Elysium

**Feeling:** largest and wealthiest city; health, beauty, biotech, media, and status.

**Positive prompt**

> A single softly rounded square Habitat Elysium civic fabric badge, centered and fully visible in a square 1:1 reference image. Its fixed family frame uses an oxidized Mars-red outer border, a basalt-navy inner containment ring, and dust-cream stitch and edge details. The center holds one stylized bone-white greenhouse petal shaped like a calm medical bioform, enclosing exactly one pale-aqua embroidered water droplet and surrounded by one thin soft-lilac orbital arc. Pearl grey and a restrained pale-aqua accent remain inside the motif. The design is refined, clean, and medically advanced but still civilian, tactile, and materially modest; it must read as stitched cloth rather than jewelry or luxury branding. Fine embroidery, woven backing, softened thread, and very light use marks keep it physically plausible. It is isolated front-on against a seamless uniform pure-white background under soft even diffuse light, with only a faint tight grounding shadow directly beneath the edge. No cross symbol, medical text, clothing, hands, packaging, or recognizable text appears.

**Append to shared negative prompt**

> red medical cross, hospital logo, caduceus, DNA helix, syringe, glossy liquid, glass jewel, pearl jewelry, cosmetics logo, luxury fashion badge, flower bouquet, multiple droplets, multiple orbital arcs

### 4. Habitat Ferrum

**Feeling:** industrial powerhouse; labour, durability, fabrication, and union solidarity.

**Positive prompt**

> A single softly rounded square Habitat Ferrum civic fabric badge, centered and fully visible in a square 1:1 reference image. Its fixed family frame uses an oxidized Mars-red outer border, a basalt-navy inner containment ring, and dust-cream stitch and edge details. The center contains one heavy iron-grey hexagonal bolt outline framing exactly two interlocking structural beams above one compact burnt-orange furnace glow. Charcoal, iron grey, muted copper, and burnt orange remain inside the central motif. The geometry is bold, stable, and readable at badge size, conveying skilled civilian fabrication and collective labour rather than combat, extraction, or corporate power. Thick embroidery, reinforced woven edges, sturdy thread, and restrained use marks make the badge practical and durable without grime or damage. It is isolated front-on against a seamless uniform pure-white background under soft even diffuse light, with only a faint tight grounding shadow directly beneath the edge. No tools, weapons, flames outside the furnace shape, clothing, hands, packaging, or recognizable text appears.

**Append to shared negative prompt**

> skull, weapon, crossed hammers, crossed tools, raised fist, gear logo, mining-company logo, hazard symbol, aggressive flames, explosion, molten metal spill, heavy soot, broken bolt, more than two beams

### 5. Habitat Astra

**Feeling:** university and research city; youthful argument, knowledge, and discovery.

**Positive prompt**

> A single softly rounded square Habitat Astra civic fabric badge, centered and fully visible in a square 1:1 reference image. Its fixed family frame uses an oxidized Mars-red outer border, a basalt-navy inner containment ring, and dust-cream stitch and edge details. The center contains one compact midnight-blue observatory aperture nested inside one simple open-book geometry, with exactly three small chalk-white embroidered star points and one measured cool-cyan trajectory arc. A restrained violet accent remains inside the central motif. The composition is curious, rigorous, and youthful but not mystical, and its few bold elements remain legible at badge size. Fine practical embroidery, woven backing, slightly uneven stitches, and restrained use marks keep it civic and field-issued rather than ceremonial. It is isolated front-on against a seamless uniform pure-white background under soft even diffuse light, with only a faint tight grounding shadow directly beneath the edge. No constellations, equations, lettering, clothing, hands, packaging, or recognizable text appears.

**Append to shared negative prompt**

> astrology, zodiac, horoscope, magic symbol, constellation lines, dense star field, galaxy photograph, rocket, spaceship, telescope silhouette, equations, academic seal, laurel wreath, more than three stars, multiple trajectory arcs

### 6. Habitat Arcadia

**Feeling:** agriculture, water, ice, ecology, and self-sufficiency.

**Positive prompt**

> A single softly rounded square Habitat Arcadia civic fabric badge, centered and fully visible in a square 1:1 reference image. Its fixed family frame uses an oxidized Mars-red outer border, a basalt-navy inner containment ring, and dust-cream stitch and edge details. The center contains one clear teal water droplet whose upper edge transitions into one pale ice-blue six-point crystal while its lower edge shelters exactly one deep algae-green leaf above one simple clay-brown terraced basin. The transition is graphic and stitched, not photoreal. The balanced motif is experimental, ecological, and legible at badge size, conveying practical stewardship of water, ice, and food systems. Tactile embroidery, woven cloth, slightly uneven stitching, softened edges, and restrained use marks make it useful rather than decorative. It is isolated front-on against a seamless uniform pure-white background under soft even diffuse light, with only a faint tight grounding shadow directly beneath the edge. No landscape scene, produce basket, clothing, hands, packaging, or recognizable text appears.

**Append to shared negative prompt**

> recycling logo, environmental NGO logo, planet Earth, globe, forest landscape, farm landscape, mountain scene, snowflake pattern covering badge, multiple leaves, multiple droplets, fruit, vegetables, wheat sheaf, photoreal water, glossy droplet

## Review and selection

Reject a candidate if it:

- contains accidental writing, numerals, commercial branding, flags, or militaristic heraldry;
- changes the fixed oxidized-red, basalt-navy, and dust-cream family frame;
- adds motifs or decorative geometry not requested by the habitat prompt;
- looks like plastic, metal, a sticker, luxury merchandise, or a clothing mockup;
- uses heavy grime or damage instead of restrained evidence of ordinary use;
- becomes illegible when reduced to the size of a badge on a jacket.

Select only a patch that has the correct silhouette, exact motif count, coherent family frame, plausible textile construction, and clear identity at both badge size and full resolution. Preserve the selected prompt, negative prompt, seed, model, resolution, and output path with the approved reference image.
