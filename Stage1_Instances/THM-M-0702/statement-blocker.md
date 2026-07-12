# Exact-statement gate: blocked

Item: `S56-M-0702-STATEMENT`  
Theorem: `THM-M-0702`  
Base revision: `f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `项的统一算法` ("an algorithm for unifying terms"), with the label
"unification algorithm", attribution to John Alan Robinson, and year 1965. This names an algorithmic
topic, not a proposition. It supplies no immutable source edition, theorem or algorithm locator,
formal term language, algorithm definition, ordered binders, hypotheses, or conclusion. Stage0
also leaves the precise definitions, assumptions, proof, axioms, and machine artifact open.

Several inequivalent roots remain compatible with this metadata:

1. termination of a specified Robinson-style procedure;
2. soundness: a returned substitution unifies the input;
3. success completeness or failure correctness: a unifier exists exactly when the procedure succeeds;
4. most-generality: every unifier factors through the returned substitution;
5. a total-correctness theorem bundling some or all of the preceding claims.

Each root still depends on choices the record does not fix: first-order signature and variable type,
two terms versus a finite equation system, substitution representation and composition direction,
syntactic versus equational unification, occurs-check behavior, equality/extensionality of
substitutions, and treatment of cyclic, empty, variable-only, and ground inputs. Choosing any such
root or convention would invent or substitute mathematics. Robinson's 1965 paper is recorded only
as a plausible discovery anchor; it has not been frozen by edition and pinpoint, crosswalked with
all incorporated definitions and assumptions, checked for corrections, or independently reviewed.

Consequently the canonical human claim fails before minimal imports, a kernel expression
fingerprint, checked alternate transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations can be produced. No theorem declaration, placeholder, axiom,
weakened special case, or broadened abstract interface was introduced. The machine state remains
`M4`; statement acceptance and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports only `Mathlib.ModelTheory.Syntax` and checks mathlib's
first-order language, term, variable, relabeling, and substitution APIs. It elaborates in the pinned
environment, showing that some encoding ingredients exist. It does not define Robinson's algorithm
or assert any correctness property and therefore receives no statement or proof credit. No narrower
canonical import can be selected while the proposition itself is absent.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the `lake-manifest.json`
SHA-256 is `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
The existing canonical `.lake` symlink and artifacts were used read-only. No update, build, clone,
fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0702` | 0 | rank 743, planned, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'THM-M-0702\|统一算法\|项的统一算法\|unification algorithm\|algorithm for unifying terms' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json Stage1_Instances/THM-M-0702` | 0 | only the topic-level source wording and intake records were found; no exact proposition or source-frozen target exists |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version and commit recorded above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0702/IntakeProbe.lean)` | 0 | all six first-order syntax substrate checks elaborated; no canonical theorem asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0702 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0702/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0702/task-dag.json` | 0 | task DAG JSON is syntactically valid |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable primary-source edition, identify
the exact algorithm and correctness theorem by pinpoint, freeze all syntax, substitution,
composition, occurs-check, result, quantifier, and boundary conventions, dispose of errata, and
independently approve the source-to-statement mapping. A later statement run can then encode that
same claim, minimize pinned imports, serialize and hash the elaborated expression, check credited
alternate forms, and run all four required mutation classes.

This is the first failed gate. The root remains `[H3, M4, R4]`, with `audit_complete: false` and
`theorem_complete: false`. The assigned phase is not genuinely self-tested to its completion gate,
so no `.stage1-worker-selftest.json` is emitted and no downstream-node credit is claimed.
