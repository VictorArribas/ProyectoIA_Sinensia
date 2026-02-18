# Repository Guidelines

## Project Structure & Module Organization
- Main content lives in `index.html`, a standalone single-page demo of HTML/CSS and the visible entry point reviewers see in the browser.
- Supporting notes are in `BRAINSTORMING.md`, which describes the ProyectoIA_Sinensia concept and should stay in sync with any feature updates or adjustments.
- Configuration for Claude/Serena agents is under the hidden `.claude/` and `.specify/` directories; avoid editing these unless you understand the automation they drive.
- No subdirectories for src/tests exist yet, so add new folders only when the feature scope justifies a more complex layout and document the addition here.

## Build, Test, and Development Commands
- Run `start .\index.html` (Windows) or `python -m http.server 8000` to preview the page locally; refresh the browser after editing.
- No build step is required because the repo is plain HTML/CSS, but rerun the preview command after every stylesheet or markup change to confirm it loads.
- If you do introduce tooling (npm, bundler, etc.), add the commands here and keep dependencies in a manifest so others can run them verbatim.

## Coding Style & Naming Conventions
- Use four spaces for indentation in HTML and CSS blocks, matching the existing `index.html` layout for consistency.
- Prefer descriptive, lowercase filenames without spaces (e.g., `feature-panel.html`) and keep assets grouped logically if the repo grows.
- Inline CSS is acceptable for small demos, but larger styles should migrate to a dedicated `.css` file with well-named selectors.

## Testing Guidelines
- There are no automated tests; rely on manual verification by reloading `index.html` in a browser and checking that the layout and copy match the intended message.
- Note any visuals or responsiveness issues in a PR description so reviewers know what to look for.

## Commit & Pull Request Guidelines
- Follow the existing pattern of concise, descriptive messages (often Spanish present-tense phrases) like `Agregar hero section` or `Actualizar estilo del botón`.
- Each PR should explain what changed, why it matters, and link to the related idea in `BRAINSTORMING.md` when relevant; include screenshots if you touched visual elements.
- Run a quick preview before committing so your description can confidently say what the page looks like after your changes.
