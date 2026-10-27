# Output Language Protocol

Determine the output language for generated artifacts and reports using this
priority:

1. Check `AGENTS.md` (or `.aris/context.json`) for a `language:` field — if
   `language: zh` or `language: cn`, write reports in Chinese.
2. If the user's most recent message is in Chinese, write reports in Chinese.
3. Default: English.

## What to Localize

- Section headings and labels in reports (Literature Landscape → 文献全景).
- Descriptions, analysis, commentary, recommendations.
- Template boilerplate text.
- Status messages and warnings.

## What NOT to Localize

- File names, directory names, run IDs, job IDs, receipt/trace paths.
- Field names in JSON receipts, `REVIEW_STATE.json`, `MANIFEST.md` headers.
- Verdict tokens (`PASS`, `BLOCK`, `SUPPORTED`, `REFUTED`, `CONTINUE`), CLI
  commands, code, BibTeX keys, CVE IDs, commit SHAs.
- LaTeX source for a venue submission stays in the venue's required language
  (English for all Big-Four venues) regardless of report language.
