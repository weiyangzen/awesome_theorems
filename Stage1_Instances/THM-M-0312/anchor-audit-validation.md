# Anchor-audit validation

Item: `S56-M-0312-ANCHOR_AUDIT`  
Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`

## Result

Pinned mathlib contains an exact proof candidate. `banach_steinhaus` has the frozen binder and
premise/conclusion structure, and `AnchorAudit.lean` checks it through a repo-local exact-type
wrapper. Its body converts the norm-bound goal to equicontinuity with
`NormedSpace.equicontinuous_TFAE`, then applies the more general
`WithSeminorms.banach_steinhaus`. Lean reports only `propext`, `Classical.choice`, and `Quot.sound`
for the wrapper and all retained mathlib candidates. Direct source scans found no placeholder,
bodyless axiom, or unsafe token in the two modules containing the root and terminal body.

`banach_steinhaus_iSup_nnnorm` is a checked alternate formulation sharing that proof route. The
bounded external search found one non-mathlib Lean 4 artifact:
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its
`UniformBoundedness.uniform_boundedness` specializes to real continuous linear maps and is a
one-line call to mathlib's theorem, so it is neither an exact polymorphic root nor an independent
terminal body. Its manifest nevertheless uses the same Lean 4.29.0 and mathlib commit, and its
source contains no prohibited placeholder token.

The exact root is therefore an `M0-W` candidate, not accepted `M0-W` state: the later obligation,
provenance, full trust, validation, hermetic replay, independent-review, and master-acceptance gates
remain open. This audit claims neither `AUDIT-Z` nor theorem completion.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Existing `.lake` artifacts were used read-only;
no update, build, fetch, clone, or dependency mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0312` | 0 | rank 814, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0312/Statement.lean` | 0 | frozen exact statement re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0312/AnchorAudit.lean` | 0 | exact wrapper and alternate candidate elaborated; all four axiom reports were `propext`, `Classical.choice`, `Quot.sound` |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b|unsafe' .../BanachSteinhaus.lean .../Barrelled.lean Stage1_Instances/THM-M-0312/AnchorAudit.lean` | 1 | expected no-match exit; no prohibited token in audited proof-body files |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{tree}` | 0 | immutable tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| Sourcegraph global Lean query recorded in `anchor-audit.json` | 0 | complete, 22 matches in mathlib3, mathlib4, and atlas-lean; response SHA-256 `b36f814c...cc1f9d2` |
| GitHub REST repository searches recorded in `anchor-audit.json` | 0 | both complete with zero repositories; each response SHA-256 `08c082fd...2600b2` |
| GitHub immutable atlas-lean source/manifest inspection | 0 | commit/tree verified; Lean 4.29.0 and pinned mathlib revision; specialized wrapper only |
| `python3 -m json.tool Stage1_Instances/THM-M-0312/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0312 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open gates

The obligation-tree phase must model the exact wrapper, its equicontinuity transport, the
barrelled-space terminal body, and their transitive dependencies without duplicate proof credit.
Only subsequent validation and release evidence may promote this candidate to accepted `M0-W` or
derive theorem completion.
