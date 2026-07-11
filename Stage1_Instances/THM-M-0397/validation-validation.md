# THM-M-0397 Validation Handoff

Item: `S56-M-0397-VALIDATION`

## Verdict boundary

This validation node is self-tested only as provisional worker evidence. The
exact conditional method-level root and a separately written reconstruction
kernel-elaborate. This does not close `M0397-SOURCE` or `M0397-TRUST`, and it
does not claim audit or theorem completion.

## Kernel, trust, and provenance results

`Proof.lean` and `Validation.lean` each reconstruct both directions of the
frozen finite-search statement. The validation probe imports only `Statement`,
not either proof-phase module. All checked declarations report exactly
`propext`, `Classical.choice`, and `Quot.sound`; neither local module contains
`sorry`, `admit`, an axiom declaration, or an unsafe declaration.

The fail-closed verifier reloads the eight-node registry and typed graph,
checks the proof receipt's input and proof-body hashes, confirms the exact
six-node kernel-closed/two-node assurance-open boundary, matches the manifest
pin to the actual mathlib checkout, and verifies source and `.olean` digests
for both direct statement imports.

## Commands and results

Commands ran from base revision
`2e3a5d5130638c6983d4febfd040ca94571e2f68` on 2026-07-12
(`Asia/Shanghai`; receipt timestamp `2026-07-11T19:47:45Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0397
  exit 0: rank 10; lifecycle planned; theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0397/check_proof.sh
  exit 0: exact root and composition elaborated; all declarations report only
  propext, Classical.choice, and Quot.sound

cd Formalizations/Lean && create a temporary directory, copy Statement.lean
and Validation.lean, elaborate Statement.olean there, then elaborate
Validation.lean with that directory prepended to lake's pinned LEAN_PATH
  exit 0: four independently reconstructed declarations elaborated and report
  only propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0397/check_validation.py
  exit 0: eight-node identity, receipt freshness, pinned source/olean
  provenance, exact-root boundary, independent reconstruction, and placeholder
  policy verified

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0397/Proof.lean \
  Stage1_Instances/THM-M-0397/Validation.lean
  exit 1 with empty output: pass, no prohibited construct found
```

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed. Temporary `.olean` output was removed after elaboration.

## Remaining gates

The first unmet release gate is section 10.6's clean, empty-cache,
network-denied cold build. The same-workspace probe is useful independent
implementation evidence, but not section 10.7's distinct signed runner.
Source/readability review, full TCB and supply-chain closure, protected CI,
deterministic bundling, master acceptance, and release remain open.
