# Anchor-audit validation record

Item: `S56-M-0339-ANCHOR_AUDIT`  
Base revision: `bd0d227173ac95971603f633607751754850337e`  
Audit date: 2026-07-12

## Result

The exact repository artifact is only the elaborated proposition
`Stage1.THM_M_0339.MSSPartitionStatement`. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the rank-one continuous-linear-map,
positivity, identity-sum, filtered-sum, norm, and square-root APIs checked by `AnchorAudit.lean`.
A complete case-insensitive source search found no MSS, Kadison-Singer, interlacing-family,
mixed-characteristic-polynomial, Weaver-paving, or rank-one partition theorem in pinned mathlib.
These are useful foundations, not a terminal anchor.

The bounded external search found one related Lean 4 project:
`PerAlexandersson/RealRooted@634a949d31683785b4181efbba6faff31e81e006`. Its complete
commit-addressed tree contains general real-rooted polynomial, interlacing-sequence, matrix
interlacing, and Cauchy interlacing modules. It contains no MSS mixed characteristic polynomial,
random-vector estimate, rank-one operator partition, or exact Corollary 1.5 declaration. Its Lean
`v4.31.0-rc2` toolchain differs from this repository's `v4.29.0`, its Lake file does not pin a
mathlib revision, and a repository-wide scan found multiple `sorry` occurrences in unrelated
modules. It is therefore related infrastructure only, not an exact or integration-ready proof.

The exact root remains `M4`: no Lean proof body is available to integrate. This completes the
node-specific bounded anchor audit, but it is not theorem proof, full audit, or release evidence.

## Commands and results

All commands ran in this worker clone. The Lean checks reused existing pinned `.lake` artifacts
read-only. No `lake update`, build, dependency clone, or dependency fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0339` | 0 | rank 832, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -ni 'Kadison|Spielman|Srivastava|interlacing famil|mixed characteristic polynomial|Anderson paving|rankOne.*sqrt|Weaver KS' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no target-family match; exit 1 is ripgrep's expected no-match result |
| GitHub REST repository searches for `"Marcus-Spielman-Srivastava" Lean`, `"Kadison-Singer" Lean`, and `interlacing polynomials Lean` | 0 | first two complete responses had zero repositories; third found only `PerAlexandersson/RealRooted` |
| Sourcegraph public searches for `"Marcus Spielman Srivastava" lang:Lean` and `"Kadison Singer" lang:Lean` | 0 | both bounded queries completed with `matchCount=0` |
| GitHub commit/tree/archive inspection of `PerAlexandersson/RealRooted@634a949d31683785b4181efbba6faff31e81e006` | 0 | complete non-truncated tree inspected; relevant modules are support-only; tree response SHA-256 `7f483ba54c2554f70ae267fb2d2208d394a73d4031f4b5087b95d0b4cdcca054` |
| `rg -n '\bsorry\b|\badmit\b|^\s*axiom\b|unsafe|implemented_by' /tmp/thm-m-0339-realrooted-src --glob '*.lean'` | 0 | multiple `sorry` hits; none supplies the absent MSS terminal theorem |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0339/AnchorAudit.lean)` | 0 | all eight pinned support declarations elaborated under Lean 4.29.0 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0339/Statement.lean)` | 0 | exact frozen proposition re-elaborated |
| `python3 Stage1_Instances/THM-M-0339/check_anchor_audit.py` | 0 | audit boundary, probes, manifest pin, and installed mathlib HEAD agreed |
| `git diff --check -- Stage1_Instances/THM-M-0339` | 0 | no whitespace errors |

## Reopening boundary

Reopen integration only for a concrete Lean 4 candidate with an immutable revision, pinned
toolchain and dependencies, exact terminal declaration or checked transport, terminal proof-body
location, license, placeholder and axiom reports, and a successful repo-local wrapper check.
Negative search results here are bounded discovery evidence, not a claim of global absence.
