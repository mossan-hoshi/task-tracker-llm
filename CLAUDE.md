# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python desktop task tracking application using Tkinter for GUI. The app allows users to track work time by starting/stopping/pausing tasks, then automatically categorizes the work using Google Gemini API and exports summaries in Markdown format.

**Tech Stack:**
- Python 3.12+
- Tkinter (built-in GUI library)
- Google Gemini Generative AI API
- No persistent data storage (memory-only, exports to clipboard)

**Project Status:** Early development phase - core implementation not yet started.

## Development Commands

This project follows **Test-Driven Development (TDD)**. Always write tests first, then implement functionality.

```bash
# Project setup (first-time setup with uv)
uv init
uv add pytest pytest-cov google-generativeai

# Development setup
uv sync

# Run tests (primary development command)
uv run pytest

# Run tests with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_session.py

# Run tests in watch mode (if pytest-watch is installed)
uv run ptw

# Run the application (once main.py exists)
uv run python main.py

# Type checking (once mypy is configured)
uv run mypy .

# Linting (if configured)
uv run ruff check .
uv run ruff format .

# Add new dependencies
uv add <package_name>

# Add development dependencies
uv add --dev <package_name>
```

## Architecture Overview

Based on the README specification, the application follows this structure:

### Core Components
1. **Session Management Class** - Handles start/stop/pause timing logic
2. **Main GUI Window** - Tkinter interface with task input and control buttons
3. **Summary View** - Displays categorized time breakdown
4. **Gemini API Integration** - Sends task lists for automatic categorization
5. **Markdown Export** - Formats and copies results to clipboard

### Key Data Flow
1. User enters task name → Session starts/switches automatically
2. Real-time timer updates (1-second intervals) 
3. Stop button → API categorization → Summary view
4. Markdown generation → Clipboard export

### UI Structure
- **Main Screen**: Task input, ▶/⏸/⏹ buttons, real-time task list
- **Summary Screen**: Category table, Copy Markdown button, back navigation

## Implementation Notes

- Sessions auto-switch when starting new tasks (previous session stops automatically)
- Time tracking requires real-time updates with 1-second precision
- API key management through environment variables (GEMINI_API_KEY) for security
- Error handling with user dialogs to prevent crashes
- No file persistence - all data exists in memory until export
- Japanese text support required for task names and UI elements

## Project Structure

Expected directory structure (to be created during development):
```
src/
├── session.py           # Session management and timing logic
├── gui/
│   ├── main_window.py   # Main application window
│   └── summary_view.py  # Summary/results display
├── api/
│   └── gemini.py        # Google Gemini API integration
└── utils/
    ├── markdown.py      # Markdown formatting
    └── clipboard.py     # Clipboard operations

tests/
├── test_session.py      # Session timing tests
├── test_api.py          # API integration tests (mocked)
└── test_utils.py        # Utility function tests

main.py                  # Application entry point
pyproject.toml           # UV project configuration and dependencies
uv.lock                  # Locked dependency versions
```

## TDD Development Approach

**Red-Green-Refactor Cycle:**
1. Write failing test first (Red)
2. Write minimal code to pass test (Green) 
3. Refactor while keeping tests green

**Test Structure:**
- `tests/` directory for all test files
- `test_*.py` naming convention
- Unit tests for core logic (session management, time calculations)
- Integration tests for API interactions (with mocking)
- GUI tests using tkinter testing patterns

**Development Task Sequence (TDD-Modified):**
Each task now follows TDD methodology:
1. Write tests for session start/stop timing
2. Write tests for task switching logic
3. Write tests for pause/resume functionality
4. Write tests for time formatting and calculations
5. Write tests for Gemini API integration (mocked)
6. Write tests for Markdown generation
7. Write tests for clipboard operations
8. Implement GUI components after core logic is tested

**Key Testing Areas:**
- Session timing accuracy (1-second precision requirements)
- Task state transitions (start/stop/pause/switch)
- Time calculation edge cases (pause durations, concurrent sessions)
- API error handling (network failures, invalid responses)
- Markdown formatting correctness
- Japanese text handling in UI and exports

## Development Task Priority

Following the README's 17-task breakdown, implement in this order:
1. **Foundation** (Tasks 1-3): Basic Tkinter setup and session management
2. **Core Logic** (Tasks 4-6): Task switching, pause/resume, real-time display
3. **Export Features** (Tasks 7-9): Summary view, Markdown generation, clipboard
4. **API Integration** (Tasks 10-12): Gemini API (mock first, then real)
5. **Polish** (Tasks 13-17): Error handling, validation, edge cases

Each task requires writing tests first, then implementing the minimal code to pass.