# Anchor audit

## Verdict

No exact Lean 4 proof anchor was found for
`Stage1Instances.THM_M_1278.OnofriInequality`. The exact local declaration is
only a proposition definition. Pinned mathlib provides relevant sphere,
stereographic-chart, gradient, and Hausdorff-measure infrastructure, but no
logarithmic exponential integral inequality or sharp energy estimate. The
disposition is **direct formalization required**; the root remains
`[H2, M3, R4]` and receives no proof credit.

## Immutable mathlib audit

The audited checkout is mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (commit date
`2026-03-30T18:47:58Z`) under Lean 4.29.0. Literal and related-term searches
of its Lean sources found no `Onofri` occurrence. Searches for
Moser-Trudinger and logarithmic-Sobolev terminology found no exact sphere
anchor; the repository hits describe distinct targets or generic material.

`AnchorAudit.lean` checks eleven retained declarations. `Metric.sphere`, the
sphere manifold/stereographic declarations, `gradient`, and Hausdorff measure
support the chosen encoding. The Hausdorff isometry results can support later
measure invariance arguments. None bounds `log (integral exp u)`, supplies the
mean/Dirichlet-energy comparison, proves the sphere has the normalization used
by the target, or contains the sharp coefficient `1/(16*pi)`.

Lean's axiom reports for the probed theorem declarations contain only
`propext`, `Classical.choice`, and `Quot.sound`. The pinned source contains
ordinary definitions and `by` proof bodies, with no placeholder declaration
or unsafe/oracle boundary in the retained candidates. This establishes their
credibility as support only, not as an Onofri proof.

## Repository and external search

The repository-wide audit found only the exact statement surface, prose, and
deliberately distinct Moser-Trudinger/logarithmic-Sobolev targets. It found no
proof-bearing local declaration.

On 2026-07-12, Sourcegraph's public global Lean index, including archived
repositories and forks, returned zero matches for `Onofri` and `"Onofri
inequality"`. GitHub's REST repository search for `Onofri Lean` returned
`total_count=0` with `incomplete_results=false`. The response bodies were
content-hashed in `anchor-audit.json`. These are bounded negative discovery
results, not a claim about unindexed, private, or future code. Because no
candidate was located, there is no external revision, type, terminal proof
body, or license to integrate and no external proof credit is assigned.

## Validation record

All commands ran in this worker clone. Lean used the existing pinned Lake
environment; no dependency was fetched or updated.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1278/AnchorAudit.lean` from `Formalizations/Lean` | 0 | eleven candidates elaborated; theorem axiom reports were exactly the standard three axioms listed above |
| `lake env lean ../../Stage1_Instances/THM-M-1278/Statement.lean` from `Formalizations/Lean` | 0 | canonical target still elaborated |
| `python3 Stage1_Instances/THM-M-1278/check_anchor_audit.py` | 0 | audit boundary, all probes, and pinned mathlib revision verified |
| `python3 -m json.tool Stage1_Instances/THM-M-1278/anchor-audit.json` | 0 | structured audit is valid JSON |
| `rg -n 'sorry\\b|^\\s*axiom\\b|^\\s*unsafe\\b' Stage1_Instances/THM-M-1278/AnchorAudit.lean` | 1 | no forbidden construct; exit 1 is ripgrep's no-match result |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets valid |
| `git diff --check -- Stage1_Instances/THM-M-1278 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is self-tested node-local evidence pending master acceptance. It does not
prove Onofri or authorize a checklist transition, and it does not complete the
obligation-tree, proof, validation, release, or theorem-completion nodes.
