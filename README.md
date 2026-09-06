# dela Cerna Lab website

A Quarto website with reusable news and publication entries. Edit content; the site generates the timeline, homepage news, publication cards, numbering, and filters.

## Update entirely in your browser

1. Open this repository on GitHub. Choose the branch you want to update.
2. Open a file and select the pencil to edit it, or use **Add file → Create new file**.
3. Save your change. For a review first, choose a new branch and open a pull request.
4. The **Website** check builds the complete site and checks local links and assets. Its `website-preview` artifact contains the rendered site. Approved changes merged into `main` publish automatically to GitHub Pages.

The refresh branch does not publish to the live site. Publishing starts only after merge into main. When you are ready to make this version live, change **Settings → Pages → Build and deployment → Source** to **GitHub Actions**, then merge the refresh pull request. This is a one-time setup; the workflow does not change Pages settings itself. A repository administrator may need to allow GitHub Actions; check the Actions tab if a build does not start.

## Add news

Copy the contents of `templates/news.md` into a new file such as `content/news/2026-09-05-student-award.md`. Change the title, ISO date, categories, and story. Upload any image to `news/images/` with **Add file → Upload files**, then enter its path and description. Remove the template instructions and change `draft: true` to `draft: false`.

News is sorted by date, newest first. The three newest published stories also appear on the homepage. To preserve a date range, add an optional `date_label: "Nov 2–11, 2024"`; `date` controls sorting. Dates and future dates are not an automatic publishing schedule: use `draft: true` to withhold an entry.

## Add a publication

Copy `templates/publication.md` into `content/publications/012.md` (choose a new filename). Edit the year, unique order, categories, optional image, and citation. Remove template instructions and set `draft: false`. Keep the citation in normal Markdown: this preserves bold lab authors, italics, links, co-author notes, and in-press status.

Papers sort by year and order, newest first. Display numbering is generated. Categories are defined only once and produce both tags and filter buttons. Reuse existing category spelling; use `Structural Biology`, for example. Avoid commas inside category names. Search and category selection work together.

## Update a person

Edit that person's file in `people/`. Metadata at the top controls the team card; the text below controls the profile. Copy a current profile for a new member and change its name, image, role, categories, order, biography, and links. Research-page team links remain in `research/index.qmd`; update those if project membership changes.

For a departing member, add `alumni: true` to their profile metadata. This removes the card from the current team grid while preserving the profile URL. Add their tenure and next position to `people/alumni.qmd`. Existing historical alumni records remain there. No person's status is inferred automatically.

## Other edits

- Homepage: `index.qmd`
- Projects and team associations: `research/index.qmd`
- Joining instructions and contact details: `contact.qmd`
- Navigation: `_quarto.yml`
- Shared colors and typography: `theme.scss`
- Layout and component styling: `styles.css`

Use `.qmd` links for internal pages and exact image filename capitalization. Keep scientific figures legible; optimized WebP copies are generated during the build for larger existing images, and originals remain available. The source mapping is in `scripts/image-sources.json`; edits to an original image regenerate its web copy on the next build.

## Local preview and build

Install Quarto 1.8.27 and Python 3.11 or newer, then run:

```sh
python3 -m pip install -r requirements.txt
python3 scripts/site.py preview
```

For a complete validation:

```sh
python3 scripts/site.py render
python3 scripts/check-site.py
```

The site wrapper bootstraps generated includes before Quarto scans a fresh checkout. A pre-render script validates content and creates `_generated/` includes. Never edit those includes or `_site/` output by hand. Generated output and Quarto caches are excluded from version control.

## Publishing and rollback

The GitHub workflow renders and validates on pull requests and pushes to `main`. Only a successful main-branch build can publish. To undo a content change, revert its pull request in GitHub and merge the revert; the workflow republishes the previous content. A failed build leaves the last published site intact.
