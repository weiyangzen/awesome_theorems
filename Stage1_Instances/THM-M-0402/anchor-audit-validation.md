# THM-M-0402 Anchor-Audit Validation

Item: `S56-M-0402-ANCHOR_AUDIT`  
Audit date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `900ed1fb51c92dde0f0024262cddfa5fc7ae64b7`

## Result

The exact canonical Evertse proposition elaborates against pinned mathlib. The
pinned `SInteger` module also elaborates the S-integer and S-unit declarations
used by that proposition. It contains no S-unit-equation finiteness theorem and
explicitly lists finite generation and Dirichlet's S-unit theorem as TODOs.

The legacy target is a narrower two-variable statement interface whose own
metadata says it is not repo-locally closed. Pinned mathlib's theorem catalog
lists the Subspace Theorem only as a documentation row without a `decl`.
Searches over `flt-regular`, the complete immutable Formal Conjectures tree,
and five GitHub repository queries found no terminal Lean 4 candidate. GitHub
code search required authentication and grep.app returned HTTP 429, so no
exhaustive public-web claim is made.

The bounded anchor inventory is fully classified. The root remains
`[H1, M3, R3]`: its proposition is checked, but no proof body was located.
This completes only the assigned anchor-audit phase pending master acceptance;
it does not prove, validate, release, or complete the theorem.

## Commands And Results

Commands were run from the repository root unless a working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all targets L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0402` | 0 | rank 15, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| scoped `rg` alias search over the local target, pinned mathlib, mathlib docs, and `flt-regular` | 0 | only local statement wrappers, S-unit definitions, and theorem-catalog rows; no terminal proof body |
| immutable GitHub recursive-tree query for `google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` | 0 | requested SHA, `truncated=false`, 1204 entries, no matching path |
| five GitHub repository API searches recorded in `anchor-audit.json` | 0 | totals `0, 0, 0, 0, 0`; every `incomplete_results=false` |
| unauthenticated GitHub code search for `"Evertse" language:Lean` | 0 transport / HTTP 401 | `Requires authentication`; recorded access limit |
| grep.app API query for `Evertse` | 0 transport / HTTP 429 | no search result; recorded access limit |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0402/Statement.lean` | 0 | exact canonical proposition elaborated and printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0402/AnchorAudit.lean` | 0 | all five pinned S-integer/S-unit declaration probes elaborated and printed |
| `python3 Stage1_Instances/THM-M-0402/check_anchor_audit.py` | 0 | pins, statement hash, source witnesses, and six non-closing candidates verified |
| `python3 -m json.tool Stage1_Instances/THM-M-0402/anchor-audit.json` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0402 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The clone's pre-existing untracked `Formalizations/Lean/.lake` link reuses the
canonical pinned artifacts. No `lake update`, build, dependency clone/fetch, or
`.lake` mutation occurred. Accepted receipts remain empty pending master review.
