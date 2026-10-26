---
name: ai-image-factory
description: Make on-brand social, blog, email and ad images with GPT Image 2 on fal.ai (and optionally Kie.ai). Asks where the image will be posted, drafts 12 different options cheaply, fixes only objective defects (wrong text, missing elements), shows a numbered contact sheet to pick from, then re-renders the picks at full quality at the exact posting size. Use when the user says "make me an image", "social image", "thumbnail", "blog cover", "ad image", "image for this post", "riff on this reference", or names a recipe from recipes.md. Not for text-heavy slides, carousels or data tables.
---

# AI Image Factory

Makes images for posts, articles, emails and ads. The user judges taste. This skill gives them a wide set of options and fixes only what is objectively broken.

## First run

If `brand/BRAND.md` still contains `[fill in]`, or `.env` is missing in this skill folder, run `SETUP.md` before anything else.

## Every run, read first

1. `brand/BRAND.md`: colours, fonts, the look, logo file, words to avoid.
2. `recipes.md`: the named styles. Pick from these, and from any the user added.

## Engine and quality routing

Same model on both engines: OpenAI GPT Image 2. Costs below were measured on 26 October 2026 at 1536x1024.

| Job | Engine | Cost per image |
|---|---|---|
| Draft, any kind | fal, `"quality": "low"` | $0.005 from text, $0.018 with a reference image |
| Final from a text prompt | fal, `"quality": "medium"` (script default) | $0.042 |
| Final or fix with a reference image | Kie, if `KIE_API_KEY` is set (`ref_generate.py` picks it automatically). Otherwise fal medium | $0.03 on Kie, $0.054 on fal |

- Never use `high` (about $0.17 per image) unless the user asks for it.
- Low can garble small text (labels, captions). Big headlines are fine on low.
- Kie takes 60 to 110 seconds per image. fal low takes 15 to 25.

## The default run: draft and pick

1. **Ask where it will be posted, first.** The size cannot change after drafting.

   | Where | `size` |
   |---|---|
   | X post, LinkedIn post, YouTube thumbnail | `1536x864` (16:9) |
   | X article header | `1536x640` (5:2) |
   | Instagram or LinkedIn portrait | `1024x1280` (4:5) |
   | Instagram square | `1024x1024` (1:1) |
   | Story, Reel cover | `864x1536` (9:16) |
   | Blog cover, email header, anything else | `1536x1024` (3:2) |

   Also confirm the exact words that must appear on the image, if any.

2. **Ideas.** Write 8 to 10 visual ideas for the message: scenes and metaphors, not styles. Pick the strongest 4 to 6.

3. **12 drafts on fal low.** Write one batch JSON for `scripts/text_generate.py`. Every item: `"quality": "low"`, the same `size`, an absolute `out` path in a `drafts/` folder. Spread the 12 across ideas, recipes and layouts (close-up, wide scene, split, object hero). No two drafts share both idea and recipe. To riff on a reference image the user gave you, add `"image": "<path>"` to that item. The user does not write prompts. You build each prompt from the recipe skeleton plus `brand/BRAND.md`.

4. **Defect check.** Look at every draft. A draft has a defect only if:
   - the text on it is wrong or misspelled
   - a required element of the prompt is missing
   - it ignored the reference image's style
   - it shows numbers that were not in the brief
   - it is only text, with no visual

   Redo a defective draft with the same prompt plus a one-line correction. At most 2 redos per draft. Do not judge taste and do not drop drafts for looking weak. That is the user's call.

5. **Contact sheet.** `python scripts/contact_sheet.py --out <folder>/contact-sheet.png <the 12 drafts in order>`, then open it. The user picks by number.

6. **Finals.** For each pick:
   ```
   python scripts/ref_generate.py --image <picked draft> \
     --prompt "Keep this exact design, layout and text. Re-render it cleanly at full fidelity." \
     --size <same size> --out <final path>
   ```
   This keeps the layout the user picked. Defect-check the final and fix once if needed.

7. **Save and report.** Save next to the content the image is for (the post or article folder) when there is one. Name finals `{platform}_{YYYY-MM-DD}_{NN}_{concept}.png`. Tell the user the full paths and the cost of the run.

**Budget: hard cap $0.50 per run.** 12 text drafts cost about $0.06, 12 reference drafts about $0.22, each redo $0.005 to $0.018, each final $0.03 to $0.054. If a run could pass $0.30, state the estimate before generating.

**Single image to a spec** (the user describes exactly one image): skip steps 2 to 5. Generate on medium, defect-check, deliver.

## Logos

Pass the logo file as a reference image (`"image"` in the batch, `--image` on `ref_generate.py`) and say "place the attached logo exactly as it is, unchanged, small in the [corner]". In testing, a simple wordmark came out right on both engines. If a complex logo comes out wrong, place the real logo file on the final with Pillow.

## Hard rules

- Every image carries a visual (scene, object, illustration, icon or texture), not just a headline on a flat background. Exception: the user asks for a text-only card.
- One accent colour per image, from `brand/BRAND.md`.
- Short on-image text only. Apply the banned words in `brand/BRAND.md`. Never invent stats or claims.
- One size per run.
- Text-heavy slides, carousels, tables and exact data: tell the user an HTML or slide tool is the better choice.
- Keys live only in `.env` in this skill folder. Never print them, never commit them.

## Setup it expects

- Python 3 with `fal-client` and `Pillow` (`pip install -r requirements.txt`).
- `.env` with `FAL_KEY` (required) and `KIE_API_KEY` (optional).
