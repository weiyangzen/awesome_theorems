# THM-M-0388 Validation Handoff

## Verdict boundary

The validation node is self-tested as provisional worker evidence. The exact proof wrapper and a
separately written probe both elaborate the frozen integer-existence root through the pinned
`Pell.exists_of_not_isSquare` terminal body. This is not release evidence: the worker clone reused
the canonical pinned `.lake` artifacts, and the two checks share one workspace and dependency cache.
Consequently `audit_complete=false` and `theorem_complete=false` remain mandatory.

## Kernel and trust results

`Proof.lean` and `Validation.lean` each elaborate successfully with Lean 4.29.0. The local predicate
transports have no axioms. The proof root, independent probe root, and terminal mathlib declaration
all report exactly `propext`, `Classical.choice`, and `Quot.sound`. No `sorry`, `admit`, axiom
declaration, or unsafe declaration occurs in either local module or the pinned Pell source.

The verifier independently reloads the frozen registry and graph bundle, compares their canonical
node sets, checks the proof receipt's input hashes, checks the mathlib manifest revision against the
actual checkout, and checks the terminal source and `.olean` digests. It does not trust the proof
phase's prose output.

## Commands and results

Commands ran from base revision `1ce8e6521114d62a27bbf1dbcfd1a6b5192d4afc` on 2026-07-12
(receipt timestamp `2026-07-11T19:12:46Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0388
  exit 0: rank 3, planned, L0/rework_required, theorem_complete=false

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0388/Proof.lean
  exit 0: exact wrapper elaborated; root axioms are propext, Classical.choice, Quot.sound

cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0388/Validation.lean
  exit 0: independent direct probe elaborated; same root axioms; predicate transport has no axioms

python3 Stage1_Instances/THM-M-0388/check_validation.py
  exit 0: receipt freshness, pinned source/olean provenance, canonical node identity, and local
  placeholder policy verified

rg -n '\b(sorry|admit)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0388/Proof.lean \
  Stage1_Instances/THM-M-0388/Validation.lean \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib/NumberTheory/Pell.lean
  exit 1 with empty output: pass, no prohibited construct found
```

No `lake update`, build, clone, fetch, or `.lake` mutation was performed.

## Remaining gates

The first unmet release-grade gate is section 10.6's clean, empty-cache, network-denied cold build.
Section 10.7 also requires a distinct verifier identity in a separately provisioned clean checkout
with no shared writable cache, two signed attestations, and a minimal independently implemented
release verifier. Those cannot truthfully be manufactured inside this one worker clone. H0/R0,
SBOM/license, protected-CI, deterministic bundle, master acceptance, and release decision likewise
remain outside this validation handoff.
