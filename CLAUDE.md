# portfolio-web

Ammaar's personal portfolio site, live at **https://ammaarkhan.com**.

## Hosting & deploys

- GitHub Pages, served from `main` branch root (repo: `ammaarkhan/portfolio-web`, custom domain via `CNAME`).
- **Pushing to `main` = deploying to production.** There is no staging. Don't push without Ammaar's go-ahead.
- No build step, no framework, no dependencies — plain HTML/CSS/JS, edited directly. Fonts load from Google Fonts.

## Design system (July 2026 redesign)

Redesigned July 3, 2026 from the old neon-dashed-cards look to "a typeset personal letter": minimal, refined, aimed at founders/collaborators.

- **Palette** (CSS vars in `styles.css`): warm charcoal bg `#161412`, bone ink `#eae4d8`, muted `#988d7d`, single sienna accent `#c98f5f` (quiet nod to the Weasel brand), hairline rules.
- **Type**: Fraunces (serif, weight ~340) for the name/headlines/epigraph; Karla (sans) for everything else. Lowercase tracked-out section labels (`now`, `before`, `notebook`, `elsewhere`).
- **Texture**: fixed `.glow` (faint sienna radial gradients) + `.grain` (SVG noise) overlays; staggered fade-up reveals on load (`.reveal`, respects reduced motion).
- **Voice**: lowercase, light emoji touch (👋 🛗), prose over bullet points. The elevator-music easter egg lives in the hero ("an elevator pitch deserves elevator music!"); the Bukowski quote closes the page as an epigraph.
- **No em dashes in site copy** (Ammaar's rule, Jul 2026). Use commas, periods, or middots instead. Obsidian note content on models.html is published verbatim and is exempt.
- Positioning (Jul 2026): The ADHD Weasel is a weekly newsletter helping 20k+ late-diagnosed women understand the science behind ADHD and feel less alone. Threads community: 287k. Use these numbers, not the old 18k/55k.
- Keep this personality — don't sanitize it, and don't reintroduce decoration (cards, borders, colors) that fights the quiet.

## Structure

- `index.html` + `styles.css` + `script.js` — homepage: hero → now → before (index rows) → notebook → elsewhere → epigraph. `script.js` only handles the elevator-music toggle (`lift.mp3`, optimistic UI, loops).
- `models.html` + `models.css` — **generated page**: the mental-models library. Never edit `models.html` by hand; regenerate it (see workflow).
- `scripts/build_models.py` — generator for `models.html`.
- `src/brokol.html` + `src/parkview.html` — story pages, both styled by shared `src/story.css` (plus `../styles.css` for vars/atmosphere). Founder log on brokol is append-only, newest on top.
- Images live in `src/`; keep them web-sized before committing (target < 300KB; `sips` works on this machine).

## Workflow

1. Edit files directly.
2. **Updating the mental models library** (routine): Ammaar edits notes in Obsidian at
   `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault/Atlas/Mental Models/`,
   then run `python3 scripts/build_models.py` to regenerate `models.html`. The script strips `{{ir::...}}` markers, skips `todo*` and empty notes, sorts alphabetically, and stamps the count + updated date. When asked to "update the models/library", this is the whole procedure.
3. Preview locally: `python3 -m http.server 8000` from repo root. Note: python's server can't stream the MP3 (no range requests), so the audio stalling locally is expected — it works on GitHub Pages.
4. Check both desktop and narrow/mobile widths — the audience largely arrives from social on phones.
5. Commit and push only when Ammaar says to (push = live deploy).

## Current state (July 3, 2026)

Working tree has the full redesign + models library, verified locally, **not yet committed or pushed**. Models content approved by Ammaar (Jul 8). Canonical links: newsletter = adhdweasel.com, threads = @theadhdweasel (threads.com), linkedin = /in/ammaarakhan. `elsewhere` order: linkedin, email, newsletter, threads, github.

Jul 8: story pages restyled into the design system (shared `src/story.css`; old brokol.css/parkview.css deleted), Marine Design Club removed from the site, parkview's empty gallery placeholder dropped, story-page numbers updated to 20k+/287k.

Still open before/after deploy:

- 1–2 real bullets for the Happipad era (currently just role/company/year).
- Confirm the app-shutdown date on the story page (log says June 2025; prose says "mid-2025").
