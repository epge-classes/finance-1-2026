# AGENTS.md
## Rules for AI Assistants (Codex / GitHub Copilot)

This repository contains material for a PhD-level Asset Pricing course.
Agents must follow these rules strictly.

---

## 1. Scope of Work

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

## 2. Pedagogical Constraints (Hard Rules)

- Slides are NOT lecture notes.
- Slides must be minimal, but not sterile.
- One core teaching point per slide.
- Fewer words is better.

If a slide looks "too empty", that is usually correct.
A sparse slide is often the right slide.

---

## 3. Slide Style Rules (Critical)

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

## 4. Notation Discipline (Non-negotiable)

- Do NOT introduce new notation if existing notation is already used.
- If asked to follow a paper, match the paper’s notation exactly.
- Keep notation consistent across slides and lectures.
- Never "simplify notation" unless explicitly requested.

---

## 5. Slide Flow and Quarto Conventions

- Only render `.qmd` files.
- Do NOT use Quarto to render `.md` files.
- Match the local lecture's style first: fragments, pacing, layout, notation, and naming.
- Preserve the lecture's sectioning pattern (`#` section dividers, `##` slide titles) unless asked otherwise.
- Preserve local conventions such as `Flight Plan` / `Our Agenda`, `Takeaways` / `Taking Stock`, and `## {.standout}` question slides.
- Columns, figure-only slides, LaTeX blocks, and custom theorem/definition environments are normal in this repo.
- Do not change formatting globally unless asked.

---

## 6. Citations & References

- Never hallucinate papers or citations.
- Prefer references already in `asset_pricing_references.bib`.
- If a paper is missing, add a comment: `TODO: add bib entry for <paper>`
- Do NOT invent a bibkey
- When editing a references slide, it can be denser than a normal content slide.

When citing a paper, be clear about:
- its main contribution
- why it mattered for the literature

---

## 7. Edit Discipline and Voice

- Keep diffs small.
- Do not reformat unrelated content.
- Do not reorder slides unless asked.
- Preserve the local tone: rhetorical questions, exercises, and occasional humor are part of the existing style.
- Do not inject jokes, slang, or pop-culture references unless that tone is already present nearby.
- Do not "normalize" older lectures to a new house style unless asked.
- If intent is unclear, leave a short `TODO` instead of guessing.

---

## 8. Code Assistance Rules

- Some lectures include Python snippets and longer data/plot chunks.
- Keep code reproducible and minimal.
- Use repo-relative paths and lecture-local files.
- Do NOT hardcode secrets, API keys, or machine-specific paths.
- If credentials are needed, use environment variables (e.g., `FRED_API_KEY`).
- Never commit keys or credentials.

---

## 9. Repository Structure (Source of Truth)

- `lectureXX/lectureXX.qmd` -> main teaching material
- `lectureXX/` may also contain lecture-local figures, tables, and data
- `Topics.md` -> tentative syllabus
- `Instructions_Research_Proposal.md` -> authoritative assignment rules
- `Instructions_Paper_Presentation.md` -> authoritative presentation rules

Do not duplicate or redefine rules across files.

---

## 10. Default Behavior

When unsure:
- do less, not more
- preserve structure
- preserve notation
- preserve pacing
- preserve voice
- preserve intent
- match the nearest neighboring slides before applying abstract rules
