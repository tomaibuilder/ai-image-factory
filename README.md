# ai-image-factory

A Claude Code skill that makes on-brand images for your posts, articles, emails and ads with GPT Image 2. You say where the image is going and what it is about. It drafts 12 different options for a few cents, fixes any with wrong text, and shows you a numbered contact sheet. You pick, and it re-makes your picks at full quality at the exact size for that platform.

I've used my own version of this skill since May 2026. This is the shareable version, with my brand and style library taken out and a setup that builds yours.

## What a run looks like

1. It asks where the image will be posted, so the size is right from the start.
2. It writes 8 to 10 visual ideas for your message.
3. It makes 12 drafts on the cheapest setting, each a different idea, style or layout.
4. It checks every draft for defects only: wrong or misspelled text, a missing element, a reference it ignored, made-up numbers. It redoes those. It doesn't judge taste, because you're the better judge of that.
5. You pick from a numbered contact sheet.
6. It re-makes each pick at full quality, using your pick as the reference so the layout stays the same.

A typical run (12 drafts plus 3 finals) costs about $0.15. There's a hard cap of $0.50 a run.

## What it costs

Same model on both services: OpenAI's GPT Image 2. I tested 12 images on 26 October 2026 at 1536x1024.

| Per image | fal low | fal medium | fal high | Kie |
|---|---|---|---|---|
| From a text prompt | $0.005 | $0.042 | $0.165 | $0.03 |
| With a reference image | $0.018 | $0.054 | $0.178 | $0.03 |

- fal charges by quality and uses high if you don't set it. This skill never uses high unless you ask.
- Kie has no quality setting. It costs a flat $0.03 per 1K image, and it took 60 to 110 seconds per image against 15 to 40 on fal.
- So the skill drafts on fal low, makes text-prompt finals on fal medium, and sends reference-image finals to Kie if you add a Kie key.

fal prices are from fal's own tables (1024x1536 row, same pixel count). fal bills by token, so long prompts cost a little more. Kie prices are what Kie charged per image in my test.

## Install

Paste this into Claude Code:

```
Install this skill for me: https://github.com/tomaibuilder/ai-image-factory
```

Then ask Claude Code to "make me an image". On the first run it walks you through setup (about 10 minutes):

- **Keys.** A fal.ai key (required) and a Kie.ai key (optional), saved in `.env` in the skill folder. You never paste keys into the chat.
- **Brand.** Your colours, fonts, the look you want, your logo file and words that never go on an image.
- **Starter recipes.** 4 starter styles you adapt to your niche, plus any reference images you love.

## What's in here

- `SKILL.md` is the workflow Claude follows.
- `SETUP.md` is the first-run interview.
- `recipes.md` holds the 4 starter styles: editorial cover, photo and headline, big number, before and after. Add your own.
- `brand/BRAND.md` is filled in during setup.
- `scripts/` contains batch drafts, reference-image finals, Kie routing and the contact sheet.

## Notes

- Big headlines come out right on every setting I tested. Small text (labels, captions) can come out garbled on low, which is why finals run on medium or Kie.
- Logos: give it your logo file as a reference image. A simple wordmark came out right in my tests. Complex logos may need to be placed on the final by hand.
- Coming next: a recipe builder that turns a folder of images you like into your own named styles.
