# THM-M-0500 release decision

Item `S56-M-0500-RELEASE` has the exact verdict **blocked**. Lifecycle remains `planned`, the
accepted root vector remains `H1/M3/R4`, and both `AUDIT-Z` and `THEOREM-Z` are blocked.
`audit_complete=false`, `theorem_complete=false`, and no receipt is accepted. This is a tested
negative release decision, not theorem completion or master acceptance.

## Evidence reconciliation

The exact frozen target has useful provisional machine evidence. `Proof.lean` freshly elaborates a
repo-local exact wrapper over pinned mathlib declaration `Nat.infinite_setOf_prime_and_eq_mod`, and
Lean reports exactly `propext`, `Classical.choice`, and `Quot.sound` for the terminal declaration and
wrapper. This supports an `M0-W` candidate only. The authoritative instance and typed graph remain
at `H1/M3/R4`, with `root_closed=false` and open cut
`M0500-T-NONSUM` / `M0500-L-SUPPORT`.

The first observed reconciliation failure is `S56-9.1-RECEIPT-FRESHNESS`. The predecessor's only
recorded recipe, `python3 Stage1_Instances/THM-M-0500/check_validation.py`, exits 1 at its receipt
base-revision assertion. `validation-receipt.json` binds commit `028e2535b686...` and tree
`2845b046547e...`, while the integrated snapshot is commit `1f79a3f74a8e...` and tree
`5024086eeb69...`. The receipt is also provisional, `release_grade=false`, `[_]`, and not master
accepted, so `S56-10.2-DEPENDENCY-ACCEPTANCE` independently blocks the release transition.
The proof receipt also lists all 12 required-machine obligations as closed while its only recorded
recipe covers `M0500-ROOT`; it supplies no node-scoped receipt basis for that blanket closure list.
The authoritative graph attaches no accepted evidence and remains open, so the weaker state wins.

`AUDIT-Z` is unavailable: no accepted primary-source edition/theorem/page/assumption/errata
crosswalk and independent `H0` review exists, and all required readable nodes remain `R4` without
independent review. Complete transitive proof-body provenance, foundation/axiom policy, and TCB
closure are absent.

The first intrinsic release failure is `S56-10.6-HERMETIC-COLD-BUILD`. The worker reused the
pre-existing warm canonical `.lake` symlink. There is no immutable empty-cache network-denied cold
build, offline restoration archive, SBOM/license closure, two qualifying independent signed
attestations, independently implemented minimal verifier, protected CI mutation suite, or
deterministic content-addressed release bundle.

## Exact validation results

Commands ran on 2026-07-12 from base revision
`1f79a3f74a8e206d44c27513f4016a26dd7050e3`.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0500
  exit 0: rank 877, planned, legacy artifacts unaccepted, theorem_complete=false

cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0500/Proof.lean
  exit 0: exact wrapper and pinned terminal declaration elaborated; both report axioms
  [propext, Classical.choice, Quot.sound]

python3 Stage1_Instances/THM-M-0500/check_validation.py
  exit 1: AssertionError at the validation receipt base_revision freshness check;
  receipt 028e2535/2845b046 does not match current 1f79a3f7/5024086e

python3 Stage1_Instances/THM-M-0500/check_release.py
  exit 0: exact root replay passes; stale predecessor recipe, provisional dependency,
  unchanged authoritative state, false terminal decisions, complete release cut set, and
  prohibited-source scan agree

python3 -m json.tool Stage1_Instances/THM-M-0500/release-decision.json
  exit 0: valid JSON

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)\b' \
  Stage1_Instances/THM-M-0500 --glob '*.lean'
  exit 1 with empty output: pass; no prohibited source token

git diff --check -- Stage1_Instances/THM-M-0500 .stage1-worker-selftest.json
for f in Stage1_Instances/THM-M-0500/check_release.py \
  Stage1_Instances/THM-M-0500/release-decision.json \
  Stage1_Instances/THM-M-0500/release-validation.md .stage1-worker-selftest.json; do
  out=$(git diff --no-index --check /dev/null "$f" 2>&1)
  test -z "$out" || { printf '%s\n' "$out"; exit 1; }
done
  exit 0: no whitespace errors in tracked diff or any new artifact
```

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. Retry
requires fresh replayable validation evidence on one immutable snapshot, dependency-legal master
acceptance and authoritative reconciliation, then independent closure of H0/R0, provenance/trust,
hermetic supply-chain, two-runner, minimal-verifier, bundle, `AUDIT-Z`, and `THEOREM-Z` gates.
