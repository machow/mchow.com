# Annotated talk posts — design

Date: 2026-07-10
Status: approved

## Goal

Add four past talks to mchow.com as flat, annotated posts (slide image + narrative per slide), in the style of simonwillison.net's annotated presentations.

## Talks

1. **The Curse of Documentation** — posit::conf(2025). Video: https://youtu.be/ML8z8xkqIA0. Slides: Google Slides `1Qyh5cl339Sjgyn0mPo3rWh3EvTB7a0A3oK7JTVgnfkg` (40 slides).
2. **The Accidental Analytics Engineer** — dbt Coalesce. Video: https://www.youtube.com/live/EYdb1x1cO9U. Slides: Google Slides `1H2fVa-I4D8ibanlqLutIrwPOVypIlXVzEITDUNzzPpU` (37 slides).
3. **User Guides: engaging new users, delighting old ones** — SciPy 2025. Video: https://youtu.be/lHCOVqCZRFw. Slides: Google Slides `149UwdljTilauGPm0AXkROm9ArTcMfBfOVxgxaEnjSbQ` (39 slides).
4. **Making Beautiful, Publication Quality Tables in Python is Possible in 2024** — PyCon US 2024, co-presented with Rich Iannone. Primary video: Posit re-recording https://youtu.be/M5zwlb8OzS0; also link PyCon live recording https://youtu.be/08yLWPpFdo4. Slides: PDF from rich-iannone/presentations (45 slides).

## Decisions

- **Dating:** posts are backdated to the talk date (exact dates confirmed from video metadata / conference schedules).
- **Narrative:** derived from the YouTube transcript — what was actually said, edited into clean written prose per slide.
- **Curation:** light — drop blank transitions, duplicate animation-build slides, closing "thanks" slides. Every kept slide is visually checked for animation/export artifacts; funky slides get flagged for Michael to help fix rather than silently included.
- **GT talk:** Posit re-recording is the primary video/transcript source; Rich Iannone credited as co-presenter.

## Format

- Hugo page bundle per talk: `content/posts/YYYY-MM-DD-<slug>/index.md` + numbered slide PNGs (`01.png` …), matching the existing post-bundle pattern.
- Frontmatter matches existing posts (title, author, date, slug, tags).
- Post structure: intro paragraph (event, date, links to video + original slides), embedded YouTube iframe, then slide-by-slide image + narrative.
- Slide images exported at ~144 DPI (~1540px wide), compressed to keep repo growth reasonable (~20–40MB total for ~140 images).

## Constraints

- Nothing is pushed to GitHub; all work stays local.
