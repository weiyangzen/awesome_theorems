# THM-M-0397 obligation-tree validation

Item: `S56-M-0397-OBLIGATION_TREE`  
Base revision: `6f186d1f0e8b92e3a37b1b5987787a8b954cd1a7`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The registry freezes eight unique root-relevant obligations and seven separate
typed graph families. The structural check binds the freeze to SHA-256 hashes
of the exact statement and anchor audit, verifies eligibility denominators,
budgets, graph typing, global edge-ID uniqueness, proof acyclicity and reach,
the honest assurance boundary, and absence of forbidden Lean mechanisms.

The narrow Lean run checked `application_compose`, conditional `root_compose`,
and `exact_root`. The exact method-level root is `M0-L`: lower-bound evidence is
an explicit premise and the application reduction/enumerator are fields of the
universally quantified interface. This closure must not be broadened into a
claim that the repository has formalized Baker's analytic lower-bound theorem
or instantiated a concrete Diophantine equation. The axiom report is
`[propext, Classical.choice, Quot.sound]`, inherited from the Finset/mathlib
interface; no new axiom declaration was introduced.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0397` | 0 | rank 10, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0397/check_obligation_tree.py` | 0 | eight obligations and five proof edges passed; root M0-L, assurance open |
| `python3 -m json.tool` on both obligation JSON files | 0 | both structured artifacts parsed |
| `tmp=$(mktemp -d ./.m0397-obligation.XXXXXX); trap 'rm -rf "$tmp"' EXIT; cp ../../Stage1_Instances/THM-M-0397/Statement.lean ../../Stage1_Instances/THM-M-0397/ObligationTree.lean "$tmp/"; lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean" && LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean "$tmp/ObligationTree.lean"` from `Formalizations/Lean` | 0 | exact statement and all composition certificates elaborated; axiom reports printed |
| `git diff --check -- Stage1_Instances/THM-M-0397 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The pre-existing untracked `Formalizations/Lean/.lake` canonical link was reused
without mutation. No update, build, clone, or fetch command ran.

## Status boundary

This self-test covers the obligation-tree phase only. It freezes an exact graph
and demonstrates kernel closure of the deliberately method-level interface.
Primary-source pinpointing, readable reconstruction, complete terminal
provenance/trust audit, hermetic replay, independent verification, audit
completion, theorem completion, and master acceptance remain open.
