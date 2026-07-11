# Anchor-audit validation record

Item: `S56-M-0183-ANCHOR_AUDIT`  
Base revision: `b4f8dc843f188c63b631e3106d2694a3b07d1af1`

## Result

The exact repo-local artifact remains a proposition definition with no proof body. Pinned mathlib
at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies complex-manifold, smooth Riemannian metric,
tangent-bundle, covariant-derivative, and algebraic Kahler-differential infrastructure. The ten
named probes elaborate, but no declaration defines the analytic Kahler/Ricci/Chern objects needed
by the target or proves its existential conclusion. Algebraic `KaehlerDifferential` is not a
geometric Kahler metric.

A bounded external search found `facebookresearch/atlas-lean` at immutable commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its Calabi-Yau hypersurface file defines Calabi-Yau
algebraically via canonical twist, not via a prescribed-class Ricci-flat metric, and contains two
`sorry` declarations. It is therefore off-target and ineligible. The complete 1204-entry tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` has no relevant path.
Public searches are dated and content-hashed discovery evidence, not immutable negative proof.
GitHub code search required authentication, so no global absence claim is made.

The root remains `M4`: no proof candidate can be integrated. This completes the bounded anchor
audit, not the human-source audit, proof, or theorem-completion gates.

## Commands and results

All commands ran on 2026-07-12 in this worker clone. Lean used only the existing pinned `.lake`
environment; no update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0183/AnchorAudit.lean` | 0 | ten pinned support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0183/Statement.lean` | 0 | frozen target and statement transport re-elaborated |
| `python3 Stage1_Instances/THM-M-0183/check_anchor_audit.py` | 0 | schema, status boundary, probes, manifest pin, and installed mathlib HEAD agreed |
| dependency-wide `rg` over all eleven pinned package source trees | 1 | no target terminal declaration; exit 1 is the expected no-match status |
| three Sourcegraph Lean query families | 0 | only off-target atlas-lean names and one physlib documentation mention; Ricci query had zero matches; exact response hashes are in the JSON receipt |
| five GitHub repository searches | 0 | one unrelated mirror-map repository and zero results for four target-oriented searches |
| unauthenticated GitHub code search | 0 HTTP transaction / HTTP 401 | authentication blocker recorded; no negative result claimed |
| immutable atlas-lean source/tree inspection | 0 | off-target canonical-twist definition; two `sorry` lines; complete 2860-entry tree at the recorded commit |
| immutable Formal Conjectures tree inspection | 0 | complete 1204-entry tree, no relevant path; response SHA-256 recorded |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-0183` | 0 | rank 130, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0183 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This phase is self-tested anchor-audit work pending master acceptance. Search failure is not proof
of global nonexistence. No source-fidelity promotion, obligation tree, proof body, external
integration, or theorem completion is claimed. Reopen the integration route only for an immutable,
exact candidate with checked dependencies, license, terminal body, placeholders, axioms, and a
successful repo-local wrapper.
