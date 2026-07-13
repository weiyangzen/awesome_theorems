# THM-M-1234 proof attempt, 2026-07-14

Item: `S56-M-1234-PROOF`. Base revision:
`c45f3c7090cb4adf616d45e5414985f956e807b2`.

## Verdict

`blocked`. The exact universal `Stage1Rev56.THMM1234.Statement` remains open,
so this attempt does not satisfy the assigned proof phase and emits no
`.stage1-worker-selftest.json`.

`ConstructionProof.lean` adds a real local body for the exact formal interface
`CandidateConstructionPackage`: admissible initial velocity and vorticity are
used as constant-in-time candidate fields. It also proves the corresponding
one-sided vorticity trace and installs that body in the existing conditional
root composition. All three declarations elaborate with exactly `propext`,
`Classical.choice`, and `Quot.sound`.

The older `Proof.lean` remains a separately checked zero-data boundary case.
This attempt does not alter or re-credit it.

This partial body exposes rather than hides a frozen-architecture mismatch.
`M1234-A-STRUCTURE` formally targets `CandidateConstructionPackage`, but its
typed proof children require smooth approximation, uniform estimates, and
compactness. The interface consumes none of those children. Consequently the
body cannot truthfully close `M1234-A-STRUCTURE`, and none of those semantic
children is credited. The root still needs the analytic construction route and
`M1234-E-CLOSURE`. The latter quantifies over every structurally admissible
candidate, not merely a candidate selected by an existence proof, so it is
stronger than the usual Yudovich equation-passage package.

The first failed gate remains `M1234-A-APPROX`: there is no child-consuming,
placeholder-free construction of global approximants in the repository or
pinned dependency closure. Retry requires repairing the exact interfaces and
composition so they consume the frozen children, then implementing or pinning
the analytic approximation, estimates, compactness, momentum passage, and
trace bodies.

## Validation

The final recorded commands use only the existing pinned environment. No Lake
update/build, dependency clone/fetch, network access, or `.lake` mutation is
part of this attempt.

```text
tmp=$(mktemp -d /tmp/thm-m-1234-proof.XXXXXX)
cp Stage1_Instances/THM-M-1234/{Statement,ObligationTree,ConstructionProof}.lean "$tmp"
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH_PINNED=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_PATH="$LEAN_PATH_PINNED" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH_PINNED" "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$LEAN_PATH_PINNED" "$LEAN_BIN" ConstructionProof.lean
rm -rf "$tmp"
  exit 0
  Statement.lean, ObligationTree.lean, and ConstructionProof.lean elaborated
  in a temporary directory; the three new declarations report
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py
  exit 0
  14 obligations and 28 typed edges passed; denominator
  cfa0a02c68993c8b3eefc0edfe7d3d7bd20e2b58d140f47a1f5444a8ba734c5d;
  root open at M3

python3 Docs/tools/check_stage1_standard.py
  exit 0
  15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1234
  exit 0
  rank 158; planned; L0/rework-required; theorem_complete=false

prohibited-device scan of owned Lean files
  exit 1 with empty output, the expected pass result: no sorry, admit,
  axiom/constant, opaque/unsafe/extern declaration, sorryAx, implemented_by,
  or native_decide

rg -ni 'yudovich|yudovitch|incompressible[ -]?euler|bounded vorticity' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
  exit 1 with empty output: no exact-topic declaration in pinned mathlib

python3 -m json.tool \
  Stage1_Instances/THM-M-1234/proof-attempt-2026-07-14.json >/dev/null
  exit 0

git diff --check -- Stage1_Instances/THM-M-1234
  exit 0

git diff --no-index --check /dev/null <each new owned file>
  exit 1 for each expected new-file difference, with empty diagnostic output
  and no whitespace errors

test ! -e .stage1-worker-selftest.json
  exit 0
```

This is nonrelease evidence because the worker clone contains the pre-existing
untracked canonical `.lake` symlink. The canonical root remains `M3`, audit and
theorem completion are false, and the later validation and release phases are
not claimed.
