# THM-M-0927 proof-phase validation

Item: `S56-M-0927-PROOF`. Base revision:
`4d389eb47e043f6f44925a418baee0d034f764ba`; base tree:
`64faabd76665273032b8cb1554b90655b5c94256`.

## Implemented proof

`Proof.lean` installs pinned mathlib's substantive function-equality theorem
`Real.coe_fib_eq'` at frozen obligation `M0927-T-FUNCTION-BINET`. It then
passes that package, the checked function-to-pointwise transport, the checked
named-root-to-radical transport, and the checked composition package to
`ObligationTree.root_of_terminal_packages`. The resulting declaration has the
unchanged exact type `BinetFormulaTarget`, including every natural index and
the source-spelled denominator `(2 : Real) ^ n * Real.sqrt 5`.

The proof consumes all four children required by the frozen root composition
certificate. `Real.coe_fib_eq` is only a pointwise wrapper around
`Real.coe_fib_eq'`; it is not used as a second substantive proof body and gets
no duplicate proof credit. The terminal body remains in pinned mathlib source
lines 180-195, bound by source, Git blob, body-slice, and compiled-artifact
hashes in `proof-receipt.json`.

Lean trust-level-zero elaboration reports the terminal theorem and both local
declarations sorry-free. Their axiom closures are exactly `propext`,
`Classical.choice`, and `Quot.sound`. The scoped source scan finds no proof
placeholder, bodyless axiom or constant, opaque or unsafe declaration, oracle,
external implementation, or native-evaluation escape.

This supports a provisional `M0-W` proposal for the exact machine root. It is
not accepted closure or theorem completion. The accepted dossier remains
`[H1, M3, R4]` with zero accepted obligations, and the eight internal pinned
body decompositions receive no individual closure credit without their own
exact composition certificates. Source, foundation, provenance, evidence,
trust, readability, workflow, validation, release, and master gates remain
open. In particular, `theorem_complete=false`.

## Commands and results

Validation ran in this worker clone on 2026-07-15 (Asia/Shanghai), using only
the existing pinned Lake environment. No `lake update`, `lake build`, clone,
fetch, network operation, or mutation of `.lake` was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
  uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0927
  exit 0: rank 1546, planned, L0/rework_required,
  theorem_complete=false

python3 -B Stage1_Instances/THM-M-0927/check_proof.py
  exit 0: fresh temporary Statement.olean and ObligationTree.olean plus
  trust-level-zero Proof elaboration passed; the pinned function body and exact
  frozen root composition were checked; all three declarations were sorry-free
  with axioms [propext, Classical.choice, Quot.sound]

run the scoped checker twice to separate temporary logs, then cmp and sha256sum
  exit 0: both 192-byte summaries matched exactly at SHA-256
  61465f53607ea91e3b9989ad02f166d3019b2a10782e353a39abf99f46b01ff4

PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0927-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0927/check_proof.py
  exit 0: checker syntax compiled outside the repository

PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0927/check_proof.py
  exit 1 as expected: the checker rejects Python optimization instead of
  allowing optimization to disable its fail-closed assertions

python3 -m json.tool Stage1_Instances/THM-M-0927/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for both structured artifacts

git diff --check -- Stage1_Instances/THM-M-0927 \
  .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics
```

The proof node is self-tested and awaits dependency-ordered master acceptance.
It does not claim `AUDIT-Z`, downstream validation, release, or `THEOREM-Z`.
