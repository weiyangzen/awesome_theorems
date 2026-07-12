# Anchor-audit validation record

Item: `S56-M-1133-ANCHOR_AUDIT`  
Base revision: `2029732601188918961647a1d1565c7d55a46f04`  
Audit date: 2026-07-12

## Result

The exact repo-local artifact remains a proposition definition, not a proof. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies compact extreme-value, local-maximum
derivative, and coordinate-Laplacian declarations. `AnchorAudit.lean` checks six representative
anchors. None relates a time derivative and spatial Laplacian to a maximum on a parabolic boundary,
so none is an exact or terminal candidate.

The only concrete external Lean 4 PDE project found was audited at immutable revision
`weiran-sun/pde@0b37f095c5ac3571084f5ea47f0435884452d86a`. Its content-addressed archive
(`3c710cdd6a4348b39df5797faf19f55b340cf0141c00e0bc2d97e5db4866783f`) contains a proved
one-dimensional heat-kernel PDE identity, but no maximum/comparison principle, bounded cylinder,
or parabolic-boundary conclusion. It uses Lean `v4.23.0-rc2` and mathlib `90c0e1...`; it was
inspected outside the repository and was not installed. Importing it would not close a target
obligation.

The root therefore remains `M3`: the statement exists, while the proof formalization is missing.
Negative discovery results are bounded to the recorded queries and access limitations; they are not
a claim that no Lean proof exists anywhere. This phase grants no theorem-completion credit.

## Commands and results

All commands ran inside this worker clone. Existing pinned `.lake` artifacts were used without an
update, fetch, clone, or build.

| Command | Exit | Exact result summary |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1133/AnchorAudit.lean` | 0 | Six pinned mathlib support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1133/Statement.lean` | 0 | Canonical statement and four mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-1133/check_anchor_audit.py` | 0 | Candidate/status boundary, probe coverage, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i --glob '*.lean' '(heat equation\|HeatEquation\|caloric\|parabolic.*(maximum\|comparison)\|maximum.*parabolic)' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | No match in pinned mathlib; exit 1 is ripgrep's expected no-match status |
| `git ls-files '*.lean' \| xargs rg -n -i 'heat equation\|HeatEquation\|caloric\|parabolic.*maximum\|maximum.*parabolic'` | 0 | Exact local statement and unrelated/adjacent heat-equation material only; no local target proof body |
| GitHub REST repository queries and Sourcegraph public Lean query recorded in `anchor-audit.json` | 0 | Bounded discovery found the PDE project above and no terminal maximum-principle candidate; authenticated GitHub code search remained unavailable |
| `curl -LfsS https://codeload.github.com/weiran-sun/pde/tar.gz/0b37f...` followed by archive-only source inspection under `/tmp` | 0 | Immutable external tree inspected; archive SHA-256 and environment recorded; nothing installed in `.lake` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1133` | 0 | rank 338, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1133 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

## Open integration gate

Reopen only for a concrete Lean 4 declaration at an immutable revision whose normalized domain,
regularity, heat-operator sign, boundary, and conclusion match the canonical target, or for a
precisely typed bridge candidate. It must then pass local wrapper, terminal-body, placeholder,
axiom, unsafe/oracle, dependency, and license checks.
