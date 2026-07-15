# THM-M-1537 proof-phase recheck at 0c26cec0 (slot19)

Item: `S56-M-1537-PROOF`

Intent: `prove`

Base revision: `0c26cec0be4f7fada10abc2c6ed0b213656d1708`

Base tree: `52417604a8aaccfac38ae970ef94337e6f38d033`

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target. The
`SemiclassicalBlackHole` record stores `thermodynamicEntropy` independently of its horizon area,
physical constants, and regime propositions. Those premises therefore cannot imply the requested
universal equality.

The placeholder-free declaration

```text
Stage1Instances.THM_M_1537.not_bekensteinHawkingAreaLaw :
  Not Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw
```

kernel-checks at trust level zero. Its admissible record has horizon area zero, entropy one, all
four constants one, and all three regime propositions true. Every premise holds, while
`entropyFromArea` reduces to zero, contradicting the required equality `1 = 0`. A temporary-copy
mutation sets the horizon area to one; the same refutation still elaborates. Thus excluding
degenerate zero-area horizons would not repair the independent entropy field.

An independent worker also reconstructed the record and negation proof in a fresh temporary file,
without importing `ObligationTree.lean`, and elaborated it with pinned Lean at trust level zero.
This confirms that the result is not merely a stale validator assertion or reuse of the dossier's
existing theorem body.

This refutes the frozen formal encoding, not the physical Bekenstein-Hawking law. The checked local
declaration `areaLaw_of_bridge` consumes `AreaLawBridge`, which is definitionally the same false
universal equality as the root. Historical `S1_M_200` declarations consume models or predicates
already carrying an area-law relation. Importing either route would hide the missing conclusion as
a premise rather than prove this target. No exact terminal proof exists in the bounded pinned
mathlib search, and the audited external Physlib candidate concerns finite canonical ensembles,
not horizon area.

No proof source, axiom, placeholder, unsafe declaration, weakened statement, substituted theorem,
unpinned dependency, or repository proof source was added. The frozen upstream vector remains
`[H2, M5, R3]`; this proof-only worker does not mutate it. The checked refutation warrants `H5` for
the exact formal proposition under rev-5.6 section 3.1, while an authorized statement phase must
reconcile that classification with the distinct physical claim.

## Failed Gate

The first failed gate is `M1537-B-PHYSICS` / exact-target consistency. Positive proof work can
resume only after an authorized, source-faithful statement/model repair gives the physical regime
substantive entropy-area semantics, followed by accepted replacement statement and registry
versions and renewed statement, anchor-audit, and obligation-tree gates.

The prerequisite `S56-M-1537-OBLIGATION_TREE` is only worker-provisional `[_]`, not master-accepted
`[x]`. The proof item remains `[ ]`. No audit completion, theorem completion, validation, release,
receipt acceptance, scheduler transition, or master acceptance is claimed. Because the assigned
positive proof phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json`
remains absent.

There were already 56 integrated proof-recheck pairs for this same item before this run. The same
countermodel blocker has therefore persisted far beyond the five-tick limit in rev-5.6 section
10.2. The master must split or redirect the item to an authorized statement/model repair rather
than schedule another identical positive-proof attempt.

## Validation

All checks ran in this worker clone with the existing pinned Lake closure. The automation-provided
untracked `Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, network access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1537` | 0 | Rank 200; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --branch` before edits | 0 | Detached HEAD and only `?? Formalizations/Lean/.lake`. |
| `python3 Stage1_Instances/THM-M-1537/check_statement.py` | 0 | Canonical expression SHA-256 `0294eb7c...7cc8`; all four structural mutations had distinct hashes. |
| `python3 Stage1_Instances/THM-M-1537/check_anchor_audit.py` | 0 | Exact statement, six pinned mathlib probes, the partial Physlib candidate, and the `M4` boundary agree. |
| `python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py` | 0 | Nine obligations and 16 typed edges passed; denominator `8c57fc2c...c19`; root remains refuted at `M5`. |
| isolated `lake env lean --trust=0 -t0` recipe below | 0 | Both Lean invocations exited 0. The exact statement, conditional composition, and countermodel refutation elaborated; both printed declarations report exactly `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256: `21763c76...c4224`; statement output SHA-256: `ff89d33c...61fb`; obligation output SHA-256: `a3249e7c...e802b`. |
| independent temporary-file refutation | 0 | A separately authored `Not BekensteinHawkingAreaLaw` elaborated at trust level zero and reported the same three axioms; it did not import the target-owned negation proof. |
| temporary positive-area countermodel replay | 0 | Changing only the temporary witness area from zero to one still elaborated the refutation at trust level zero. |
| bounded exact-target/local-library search | 0 | Found the frozen dossier and historical assumption-carrying wrappers, but no exact root proof in the pinned closure. |
| prohibited-construct scan over `Statement.lean` and `ObligationTree.lean` | 1 | Expected ripgrep no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, or `native_decide`. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| pinned mathlib and `flt-regular` `git status --short` | 0 | Empty output; both dependency worktrees remained clean. |

Exact Lean recipe, run from the worker clone:

```bash
ROOT=$PWD
TOP=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-1537-slot19-0c26cec0.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$ROOT/Stage1_Instances/THM-M-1537/Statement.lean" "$TMP/Statement.lean"
cp "$ROOT/Stage1_Instances/THM-M-1537/ObligationTree.lean" "$TMP/ObligationTree.lean"
LEAN_BIN=$(cd "$TOP" && lake env which lean)
LEAN_PATH_BASE=$(cd "$TOP" && lake env printenv LEAN_PATH)
(cd "$TOP" && LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH_BASE" timeout 300 \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean")
(cd "$TOP" && LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH_BASE" timeout 300 \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean")
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Exact source hashes, output hashes, commands, failed
gate, retry condition, and changed paths are recorded in the adjacent JSON artifact.

This is fresh current-base, target-specific negative kernel evidence and a mandatory escalation
handoff. It is not a proof receipt and does not satisfy `S56-M-1537-PROOF`.
