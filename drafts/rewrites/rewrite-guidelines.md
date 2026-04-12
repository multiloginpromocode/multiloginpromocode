Rewrite Guidelines for /compare/, /guides/, /promo/
-------------------------------------------------

Goal: Produce semantically equivalent pages with distinct phrasing, structure, and microcopy so search engines treat them as original content.

Techniques:
- Change the headline pattern: use question-, benefit-, or outcome-focused headlines instead of direct comparisons.
- Reorder sections: move verdicts, tables, and timelines around to alter document structure.
- Vary intros: use a short anecdote, a data point, or a one-line use-case instead of the original lead.
- Swap lexical choices: "stability" -> "resilience", "validation" -> "proofing", "pilot" -> "trial".
- Modify CTAs and destinations: point some CTAs to internal tools or to a different guide to avoid exact duplication.
- Alter JSON-LD: change @id, dateModified, headline phrasing and remove verbatim paragraph strings.
- Add small unique elements: brief local example, 1-line case study, or a small opinionated tip.
- Meta tweaks: update meta description sentence order and include a unique token (e.g., "Verified by K.")
- FAQ rewrite: rephrase questions and answers; combine or split Q/A pairs.

Automation notes:
- Use a template engine to map source sections to target templates: Hero, Executive Verdict, Matrix, HowTo, FAQ, Next Steps.
- Apply light paraphrasing per paragraph with a synonym dictionary and sentence-splitting to recompose sentences.
- Insert a unique sentence per page (author opinion, example) to increase uniqueness score.
- Preserve structured data semantics but reword text fields and update timestamps.

Quality checks before publish:
- Run diff against original to ensure < 40% exact-line overlap.
- Manual spot-check: hero, first two paragraphs, FAQ entries.
- Validate HTML and JSON-LD.

Examples: follow the sample pages in this folder as patterns.
