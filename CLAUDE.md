# portfolio-web

Ammaar's personal portfolio site, live at **https://ammaarkhan.com**.

## Hosting & deploys

- GitHub Pages, served from `main` branch root (repo: `ammaarkhan/portfolio-web`, custom domain via `CNAME`).
- **Pushing to `main` = deploying to production.** There is no staging. Commit and push after every change (global Always Push rule), then verify the deploy (workflow step 7).
- No build step, no framework, no dependencies — plain HTML/CSS/JS, edited directly. Fonts load from Google Fonts.

## Design system (July 2026 redesign)

Redesigned July 3, 2026 from the old neon-dashed-cards look to "a typeset personal letter": minimal, refined, aimed at founders/collaborators.

- **Palette** (CSS vars in `styles.css`): warm charcoal bg `#161412`, bone ink `#eae4d8`, muted `#a89d8c`, faint `#8b8173`, single cool accent `#48b6cc`, hairline rules. All four pass WCAG AA on the bg; check with a contrast calc before changing any of them. The `.glow` wash stays warm sienna on purpose, so a cool accent reads against a warm atmosphere. Accent-derived colours go through `--accent-line`, never hardcoded rgba.
- **Type**: Fraunces (serif, weight ~340) for the name/headlines/epigraph; Schibsted Grotesk (sans) for everything else, picked over Space Grotesk because the captions and pitch note need true italics. Lowercase section labels (`now`, `before`, `notebook`, `reading`, `elsewhere`) at 0.84rem/0.14em. Don't shrink small text below ~0.8rem or track it past ~0.15em, that combination is what made the July build hard to read.
- **Texture**: fixed `.glow` (faint sienna radial gradients) + `.grain` (SVG noise) overlays; staggered fade-up reveals on load (`.reveal`, respects reduced motion).
- **Voice**: lowercase, light emoji touch (👋 🛗), prose over bullet points. The elevator-music easter egg lives in the hero ("an elevator pitch deserves elevator music!"); the Bukowski quote closes the page as an epigraph.
- **No em dashes in site copy** (Ammaar's rule, Jul 2026). Use commas, periods, or middots instead. Obsidian note content on models.html is published verbatim and is exempt.
- Positioning (Aug 2026): The ADHD Weasel is a weekly newsletter helping 36k+ late-diagnosed women understand the science behind ADHD and feel less alone. Threads community: 290k. 250+ ADHD interviews, a running total that includes interviews after the pivot, so don't attribute all of them to the 2024 listening period.
- Canonical links: newsletter adhdweasel.com &middot; threads.com/@theadhdweasel &middot; instagram.com/theadhdweasel &middot; linkedin.com/in/ammaarakhan (extra "a" is correct) &middot; github.com/ammaarkhan &middot; ammaarkhan03@gmail.com. Homepage `elsewhere` order: linkedin, email, newsletter, threads, github.
- Keep this personality — don't sanitize it, and don't reintroduce decoration (cards, borders, colors) that fights the quiet.

## Structure

- `index.html` + `styles.css` + `script.js` — homepage: hero → now → notebook → reading → before (index rows) → elsewhere → epigraph. `script.js` only handles the elevator-music toggle (`lift.mp3`, optimistic UI, loops). Reveal delays in `styles.css` are indexed by `nth-of-type`, so adding or removing a section means updating them.
- `models.html` + `models.css` — **generated page**: the mental-models library. Never edit `models.html` by hand; regenerate it (see workflow).
- `scripts/build_models.py` — generator for `models.html`.
- `reading.html` + `reading.css` — books grouped by month, newest month first. Covers are self-hosted in `src/books/`. Books in progress sit in their own month block at the top with `<span class="shelf-now">&middot; currently reading</span>` inside the `.shelf-date`; the meta line under the title counts finished books and in-progress books separately ("13 books · 2 in progress · updated september 2026"). Source of truth for what was read is the monthly update emails in `~/Desktop/Ammaar/02 Career/Monthly Updates/Archive/` (moved out of Weasel-HQ Oct 2026). Every sent email's reading gets added here as step 9 of that folder's checklist. When a meta-line count hits zero in progress, drop that part.
- `src/brokol.html` + `src/parkview.html` — story pages, both styled by shared `src/story.css` (plus `../styles.css` for vars/atmosphere). The brokol log is one chronological timeline, **oldest first**, with each artifact sitting inside its own entry (`figure.story-figure` within `.log-entry`). There is no separate gallery section; new milestones go in as a dated entry with the image under the prose.
- Images live in `src/`; keep them web-sized before committing (target < 300KB; `sips` works on this machine).

## Workflow

1. Edit files directly.
2. **Updating the mental models library** (routine): Ammaar edits notes in Obsidian at
   `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault/Atlas/Mental Models/`,
   then run `python3 scripts/build_models.py` to regenerate `models.html`. The script strips `{{ir::...}}` markers, skips `todo*` and empty notes, sorts alphabetically, and stamps the count + updated date. When asked to "update the models/library", this is the whole procedure.
3. **Adding books to the reading page** (routine): Ammaar gives the titles and whether they're finished or in progress.
   - Cover: `curl -sL -o src/books/<slug>.jpg "https://covers.openlibrary.org/b/isbn/<isbn>-L.jpg?default=false"`. Look at the image before committing: it must be the English edition, not French or audiobook-only. ~330×500px and under 40KB is what the others are.
   - Markup: copy an existing `.shelf-month` block, place it in date order (newest first). For books in progress, add the `shelf-now` span to the date line.
   - Update the meta line (finished count, in-progress count, "updated <month year>").
   - When an in-progress book is finished: drop the `shelf-now` span (or move the book into the month it was finished), then fix both counts.
4. Preview locally: `python3 -m http.server 8000` from repo root. Note: python's server can't stream the MP3 (no range requests), so the audio stalling locally is expected — it works on GitHub Pages.
5. Check both desktop and narrow/mobile widths — the audience largely arrives from social on phones. Headless Chrome `--screenshot --window-size=390,...` crops at ~500px instead of reflowing, so a cut-off right edge in that screenshot is the tool, not an overflow; compare against the live page at the same settings before chasing it.
6. Commit and push after every change (push = live deploy).
7. After pushing, verify the deploy: poll `gh api repos/ammaarkhan/portfolio-web/pages/builds/latest --jq '.status'` until it reads "built" (typically under a minute), then curl ammaarkhan.com for a string from the change.

## Current state (updated Oct 1, 2026)

Deployed: refreshed Weasel story page (chronological log with inline artifacts, real brand logo), the `reading` page (15 finished through September 2026, none in progress; Principles is listed as "Principles (Part 1)", the only part he read), updated numbers, and a type/colour pass for legibility.

Open items:
- The separation from The ADHD Weasel is **not closed** (upfront due ~Aug 15 2026). The site deliberately still reads present tense, "Co-founder of The ADHD Weasel". Ammaar's call on when that changes, don't pre-empt it.
- The July 2024 log entry still says "more than 200 ADHDers" while the signals block says 250+. Needs the real number for that window.
- Copy on this page has been wrong twice in ways only Ammaar could catch (a fabricated "teach us first" quote, and framing the pivot insight as a vague "education gap"). The real story: readers had been diagnosed recently, nobody had explained the science, so they blamed themselves. Nobody ever asked to be taught, that was read between the lines. Never invent a quote.

## Sibling project

`~/Desktop/projects/life` — Ammaar's private life tracker (life.ammaarkhan.com), same design system, separate repos (`life-web` public shell + `life-data` private). It has its own CLAUDE.md; work on it from that folder, not here.
