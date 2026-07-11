# THM-M-0390 validation handoff

## Verdict boundary

The validation node is self-tested only as a fail-closed provisional handoff. The implemented
`NP.4` coprime-bases lemma and an independently written reconstruction both kernel-elaborate, but
the proof dependency does not close the normalization obligation, any exponent branch, or the
Catalan root. Therefore `audit_complete=false` and `theorem_complete=false` remain mandatory.

## Commands and results

Commands ran from base revision `62c2c0315a74e39528d22069068ffe85fea50afd` on 2026-07-12
(receipt timestamp `2026-07-11T19:26:13Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0390
  exit 0: rank 4; lifecycle planned; theorem_complete=false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/Proof.lean
  exit 0: implemented lemma and exact-hypothesis wrapper elaborate; both report only
  propext and Quot.sound

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/Validation.lean
  exit 0: independently reconstructed coprime-bases lemma elaborates; reports only
  propext and Quot.sound

python3 Stage1_Instances/THM-M-0390/check_validation.py
  exit 0: 14-node registry/graph identity, open root state, partial proof identity,
  independent probe, and placeholder policy verified

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0390/Proof.lean \
  Stage1_Instances/THM-M-0390/Validation.lean
  exit 1 with empty output: pass, no prohibited construct found
```

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
pre-existing canonical pinned `.lake` link was reused.

## Failed gates

The first failed gate is the validation node's proof prerequisite: the proof phase supplies a real
kernel-checked `NP.4` lemma but not exact-root closure or master acceptance. The same-workspace
independent probe is useful cross-check evidence, not the distinct signed runner required by section
10.7. Empty-cache hermetic replay, root provenance and trust closure, H0/R0 review, SBOM/licenses,
deterministic bundling, and master acceptance remain open.
