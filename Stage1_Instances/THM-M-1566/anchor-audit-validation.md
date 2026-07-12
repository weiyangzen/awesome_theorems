# Anchor-audit validation record

Item: `S56-M-1566-ANCHOR_AUDIT`  
Base revision: `d698933c7bdc6a4c46601381f122d3dc6855cda3`

## Result

The exact repo-local artifact is the proposition definition
`Stage1Instances.THMM1566.GIPCorollary59Target`; it has no proof body and is
classified as a statement anchor only. The legacy `S1_M_182.StatementShape`
is not equivalent: it is an arbitrary-dimensional scaffold that packages the
hard analytic claims as hypotheses. It receives no proof or transport credit.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95`
provides Gaussian-process, Fernique, Holder, tempered-distribution, and
convergence-in-measure infrastructure. `AnchorAudit.lean` elaborates five
representative declarations. A source-wide terminal-name search found no GIP,
paracontrolled-distribution, singular-SPDE, regularity-structure, or parabolic
Anderson proof. These APIs are useful substrate, not the root theorem.

Public repository searches for `paracontrolled` and `Gubinelli` with `lean`
returned no repositories. The broader `regularity structures lean` query
located `TKojar/Regularity_Structures_Lean`; its archive was inspected at the
immutable commit `1df1e169df46e5a7140c816c329296b3419f2535` (archive SHA-256
`7f86090d...f5f77`). Both included Lean projects contain only generated
hello-world modules, and there is no license file, relevant declaration, or
proof body to integrate. GitHub code search was rate-limited, so that lane is
recorded as blocked and is not reported as a negative result.

The root therefore remains `M4`: no exact Lean 4 proof candidate was found.
This is a completed bounded anchor audit, not theorem completion and not a
claim that no proof exists outside the recorded search surfaces.

## Commands and results

Commands ran on 2026-07-12. Lean used only the existing pinned `.lake`
artifacts. No dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1566/AnchorAudit.lean` | 0 | five pinned mathlib support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1566/Statement.lean` | 0 | canonical target re-elaborated and explicit expression printed |
| `python3 Stage1_Instances/THM-M-1566/check_anchor_audit.py` | 0 | four candidates, four search records, five probes, M4 boundary, manifest pin, and installed mathlib HEAD agreed |
| pinned-mathlib `rg` over 12 translated/alias terminal query families | 1 | expected no-match status; no terminal source match |
| GitHub REST repository searches for `paracontrolled`, `Gubinelli`, and `regularity structures` plus `lean` | 0 | counts 0, 0, and 2; responses SHA-256 `08c082...2600b2`, `08c082...2600b2`, `b1ce94...9550` |
| GitHub REST code search for `paracontrolled language:Lean` | 0 | response captured; unauthenticated API rate-limit blocker; SHA-256 `1db366...386e` |
| download and inspect `TKojar/Regularity_Structures_Lean@1df1e169...` archive | 0 | only hello-world Lean modules; archive SHA-256 `7f8609...f5f77` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1566` | 0 | rank 182, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1566/anchor-audit.json` | 0 | structured audit parses |
| forbidden-term scan of the Lean probe | 1 | no `sorry`, `admit`, or `axiom` token; 1 is ripgrep no-match |
| `git diff --check -- Stage1_Instances/THM-M-1566 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open integration gate

Reopen only upon locating a canonical remote, immutable revision, license,
toolchain and dependency graph, module, declaration, and exact normalized
type. Its terminal body must then pass placeholder, axiom, unsafe/oracle,
provenance, and repo-local wrapper checks. Until then no `M1`, `M0-P`, or
theorem-completion credit is valid.
