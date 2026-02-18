# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ProyectoIA_Sinensia**: Coach deportivo inteligente mediante LLMs. Proyecto para el Curso de IA y ML de Sinensia.

This is an early-stage web application project focused on building an AI-powered sports coaching system using Large Language Models.

## Development Workflow

### Feature Development with Speckit

This project uses **Speckit**, a specification-driven development system. All feature work follows this workflow:

1. **Specify** (`/specify`): Create feature specification from natural language description
2. **Clarify** (`/clarify`): Identify and resolve underspecified requirements
3. **Plan** (`/plan`): Generate implementation design and architecture
4. **Tasks** (`/tasks`): Break down plan into actionable, dependency-ordered tasks
5. **Implement** (`/implement`): Execute all tasks from tasks.md
6. **Analyze** (`/analyze`): Cross-artifact consistency check (spec/plan/tasks)

### PowerShell Scripts

The `.specify/scripts/powershell/` directory contains automation scripts:

- `create-new-feature.ps1`: Creates numbered feature branches and directories
  - Auto-generates branch names from descriptions
  - Creates feature directory in `specs/###-feature-name/`
  - Sets up spec.md from template
  - Usage: `./create-new-feature.ps1 "Add user authentication"`

- `setup-plan.ps1`: Initializes plan.md for implementation planning
- `update-agent-context.ps1`: Updates agent context information
- `check-prerequisites.ps1`: Validates development environment

All scripts support `-Json` flag for machine-readable output and `-Help` for usage information.

## Project Structure

```
/
├── index.html              # Main web application (current: "Hola Mundo" demo)
├── specs/                  # Feature specifications organized by number
│   └── ###-feature-name/  # Each feature gets numbered directory
│       ├── spec.md        # Feature specification
│       ├── plan.md        # Implementation plan (optional)
│       └── tasks.md       # Task breakdown (optional)
├── .specify/
│   ├── templates/         # Templates for spec, plan, tasks, constitution
│   ├── scripts/           # PowerShell automation scripts
│   └── memory/            # Project constitution and principles
├── .serena/
│   ├── memories/          # Persistent memory across conversations
│   └── project.yml        # Serena MCP server project config
└── .claude/
    └── commands/          # Speckit slash command definitions
```

## Architecture

### Current State
- Single-page HTML application with embedded CSS
- No external dependencies or build system yet
- No JavaScript modules yet
- Gradient purple theme (background: #667eea to #764ba2)

### MCP Servers
- **Serena**: Semantic code analysis and intelligent editing tools (via uvx from GitHub)
- Configured in `.mcp.json`

## Feature Branch Naming

Features use numeric prefixes for ordering: `001-feature-name`, `002-another-feature`, etc.
- Numbers auto-increment based on existing branches and spec directories
- Branch names are sanitized (lowercase, hyphens, max 244 chars for GitHub)
- The `SPECIFY_FEATURE` environment variable tracks the active feature

## Constitution System

The project supports a constitution-based development approach stored in `.specify/memory/constitution.md`. Use `/constitution` to create or update core principles that govern development decisions.

When starting significant architectural work, consider whether project principles should be documented in the constitution first.
