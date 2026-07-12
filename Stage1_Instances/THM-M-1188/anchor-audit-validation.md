# Anchor-audit validation record

Item: `S56-M-1188-ANCHOR_AUDIT`  
Base revision: `446f3e80e7a93deeca70150fa80d9ee079ee0586`  
Audit date: 2026-07-12

## Result

The exact repo-local artifact remains a proposition definition, not a proof. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies compact-extremum, local-maximum derivative,
and coordinate-Laplacian declarations. `AnchorAudit.lean` checks six representative declarations.
None connects a time derivative and spatial Laplacian to a maximum on the parabolic boundary.

The concrete external Lean 4 PDE project was inspected at immutable revision
`weiran-sun/pde@0b37f095c5ac3571084f5ea47f0435884452d86a`. Its source archive has SHA-256
`3c710cdd6a4348b39df5797faf19f55b340cf0141c00e0bc2d97e5db4866783f`. It proves a
one-dimensional heat-kernel PDE identity, but has no maximum/comparison principle, bounded
cylinder, or parabolic-boundary conclusion. Its HeatKernel module contains no `sorry`, `admit`, or
`axiom`. It uses Lean `v4.23.0-rc2` and mathlib `90c0e1...`; nothing was installed into `.lake`.

The root therefore remains `M3`: the exact statement exists while its proof formalization is
missing. Negative search results are bounded to the recorded queries and access limits, not a claim
of global absence. This phase gives no theorem-completion credit.

## Commands and results

All commands ran from this worker clone. Existing pinned `.lake` artifacts were used without an
update, fetch, clone, or build.

| Command | Exit | Exact result summary |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1188/AnchorAudit.lean` | 0 | Six pinned mathlib support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1188/Statement.lean` | 0 | Canonical target, transport, mutations, and boundary fact re-elaborated |
| `python3 Stage1_Instances/THM-M-1188/check_anchor_audit.py` | 0 | Candidate boundary, probes, statement, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i --glob '*.lean' '(heat equation\|HeatEquation\|caloric\|parabolic.*(maximum\|comparison)\|maximum.*parabolic)' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | No match; exit 1 is ripgrep's expected no-match status |
| Immutable archive download plus `sha256sum`, toolchain/manifest inspection, and scoped `rg` under `/tmp/thm-m-1188-pde` | 0 | Archive hash and pins agreed; only adjacent heat-kernel theorem found; no admissions in its HeatKernel module |
| GitHub REST repository searches for quoted maximum principle/Lean and parabolic PDE/Lean | 0 | Bounded metadata queries found no relevant terminal candidate |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1188` | 0 | rank 383, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1188 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

## Open integration gate

Reopen for a concrete Lean 4 declaration at an immutable revision whose normalized domain,
regularity, operator sign, boundary, and conclusion match the canonical target, or for a precisely
typed bridge candidate. It must pass local wrapper, terminal-body, placeholder, axiom,
unsafe/oracle, dependency, and license checks.
