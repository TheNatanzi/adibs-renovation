"""Render the ATA storefront idea on the real photo with Gemini and OpenAI (Codex) image editing.

Run on a computer that has GEMINI_API_KEY and/or OPENAI_API_KEY set:
    pip install requests
    python tools/ai_render.py
Outputs: tools/out/gemini-storefront.png, tools/out/openai-storefront.png
"""
import base64, os, sys, requests

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "storefront-original.png")
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)

PROMPT = """Photorealistic architectural edit of this exact photo. Same camera angle, same golden-hour lighting,
same sky, trees, roof, teal fascia, gables, lanterns, signs, sidewalk and street. Change only the storefront:

1. LEFT covered walkway (between the left wing and the center gable): enclose its front with a 2 ft tall
   painted white brick pony wall that matches the existing painted white brick exactly (same coursing, color,
   texture), with dark bronze aluminum storefront glazing above it up to the teal fascia beam, 3 equal glass lites.
2. RIGHT covered walkway (between the center gable and the right wing): same as the left, 3 glass lites.
3. CENTER gable porch: enclose the front of the porch at the face of the gable walls with a full-height dark
   bronze aluminum storefront: a 7 ft wide x 8 ft tall pair of glass doors with long stainless vertical pull
   handles, narrow sidelights on each side, and transom glass above up to the soffit. Keep the hanging lantern
   and the ADIB'S PERSIAN RUG sign visible behind the glass.
4. Glass should be realistic clear double-pane glass: you can see into the lit interior, with soft reflections
   of the street and sky.
5. Remove the tall blue agapanthus flowers in front of the building. Keep the low trimmed hedges below the
   window sills. Do not add anything else. No text, no people, no cars."""

def gemini():
    key = os.environ.get("GEMINI_API_KEY")
    if not key: return print("skip Gemini: GEMINI_API_KEY not set")
    model = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
    img = base64.b64encode(open(SRC, "rb").read()).decode()
    body = {"contents": [{"parts": [{"text": PROMPT}, {"inline_data": {"mime_type": "image/png", "data": img}}]}],
            "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]}}
    r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                      params={"key": key}, json=body, timeout=300)
    if r.status_code != 200: return print("Gemini error", r.status_code, r.text[:300])
    for part in r.json()["candidates"][0]["content"]["parts"]:
        d = part.get("inline_data") or part.get("inlineData")
        if d:
            p = os.path.join(OUT, "gemini-storefront.png"); open(p, "wb").write(base64.b64decode(d["data"])); print("wrote", p); return
    print("Gemini returned no image")

def openai():
    key = os.environ.get("OPENAI_API_KEY")
    if not key: return print("skip OpenAI: OPENAI_API_KEY not set")
    model = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")
    r = requests.post("https://api.openai.com/v1/images/edits", headers={"Authorization": f"Bearer {key}"},
                      files={"image": ("storefront.png", open(SRC, "rb"), "image/png")},
                      data={"model": model, "prompt": PROMPT, "size": "1536x1024", "quality": "high"}, timeout=300)
    if r.status_code != 200: return print("OpenAI error", r.status_code, r.text[:300])
    p = os.path.join(OUT, "openai-storefront.png"); open(p, "wb").write(base64.b64decode(r.json()["data"][0]["b64_json"])); print("wrote", p)

if __name__ == "__main__":
    which = sys.argv[1:] or ["gemini", "openai"]
    if "gemini" in which: gemini()
    if "openai" in which: openai()
