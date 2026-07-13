# THM-M-0112 proof-phase recheck at current base

Item: `S56-M-0112-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `92246ea92c0c44282c05728798bc7c7e4a5a1464`

Base tree: `bd58be98bf3046078c016d44fb4a677ea231cb23`

## Verdict

`blocked`. No consistent positive proof body exists for the exact frozen Lean
target. The existing placeholder-free declaration

```text
Stage1Instances.THMM0112.Proof.not_weakTopologicalLefschetzTarget :
  Not (Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget.{0, 0})
```

kernel-checks at trust level zero against a fresh temporary `Statement.olean`.
A universe-polymorphic proof of the positive target would specialize to
universes `(0, 0)` and contradict this declaration.

The countermodel takes `X := PUnit`, discrete `Y := Bool`, and complex
dimension two. It makes every opaque geometric proposition `True`, uses a
constant inclusion, and supplies a constant `piMap`. The frozen target then
requires injectivity in degree zero because `0 < 2 - 1`. The two path
components of `Bool` are distinct, but the constant map sends both to the same
element. Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for
the refutation.

This refutes the abstract Lean encoding, not the mathematical Lefschetz
hyperplane theorem. The field `piMapIsInducedByInclusion : Prop` has no law
relating `piMap` to `inclusion`, and the smoothness, projectivity, and
hyperplane fields are likewise unconstrained propositions. Adding the needed
semantic laws during this proof phase would change the frozen target and is
outside the assigned node.

No positive proof body, receipt, or frozen-obligation closure was added. The
proof item remains `[ ]`; the accepted dossier vector remains `[H1, M3, R3]`,
with `M5` only the proposed machine diagnosis for the refutable encoding.
Neither audit completion, validation, release, theorem completion, nor master
acceptance is claimed. `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is exact-target consistency at `M0112-S-INTERFACE`, not
the later relative-homotopy API described by the older `proof-result.md`. The
actionable remaining root cut is `S56-M-0112-STATEMENT`,
`M0112-S-INTERFACE`, and `M0112-ROOT`.

Resume only after reopening the statement phase, replacing the opaque
stand-ins with native complex-geometric constructions or noncircular semantic
laws that tie `piMap` to the actual inclusion-induced homotopy map, accepting a
new exact statement fingerprint and obligation-registry version, and rerunning
the statement, anchor-audit, obligation-tree, and proof gates.

## Validation

All completed checks ran in this worker clone against the existing pinned Lake
artifacts. The automation-provided untracked `Formalizations/Lean/.lake`
symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network access, or `.lake` mutation was performed. Temporary Lean
objects were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0112` | 0 | Rank 35; planned lifecycle; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0112/check_obligation_tree.py` | 0 | 13 obligations and 31 typed edges passed; denominator `5d119562...7df7f4`; the predecessor graph still records the root as open M3. |
| Isolated trust-zero `lake env lean` recipe below | 0 | Exact statement and refutation elaborated; the negative declaration has the exact type above and reports `[propext, Classical.choice, Quot.sound]`. |
| Independent isolated trust-zero replay of the same tracked inputs | 0 | A second worker independently obtained statement exit 0 and proof exit 0 with the same exact declaration and axiom report. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-0112/Proof.lean` | 1 | Expected no-match exit; no prohibited proof escape occurs. |
| `python3 -m json.tool Stage1_Instances/THM-M-0112/proof-recheck-2026-07-14-head-92246ea.json` | 0 | Current-base structured blocker record is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0112` | 0 | No whitespace errors in the owned-path delta. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

Exact isolated Lean recipe, run from the repository root:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0112-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0112/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0112/Proof.lean "$tmp/Proof.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=.:"$lean_path" "$lean" --trust=0 -t0 Proof.lean
```

The statement and anchor-audit Python wrappers were also started, but severe
shared-host Lean contention made them exceed the useful narrow-check window;
they were interrupted and left only temporary files, which were removed. This
blocker does not rely on those wrappers: the structural standard, target
manifest, frozen obligation graph, and direct isolated kernel replay all
completed. Their previously accepted input files are byte-identical to the
hashes bound above.

This is durable blocker evidence, not a proof receipt.
