# THM-M-1122 proof-phase recheck at current base

Item: `S56-M-1122-PROOF`

Recheck date: `2026-07-16` (`Asia/Shanghai`)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target uniformly over its
explicit parameters. The existing repo-local, placeholder-free declaration

```text
Stage1Instances.THM_M_1122.proofPhaseCountermodel :
  Not (SchrammLoewnerEvolutionTarget
    (Measure.dirac ()) (Measure.dirac false) True
    (fun _ : Unit => true)
    (fun _ : Bool -> Real -> Unit => True)
    (fun _ : NegativeTime -> Unit => fun _ : Bool => True))
```

kernel-checks at trust level zero against a freshly elaborated `Statement.olean`.

The target leaves `lerwScalingLimit` arbitrary and represents circle Brownian motion and the radial
Loewner solution by arbitrary predicates. The countermodel makes both predicates true, takes the
Brownian-side curve to be the identity on `Bool`, and takes the alleged LERW limit to be constantly
`true` on `Unit`. Under Dirac measures at `false` and `()`,
`IdentDistrib.measure_preimage_eq` for the measurable singleton `{true}` would equate measures zero
and one.

This refutes the intended universal closure of the frozen Lean encoding, not every application of
the parameterized proposition and not Schramm's mathematical theorem. Repairing or strengthening
the target in this proof item would substitute a different theorem. The checked declaration
`root_of_conditionalIdentification` also supplies no positive root proof credit: its extra
`ConditionalIdentification` premise is definitionally the substantive conclusion being sought.

The assigned item remains `[ ]`. No positive proof receipt, state transition, audit completion,
theorem completion, validation completion, release, or master-acceptance claim is made. Because the
requested proof phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately
absent.

## Dependency And Reuse Audit

The required schema-1.1 ledger is
`Stage1_Instances/THM-M-1122/dependency-reuse-ledger.json` (SHA-256
`93c66b2f5f14bc38aca344d0fcdcbe909a9f5b9b6985d52520f140e885161605`). It binds the supplied
v2 graph digest `73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
dependency-context digest `8bfdab2a4897aa301b381fa47e73554a8d0b933b9fd78a4c5b4dce8ace6effb6`,
and this repository revision.

The audited hard-parent and hint closure is empty: there are no direct parents, transitive
ancestors, hard edges, or direct reuse hints. The one weak shared-module group,
`SHARED-MODULE-675723ec1da275fd`, was checked through actual member `THM-M-1027`. Its current
`[_]` artifacts contain only conditional Wiener-process adapter bodies and no circle Brownian,
radial Loewner, LERW, SLE identification, common terminal body, or checked transport usable by
`THM-M-1122`. The ledger therefore records the group as `not_applicable`; it transfers no proof
credit and creates no unresolved compatibility obligation. The repository ledger validator passed
with zero hard-parent inspections and one shared-group decision.

## Failed Gate And Retry

The first failed semantic gate is `S56-5.1-EXACT-TARGET-CONSISTENCY /
M1122-S-INTERFACES`. The frozen opaque interfaces permit the checked finite countermodel. The
predecessor-recorded open proof obligation is `M1122-L-IDENTIFICATION`, but the countermodel
invalidates the current statement/interface route before that obligation can receive positive
proof credit. The registry validator reports the root open at `M3`. The authoritative prerequisite
`S56-M-1122-OBLIGATION_TREE` also remains worker-provisional `[_]`, not master-accepted `[x]`.

Retry only after reopening `S56-M-1122-STATEMENT`, replacing the opaque interfaces with fixed,
source-faithful definitions and sufficient noncircular hypotheses, accepting a new statement
fingerprint, and freezing a new obligation-registry version. The statement, anchor-audit, and
obligation-tree phases must then be rerun before positive proof execution resumes. Alternatively,
redirect the work explicitly to the checked counterexample target.

The dossier has pre-existing projection inconsistencies that this proof-only worker did not alter:
`instance.json` reports root `M4` while the frozen registry validator reports `M3`;
`task-dag.json` retains stale intake-era task prose; and `scope-map.md` and
`source-statement-crosswalk.md` discuss a chordal-characterization route while the frozen statement
selects the radial LERW identification. Those inconsistencies provide no proof credit.

Blueprint section 10.2 requires an unresolved item to be split after five execution ticks. This is
the forty-ninth current-base handoff packet while the authoritative DAG still records `attempts: 0`
and `children: []`. The integration lane must reconcile the retry ledger and split, redirect, or
stop rescheduling the unchanged false target. This packet exists only because the scheduler
required a target-scoped current-base handoff.

## Validation

All Lean checks ran in this worker clone using the existing symlink to the canonical pinned Lake
artifacts. No `lake update`, `lake build`, dependency clone/fetch/checkout, network action, or
`.lake` mutation was performed. Lean output was confined to a fresh directory under `/tmp` and
removed. The pre-existing untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` final replay | 1 | Its nested v2 graph validator detected that the new blocker JSON is absent from the checked-in evidence inventory. The underlying target manifest and assurance sources were not edited. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` before new blocker files | 0 | Current checked-in graph passed before the target-owned blocker files were written. A final replay returned 1 because graph discovery inventories ordinary JSON evidence; only the required dependency ledger is explicitly excluded. Regeneration is master-owned. |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1122` | 0 | Rank 562; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` final replay | 1 | It delegates to the graph validator and failed only because the new blocker JSON is absent from the checked-in graph inventory. No graph content or state was edited by this worker. |
| `python3 Stage1_Instances/THM-M-1122/check_obligation_tree.py` | 0 | 11 obligations and 19 typed edges passed; denominator `1d0de239...863fd`; root open at `M3`, `ConditionalIdentification` at `M4`. |
| Schema-1.1 `validate_dependency_reuse_ledger` invocation | 0 | Current graph, context, base revision, empty hard-parent closure, and one weak-group non-reuse decision passed. |
| Isolated trust-zero `lake env lean` recipe below | 0 | The exact statement, conditional composition, and concrete negation elaborated. Both checked theorems report only `[propext, Classical.choice, Quot.sound]`; Lean emitted one non-failing `unnecessarySimpa` warning. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, `native_decide`, bodyless declaration, unsafe/oracle escape, `implemented_by`, or `extern` occurs in the checked Lean sources. |
| Direct pinned `lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Pinned mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}` | 0 | Manifest-pinned commit `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree `32c9eace926573a9981787ae97643e520353c893`. |
| `git diff --exit-code 5343398e..HEAD --` eight proof-relevant target inputs | 0 | The previous blocker packet's checked inputs remain byte-unchanged. |
| JSON parsing plus scoped invariant assertions on the ledger and companion packet | 0 | Structured identity, digests, open state, false completion fields, empty receipts, and absent self-test claim agree. |
| Scoped tracked and no-index new-file `git diff --check` wrapper | 0 | No whitespace diagnostics; each no-index command returned 1 only because the artifact is new. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

The isolated Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1122
tmp=$(mktemp -d /tmp/s56m1122-6bf9ee93-slot40.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/ProofCountermodel.lean" "$tmp/"
cd "$repo/Formalizations/Lean"
base_path=$(timeout --foreground 600 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$base_path" LEAN_NUM_THREADS=1 timeout --foreground 600 \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/ProofCountermodel.olean" \
  "$tmp/ProofCountermodel.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean" \
  "$tmp/ProofCountermodel.olean"
```

Replay-stable output hashes were:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `88f36fe6436c03754a145ec6c4958e668428a969a6ac2c5d9b30af2240fc6578` |
| `ObligationTree.olean` | `9ee3f8cf2221d4dc1a245ce4fa7fa5fa4920cb22629b31c1ba9bf477320c5c06` |
| `ProofCountermodel.olean` | `435977135a1829aa059464bcfc2711b5b16d5e9ca962020234eca099bba99b9d` |

The checked source SHA-256 values are:

| Input | SHA-256 |
|---|---|
| `dependency-reuse-ledger.json` | `93c66b2f5f14bc38aca344d0fcdcbe909a9f5b9b6985d52520f140e885161605` |
| `Statement.lean` | `8f6087a0c3bcf79a73348ccf978fd4761406bbe8314113b4f3b1a309f7591057` |
| `ObligationTree.lean` | `55e2616243844c3fbc8bb453bf1dc007e2deaa9ef129872c4fc9dfe97545e7a1` |
| `ProofCountermodel.lean` | `8d0c657c535ce046881b9fee5af80785dc79ac4c4275af19bb15a3673167dd1f` |
| `anchor-audit.json` | `f6dfa8a45faa5f5631500d5356c0b8c31624e5d1c28cb33f5ed8c4cf9d5309bb` |
| `obligation-registry.json` | `9bd28d167236090c1acf756f0c877c52c8095245626bc89ef55a070b338af300` |
| `typed-graphs.json` | `e9da2608d87b3315438d2eca842453c82ca717cedc5ee7aadecdf7f04814d0be` |
| `validation-specs.json` | `b87288aa846f365fdf0141a1baae6e91881fe34becb16d403bc898ec4532adde` |
| `Formalizations/Lean/lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `Formalizations/Lean/lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

This is durable current-base blocker evidence, not a proof receipt.
