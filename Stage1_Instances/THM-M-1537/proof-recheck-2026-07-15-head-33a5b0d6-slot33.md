# THM-M-1537 proof-phase blocker recheck

Item: `S56-M-1537-PROOF`

Intent: `prove`

Date: `2026-07-15`

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

## Verdict

`blocked`. No placeholder-free positive proof body can inhabit the exact frozen target in the
current consistent environment. `SemiclassicalBlackHole` stores `thermodynamicEntropy`
independently of horizon area and the four constants, while its three regime fields are propositions
with no relation to entropy. The frozen countermodel sets area to zero, entropy to one, every
constant to one, and every regime proposition to `True`. All target hypotheses hold, but
`entropyFromArea` is zero.

The trust-zero Lean replay checks
`Stage1Instances.THM_M_1537.not_bekensteinHawkingAreaLaw :
Not Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw`. The conditional theorem
`areaLaw_of_bridge` does not close the root: `AreaLawBridge` is definitionally the same refuted
universal equality. The historical `S1_M_200` model likewise stores an area-law field and proves
consequences rather than deriving this unconstrained root. Pinned mathlib and the audited Physlib
candidate contain no exact terminal proof. Requiring positive rather than nonnegative area also
would not repair the independence of the entropy field.

The first failed gate is `M1537-B-PHYSICS / exact-target consistency`; the remaining root cut is
`M1537-B-PHYSICS`. The frozen obligation architecture remains `[H2, M5, R3]`. No statement, proof
source, registry, graph, proof body, axiom, placeholder, unsafe declaration, or dependency was
changed. The prerequisite `S56-M-1537-OBLIGATION_TREE` remains worker-provisional `[_]`, not
master-accepted `[x]`. Because the assigned positive proof phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation Evidence

Commands ran in the slot33 worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and was reused read-only.
No `lake update`, build, clone, fetch, checkout repair, or other dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Fifteen assurance groups and 1546 uniform-L0 Lean 4 targets pass. |
| `python3 scripts/stage1_target.py check` | 0 | The manifest has 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1537` | 0 | Rank 200; planned; hard-mathlib-anchor lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1537/check_anchor_audit.py` | 0 | Exact statement, six pinned mathlib probes, partial Physlib candidate, and M4 boundary agree. |
| `python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py` | 0 | Nine obligations and 16 typed edges pass; root is M5 and refuted by the checked witness. |
| `python3 Stage1_Instances/THM-M-1537/check_statement.py` | 1 | Top-level Lake resolution stops before Lean because unrelated shared `flt-regular` cannot resolve `HEAD`. |
| `cd Formalizations/Lean && lake env lean --version` | 1 | Same pre-Lean shared-artifact failure. |
| Isolated source copies; pinned mathlib `lake env lean --trust=0 -t0`; existing canonical dependency olean `LEAN_PATH`; `Statement.lean` then `ObligationTree.lean` | 0 | Both elaborate. The refutation and conditional wrapper report only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-construct scan of both checked Lean files | 1 | No `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, or `native_decide`; exit 1 means no match. |

The narrow replay used `lake env lean` from the pinned mathlib package because these two sources
import only mathlib. It supplied the already-built canonical top-level dependency olean directories
through `LEAN_PATH`; it did not build or change them. This avoided asking top-level Lake to resolve
the unrelated invalid `flt-regular` checkout while still invoking the pinned Lean toolchain through
Lake. It reproduced these hashes:

- `Statement.olean`: `21763c76f8db541140516a7e0e4a158bdadd228e85a254c17fe5d35e710c4224`
- statement output: `ff89d33cc918db629fe730ab7c1a2e5b507b7373f6446a98bf776a2cc07661fb`
- obligation output: `a3249e7c677d02614229aef9780b2e1266026bf5fc7f233d1b025808cb2e802b`

Exact replay recipe, run from the repository root:

```bash
set -uo pipefail
ROOT=$PWD
TOP=$ROOT/Formalizations/Lean
ML=$TOP/.lake/packages/mathlib
TOOLCHAIN_LIB=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean
LEAN_PATH_BASE="$TOP/.lake/packages/Cli/.lake/build/lib/lean:$TOP/.lake/packages/batteries/.lake/build/lib/lean:$TOP/.lake/packages/Qq/.lake/build/lib/lean:$TOP/.lake/packages/aesop/.lake/build/lib/lean:$TOP/.lake/packages/proofwidgets/.lake/build/lib/lean:$TOP/.lake/packages/importGraph/.lake/build/lib/lean:$TOP/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$TOP/.lake/packages/plausible/.lake/build/lib/lean:$TOP/.lake/packages/mathlib/.lake/build/lib/lean:$TOOLCHAIN_LIB"
TMP=$(mktemp -d /tmp/thm-m-1537-lake-env-slot33-33a5b0d6.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$ROOT/Stage1_Instances/THM-M-1537/Statement.lean" "$TMP/Statement.lean"
cp "$ROOT/Stage1_Instances/THM-M-1537/ObligationTree.lean" "$TMP/ObligationTree.lean"
(
  cd "$ML"
  LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH_BASE" timeout 300 \
    lake env lean --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
    "$TMP/Statement.lean" >"$TMP/statement.out" 2>&1
)
statement_exit=$?
cat "$TMP/statement.out"
test "$statement_exit" -eq 0 || exit "$statement_exit"
(
  cd "$ML"
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH_BASE" timeout 300 \
    lake env lean --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean" \
    >"$TMP/obligation.out" 2>&1
)
obligation_exit=$?
cat "$TMP/obligation.out"
printf 'statement_exit=%s\nobligation_exit=%s\n' "$statement_exit" "$obligation_exit"
sha256sum "$TMP/Statement.olean" "$TMP/statement.out" "$TMP/obligation.out"
exit "$obligation_exit"
```

This is exact negative kernel evidence, not a positive proof receipt. The broken top-level Lake
route remains a separate pinned-artifact blocker for later validation or release work.

## Required Escalation

This target already had 32 integrated proof-recheck JSON records before this run. The same
mathematical blocker has therefore exceeded the five unresolved execution ticks allowed by
rev-5.6 section 10.2. The master must stop or split the repeated assignment rather than schedule
another unchanged proof attempt.

A positive theorem requires an authorized upstream statement/model repair that genuinely relates
`thermodynamicEntropy` to horizon area, followed by replacement statement and registry acceptance
and renewed statement, anchor-audit, and obligation-tree gates. Independently, the manifest-pinned
`flt-regular` artifact must be restored outside this worker without fetching a moving dependency.
This handoff claims no proof completion, scheduler transition, release evidence, or master
acceptance.
