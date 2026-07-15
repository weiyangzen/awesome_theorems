# THM-M-0070 proof-phase recheck at `6bf9ee93` (slot55)

Item: `S56-M-0070-PROOF`

Intent: `prove`

Validated at: `2026-07-16T04:47:06+08:00` (`Asia/Shanghai`)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. The unchanged frozen target is the full Feit-Thompson odd-order theorem:

```text
forall (G : Type u) [Group G] [Finite G],
  Odd (Nat.card G) -> IsSolvable G
```

The prerequisite `S56-M-0070-OBLIGATION_TREE` is still worker-provisional `[_]`, not master
accepted. Independently, the first proof-content gate fails at `M0070-X-LEAN-BODY`: no
placeholder-free Lean term inhabiting the exact target is present in the repository or pinned
dependency closure. `Stage1Instances.THM_M_0070.ObligationTree.TranslatedOddOrderBody` is
definitionally the canonical target. The checked adapter and terminal declarations consume that
open proposition; none constructs it.

Pinned mathlib supplies solvability interfaces and strict commutative, nilpotent, and Z-group
special cases, but no theorem deriving solvability from finite odd order. The exact external Lean
candidate ends in `by sorry` and has incompatible pins. The complete MathComp theorem is a Coq/Rocq
kernel object; there is no approved semantics-preserving Lean bridge or repo-local cross-kernel
validation closure.

No proof body, axiom, placeholder, unsafe declaration, weakened statement, substituted theorem, or
dependency was added. No obligation receives closure credit. The root stays `[H1, M3, R4]`, and
this proof item stays `[ ]`. Because the phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Dependency Context

The mandatory v2 ledger is
`Stage1_Instances/THM-M-0070/dependency-reuse-ledger.json` (SHA-256
`05bf5cdcc0f0f268809d7f08a8ce281177d2b9e68cd399e5ceafff2a8b58a356`). It binds graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`, target context
`14d971cd845d0229894906a2ef063d2601728147ac4829ee2d4f725413f8803f`, and this base revision.

The target has no hard parents, transitive hard ancestors, hard edges, or reuse hints. Its sole
shared group, `SHARED-MODULE-9a51f458e8582369`, is a weak co-mention of
`Mathlib.GroupTheory.Solvable`, not a shared lemma or body. Inspection of actual member
`THM-M-0069` found only provisional intake material, no frozen canonical statement, and no proof
artifact or checked transport for `M0070-X-LEAN-BODY`. The ledger therefore records
`not_applicable`, not proof reuse. The repository scheduler's schema-1.1 validator accepted the
ledger exactly; no parent or hint state is used as proof credit.

## Mandatory Split Handoff

The immediate proof cut is `M0070-X-LEAN-BODY`. The broader root cut also retains
`M0070-X-SOURCE`, `M0070-S-FOUNDATION`, `M0070-X-PROVENANCE`, `M0070-X-TRUST`,
`M0070-X-LICENSE`, `M0070-X-READABLE`, and `M0070-X-WORKFLOW`. The architecture contains 51 open
logical-decomposition nodes, 2,084 exact MathComp source-declaration obligations, and 229 bounded
source-body chunks. That inventory is a translation plan, not Lean proof evidence. Its package rows
do not yet expose dependency-legal Lean propositions for bounded proof implementation.

Twenty-one prior integrated proof-recheck pairs already record this blocker. This is the
twenty-second target-scoped execution. Section 10.2 of the rev-5.6 standard requires splitting after
five unresolved ticks rather than redispatching the same oversized item. The authoritative DAG
still records zero attempts and no children. The integration lane must reconcile that drift and
split `S56-M-0070-PROOF` into bounded dependency-legal child nodes, first freezing exact Lean
interfaces for the architecture/source packages, while retaining `M0070-X-LEAN-BODY` as the
terminal gate. This worker cannot edit the authoritative DAG or generated blueprint and does not
invent scheduler children.

Positive proof work can resume only on bounded child nodes with typed Lean interfaces, or when an
immutable compatible placeholder-free Lean body inhabits the unchanged `TranslatedOddOrderBody`.
Any body must pass exact-type, terminal provenance, axiom/TCB, placeholder, dependency, and
child-to-parent composition checks. The predecessor's owned-artifact inventory was already stale
because 42 integrated proof-recheck files were absent from `instance.json`; this proof worker did
not rewrite prerequisite authority.

## Narrow Validation

All checks ran from this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation occurred. This is warm, dirty, nonrelease
evidence. The standard and v2 DAG checks passed at preflight before target-owned edits. Their final
rerun fails closed because the generated DAG has not yet inventoried this new blocker batch; the
worker is expressly forbidden to regenerate or edit that authority.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Its nested v2 validator reported that the checked-in theorem DAG differs from fresh deterministic generation after this target-owned blocker batch was added. Worker policy forbids regenerating the protected DAG; integration must inventory the new evidence. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | The checked-in generated DAG does not yet inventory this blocker batch. This is an expected integration-boundary failure, not proof evidence; the worker did not edit or regenerate the protected authority. |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0070` | 0 | Rank 1101; lifecycle `planned`; lane `hard_statement_first_partial_verification`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| Repository scheduler schema-1.1 validation of `dependency-reuse-ledger.json` with the supplied graph and base revision | 0 | `PASS THM-M-0070 dependency reuse ledger`; the empty hard closure and weak shared-module non-reuse decision exactly cover the current context. |
| Temporary `lake env lean --trust=0 -t0` replay of `Statement.lean`, followed by `ObligationTree.lean` with a temporary `Statement.olean` | 0 | Both modules elaborated under Lean 4.29.0. `TranslatedOddOrderBody` printed definitionally as the exact target; all four conditional declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. Statement output was 1,977 bytes / 54 lines / SHA-256 `395d768d...fade5`; obligation output was 648 bytes / 14 lines / SHA-256 `a5972c2a...b1f3`. |
| Temporary pinned `lake env lean --trust=0 -t0` replay of `AnchorAudit.lean` | 0 | The exact target and available interfaces/special cases elaborated; output was 1,518 bytes / 22 lines / SHA-256 `37c22861...7818`. No odd-order root body was exposed. |
| Bounded exact-topic search over repo-local Lean and pinned package source | 1 | Expected no-match exit: no Feit-Thompson or odd-order-solvability root endpoint exists in the checked source surface; output was empty. |
| Scoped prohibited-device scan over owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, bodyless axiom/constant, unsafe/opaque/extern body, external implementation, native oracle, or `proof_wanted` occurs; output was empty. |
| Pin/tree/clean checks for pinned mathlib and `flt-regular`, plus Lean/Lake version checks | 0 | Mathlib is `8a178386...ea95` / tree `bdc39a31...c2b`; `flt-regular` is `56161b6e...1a27` / tree `32c9eace...c893`; both worktrees were tracked-clean; Lean 4.29.0 and Lake 5.0.0 were used. |
| `env LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 420 python3 -B Stage1_Instances/THM-M-0070/check_obligation_tree.py` | 1 | Lean elaboration completed, then the validator failed its final owned-artifact equality assertion. The pre-existing `instance.json` omits the 42 integrated recheck files; this proof run's new artifacts are also outside that predecessor inventory. This supplies no proof evidence. |
| `env LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 420 python3 -B Stage1_Instances/THM-M-0070/check_statement.py` | 1 | Lean elaboration completed, then it reported `instance owned-artifact inventory is stale`. |

The direct Lean replay used pinned Lean commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`, trust level zero, and only
temporary output removed after checking. Exact input hashes, the full cut set, command results,
candidate classifications, known failures, and retry conditions are in the companion JSON.

This is current-base durable blocker evidence. It does not satisfy `S56-M-0070-PROOF`, propose a
state transition, close any obligation or the root, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
