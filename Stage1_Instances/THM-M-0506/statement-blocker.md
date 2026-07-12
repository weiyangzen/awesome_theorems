# Statement-phase blocker

Item: `S56-M-0506-STATEMENT`

Base revision: `aa55669bb59986e08ea8a0d1d77a1e40343d8142`.

## Verdict

The exact Lean 4 target cannot be elaborated truthfully from the repository source. The only source
wording is `级数收敛与可和性的关系` ("the relationship between series convergence and
summability"), together with the family label `陶伯型定理`, Alfred Tauber, and 1897. It contains no
formula, bibliographic edition, theorem/page locator, coefficient field, summability method,
asymptotic side condition, ordered binders, or conclusion. Stage0 independently marks the exact
definitions and premises as open.

This is a hard statement-freeze failure, not a Lean syntax or dependency failure. Selecting the
often-associated converse to Abel's theorem would still require inventing at least the real versus
complex domain, the Abel-limit filter, the indexing convention, and whether the coefficient
condition is little-o, big-O, positivity, or monotonicity. Those choices distinguish materially
different Tauberian theorems. Abel's limit theorem already present in mathlib has the opposite
direction and is not a permissible substitute.

Consequently there is no canonical declaration or expression to put in a statement module, no
exact-expression hash, no checked alternate-encoding transport, and no meaningful hypothesis or
boundary mutation test. Creating a compilable proposition here would broaden or substitute the
source rather than elaborate it. The node remains blocked at `M4`; no statement acceptance, proof
credit, audit completion, or theorem completion is claimed.

## Retry condition

Provide and independently inspect an immutable primary-source edition or scan with an exact
theorem/page locator. A retry can then crosswalk every premise and conclusion, freeze all domains
and boundary conventions, and elaborate that proposition with the smallest pinned import set.

## Validation evidence

The canonical `.lake` directory was used through its existing read-only symlink. No update, build,
fetch, clone, or dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0506` | exit 0; rank 880, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 4 '陶伯型定理\|Tauberian\|Tauber\|级数收敛与可和性' Docs Stage1_Instances Formalizations --glob '!Stage1_Instances/THM-M-0506/**' --glob '!Formalizations/Lean/.lake/**'` | exit 0; repository search found only the same metadata/gloss, open Stage0 fields, and unrelated use of the word `Tauberian`; no exact proposition or source locator |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0506/IntakeProbe.lean)` | exit 0; pinned Lean 4.29.0 elaborated the six series/Abel API checks, confirming that the blocker is source identification rather than toolchain availability |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0506 -g '*.lean'` | exit 1, expected no-match; no prohibited placeholder or axiom |
| `git diff --check -- Stage1_Instances/THM-M-0506` | exit 0; no whitespace errors |

This phase is not self-tested as complete because its required exact target does not exist in the
available source material. Therefore no workspace `.stage1-worker-selftest.json` is emitted.
