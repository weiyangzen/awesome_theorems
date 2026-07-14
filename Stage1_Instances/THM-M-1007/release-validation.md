# THM-M-1007 release decision handoff

Item: `S56-M-1007-RELEASE`

Base revision: `a9274bb02f984e5c74d2c97339044c6db8eb14f9`

Decision date: `2026-07-15` (`Asia/Shanghai`)

## Exact verdict

The release verdict is `blocked`. Lifecycle remains `planned`, the recorded root vector remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false. No receipt or frozen
obligation is accepted, so neither `AUDIT-Z` nor `THEOREM-Z` is claimed.

The first node gate failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the prerequisite validation item
is only worker-self-tested `[_]`; its receipt is `accepted=false` and `release_grade=false`, and no
master-accepted predecessor exists. The first mathematical root failure is
`proof.root_kernel_closure.M1007-L-BOUNDED-NEC`. The first intrinsic release failure is incomplete
transitive provenance/TCB closure, followed by the section 10.6 cold-build gate.

## Evidence reconciliation

The exact frozen target currently elaborates at Lean trust level zero on the pinned toolchain. The
conditional child-to-root composition and exact proved sufficiency implication are also supported
by unchanged, hash-bound historical proof and validation receipts. Those older recipes are not
misrepresented as current replays. Nothing declares or derives the missing necessity direction or
the canonical biconditional root.

The historical validation receipt is useful hash-bound evidence, but its recorded recipe is stale
at this integrated snapshot: its checker requires the earlier validation worker's base revision,
pre-integration DAG state, exact changed-path set, and now-absent worker packet. The release checker
therefore does not misrepresent that recipe as replayed. The separate current packet-free Lean
check covers only the canonical statement and records this stale-recipe boundary explicitly.

The proof source contains a placeholder-free exact sufficiency direction and related subbranches,
but no bounded independent-series necessity theorem. Thus `M1007-L-BOUNDED-NEC`, necessity,
assembly, and the canonical biconditional root remain open. The frozen graph has no accepted closed
obligations and retains the weaker `H1/M3/R3` root state.

`AUDIT-Z` also remains blocked: the primary-source crosswalk lacks an accepted pinpoint page,
assumption and errata mapping with independent H0 review, and there is no independently reviewed R0
reconstruction. Release additionally lacks an accepted foundation profile, complete transitive
provenance/TCB/SBOM, immutable clean empty-cache cold and offline reproduction, durable license
archives, two independently provisioned signed runners, an independently implemented minimal
verifier, protected release CI, and a deterministic current evidence bundle.

## Commands and exact results

Commands ran from this worker clone. No `lake update`, `lake build`, dependency clone/fetch,
checkout, network request, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required

python3 scripts/stage1_target.py show THM-M-1007
  exit 0: rank 287, planned, legacy artifacts unaccepted, theorem_complete=false

python3 Stage1_Instances/THM-M-1007/check_obligation_tree.py
  exit 0: 19 obligations and 54 typed edges passed; root remains M3 with the frozen seven-node cut

cd Formalizations/Lean && lake env lean --trust=0 -t0 \
  ../../Stage1_Instances/THM-M-1007/Statement.lean
  exit 0: the exact canonical target elaborated on Lean 4.29.0

python3 -B Stage1_Instances/THM-M-1007/check_release.py
  exit 0: current authority and input hashes, receipt boundaries, source hygiene, and the
  fail-closed release decision passed

python3 -m json.tool Stage1_Instances/THM-M-1007/release-spec.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1007/release-decision.json >/dev/null
python3 -m json.tool Stage1_Instances/THM-M-1007/release-receipt.json >/dev/null
python3 -m json.tool .stage1-worker-selftest.json >/dev/null
  exit 0 for all four structured artifacts

PYTHONPYCACHEPREFIX=/tmp/stage1-m1007-release-pycache python3 -m py_compile \
  Stage1_Instances/THM-M-1007/check_release.py
  exit 0: checker bytecode compiled outside the repository

git diff --check -- Stage1_Instances/THM-M-1007 .stage1-worker-selftest.json
  exit 0: no scoped whitespace errors
```

The narrow current statement check reuses the existing pinned shared `.lake` dependency artifacts.
It is deliberately classified as warm nonrelease evidence, not as a cold hermetic build or
independent verification. This self-tests the negative release decision only.
