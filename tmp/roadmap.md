# Roadmap

Future enhancements and development plans for doc-gen.

## Current Status

doc-gen is functional with core features implemented:
- ✅ Menu-driven interface
- ✅ Interactive file selection
- ✅ YAML configuration
- ✅ Project scanning with .gitignore support
- ✅ Manifest generation with timestamped backups
- ✅ Markdown documentation with syntax highlighting
- ✅ Check mode with pagination
- ✅ Project tree generation
- ✅ Consolidated `.doc-gen/` output directory

## Near-Term Enhancements

### Single-Page Documentation Option

**Status:** Planned for next version

**What:** Generate one consolidated markdown file instead of mirrored structure.

**Features:**
- Hyperlinked table of contents
- Each file becomes a section
- Internal anchor links for navigation
- Better for BookStack import

**Use case:** Some documentation platforms prefer single-page imports.

### Project Tree Hyperlinking

**Status:** Planned

**What:** Make project tree interactive by cross-referencing with manifest.

**Features:**
- Files in manifest → hyperlinked to their `.md` docs
- Files not in manifest → plain text
- Tree becomes navigable table of contents

**Benefit:** Quick navigation from tree to documentation.

### Auto-Create Config on First Run

**Status:** Partially implemented

**What:** Automatically initialize `.doc-gen/config.yml` if missing.

**Current state:** Structure is auto-created, config should be too.

**Why:** Removes manual initialization step, smoother first-run experience.

### Hardcoded .doc-gen/ Exclusion

**Status:** In progress

**What:** Ensure `.doc-gen/` is ALWAYS excluded from scans, even if not in ignore patterns.

**Why:** Prevents recursion issues and accidental self-documentation.

## Medium-Term Features

### Plugin System Enhancements

**Current state:** Plugin architecture exists but minimal plugins included.

**Planned:**
- More example plugins
- Better plugin discovery
- Plugin documentation
- Community plugin repository

**Example plugins to add:**
- HTML formatter (alternative to markdown)
- PDF formatter
- Image processor (add image descriptions)
- Metadata extractor (parse docstrings)

### Diff Mode

**What:** Show what changed since last documentation generation.

**Features:**
- Compare current files with manifest
- Highlight new files
- Show modified files
- Prompt to update manifest

**Use case:** Incremental updates to documentation.

### Watch Mode

**What:** Auto-regenerate documentation when source files change.

**How:**
- Monitor files in manifest
- Detect changes
- Automatically run generation
- Optional desktop notifications

**Use case:** Live documentation during development.

### CLI Automation Mode

**What:** Non-interactive mode for CI/CD pipelines.

**Features:**
```bash
doc-gen --manifest .doc-gen/manifest.yml --generate
doc-gen --scan --auto-accept --generate
```

**Why:** Enable automated documentation in build pipelines.

## Long-Term Vision

### Incremental Updates

**What:** Only regenerate documentation for changed files.

**How:**
- Store file hashes in manifest
- Compare current vs stored hashes
- Skip unchanged files

**Benefit:** Faster regeneration for large projects.

### Metadata Extraction

**What:** Parse source files for documentation comments.

**Features:**
- Extract docstrings (Python)
- Parse JSDoc comments (JavaScript)
- Extract header comments (shell scripts)
- Include in generated markdown

**Benefit:** Richer documentation with inline explanations.

### Multi-Format Output

**What:** Support output formats beyond markdown.

**Planned formats:**
- HTML (with navigation)
- PDF (via LaTeX or similar)
- ReStructuredText
- AsciiDoc

**Configuration:**
```yaml
output:
  format: markdown  # or html, pdf, rst
```

### API Integration

**What:** Direct upload to documentation platforms.

**Target platforms:**
- BookStack (via API)
- Confluence
- GitHub Wiki
- ReadTheDocs

**Configuration:**
```yaml
upload:
  platform: bookstack
  url: https://docs.example.com
  api_key: ${API_KEY}
```

### Custom Templates

**What:** User-defined markdown templates.

**Features:**
- Template variables (path, syntax, content)
- Custom headers/footers
- Project-specific formatting
- Conditional sections

**Example:**
```markdown
# ${filename}

Project: ${project_name}
Author: ${author}
Last Modified: ${mtime}

## Code

```${syntax}
${content}
```

## Related Files
${related_files}
```

### Web Interface (Maybe)

**What:** Optional web UI for file selection and configuration.

**Why:** Some users prefer GUI over terminal.

**Scope:** Would be separate from core tool, optional install.

## Deferred / Maybe Never

### Binary File Documentation

**Challenge:** How to "document" images, PDFs, etc.?

**Possible approach:**
- Generate thumbnails
- Extract metadata
- List file properties
- Include in special section

**Status:** Low priority, unclear value.

### Automatic Translation

**What:** Generate documentation in multiple languages.

**Challenge:** Requires AI/translation service, adds complexity.

**Status:** Out of scope for now.

## Community Contributions

We welcome contributions in these areas:

### High Priority
- Bug fixes
- Documentation improvements
- Example plugins
- Test coverage

### Medium Priority
- New syntax highlighters
- Performance optimizations
- Additional output formats

### Low Priority
- UI enhancements
- Feature requests (discuss first)

See [Contributing](contributing.md) for how to get involved.

## Versioning Strategy

Following semantic versioning:
- **Major (X.0.0):** Breaking changes to config or manifest format
- **Minor (x.Y.0):** New features, backward compatible
- **Patch (x.y.Z):** Bug fixes, no new features

Current: Pre-1.0 (in development)

## Stability Commitment

Once 1.0 is released:
- Manifest format will remain backward compatible
- Configuration breaking changes will be versioned
- Migration tools provided for major updates
- Deprecation warnings before removal

## Timeline

**No specific dates** - this is a learning project and side work.

**Priority order:**
1. Bug fixes
2. Core feature completion
3. Documentation
4. Nice-to-have enhancements

## Feedback Welcome

This roadmap isn't set in stone. If you have ideas or want to see something prioritized:

1. Open a GitHub issue
2. Discuss in pull requests
3. Submit your own contributions

The best features come from real-world usage and user feedback.

## Next Steps

- See current [TODO.md](https://github.com/carolynboyle/doc-gen/blob/main/TODO.md) for tactical tasks
- Check [Contributing](contributing.md) to help with roadmap items
- Review [Design Philosophy](design-philosophy.md) for guiding principles
