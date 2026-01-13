# Design Philosophy

Why doc-gen works the way it does.

## Core Principles

### 1. "Idiot-Proof" Interface

The menu-driven interface is designed so that if it doesn't confuse the developer (who has ADHD and is new to Python), it won't confuse anyone.

**What this means:**
- No memorizing command flags
- Clear menu options with descriptive names
- Logical workflow ordering
- Immediate feedback on actions
- No "gotchas" or hidden complexity

**Design decisions:**
- Menu over CLI arguments for main workflow
- Interactive file selection (not glob patterns)
- Check mode before generation (preview first)
- Automatic backups (no "are you sure?" needed)

### 2. Non-Destructive by Default

Nothing doc-gen does should break your project or require you to start over.

**Implementation:**
- All output in `.doc-gen/` directory (never touches source)
- Automatic timestamped backups
- Manifest is version-controllable
- Can delete `.doc-gen/` and start fresh anytime
- Idempotent operations (run repeatedly safely)

**Philosophy:**
If you can't easily undo it, don't do it automatically.

### 3. Respect Existing Conventions

doc-gen doesn't invent new ways to do things you're already doing.

**Examples:**
- Uses `.gitignore` patterns (no new syntax to learn)
- YAML configuration (widely understood)
- Standard markdown with code fences
- Familiar directory mirroring
- Common syntax highlighting names

**Rationale:**
Learning curve is reduced when tools work the way you expect.

### 4. Visible State

You should be able to see what doc-gen is doing and has done.

**Manifestation:**
- Manifest file is human-readable YAML
- Configuration is transparent
- Project tree shows what's included
- Check mode previews before generation
- All state in one directory (`.doc-gen/`)

**Anti-pattern avoided:**
Hidden state, binary databases, or magic behavior.

### 5. ADHD-Friendly Workflows

Designed to work with, not against, ADHD brain patterns.

**Features:**
- Menu reduces decision fatigue
- Chunked workflow (one step at a time)
- Progress indicators
- Auto-accept mode for repetitive tasks
- Can quit and resume anytime
- State is preserved

**Theory:**
If the tool fights your attention span, you won't use it.

## Architectural Decisions

### Why Two-Phase (Scan → Generate)?

**Problem:** Generating docs for everything wastes time and clutters output.

**Solution:** Scan first, select what matters, then generate.

**Benefits:**
- User control over what's documented
- Repeatable generation (just re-run Option 4)
- Manifest serves as documentation of intent
- Can update source files and regenerate easily

### Why Object-Oriented?

**Developer preference:** OOP fits the kinesthetic cognitive style better than functional programming.

**Practical benefits:**
- Clear class responsibilities
- Easy to extend (plugins)
- Testable (unit tests per class)
- Maintainable (find things easily)

**Trade-off accepted:**
More verbose than functional style, but clarity matters more.

### Why Menu-Driven Interface?

**Alternative considered:** Pure CLI with flags like `doc-gen --scan --output=docs/`

**Rejected because:**
- Requires memorizing flags
- Easy to make mistakes
- Harder to discover features
- Less friendly for new users

**Menu chosen because:**
- Self-documenting (see all options)
- Hard to make mistakes
- Guides user through workflow
- Still scriptable via CLI for automation

### Why YAML Configuration?

**Alternatives:** JSON, TOML, INI, Python files

**YAML chosen because:**
- Human-readable and writeable
- Supports comments
- Ansible-compatible (future automation)
- Widely understood
- Clean syntax for lists and maps

**Trade-offs:**
Indentation-sensitive, but so is Python, so consistent with ecosystem.

### Why Mirror Directory Structure?

**Alternative:** Flatten all docs into one directory.

**Rejected because:**
- Loses context (where did this file come from?)
- Name collisions (`utils.py` is common)
- Harder to navigate

**Mirroring chosen because:**
- Preserves context
- No name collisions
- Easy to find corresponding doc
- Matches mental model

### Why `.doc-gen/` Directory?

**Problem:** Polluting project root with doc-gen files is annoying.

**Solution:** Everything in `.doc-gen/` subdirectory.

**Benefits:**
- Single directory to ignore in `.gitignore`
- Easy to delete entire state
- No file-by-file cleanup
- Clear separation of concerns

**Lesson learned:**
This was added mid-development after realizing the old approach was messy.

## Evolution & Lessons

### Original Design

Started as a simple bash script to copy files to markdown for BookStack documentation.

**Problems:**
- Not reusable across projects
- No file selection (all or nothing)
- Hardcoded paths
- No configuration

### Second Iteration

Designed as OOP Python tool with interactive selection.

**Improvements:**
- Reusable
- Interactive file selection
- Configuration via YAML
- Respects `.gitignore`

**But still had issues:**
- Files scattered in project root
- Config initialization required manual step

### Current Version

Consolidated all output to `.doc-gen/` directory.

**Final improvements:**
- Non-polluting
- Auto-creates structure
- Better UX (no initialization step)
- Ready for GitHub/sharing

**Key insight:**
The "rule of three" for refactoring - if you improve something three times, you've probably got it right.

## User-Centered Thinking

### "If I can't break it, nobody can"

Heavy edge-case testing by developer with ADHD tendencies means:
- Rapid keypresses handled
- Invalid inputs caught
- Empty inputs handled gracefully
- Quit-anywhere works correctly

### Preference for Obvious Over Clever

**Example:** Menu text says exactly what happens:
- "Generate Project Tree" not "Tree Mode"
- "Scan Project - Select files to document" not "Scan"
- "Check Mode - Review selected files" not "Review"

**Principle:**
Clarity over brevity. Users shouldn't have to guess.

### Feedback Is Valuable

This project is being shared for class feedback because:
- Fresh perspectives catch blind spots
- Users will do unexpected things
- Real-world usage reveals assumptions
- Community input improves design

## Future Considerations

See [Roadmap](roadmap.md) for planned enhancements, but philosophy remains:

1. Don't break existing workflows
2. Keep it simple
3. Make changes optional
4. Preserve backward compatibility
5. User control over features

## Summary

doc-gen is designed to be:
- **Easy to use** - Menu-driven, no hidden complexity
- **Safe** - Non-destructive, everything in `.doc-gen/`
- **Respectful** - Uses existing conventions
- **Transparent** - State is visible and editable
- **Forgiving** - Can undo, restart, modify freely

The goal isn't to be the most powerful documentation tool, but to be the most usable one for everyday needs.

## Next Steps

- See how these principles manifest in [Workflows](workflows.md)
- Understand the [Menu Reference](menu-reference.md) design
- Check the [Roadmap](roadmap.md) for future philosophy evolution
