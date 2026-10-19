# Rebuilding the site

From the repo root:

    python tools/build/build.py              # writes index, drawings, photos, storage, research .html
    npm i playwright && node tools/build/pdf.js "$(pwd)"   # regenerates the three PDFs

Edit the page content in `storage_src.html` (Storage tab) and the `p_*.html` fragments (Renovation and Drawings),
then rebuild. `research-rows/*.json` are the raw rows behind `research.json`. Rebuild that file with
`python tools/build/merge.py .` (merge.py reads `rows/` next to it, so rename `research-rows` to `rows` or edit
the path first). `layout.py` draws the container layout on survey 1318.
