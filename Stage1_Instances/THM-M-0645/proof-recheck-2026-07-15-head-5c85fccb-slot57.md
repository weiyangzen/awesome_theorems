# THM-M-0645 proof recheck at `5c85fccb` (slot57)

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T14:57:11+08:00`

Base revision: `5c85fccbb71a5ac8b4a5d95413a0f36af5e04294`

Base tree: `f80ad746fe4c15d869994cc47c3f10b881d89dd5`

## Verdict

`blocked`. No positive proof body can truthfully close the exact frozen target because the owned,
placeholder-free module `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

The defect is in the frozen custom calculus. `Provable` specializes `Derivation`'s free-variable
type to `Empty`, while `Derivation.allIntro` requires an explicit eigenvariable `x : alpha`.
Universal introduction is therefore impossible in a closed derivation. A structural induction
shows that every remaining derivation constructor preserves `proofInvariant`, in which every
universally quantified formula is false. The universe-polymorphic symbol-free sentence
`forall x, x = x` is nevertheless semantically valid, violates that invariant, and is not
provable. Instantiating the exact root with this language and sentence yields the checked negation.

This refutes only the defective Lean target, not Goedel's mathematical completeness theorem. The
first failed gate is exact-target truth and consistency at `M0645-D-CALCULUS`, before Henkin or
term-model proof execution. The predecessor graph retains its authoritative open `M4` state; this
proof evidence diagnoses an `M5` statement/calculus mismatch without rewriting predecessor state.

The existing `Proof.lean` declarations are real but conditional. `builder_of_countermodel` takes an
explicit `CountermodelProperty` premise, and `completenessTarget_of_countermodel` composes it with
the exact-root wrapper. Neither declaration constructs that premise, so neither closes the positive
root. No compatible terminal theorem for this custom `Derivation` exists in the pinned mathlib
closure.

The proof item remains `[ ]`, lifecycle remains `planned`, and the accepted root vector remains
`[H2, M4, R4]`. No proof receipt, audit completion, validation, release, theorem completion, or
master acceptance is claimed. Because the assigned positive proof phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Scoped validation

All checks ran inside this worker clone. The automation-provided `.lake` symlink and already-built
pinned packages were reused read-only. No update, build, clone, fetch, network operation, or `.lake`
mutation was performed. Lean sources and outputs were copied to a disposable `/tmp` directory and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 and the uniform L0/rework-required baseline passed. |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | Rank 691; planned `hard_statement_first_partial_verification` lane; theorem incomplete. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated in dependency order. |
| Comment-stripped source scan plus output/axiom assertions in the replay | 0 | No `sorry`, `admit`, `sorryAx`, declared `axiom`, `constant`, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide`; all audited axiom sets were subsets of `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; denominator `ade5c7f404980300aed3c54b9ac7289122562478f2866babd794986ddf37fc01`; predecessor root remains open M4. |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | Anchor receipt `d61ebc24...1506` and pinned mathlib revision passed. |

The successful narrow Lake replay was run from a fresh directory so Lake had no workspace root to
prepend. This prevents the canonical workspace's unrelated top-level `ObligationTree.olean` from
shadowing the freshly elaborated target module:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lean_root=$root/Formalizations/Lean
lake=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lake
paths=()
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do
  test -d "$p" && paths+=("$p")
done
paths+=("$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
package_path=$(IFS=:; printf '%s' "${paths[*]}")
tmp=$(mktemp -d /tmp/thm-m-0645-head5c85fccb.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
cd "$tmp"
for mod in Statement ObligationTree Proof Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$package_path" timeout 300 "$lake" env lean \
    --trust=0 -t0 -R "$tmp" -o "$tmp/$mod.olean" "$tmp/$mod.lean" \
    >"$tmp/$mod.out" 2>&1
done
python3 - "$target" "$tmp/Proof.out" "$tmp/Counterexample.out" <<'PY'
import re
import sys
from pathlib import Path

target = Path(sys.argv[1])
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Counterexample.lean"):
    source = (target / name).read_text(encoding="utf-8")
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    source = re.sub(r"--.*", "", source)
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(source) is None, name
allowed = {"propext", "Classical.choice", "Quot.sound"}
checks = (
    (Path(sys.argv[2]).read_text(),
     ("builder_of_countermodel", "completenessTarget_of_countermodel")),
    (Path(sys.argv[3]).read_text(),
     ("proofInvariant_of_derivation", "reflexivitySentence_valid",
      "reflexivitySentence_not_provable", "not_completenessTarget")),
)
for output, names in checks:
    assert "sorryAx" not in output and "error:" not in output
    for name in names:
        declaration = "Stage1Instances.THM_M_0645." + name
        report = re.search(
            re.escape("'" + declaration + "' depends on axioms: [") + r"(.*?)]",
            output,
            re.DOTALL,
        )
        no_axioms = ("'" + declaration + "' does not depend on any axioms") in output
        assert report or no_axioms, declaration
        actual = ({part.strip() for part in report.group(1).split(",") if part.strip()}
                  if report else set())
        assert actual <= allowed, (declaration, actual)
print("TRUST_ZERO_REPLAY=PASS")
PY
sha256sum "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.olean \
  "$tmp"/{Proof,Counterexample}.out
```

The same run applied a comment-stripped prohibited-device scan and parsed each `#print axioms`
report. `not_completenessTarget` reported exactly `propext`, `Classical.choice`, and `Quot.sound`.
Output hashes were:

| Artifact | SHA-256 |
|---|---|
| `Statement.olean` | `25eb67ade92875261cb4dafa5ae9075c3fe28e1e657ac763d2b7624430e04024` |
| `ObligationTree.olean` | `6c98e1bb9243a0930eae92822ff4d7a1043165662164476f7c47f7b0894bc614` |
| `Proof.olean` | `7c54139cf4e0d1fc38e44d2f6c1cca225e2fd83bd46dc35daa60ab86b344e7ce` |
| `Counterexample.olean` | `8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32` |
| `Proof` output | `bfd3e14def163e4418a27cd1c1890dbe8e26ff0cf2c2589ff3631541c48b5e2b` |
| `Counterexample` output | `80fb95cd6ab7948cfd7822889b590175b38af7d6180dd61103cbc634e37f48c1` |

The replay used Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. An independent subagent replayed
`Statement.lean` and `Counterexample.lean` under trust level zero and obtained the same hashes and
axiom reports. This is narrow nonrelease blocker evidence, not release validation.

## Retry condition

Positive proof work may resume only after an authorized statement-phase repair replaces the
unusable universal-introduction interface with a source-faithful eigenvariable or context-extension
rule and kernel-checks the quantified empty-language equality boundary. The integration lane must
then accept a new statement fingerprint, publish an append-only obligation-registry delta, and
rerun statement mutation testing, anchor audit, obligation-tree construction, and proof execution
in dependency order.
