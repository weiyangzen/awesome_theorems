# THM-M-1537 proof-phase recheck at 59d3efc3 (slot32)

Item: `S56-M-1537-PROOF`

Intent: `prove`

Base revision: `59d3efc3c70ee359dde2def219bf6b11be2ce804`

Base tree: `1af36aa5b2df068ecde61222e69414be53acd4bc`

Recheck time: `2026-07-15T08:35:22+08:00` (Asia/Shanghai)

## Verdict

`blocked`. No legal positive proof body exists for the exact frozen target. The
`SemiclassicalBlackHole` record stores `thermodynamicEntropy` independently of its area, physical
constants, and regime propositions. The frozen premises therefore cannot imply the requested
universal equality.

The existing placeholder-free declaration

```text
Stage1Instances.THM_M_1537.not_bekensteinHawkingAreaLaw :
  Not Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw
```

kernel-checks at trust level zero. Its witness has horizon area zero, entropy one, all four
constants one, and all three regime propositions true. Every premise holds, while
`entropyFromArea` reduces to zero, so the target would require `1 = 0`.

This refutes the frozen formal encoding, not the physical Bekenstein-Hawking law. The checked local
declaration `areaLaw_of_bridge` consumes `AreaLawBridge`, which is definitionally the same universal
equality as the root. The historical `S1_M_200` model stores an area-law proof as a structure field,
and its wrappers only project or consume that field. Neither route derives the exact unconstrained
target. A pinned-mathlib source search found no Bekenstein, black-hole, or horizon-area declaration.

No proof source, axiom, placeholder, unsafe declaration, weakened statement, substituted theorem,
or unpinned dependency was added. The frozen upstream vector remains `[H2, M5, R3]`; this proof-only
worker does not mutate it. The checked refutation suggests `H5` for the exact formal proposition
under rev-5.6 section 3.1, but an authorized statement phase must reconcile that classification with
the distinct physical claim.

## Failed gate

The first failed gate is `M1537-B-PHYSICS` / exact-target consistency. Positive proof work can
resume only after an authorized, source-faithful statement/model repair gives the regime substantive
entropy-area semantics, followed by accepted replacement statement and obligation-registry versions
and renewed statement, anchor-audit, and obligation-tree gates.

The prerequisite `S56-M-1537-OBLIGATION_TREE` is only worker-provisional `[_]`, not master-accepted
`[x]`. The proof item remains `[ ]`. No audit-completion, theorem-completion, validation, release,
receipt-acceptance, scheduler-transition, or master-acceptance claim is made. Because the assigned
positive proof phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

All checks ran in this worker clone against the existing pinned Lake closure. The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, network access, or `.lake` mutation occurred.
This is dirty, nonrelease worker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1537` | 0 | Rank 200; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only `?? Formalizations/Lean/.lake` was present. |
| `python3 Stage1_Instances/THM-M-1537/check_statement.py` | 0 | Canonical expression SHA-256 `0294eb7c5af32d8a7dfc2abf6ff5ac0431343f4eeab5fe4d331217a398d07cc8`; all four structural mutations had distinct hashes. |
| `python3 Stage1_Instances/THM-M-1537/check_anchor_audit.py` | 0 | `ok: exact statement, 6 pinned mathlib probes, partial Physlib candidate, and M4 boundary agree` |
| `python3 Stage1_Instances/THM-M-1537/check_obligation_tree.py` | 0 | Nine obligations and 16 typed edges passed; denominator `8c57fc2c6fdba40bd4293e06ca656fbe2cc371cbe00d7ac34528108b2fb13c19`; root remains refuted at `M5`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Both Lean invocations exited 0. The exact statement, conditional composition, and countermodel refutation elaborated. Both printed declarations report only `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256: `21763c76...c4224`; statement output: `ff89d33c...61fb`; obligation output: `a3249e7c...e802b`. |
| Fresh stdin `lake env lean --trust=0 -t0` replay | 0 | Exact statement, composition, countermodel, and refutation elaborated without output files; both declarations again report only `[propext, Classical.choice, Quot.sound]`. |
| Bounded repo-local candidate search | 0 | Found the frozen dossier and historical conclusion-carrying wrappers, but no proof of the exact unconstrained target. |
| `rg -n -i 'Bekenstein|black[- ]?hole|horizonArea' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match result: no such declaration in pinned mathlib. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1537/Statement.lean Stage1_Instances/THM-M-1537/ObligationTree.lean` | 1 | Expected no-match result: no prohibited construct in the checked Lean sources. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | Empty output; the pinned mathlib checkout was clean after validation. |

Exact narrow Lean recipe, run from `Formalizations/Lean`:

```bash
set -uo pipefail
TMP=$(mktemp -d /tmp/thm-m-1537-slot32-lake-env.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_PATH_BASE=$(lake env printenv LEAN_PATH)
cp ../../Stage1_Instances/THM-M-1537/Statement.lean "$TMP/Statement.lean"
cp ../../Stage1_Instances/THM-M-1537/ObligationTree.lean "$TMP/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH_BASE" timeout 300 \
  lake env lean --trust=0 -t0 --root="$TMP" \
    -o "$TMP/Statement.olean" "$TMP/Statement.lean" \
    >"$TMP/statement.out" 2>&1
statement_exit=$?
cat "$TMP/statement.out"
test "$statement_exit" -eq 0 || exit "$statement_exit"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH_BASE" timeout 300 \
  lake env lean --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean" \
    >"$TMP/obligation.out" 2>&1
obligation_exit=$?
cat "$TMP/obligation.out"
sha256sum "$TMP/Statement.olean" "$TMP/statement.out" "$TMP/obligation.out"
exit "$obligation_exit"
```

Pinned environment: Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Exact source hashes, commands,
results, failed gate, retry condition, and changed paths are recorded in the adjacent JSON artifact.

This is current-HEAD, target-specific negative kernel evidence. It is not a proof receipt and does
not satisfy `S56-M-1537-PROOF`.
