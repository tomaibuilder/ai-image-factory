# Setup: run once, about 10 minutes

Claude runs this when `brand/BRAND.md` is still the template or `.env` is missing. Work through it one section at a time and wait for the user's answers. Do not fill anything in for them.

## 1. Install

- Check `python3 --version` works.
- Run `pip install -r requirements.txt` from this skill folder. If the user prefers, make a virtual environment in `.venv/` first and use its Python for every script.

## 2. Keys

Explain both, then have the user paste each key into `.env` in this skill folder themselves (copy `.env.example` to `.env`). Never ask them to paste a key into the chat.

- **fal.ai (required).** Sign up at https://fal.ai, open Dashboard, then Keys, and create a key. Pay as you go. A typical run of 12 drafts plus 3 finals costs about $0.15.
- **Kie.ai (optional).** Sign up at https://kie.ai and create an API key. New accounts get 80 free credits. With a Kie key, finals made from a reference image cost $0.03 instead of $0.054. Without it, everything runs on fal.

Confirm `.env` is listed in `.gitignore`.

## 3. Brand

Interview the user and fill in `brand/BRAND.md`:

- Brand or business name, and who the images are for.
- Colours: background, text (ink) and one accent, as hex codes. If they don't know, ask for their website and read the colours from it.
- Headline and body fonts, or the feel if they don't know the names ("heavy condensed sans", "classic serif").
- The look in three or four words, and two or three brands or accounts whose images they like.
- Their logo file. Ask them to put it in `brand/` and write the filename down.
- Words and phrases that must never appear on an image.
- Where they post most (this sets their default size).

## 4. Starter recipes

Show them the 4 recipes in `recipes.md`. Ask which fit their niche, and whether any should be cut or renamed. Then ask for a scene from their world for each recipe (for example a dentist's front desk, a site office, a kitchen pass) and write it into that recipe's notes.

## 5. Their own references (optional)

If they have images they love, ask them to drop them into a `my-references/` folder in this skill folder. For each one, add a short recipe to `recipes.md`: what it looks like, when to use it, a prompt skeleton, and the file path to pass as `"image"` when riffing on it.

## 6. Test run

Run the default draft-and-pick run on a real message they need an image for this week. Show the contact sheet, make one final, and report the cost.
