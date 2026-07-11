# Scope Map

| Surface | Observed content | Intake decision |
|---|---|---|
| `Docs/Stage1_Targets_rev-5.6.json` | Member, rank 21, planned, uniform L0 | Authoritative membership and order |
| `Docs/researches/math_theorems.md` | Name, Nagell, 1948, vague cubic-curve gloss | Untrusted source metadata |
| `Docs/Stage0_Blueprint.md` | Repeats metadata; exact definition absent | Discovery only |
| `Docs/Stage1_Blueprint.md` | Same vague gloss and execution guidance | Legacy discovery only |
| Legacy Lean module | Abstract Nagell-Lutz-shaped conditional package | Not an exact source statement or proof |

## In Scope

Resolve the exact primary mathematical source and claim; freeze its integer/rational domains,
specific curve or curve family, parameters, nonsingularity conditions, ordered binders, hypotheses,
conclusion, and degenerate cases; then elaborate that same claim in Lean 4.

## Excluded Until Source Resolution

- Treating the repository's source label `已验证` as human or kernel evidence.
- Selecting the Nagell-Lutz theorem merely because the attribution says Nagell.
- Selecting the Markov equation `x^2 + y^2 + z^2 = 3xyz`; this text appears in an adjacent legacy
  generated entry and conflicts with the target's own cubic-curve gloss.
- Treating an abstract proposition-valued data package as a formalization of the arithmetic claim.
- Claiming any source, proof, readability, audit, or theorem-completion gate.

## Next-Gate Inputs

The statement phase requires a primary-source bibliographic identity (edition, title, year,
theorem/page), an exact transcription, and a source-backed explanation of whether "Pierce" is a
translation/transliteration error. If this cannot be established, the statement gate must remain
blocked rather than choosing a nearby theorem.
