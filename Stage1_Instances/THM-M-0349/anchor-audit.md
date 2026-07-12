# Anchor audit

## Scope and outcome

At the `2026-07-12T11:51:26Z` cutoff, the bounded rev-5.6 search found no exact Lean 4 proof of
`Stage1Instances.THM_M_0349.ConjugateFunctionTheoremTarget`. The machine classification remains
`M3`: the exact proposition elaborates, but no repo-local, pinned-mathlib, or discoverable public
Lean candidate closes it. This completes only the self-tested anchor inventory pending master
acceptance. It gives no proof or theorem-completion credit.

The search followed the required order and used aliases for conjugate functions, the Hilbert
transform, Marcel Riesz, the original French title, and Fourier multipliers. Repo-local results
were adjacent dossiers or unrelated distributional multiplier infrastructure. No existing proof
body or wrapper matched the frozen periodic `Lp` target.

## Pinned mathlib candidates

Mathlib is fixed at commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Its relevant additive-circle file has SHA-256
`32363b7144bee4cdc3f96e41237eb6944c8dd6ac92449340a0c27462959e7c81`.

| Candidate | Exact comparison | Decision |
|---|---|---|
| `span_fourierLp_closure_eq_top` | Proves density of Fourier monomials for finite `p`; defines no conjugate operator and supplies no norm bound. | Useful construction anchor only. |
| `hasSum_fourier_series_L2` | Proves Hilbert-basis Fourier expansion only at `p = 2`; does not construct the conjugate function or cover all `1 < p < infinity`. | Special-exponent infrastructure only. |

`AnchorAudit.lean` checks both declaration types through typed wrappers. The wrappers' printed axiom
profiles contain only `propext`, `Classical.choice`, and `Quot.sound`. A name and documentation
search of the pinned source found no Hilbert-transform or conjugate-function declaration.

## External search

GitHub repository queries for conjugate functions, Hilbert transforms, harmonic analysis, and
singular integrals in Lean returned no relevant project. One broad query found a Hilbert-space
projection repository, which is unrelated by statement and was rejected. GitLab's corresponding
project queries returned no project. No external candidate existed to pin, inspect, or test.

The negative result is bounded rather than exhaustive: GitHub code search required authentication,
grep.app returned HTTP 429 with a security checkpoint, and Sourcegraph's former stream endpoint
returned HTTP 404. These failures are recorded rather than silently converted into absence claims.

## Validation ledger

All checks used repository base `396f523f7db5499e43d86728d9cfe073ac081dfa` and the existing
pinned Lake environment. No update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0349/AnchorAudit.lean` | 0 | Both typed wrappers elaborated; each axiom profile was `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0349/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0349` | 0 | Rank 842, planned, legacy artifacts unaccepted, theorem incomplete. |
| `python3 -m json.tool Stage1_Instances/THM-M-0349/anchor-audit.json` | 0 | Structured audit JSON parsed. |
| placeholder/axiom `rg` scan over target Lean files | 1, expected | No `sorry`, `admit`, or declared `axiom` found. |
| `git diff --check -- Stage1_Instances/THM-M-0349` | 0 | No whitespace errors. |

The next phase must build an obligation tree for a local analytic proof, beginning with a
conjugate multiplier on a dense Fourier subspace and its strong-type extension. Human-source debt
remains open, readability remains `R4`, and no `M1` integration task is created because no exact
external closure was found.
