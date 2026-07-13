# THM-M-0471 proof-phase validation

Item: `S56-M-0471-PROOF`. Base revision:
`48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0` (tree
`0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1`).

## Implemented proof route

`Proof.lean` installs the exact pinned natural-factorization family at every leaf exposed by the
frozen proof graph. It chooses `Nat.primeFactorsList`, proves its nonemptiness, primality, and
product packages, installs the generic prime-product permutation engine and its divisor,
membership, erasure, cancellation, and nonzero interfaces, and applies
`Nat.primeFactorsList_unique` to every alternative prime list.

`exactPrimeListAnchor` consumes the five registered packages through
`exactPrimeListAnchor_of_packages`. `fundamentalTheoremOfArithmetic_via_frozen_composition` then
consumes that exact child through `root_of_exactPrimeListAnchor` and returns the unchanged
`FundamentalTheoremOfArithmeticTarget`. A direct exact-root wrapper is a second type check over the
same deduplicated upstream bodies.

The terminal bodies remain in `Mathlib/Data/Nat/Factors.lean` and
`Mathlib/Data/List/Prime.lean` at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. They are not vendored or duplicated. Accordingly,
this proof phase proposes `M0-W` only; master acceptance and downstream validation remain required.

## Commands and results

Validation ran in the isolated worker clone on 2026-07-13 (Asia/Shanghai). The existing pinned
`.lake` symlink was reused. No `lake update`, `lake build`, or mathlib source/olean mutation was
performed. One delegated inspection mistakenly ran `cd Formalizations/Lean && lake env printenv
LEAN_PATH`; because the pinned `flt-regular` package directory was absent, Lake began materializing
it before the command was stopped. That cache mutation is prohibited by the worker protocol and is
not credited as validation. This target does not import `flt-regular`; the proof replay below uses
the already-present Lean binary and explicit mathlib artifact paths. The incident is a known
nonrelease failure for integration review.

```text
cd Formalizations/Lean && lake env printenv LEAN_PATH
  interrupted, not credited: attempted to resolve the absent pinned flt-regular package and left
  an untracked package directory in the shared cache

bash Stage1_Instances/THM-M-0471/check_proof.sh
  exit 0
  used the pinned Lean 4.29.0 binary and explicit pre-existing mathlib package paths, without
  asking Lake to resolve or fetch any manifest package
  temporary isolated Statement.olean and ObligationTree.olean elaborated
  Proof.lean elaborated; 24 declarations were sorry-free
  every axiom report was a subset of propext, Classical.choice, and Quot.sound
  both exact canonical root declarations closed

python3 -B Stage1_Instances/THM-M-0471/check_proof.py
  exit 0
  exact item identity, canonical fingerprint, registry denominator, complete proof-graph
  reachability, source/olean pins, local wrappers, composition, receipt, and handoff passed

python3 Docs/tools/check_stage1_standard.py
  exit 0
  15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0471
  exit 0
  rank 1353, planned, L0/rework_required, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-0471/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0
  both proof-phase JSON artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-m0471-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0471/check_proof.py
  exit 0

git diff --check -- Stage1_Instances/THM-M-0471 .stage1-worker-selftest.json
plus direct trailing-whitespace/newline checks over every new proof-phase file
  exit 0; no whitespace errors
```

The scoped checker also verifies the immutable mathlib revision/tree, both source blobs and source
SHA-256 values, both pinned olean hashes, required declarations in the visible terminal bodies,
absence of prohibited proof/oracle markers, the exact 15-node proof reachability set, and the
unchanged open authoritative and local task state.

## Status boundary

This is genuine kernel-checked proof progress but does not claim theorem completion. The accepted
instance remains `[H1, M3, R4]` with no accepted proof receipt until the integration lane acts. The
separate `M0471-S-FOUNDATION` trust/TCB certificate, H0 primary-source crosswalk, R0 readable
review, transitive provenance, hermetic replay, independent verification, validation, release,
`AUDIT-Z`, and `THEOREM-Z` remain open. The warm shared cache also makes this nonrelease evidence.
