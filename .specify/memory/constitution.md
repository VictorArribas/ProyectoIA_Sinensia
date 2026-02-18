<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles: None
- Added sections: AI Coaching Principles (5 new domain-specific principles)
- Removed sections: None
- New principles added:
  - VII. Seguridad ante todo (Safety First)
  - VIII. Base Científica (Scientific Foundation)
  - IX. Privacidad de datos (Data Privacy)
  - X. Claridad Técnica (Technical Clarity)
  - XI. Neutralidad Tecnológica (Technological Neutrality)
- Templates requiring updates:
  ✅ spec-template.md - Should now include safety/scientific validation in acceptance criteria
  ✅ plan-template.md - Constitution Check must validate AI coaching principles
  ✅ tasks-template.md - Tasks should include privacy, safety, and clarity validation steps
- Follow-up TODOs:
  - Consider adding medical disclaimer template to .specify/templates/
  - Document sensitive data handling guidelines in AGENTS.md
-->

# ProyectoIA_Sinensia Constitution

## Core Principles

### I. Specification-First Development

Every feature MUST follow the Speckit workflow in order:

1. **Specify** (`/specify`): Create feature specification from natural language
2. **Clarify** (`/clarify`): Resolve underspecified requirements through targeted questions
3. **Plan** (`/plan`): Generate implementation design and architecture
4. **Tasks** (`/tasks`): Break down plan into actionable, dependency-ordered tasks
5. **Implement** (`/implement`): Execute all tasks from tasks.md

**Rationale**: Speckit ensures thoughtful design before implementation, reducing rework and maintaining consistency across the codebase. This is non-negotiable for features but does not apply to bug fixes or minor adjustments to existing code.

### II. User Story Independence

Each user story in a feature specification MUST be:

- **Independently implementable**: Can be developed without completing other stories
- **Independently testable**: Can be verified and demonstrated on its own
- **Independently deployable**: Delivers standalone value as an MVP increment
- **Prioritized**: Assigned P1 (critical), P2 (important), or P3 (enhancement) based on user value

**Rationale**: Independent user stories enable incremental delivery, parallel development, and flexible scope adjustment. They allow the team to ship MVP functionality quickly and validate value before investing in additional features.

### III. Simplicity & YAGNI (You Aren't Gonna Need It)

Start with the simplest solution that meets requirements:

- **Inline CSS acceptable** for initial demos; migrate to separate `.css` files only when complexity justifies it
- **No build system** until external dependencies require one
- **No subdirectories** until file count or logical grouping makes them necessary
- **No abstractions** until patterns repeat 3+ times
- **Justify complexity**: All deviations from simplicity MUST be documented in plan.md Complexity Tracking table

**Rationale**: Premature optimization and over-engineering waste time and create maintenance burden. Simple solutions are easier to understand, modify, and debug. The project is in early stages; let requirements drive architecture, not speculation.

### IV. Manual Quality Assurance

Before committing any visual or functional change:

- **MUST preview** `index.html` in a browser (via `start .\index.html` or `python -m http.server 8000`)
- **MUST verify** the page loads correctly and displays intended changes
- **MUST note** any visual or responsiveness issues in PR description
- **Testing philosophy**: Manual verification via browser is the standard; automated tests are OPTIONAL unless explicitly requested in the feature specification

**Rationale**: For an early-stage HTML/CSS project, manual browser testing provides immediate feedback and catches issues faster than setting up test infrastructure. Automated testing will be introduced when complexity and risk justify the investment.

### V. Incremental Growth

Add project structure complexity only when scope justifies it:

- **Current state**: Single `index.html` with embedded CSS
- **Growth triggers**:
  - Multiple HTML pages → create `pages/` or `views/` directory
  - Significant CSS → create `styles/` directory with modular stylesheets
  - JavaScript logic → create `scripts/` or `src/js/` directory
  - Backend API needed → create `backend/` or `api/` directory
  - Tests added → create `tests/` directory
- **MUST document** structural changes in AGENTS.md under "Project Structure & Module Organization"

**Rationale**: Directory structure should reflect actual complexity, not anticipated complexity. Flat structure is easier to navigate for small projects; premature directory hierarchy adds cognitive overhead without benefit.

### VI. Documentation Synchronization

Keep documentation in sync across artifacts:

- **BRAINSTORMING.md**: High-level project concept and goals
- **AGENTS.md**: Repository guidelines, coding standards, commit conventions
- **CLAUDE.md**: Agent instructions, Speckit workflow, project structure
- **specs/###-feature-name/spec.md**: Individual feature specifications
- **constitution.md**: This file (core principles and governance)

**When updating**:
- New feature → update BRAINSTORMING.md if concept changes
- New directory/file convention → update AGENTS.md
- New Speckit workflow step → update CLAUDE.md
- New principle/governance rule → update constitution.md + check template alignment

**Rationale**: Documentation drift creates confusion and wasted effort. Synchronized documentation ensures all contributors (human and AI) operate from the same understanding.

## AI Coaching Principles

These domain-specific principles govern the behavior and recommendations of the AI sports coaching system. They are **NON-NEGOTIABLE** and take precedence over development convenience.

### VII. Seguridad ante todo (Safety First)

**CRITICAL - NON-NEGOTIABLE**:

- The AI MUST NEVER suggest weights, exercises, or training modifications if the user reports pain, injury, or discomfort
- Every training recommendation MUST include a medical disclaimer stating: "Consult with a healthcare professional before starting any exercise program. Stop immediately if you experience pain."
- If a user reports pain during or after exercise, the AI MUST recommend stopping and consulting a medical professional
- The system MUST NOT provide medical diagnosis or treatment advice
- Error on the side of caution: when in doubt, recommend conservative progressions and medical consultation

**Rationale**: User safety is paramount. An AI coach cannot assess physical conditions like a medical professional and must never risk user injury. Legal liability and ethical responsibility require explicit disclaimers and conservative recommendations.

### VIII. Base Científica (Scientific Foundation)

All training recommendations MUST be grounded in evidence-based sports science:

- **Hypertrophy principles**: Progressive overload, mechanical tension, metabolic stress, muscle damage (Schoenfeld, 2010)
- **Strength training**: Specificity, progressive resistance, adequate recovery (Kraemer & Ratamess, 2004)
- **Periodization**: Structured variation in volume, intensity, and exercise selection (Rhea et al., 2003)
- **NO pseudoscience**: Reject spot reduction, detox claims, "toning" myths, or unvalidated supplements
- **Citations preferred**: When possible, reference recognized sources (NSCA, ACSM, peer-reviewed research)

**Prohibited**:
- "Toning" or "lengthening" muscles (physiologically inaccurate)
- Spot reduction of fat (not supported by evidence)
- Unrealistic timelines ("6-pack in 2 weeks")
- Unvalidated supplements or extreme diets

**Rationale**: Evidence-based recommendations build user trust and deliver real results. Pseudoscience undermines credibility and can harm users through ineffective or dangerous practices.

### IX. Privacidad de datos (Data Privacy)

User health and biometric data MUST be treated as **sensitive personal information**:

- **Data minimization**: Only collect data necessary for coaching functionality
- **No third-party sharing**: User health data must never be shared with third parties without explicit, informed consent
- **Local storage preferred**: When possible, store sensitive data locally on the user's device
- **Encryption**: If data is transmitted or stored server-side, use encryption (TLS in transit, AES-256 at rest)
- **Anonymization**: Analytics and aggregated data must be fully anonymized
- **Right to deletion**: Users must be able to delete all their data permanently
- **Transparency**: Privacy policy must clearly explain what data is collected, how it's used, and how long it's retained

**Sensitive data includes**: Weight, body measurements, medical history, fitness level, injuries, photos, age, health conditions.

**Rationale**: Health data is highly personal and legally protected (GDPR, HIPAA principles). Mishandling user data can cause harm, erode trust, and create legal liability. Users must maintain full control over their personal information.

### X. Claridad Técnica (Technical Clarity)

Exercise instructions and training guidance MUST be clear, concise, and accessible to beginners:

- **Simple language**: Avoid jargon; explain technical terms when first introduced
- **Step-by-step instructions**: Break down complex movements into discrete steps
- **Visual cues**: When possible, provide or reference images/videos demonstrating proper form
- **Common mistakes**: Proactively warn about frequent errors (e.g., "Keep your back straight, don't round your spine")
- **Beginner-first**: Write for someone with zero training experience; advanced users can always skip details
- **Concise format**: Use bullet points, numbered lists, and short sentences (max 20 words)

**Example - Good**:
> **Squat**: Stand with feet shoulder-width apart. Lower your hips back and down as if sitting in a chair. Keep your chest up and knees tracking over your toes. Stop when thighs are parallel to the floor. Push through your heels to stand up.

**Example - Bad**:
> Execute a bilateral lower-extremity compound movement pattern involving hip and knee flexion with maintenance of neutral spinal alignment through the eccentric and concentric phases.

**Rationale**: Complex instructions create barriers to entry and increase injury risk through poor form. Clear, simple guidance empowers beginners and ensures safer, more effective training.

### XI. Neutralidad Tecnológica (Technological Neutrality)

Code architecture MUST prioritize maintainability and flexibility over framework lock-in:

- **Modular design**: Separate business logic (training algorithms, exercise selection) from UI/framework code
- **Minimal dependencies**: Avoid heavy frameworks unless they provide clear, irreplaceable value
- **Standard interfaces**: Use well-defined APIs/interfaces between modules to enable component replacement
- **Framework-agnostic core**: Training logic should be framework-independent (no React/Vue/Angular in core algorithms)
- **No vendor lock-in**: Avoid proprietary platforms or services that prevent migration (when feasible)
- **Progressive enhancement**: Start with simple, working solutions; add complexity only when needed

**Architecture pattern**:
```
core/
  ├── training-logic/     # Pure functions, no framework dependencies
  ├── exercise-library/   # Data models and validation
  └── recommendation-engine/
ui/
  └── [framework]/        # Framework-specific presentation layer
```

**Rationale**: Technology churn is inevitable. Modular, dependency-light code survives framework changes, reduces maintenance burden, and makes testing easier. This aligns with Principle III (Simplicity & YAGNI) but emphasizes long-term architectural flexibility.

## Development Standards

### Coding Style

- **Indentation**: 4 spaces for HTML and CSS blocks
- **Filenames**: Lowercase, descriptive, hyphen-separated (e.g., `feature-panel.html`)
- **CSS organization**: Inline acceptable for demos; migrate to external files when styles exceed ~50 lines or are reused
- **Asset grouping**: Keep related assets logically grouped if the repo grows

### Commit & Pull Request Guidelines

- **Commit messages**: Concise, descriptive, often Spanish present-tense phrases (e.g., `Agregar hero section`, `Actualizar estilo del botón`)
- **PR description MUST include**:
  - What changed
  - Why it matters
  - Link to related spec or BRAINSTORMING.md section
  - Screenshots if visual elements were modified
- **Before committing**: Run preview command to ensure page loads correctly

### Branch Naming

- **Feature branches**: Numeric prefixes for ordering (`001-feature-name`, `002-another-feature`)
- **Auto-increment**: Numbers based on existing branches and spec directories
- **Sanitization**: Lowercase, hyphens, max 244 characters for GitHub compatibility
- **Environment variable**: `SPECIFY_FEATURE` tracks the active feature

## Quality Gates

### Constitution Compliance Check

**REQUIRED** before Phase 0 research in `/plan` workflow and re-checked after Phase 1 design.

All features MUST pass these gates:

### Development Process Gates
1. **Specification exists**: Feature has a completed spec.md with user stories, requirements, and success criteria
2. **Simplicity justified**: Any complexity beyond "single HTML file with inline CSS" is documented in plan.md Complexity Tracking table
3. **User stories independent**: Each story can be tested and deployed independently
4. **Preview performed**: Visual changes have been browser-tested before commit

### AI Coaching Compliance Gates
5. **Safety validation**: Features involving exercise recommendations include medical disclaimers and pain detection/warnings
6. **Scientific accuracy**: All training advice references evidence-based principles (no pseudoscience)
7. **Privacy by design**: Features collecting user data document data handling, storage, encryption, and deletion procedures
8. **Clarity check**: Exercise instructions and guidance are written at beginner comprehension level (validated by readability review)
9. **Modularity verified**: Business logic is separated from UI framework code (core training logic is framework-agnostic)

### Complexity Justification

When plan.md shows violations of simplicity principles:

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [Example: External CSS file] | [Styles exceed 50 lines, reused across pages] | [Inline CSS causes duplication and maintenance burden] |

**Gate**: If complexity cannot be justified, return to clarification or simplify the design.

## Governance

### Amendment Procedure

1. **Proposal**: Submit proposed change with rationale (via `/constitution` command or PR)
2. **Impact assessment**: Check affected templates (spec, plan, tasks) and documentation files
3. **Version bump**: Apply semantic versioning (MAJOR.MINOR.PATCH)
4. **Sync updates**: Update all dependent artifacts before finalizing
5. **Approval**: User/project lead approves the change
6. **Migration plan**: Document any necessary changes to existing features or workflows

### Versioning Policy

- **MAJOR (X.0.0)**: Backward-incompatible changes (e.g., removing a required principle, changing workflow order)
- **MINOR (0.X.0)**: New principles added or materially expanded guidance (e.g., adding security requirements)
- **PATCH (0.0.X)**: Clarifications, wording improvements, typo fixes

### Compliance Review

- **All PRs** should reference constitution principles when making architectural decisions
- **Plan phase** includes mandatory Constitution Check gate
- **Deviations** from principles MUST be justified in plan.md Complexity Tracking table
- **Project lead** may request constitution amendments when patterns emerge that aren't well-served by current principles

### Runtime Development Guidance

For day-to-day development practices not covered in this constitution, refer to:

- **CLAUDE.md**: Agent-specific instructions for Claude Code
- **AGENTS.md**: Repository guidelines, coding standards, commit conventions
- **Speckit templates**: Detailed workflow instructions in `.specify/templates/commands/*.md`

**Version**: 1.1.0 | **Ratified**: 2026-02-17 | **Last Amended**: 2026-02-17
