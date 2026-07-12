# Anchor-audit validation record

Item: `S56-M-1140-ANCHOR_AUDIT`  
Base revision: `87fd2c8bd824761816fc0e1d0cac9f0a11fc8786`  
Audit date: 2026-07-12

## Result

The exact repo-local artifact remains a proposition definition, not a proof. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides harmonic continuity and negation, plus a
mean-value equality for real harmonic functions on discs in the complex plane. The latter does not
cover arbitrary `EuclideanSpace Real (Fin n)`. Mathlib's connected-open maximum-modulus theorems
have a strikingly close conclusion, but require complex differentiability and maximal norm; those
hypotheses do not follow from the root's real harmonicity and ordered maximum. Substituting them
would change the theorem.

Two public Lean projects were inspected at immutable revisions. `mccorvie/lean-harmonic` at
`f3b75687e0ff790ab135811db54d5c2e4ea2170b` contains preliminary polar-coordinate work and no
maximum principle. `rootkiller6788/mini-harmonic-pde-geometric-analysis` at
`ed1d36973c213f42cc69c023ebbc535f50f530c0` contains maximum-principle names, but the relevant
surfaces are assumptions, tautological `True` results, or a theorem that assumes global constancy.
They supply no acceptable terminal proof body. Neither project was installed or added to `.lake`.

The root is therefore `M3`: its exact statement exists, while the proof interface remains open.
The negative result is bounded to the recorded repository and public-index queries, not a claim
that no Lean proof exists anywhere. This phase grants no proof or theorem-completion credit.

## Commands and results

All commands ran in this worker clone. Existing pinned Lake artifacts were reused without an
update, build, dependency clone, or dependency fetch.

| Command | Exit | Exact result summary |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1140/AnchorAudit.lean` | 0 | Six closest pinned mathlib declarations elaborated and their trust reports were printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1140/Statement.lean` | 0 | Exact canonical statement and checked encoding transport re-elaborated |
| `rg -n -i 'strong maximum\|maximum principle\|harmonic.*maximum\|maximum.*harmonic' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Complex maximum-modulus and descriptive references only; no real harmonic root declaration |
| `rg -n 'theorem\|lemma\|maximum\|Maximum\|IsLocalMax' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Harmonic --glob '*.lean'` | 0 | Harmonic definitions, closure-continuity, and constructions only; no maximum theorem |
| GitHub REST repository searches recorded in `anchor-audit.json` | 0 | Exact-name queries returned zero; broad queries exposed two relevant projects for immutable source inspection |
| Sourcegraph public Lean queries recorded in `anchor-audit.json` | 0 | No strong/harmonic maximum-principle lexical match; `HarmonicOnNhd` results were mathlib and dataset mirrors only |
| immutable raw-source/archive retrieval for both external projects | 0 | Revisions and SHA-256 values recorded; neither project supplied a trusted matching declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1140/anchor-audit.json >/dev/null` | 0 | Structured audit parsed successfully |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | rank 345, planned, L0/rework-required, theorem incomplete |
| scoped prohibited-proof-token scan of `AnchorAudit.lean` | 1 | No match; exit 1 is ripgrep's expected clean no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1140 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors |

## Open integration gate

The next proof architecture must expose the missing general-dimensional local-rigidity step and
connected propagation explicitly. A later candidate can receive proof credit only after exact-type
normalization, a local checked wrapper, terminal-body provenance, trust and prohibited-token scans,
license review, and immutable dependency validation.
