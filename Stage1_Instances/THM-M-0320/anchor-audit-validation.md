# Anchor-audit validation record

Item: `S56-M-0320-ANCHOR_AUDIT`  
Base revision: `5467f527e0c402d2d52235957d4f316892fcfb75`

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` has the exact upper
hemicontinuity definition and useful compactness, sequential-closure, and convexity APIs, but no
Kakutani fixed-point declaration. `AnchorAudit.lean` checks the seven retained interfaces through
the existing pinned environment.

The audit found one substantive external Lean 4 candidate:
`harfe/fixed-point-theorems-lean4@11a9f041246d28374edae384241757f9a0cbd5e4`, declaration
`kakutani_fixed_point`. Its immutable source proves the compact-convex closed-graph formulation in
a finite-dimensional real normed space without matched placeholders. This is a close mathematical
anchor, not an exact local closure: it uses a subtype correspondence and a closed-graph hypothesis,
while the frozen target uses an ambient correspondence, closed bounded Euclidean domain, closed
values, and `UpperHemicontinuousOn`. The required compactness and closed-graph transports have not
been implemented or checked. Its Lean/mathlib revisions differ from this repository, it is not a
pinned dependency, and no license file or license metadata was located.

The root is therefore `M1`, not `M0-P`. The candidate creates explicit repo-local integration and
wrapper debt. No upstream README or source inspection was counted as local kernel evidence.

## Commands and results

Commands ran on 2026-07-12. External source was downloaded only to `/tmp` at an immutable commit;
no dependency clone, fetch, build, Lake update, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the manifest pin |
| `rg -n -i 'Kakutani.?fixed\|kakutani_fixed\|set.?valued.*fixed\|correspondence.*fixed' Formalizations/Lean/.lake/packages/mathlib/{Mathlib,Archive} --glob '*.lean'` | 1 | no exact fixed-point anchor in pinned mathlib; exit 1 is the expected no-match status |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0320/AnchorAudit.lean` | 0 | all seven pinned mathlib declarations elaborated and printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0320/Statement.lean` | 0 | canonical target and statement mutations re-elaborated |
| `git ls-remote https://github.com/harfe/fixed-point-theorems-lean4.git refs/heads/main` | 0 | immutable main revision `11a9f041246d28374edae384241757f9a0cbd5e4` |
| `curl ... codeload .../11a9f041...` plus `sha256sum` | 0 | immutable archive SHA-256 `08749ae7e97b6125a68ae89e1a5ef59e3a2c9793bb850d6ae3b5d96bb2388d70`; Kakutani source SHA-256 `c73b57bb952ceed4f4716c00de4e723dbacdff8d074369df6a96bce54e404903` |
| `rg -n '\bsorry\b\|\badmit\b\|(^|\s)axiom\s\|unsafe\|implemented_by' /tmp/kak-exact --glob '*.lean'` | 1 | no matched placeholder, explicit axiom declaration, unsafe declaration, or implementation override |
| `python3 Stage1_Instances/THM-M-0320/check_anchor_audit.py` | 0 | audit boundary, probes, manifest pin, and installed mathlib HEAD agreed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0320` | 0 | rank 686, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0320/anchor-audit.json` | 0 | JSON valid |
| `git diff --check -- Stage1_Instances/THM-M-0320 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is self-tested anchor-audit evidence pending master acceptance. It does not prove the frozen
target. Exact integration, obligation-tree, proof, trust, hermetic, independent-validation, and
release gates remain open. Public searches are bounded discovery evidence, not proof that no other
Lean formalization exists.
