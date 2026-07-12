# THM-M-1003 obligation-tree validation

Item: `S56-M-1003-OBLIGATION_TREE`. Base revision:
`e306ea5b76dd61ecebbd9cd4e0aeeb124c9d6129`.

Validation ran in the worker clone on 2026-07-12 using the existing pinned Lake artifacts. No
dependency update, build, clone, fetch, or `.lake` mutation was performed. The temporary local
`Statement.olean` used to resolve `import Statement` was removed after the scoped Lean check.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1003/build_obligation_artifacts.py` | 0 | Generated denominator `d44a39b4a9b24a0cce89719cf41820d368483961dc0c2c624423e82136092b3c` |
| `python3 Stage1_Instances/THM-M-1003/check_obligation_tree.py` | 0 | Validated 16 obligations, required node fields, 37 typed edges, reciprocal proof/composition edges, acyclic root reachability, frozen input hashes, and the open closure boundary |
| scoped pinned `lean` compilation of `Statement.lean` to a temporary local olean followed by `ObligationTree.lean` | 0 | Exact conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets remain uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1003` | 0 | Rank 283, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1003 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The exact Lean command was:

```text
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean) &&
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH) &&
cd Stage1_Instances/THM-M-1003 &&
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean &&
LEAN_PATH=.:"$LEAN_PATH" "$LEAN_BIN" ObligationTree.lean
```

The conditional certificate only shows that the common candidate and same-exponent norm packages
entail the exact root. It does not inhabit either premise. The root cut set remains
`M1003-T-CANDIDATE` and `M1003-T-SAME-EXPONENT`; proof, source, readability, full validation,
release, and theorem-completion gates remain open.
