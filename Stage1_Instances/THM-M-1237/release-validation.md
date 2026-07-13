# THM-M-1237 release decision

Item `S56-M-1237-RELEASE` has the exact verdict **blocked**. The lifecycle remains `planned`, the
root vector remains `H1/M3/R3`, and both `AUDIT-Z` and `THEOREM-Z` are false. `theorem_complete`
remains false and this worker accepts no receipt. This is a tested negative release reconciliation,
not a theorem proof, release-grade evidence, or master acceptance.

## Evidence reconciliation

The prerequisite validation receipt is only provisional `[_]` worker evidence, has
`release_grade=false`, and is not master accepted. Therefore the first failed workflow gate is
`S56-10.2-DEPENDENCY-ACCEPTANCE`; release is not dependency-legal.

There is also an intrinsic mathematical blocker. The narrow trust-zero replay elaborates the exact
Lean proposition and reflexive transport, the conditional composition, and a local representative
declaration. It does not establish that the Lean proposition is faithful to the human canonical
theorem: extension data is supplied per input instead of as a domain-level bounded operator, the
embedding constant is chosen after the input, and the weak-derivative encoding uses unrestricted
global compactly supported tests instead of a test class supported in the domain. This is the first
intrinsic theorem gate, `S56-5.1-EXACT-SOURCE-FIDELITY`.

The replay also checks two separately written counterexamples to the frozen `ValueEstimateFamily`. That
interface is false because it quantifies over every almost-everywhere-equal representative and every
constant, including a point spike with `C = 0`. The analogous arbitrary-representative issue remains
in `HolderEstimateFamily`. This refutes the frozen proof route, not the canonical existential
Sobolev statement. The exact root remains kernel-open at `M3`.

The authoritative typed graph records no accepted closed obligations and the root cut
`M1237-C`, `M1237-L-HOLDER`, and `M1237-L-VALUE`. The proof receipt only provisionally calls
`M1237-C` closed, but the graph still makes that node depend on open `M1237-N` and `M1237-B`, so the
Lean declaration is not a dependency-legal graph closure. The graph also labels terminal
`M1237-T` as `M0-L` while giving it no evidence and leaving validation pending. These conflicts keep
graph reconciliation and `AUDIT-Z` false.

`AUDIT-Z` is false because the complete discovery, source-boundary, evidence-state, and public-state
reconciliation is not accepted; primary-source `H0` and independently reviewed `R0` are missing.
The first release-specific failure is `S56-10.6-HERMETIC-COLD-BUILD`: the existing replay uses a
shared warm pinned `.lake` cache. There is no immutable clean empty-cache build, offline restoration,
complete proof-body provenance/foundation/TCB closure, SBOM/license closure, two distinct signed
runner attestations, independently implemented minimal verifier, required mutation/metamorphic
evidence, or deterministic content-addressed release bundle.

## Validation

Commands were run on 2026-07-14 from base revision
`2aab68338c370228923a5f7aba2a10b328902eab`. Existing pinned `.lake` artifacts were reused without
`lake update`, `lake build`, clone, fetch, or dependency mutation.

```text
python3 Stage1_Instances/THM-M-1237/check_release.py
  exit 0: hashes, task/dependency state, the blocked verdict, false terminal decisions, root cut,
  and a fresh narrow trust-zero Lean replay agree

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets at ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1237
  exit 0: rank 175; planned; L0/rework-required; theorem_complete=false

python3 -m json.tool Stage1_Instances/THM-M-1237/release-decision.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

git diff --check -- Stage1_Instances/THM-M-1237 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

Retry first requires repairing or replacing the false estimate interfaces and kernel-closing the
exact canonical root, then master acceptance of the dependency chain. Independent audit and release
lanes must subsequently close `H0/R0`, complete trust/provenance, hermetic supply-chain replay,
distinct-runner, minimal-verifier, mutation, deterministic-bundle, and final master gates. Only the
integration lane may accept this node or change authoritative task state.
