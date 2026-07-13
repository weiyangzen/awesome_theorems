# Intake validation

Item: `S56-M-0952-INTAKE`

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`

Validation date: `2026-07-13` (`Asia/Shanghai`)

This validation covers target membership, the planned dossier, scope and source crosswalk, JSON
integrity, source discovery, the six-node open task DAG, and a narrow pinned Lean interface and
candidate-shape probe. It does not cover a canonical target, expression fingerprint, statement
mutations, source acceptance, proof, audit completion, or theorem completion. The
automation-provided canonical `.lake` link and artifacts were used read-only; no dependency update,
build, clone, fetch, or `.lake` mutation was performed. The external source PDF was inspected as a
temporary discovery input and was not added to the repository or accepted as H0 evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok`; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0952` | 0 | rank 1487, planned, legacy artifacts unaccepted, theorem_complete false |
| `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | base `a3b18eec...`, tree `fdfff18d...` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `curl ... http://matwbn.icm.edu.pl/ksiazki/aa/aa81/aa8145.pdf` followed by `sha256sum`, `pdfinfo`, and `pdftotext` | 0 | inspected 3-page, 158206-byte Elekes paper; SHA-256 `f217314f...9a44`; definitions and Theorem 1 on p. 365 and proof on p. 366 located; temporary external input only |
| `curl ... https://api.crossref.org/works/10.4064%2Faa-81-4-365-367` with `jq` | 0 | DOI metadata corroborated title, sole author, 1997, Acta Arithmetica 81(4), pp. 365-367 |
| bounded `rg` search for Elekes, Szemeredi-Trotter, and exact sum-product names in pinned mathlib and repository Lean | 1 | expected no-match; no named formal target found in this bounded local search; not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0952/IntakeProbe.lean)` | 0 | sumset, product-set, cardinality, maximum, `Real.rpow`, and `CandidateTargetShape : Prop` interfaces elaborated; stdout SHA-256 `9f44d0b...181f`, empty stderr |
| `python3 -B Stage1_Instances/THM-M-0952/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | planned H1/M3/R4 boundary, immutable inputs, exact artifact inventory, worker packet, and six open tasks agree |
| scoped prohibited-declaration scan | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0952 .stage1-worker-selftest.json` plus scoped untracked-file whitespace checks | 0 | no whitespace diagnostics |

Known downstream failures are intentionally open: master acceptance of intake; immutable source
admission and independent review; correction and errata audit; exact finite-set/domain/nonzero,
pairwise-operation, constant, exponent, cast, binder, inequality, and boundary decisions; canonical
Lean elaboration, checked transports, and four mutation classes; exhaustive anchor and provenance
audit; obligation registry and typed graphs; proof and composition; readable reconstruction;
hermetic replay; deterministic evidence bundle; and independent verification. These prevent audit
and theorem completion but do not invalidate a truthful, self-tested `planned` intake.
