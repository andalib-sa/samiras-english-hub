# Samira’s English Hub

A free, editable English-learning resource hub built as a static site for GitHub Pages, with Decap CMS for browser-based content editing.

## What is included

- Responsive homepage with interactive skill tiles
- Searchable/filterable English resource library
- Academic English, Dictionaries, Communities, About and Contact pages
- Australia-focused resource section
- Decap CMS editor at `/admin/`
- Automatic GitHub Pages deployment on every content change
- Resources stored as simple JSON files so your content is portable

## Local preview

```bash
python build.py
cd _site
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Publishing

GitHub Pages is enabled and deployment is handled automatically by `.github/workflows/deploy.yml` on pushes to `main`.

The site has been restored to the stable pre-preview-card version.

## CMS setup

Follow `SETUP.md` to connect the Decap CMS login after the public site is live.
