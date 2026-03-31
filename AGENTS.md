# AGENTS.md
## Rules for AI Assistants (Codex / GitHub Copilot)

This repository contains material for a PhD-level Asset Pricing course.
Agents must follow these rules strictly.

---

## 1. What This Repo Actually Contains

- Main teaching files are Quarto slides in `lectureXX/lectureXX.qmd`.
- Exception: lecture 0 lives in `lecture00/lecture0.qmd`.
- Lecture folders often also contain lecture-local figures, tables, data, and a rendered PDF.
- `asset_pricing_references.bib` is the citation source for lecture slides.
- `Topics.md` is the tentative syllabus and reading list.
- `Instructions_Research_Proposal.md` and `Instructions_Paper_Presentation.md` are the authoritative assignment-policy files.
- `_quarto.yml` and `beamer_template.tex` define the repo-wide slide rendering setup.

Implication:
- edit source files, not outputs
- if a lecture has both `.qmd` and `.pdf`, change the `.qmd`
- do not redefine assignment rules inside slides or other files

---

## 2. Scope of Work

You may be asked to:
- edit Quarto slides (`.qmd`)
- add derivations
- explain papers
- add Python snippets (including figure/table generation when a lecture already does this)
- suggest references

You must NOT:
- change course policies or logistics
- refactor files wholesale
- rewrite content unless explicitly asked

Prefer minimal, surgical edits.
Preserve the established flow, pacing, and voice unless the user asks to change them.

---

## 3. Pedagogical Constraints (Hard Rules)

- Slides are NOT lecture notes.
- Slides must be minimal, but not sterile.
- One core teaching point per slide.
- Fewer words is better.

If a slide looks "too empty", that is usually correct.
A sparse slide is often the right slide.

---

## 4. Match the Local Lecture Before Global Rules

- The lectures are consistent in spirit, but not perfectly uniform in execution.
- Do NOT harmonize older lectures to the style of newer lectures unless explicitly asked.
- Before editing, inspect nearby slides in the same lecture and match:
  - title style
  - pacing
  - notation
  - use of fragments (`. . .`)
  - use of columns
  - figure style
  - theorem/definition environments
  - intro and closing slide naming
- If local style and generic advice conflict, local style wins.

---

## 5. Slide Style Rules (Critical)

When generating or editing slides:

- Avoid paragraphs. A one-line setup, transition, or punchline is fine when it improves flow.
- Prefer short bullets. Default: 3-6.
- 7-9 bullets are acceptable on agenda, takeaway, reference, or logistics-heavy slides.
- Prefer equations over prose when they carry the main idea.
- One main equation block is the default.
- Two compact display blocks are acceptable on derivation, comparison, or "definition + implication" slides.
- Titles should be short and informative.
- Do not compress multiple logical steps just to save slides.

Derivations:
- Split across multiple slides.
- One logical step per slide.
- Use short bridge lines, reveals, or a compact reminder equation when needed.
- Do not create new walls of math.
- Dense math is only acceptable when the surrounding lecture already uses it and the content requires it.

---

## 6. Notation Discipline (Non-negotiable)

- Do NOT introduce new notation if existing notation is already used.
- If asked to follow a paper, match the paper’s notation exactly.
- Keep notation consistent across slides and lectures.
- Never "simplify notation" unless explicitly requested.

---

## 7. Repo-Specific Slide Flow and Quarto Conventions

- Only render `.qmd` files.
- Do NOT use Quarto to render `.md` files.
- Preserve the lecture's sectioning pattern (`#` section dividers, `##` slide titles) unless asked otherwise.
- Common patterns in this repo include:
  - `# Intro`
  - `## Intro`, `## Why This Lecture?`, `## Flight Plan`, or `## Our Agenda`
  - `# Part I`, `# Part II`, ...
  - `## {.standout}` question slides
  - `## Takeaways` or `## Taking Stock`
  - `## Readings and References {.noframenumbering .allowframebreaks}`
- Reuse these patterns when extending a lecture, but only if they are already present nearby.
- Columns, figure-only slides, LaTeX blocks, reveal fragments, and custom environments such as `mydef` are all normal in this repo.
- Preserve existing front matter when present. Do not add or remove fields just for consistency.
- Many lectures use `bibliography: ../asset_pricing_references.bib`; newer ones may also include `date:` and `callout-appearance: minimal`.
- Do not restyle slides independently of `_quarto.yml` and `beamer_template.tex`.
- Do not change formatting globally unless asked.

---

## 8. Citations and References

- Never hallucinate papers or citations.
- Prefer references already in `asset_pricing_references.bib`.
- If a paper is missing, add a comment: `TODO: add bib entry for <paper>`
- Do NOT invent a bibkey
- When editing a references slide, it can be denser than a normal content slide.
- In lecture `.qmd` files, use Pandoc citation syntax such as `@AuthorYearKey`.
- In markdown files such as `Topics.md`, `README.md`, and assignment instructions, use markdown links and plain text instead of Pandoc citations.

When citing a paper, be clear about:
- its main contribution
- why it mattered for the literature

---

## 9. Code, Figures, and Data Chunks

- Some lectures include Python snippets and longer figure-generation chunks.
- Hidden code chunks with options such as `#| echo: false`, `#| warning: false`, and `#| message: false` are common.
- Match the local chunk style before introducing a new chunk.
- Keep code reproducible and minimal.
- Use repo-relative paths or lecture-local files, matching the local lecture.
- If a lecture already uses `pyprojroot`, keep that style there.
- If a lecture already uses local relative paths, keep that style there.
- Put new lecture-specific assets in the same lecture folder unless the existing lecture uses another pattern.
- Do NOT hardcode secrets, API keys, or machine-specific paths.
- If credentials are needed, use environment variables (e.g., `FRED_API_KEY`).
- Never commit keys or credentials.

---

## 10. File-Type-Specific Rules

### Lecture files (`lectureXX/lectureXX.qmd`)

- Preserve lecture-local tone, structure, and notation.
- Do not reorder slides unless asked.
- Do not turn slides into notes.
- Do not clean up unrelated wording while making a local edit.

### `Topics.md`

- Keep the format `### Lecture N: Title`.
- Add concise reading bullets, not long prose.
- Use markdown links or book shorthand already used in the file.
- Do not silently rewrite older entries to a new style.

### `README.md`

- Treat this as course-facing administrative context.
- Do not change logistics, evaluation, or policy unless explicitly asked.

### Assignment instruction files

- Treat `Instructions_Research_Proposal.md` and `Instructions_Paper_Presentation.md` as authoritative.
- If asked to update related material elsewhere, point back to these files instead of duplicating rules.

Do not duplicate or redefine rules across files.

---

## 11. Edit Discipline and Voice

- Keep diffs small.
- Do not reformat unrelated content.
- Do not reorder slides unless asked.
- Preserve the local tone: rhetorical questions, exercises, direct phrasing, and occasional humor are part of the existing style.
- Do not inject jokes, slang, or pop-culture references unless that tone is already present nearby.
- Do not "normalize" older lectures to a new house style unless asked.
- If intent is unclear, leave a short `TODO` instead of guessing.

---

## 12. Default Workflow

Before editing:
- identify the target file type
- inspect nearby material in the same lecture or file
- locate the existing notation and slide rhythm
- check whether the task belongs in a lecture, `Topics.md`, `README.md`, or an assignment instruction file

When unsure:
- do less, not more
- preserve structure
- preserve notation
- preserve pacing
- preserve voice
- preserve intent
- match the nearest neighboring slides before applying abstract rules
