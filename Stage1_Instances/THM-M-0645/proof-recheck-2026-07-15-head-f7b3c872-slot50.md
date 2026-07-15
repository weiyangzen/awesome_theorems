# THM-M-0645 Proof-Phase Recheck

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T19:28:41+08:00`

Base revision: `f7b3c872ab727ab689486d74020c11dc5d99869f`

Base tree: `6c3dc9661349dd7774b23660eb9bde0212918c51`

## Verdict

`blocked`. No positive proof body can truthfully close the exact frozen target because the
placeholder-free module `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

The defect is in the frozen custom calculus, not Goedel's mathematical completeness theorem.
`Provable` specializes `Derivation`'s free-variable type to `Empty`, while
`Derivation.allIntro` requires an explicit eigenvariable `x : alpha`. Universal introduction is
therefore impossible in a closed derivation. A structural induction over every constructor proves
that closed derivations preserve `proofInvariant`, under which every universal formula is false.
The universe-polymorphic symbol-free sentence `forall x, x = x` is nevertheless valid in every
nonempty structure, violates the invariant, and is not provable. Instantiating the exact root with
that language and sentence gives the checked negation above.

The existing `Proof.lean` declarations are real but conditional. `builder_of_countermodel` requires
an explicit `CountermodelProperty` premise, and `completenessTarget_of_countermodel` merely composes
that conditional result with the frozen root wrapper. Neither declaration constructs the premise
or closes the positive root. Pinned mathlib has semantic compactness/model-theory results but no
syntactic derivation theorem for this custom calculus. A candidate external completeness theorem
uses a different proof system and is not pinned locally; in any case, no consistent transport can
map it to this false target.

The first failed gate is exact-target truth and consistency at `M0645-D-CALCULUS`, before Henkin or
term-model proof execution. The proof item remains `[ ]`, the lifecycle remains `planned`, and the
authoritative root vector remains `[H2, M4, R4]`; this recheck only confirms an `M5` proof-phase
diagnosis. No obligation, receipt, audit, validation, release, theorem completion, or master
acceptance is claimed. Because the assigned positive proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

The scheduler projects the four predecessors as worker-self-tested `[_]`, not master-accepted
`[x]`. The target-local registry still reports an `M4` root with `M0645-T-CLASSICAL` as its cut set
because it predates the refutation. Neither projection supplies proof credit; this proof worker does
not rewrite predecessor or authoritative state.

## Current-Base Validation

All checks ran inside this worker clone. The automation-provided `.lake` symlink and existing pinned
packages were reused read-only. No update, build, clone, fetch, network operation, or `.lake`
mutation was performed. The Lean sources and generated outputs used for replay were confined to
disposable `/tmp` directories and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0645/check_statement.py` | 0 | All four statement mutations were killed; canonical expression hash and pinned mathlib revision matched. |
| Initial isolated replay with an over-specific one-line `rg -F` assertion | 1 | All four Lean modules elaborated, but pretty-printing wrapped the conditional theorem's axiom list; no evidence is credited to this wrapper. |
| Corrected isolated four-module `lake env lean --trust=0 -t0` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order. |
| Comment-stripped proof-device and diagnostic scan in that replay | 0 | No prohibited proof device or `sorryAx`; audited axiom sets use only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; denominator `ade5c7f4...7fc01`; predecessor root remains open M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |
| Three independent read-only audits/replays | 0 | All confirmed the `Empty` eigenvariable defect; one separately replayed the exact negation and one audited the current-base gate boundary and artifact freshness. |
| Structured JSON, source-hash, and fail-closed assertions | 0 | The blocker record parsed; all frozen source hashes matched; verdict/state remained `blocked`/`[ ]`; all completion fields remained false. |
| `git diff --check -- Stage1_Instances/THM-M-0645` plus new-file whitespace scan | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists. |

Exact successful replay command from the worker root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lean_dir=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0645-headf7b3c872-slot50.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
base_path=$(cd "$lean_dir" && {
  for path in .lake/packages/*/.lake/build/lib/lean; do
    test -d "$path" && realpath "$path"
  done
  lean=$(env -u LEAN_PATH lake env which lean)
  realpath "$(dirname "$(dirname "$lean")")/lib/lean"
} | paste -sd:)
for mod in Statement ObligationTree Proof Counterexample; do
  (
    cd "$lean_dir"
    LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s \
      env -u LEAN_PATH lake env env LEAN_PATH="$tmp:$base_path" \
      lean --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean"
  ) >"$tmp/$mod.out" 2>&1
done
for source in "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.lean; do
  perl -0777 -pe 's!/\-.*?\-/!!gs; s/--[^\n]*//g' "$source"
done >"$tmp/scoped-stripped.lean"
! rg -n '\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|extern|implemented_by|native_decide)\b' \
  "$tmp/scoped-stripped.lean"
! rg -n 'declaration uses .sorry|sorryAx' "$tmp"/*.out
rg -F "'Stage1Instances.THM_M_0645.not_completenessTarget' depends on axioms: [propext, Classical.choice, Quot.sound]" \
  "$tmp/Counterexample.out"
rg -F "'Stage1Instances.THM_M_0645.completenessTarget_of_countermodel' depends on axioms: [propext," \
  "$tmp/Proof.out"
rg -F " Classical.choice," "$tmp/Proof.out"
rg -F " Quot.sound]" "$tmp/Proof.out"
sha256sum "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.olean \
  "$tmp"/{Proof,Counterexample}.out
```

The explicit `LEAN_PATH` puts the copied target modules before pinned package libraries while
excluding the project build output. This prevents a stale project-level `ObligationTree.olean`
from being read and confines every new Lean artifact to `/tmp`.

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof.out` | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample.out` | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

## Retry Condition

Do not resume positive completeness proof work against the current target. First repair universal
introduction in the statement/calculus phase, for example by representing an eigenvariable through
an extended free-variable type rather than requiring an inhabitant of `alpha`. Then kernel-check
the quantified equality boundary, rerun statement mutations, and regenerate and reaccept every
downstream registry, graph, source audit, proof, and receipt invalidated by the changed target.

## Status Boundary

This artifact is fresh negative kernel evidence for `S56-M-0645-PROOF`. It refutes only the frozen
defective Lean calculus/target, not Goedel's classical completeness theorem. It is not a positive
proof receipt, does not satisfy the assigned proof item, and supports no provisional state, audit
completion, validation, release, theorem completion, or master-acceptance claim.
