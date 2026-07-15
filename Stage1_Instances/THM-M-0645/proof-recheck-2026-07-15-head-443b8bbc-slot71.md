# THM-M-0645 proof recheck at `443b8bbc` (slot71)

Item: `S56-M-0645-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T11:42:26+08:00`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. The exact frozen positive target cannot be proved truthfully because its negation is
already kernel checked. `Counterexample.lean` contains the placeholder-free declaration

```text
Stage1Instances.THM_M_0645.not_completenessTarget :
  Not Stage1Instances.THM_M_0645.CompletenessTarget
```

`Provable` fixes `Derivation`'s free-variable type to `Empty`, but `Derivation.allIntro` requires
an explicit eigenvariable `x : alpha`. Universal introduction is therefore unusable in a closed
sentence derivation. A structural invariant proves that every remaining derivation constructor
preserves a fragment in which universal formulas are false. The symbol-free closed sentence
`forall x, x = x` is semantically valid, violates that invariant, and is not provable. Instantiating
the exact root with this language and sentence yields the checked negation.

This refutes only the frozen custom Lean calculus and target, not Goedel's mathematical
completeness theorem. The proof phase remains `[ ]`; `root_closed=false`,
`theorem_complete=false`, and no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Proof Boundary

The pre-existing `Proof.lean` has two real conditional bodies. `builder_of_countermodel` performs
classical contraposition, and `completenessTarget_of_countermodel` composes it with the exact-root
wrapper. Both require `CountermodelProperty` as an explicit premise. They do not construct that
premise and cannot close a root whose negation is checked.

The first failed gate is exact-target truth/consistency at `M0645-D-CALCULUS`, before the planned
Henkin and countermodel cut. The predecessor graph still reports its open `M4` architecture;
current proof evidence diagnoses `M5` statement/calculus mismatch without rewriting predecessor
authority.

## Validation

The final trust-zero replay used the pinned Lean 4.29.0 executable and existing compiled pinned
dependencies only. Outputs and oleans were confined to a fresh `/tmp` directory and removed. The
project build directory was deliberately excluded from `LEAN_PATH` because it contains an
unrelated top-level `ObligationTree.olean`. No update, build, clone, fetch, network access, or
`.lake` mutation was performed by this worker.

The requested `lake env lean` path was attempted first but failed before elaboration: the shared
automation `.lake/packages/flt-regular` directory was concurrently incomplete and could not
resolve `HEAD`. Other automation processes were visibly fetching that package. Worker policy
forbids repairing or fetching a moving dependency, so the missing artifact is recorded rather
than mutated. The fallback replay used the pinned executable named by `lean-toolchain` and only
already-existing `.olean` directories.

An initial direct fallback put the project build directory ahead of the temporary target. The
statement and obligation modules exited zero, but `Proof.lean` exited 1 after importing an unrelated
top-level `ObligationTree.olean`; its diagnostics included `sorryAx` only as the consequence of the
failed elaboration. That run grants no evidence. The corrected command below removes the colliding
project build directory and puts the temporary target first.

Exact successful replay command, run from the worker root:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0645
lake_root=$root/Formalizations/Lean/.lake
lean=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
paths=()
for p in "$lake_root"/packages/*/.lake/build/lib/lean; do
  test -d "$p" && paths+=("$p")
done
paths+=("$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
tmp=$(mktemp -d /tmp/thm-m-0645-final.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target"/{Statement,ObligationTree,Proof,Counterexample}.lean "$tmp"/
for mod in Statement ObligationTree Proof Counterexample; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" \
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
    assert "sorryAx" not in output
    assert "declaration uses 'sorry'" not in output
    assert "error:" not in output
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
print("FINAL_TRUST_ZERO_REPLAY=PASS")
PY
sha256sum "$tmp"/{Statement,ObligationTree,Proof,Counterexample}.olean \
  "$tmp"/{Proof,Counterexample}.out
"$lean" --version
git -C "$lake_root/packages/mathlib" rev-parse HEAD HEAD^{tree}
```

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0645` | 0 | rank 691; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && env -u LEAN_PATH lake env printenv LEAN_PATH` | 1 | shared `flt-regular` artifact could not resolve `HEAD`; no repair or fetch attempted |
| initial direct fallback with the project build directory in `LEAN_PATH` | 1 | `Proof.lean` imported a colliding top-level `ObligationTree.olean`; failed run rejected and recipe corrected |
| isolated pinned Lean replay with `--trust=0 -t0` | 0 | `Statement`, `ObligationTree`, `Proof`, and `Counterexample` elaborated; all checked declarations had axiom sets contained in `propext`, `Classical.choice`, and `Quot.sound`; no forbidden proof device or `sorryAx` |
| `python3 Stage1_Instances/THM-M-0645/check_obligation_tree.py` | 0 | 15 obligations and 43 typed edges passed; predecessor open-M4 boundary retained |
| `python3 Stage1_Instances/THM-M-0645/check_anchor_audit.py` | 0 | receipt hash and pinned mathlib revision passed |
| JSON parsing, whitespace checks, and absence-of-selftest check | 0 | fresh reports parse cleanly, have no whitespace errors, and no completion manifest exists |

Lean reported version 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib was pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `Counterexample.olean` has SHA-256
`8dcfbde337211b11b3eb525b6f3cc2a5a191f3abfd60fc7d312725382d300c32`.
`#print axioms not_completenessTarget` reported exactly `propext`, `Classical.choice`, and
`Quot.sound`.

## Retry Condition

Positive proof work may resume only after authorized statement repair replaces the unusable
universal-introduction interface with a source-faithful eigenvariable or context-extension rule.
The repaired calculus must derive the quantified empty-language equality boundary. The integration
lane must then accept a new statement fingerprint, publish an append-only obligation-registry
delta, and rerun mutation testing, anchor audit, graph construction, and proof execution in
dependency order.

This is fresh nonrelease blocker evidence only. It does not satisfy `S56-M-0645-PROOF`, change
scheduler state, close the positive root, or claim audit completion, validation, release, theorem
completion, receipt acceptance, or master acceptance.
