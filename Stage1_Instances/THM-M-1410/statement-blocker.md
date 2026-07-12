# Exact-statement gate: blocked

Item: `S56-M-1410-STATEMENT`

Theorem: `THM-M-1410`

Base revision: `ffe94ac84965dc19f4923f88b7566072ddee37ae`

Base tree: `876a17f277d84dcf06ca672e5cd351edaa294495`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record gives the title `Rokhlin塔` (`Rokhlin tower`), attributes it to Vladimir Rokhlin in
1948, and says only `遍历理论的工具` (`an ergodic-theory tool`). This is a name and use-description,
not a truth-valued proposition. Stage0 leaves the definitions, premises, proof route, equivalent
forms, logical foundation, and formal artifacts open, while rev-5.6 treats its `已验证` label as
untrusted metadata.

The intake correctly freezes this ambiguity. Benjamin Weiss's inspected 1989 survey gives a
serious candidate: for an aperiodic invertible measurable transformation of `[0,1]` preserving
Lebesgue measure, every natural height and positive error admit a measurable base whose forward
levels are pairwise disjoint and cover measure greater than `1 - epsilon`. But that secondary
formulation is not an accepted canonical root. Another inspected source describes instead an
aperiodic nonsingular automorphism of a standard measure space and requires height at least two.
Those variants differ in domain, transformation and measure hypotheses, height boundary, and Lean
encoding. The 1948 note is reported by Weiss to contain no proof of the lemma, while the candidate
1949 survey/1966 translation passage has not been inspected or independently reviewed.

Selecting the familiar Weiss formulation would therefore add unresolved mathematics rather than
transcribe the received target. The same applies to choosing a nonsingular version, an ergodic
special case, a periodic-approximation corollary, literal rather than almost-everywhere disjointness,
or image rather than preimage levels. No canonical claim, ordered binders, exact hypotheses,
conclusion, universe context, or degenerate-case convention is approved. Consequently there is no
legitimate minimal-import target, normalized kernel-expression fingerprint, alternate transport,
or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutation suite.
No theorem declaration, axiom, placeholder, assumed tower structure, weakened special case, or
substituted theorem was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports five pinned mathlib modules and re-elaborates nine adjacent
interfaces: `MeasurePreserving`, its iterate theorem, `QuasiMeasurePreserving`, `Ergodic`,
`Function.periodicPts`, `StandardBorelSpace`, `IsProbabilityMeasure`, `NoAtoms`, and `AEDisjoint`.
This confirms only that useful vocabulary exists. It neither states a Rokhlin lemma nor proves that
the imports are minimal for the unknown target, and it receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`; and the probe SHA-256 is
`87e9b7f3c222c2c7f434cfb792242e144fcdba3fbb305b02f426ef9c5740ad9c`.

The pre-existing untracked `Formalizations/Lean/.lake` link points to the canonical checkout's
pinned artifacts and was used read-only. No `lake update`, `lake build`, dependency clone/fetch, or
other `.lake` mutation was run. This is nonrelease worker evidence.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `LC_ALL=C TZ=UTC python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `LC_ALL=C TZ=UTC python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `LC_ALL=C TZ=UTC python3 scripts/stage1_target.py show THM-M-1410` | 0 | rank 909, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short` | 0 | before this phase, only the pre-existing untracked `Formalizations/Lean/.lake` link was present |
| `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` | 0 | base revision and tree recorded above |
| `LC_ALL=C TZ=UTC rg -n -C 5 'Rokhlin塔\|遍历理论的工具\|THM-M-1410 Rokhlin塔' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | 0 | found only the title/gloss record and Stage0's open fields; no exact proposition or source locator |
| cwd `Formalizations/Lean`: `lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| cwd `Formalizations/Lean`: `lake --version` | 0 | Lake version above |
| cwd `Formalizations/Lean`: `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| cwd `Formalizations/Lean`: `git -C .lake/packages/mathlib status --short` | 0 | empty output; pinned mathlib worktree clean |
| cwd `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1410/IntakeProbe.lean` | 0 | all nine adjacent APIs elaborated; no target proposition was stated |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1410/IntakeProbe.lean Stage1_Instances/THM-M-1410/instance.json Stage1_Instances/THM-M-1410/source-statement-crosswalk.md` | 0 | pinned-input and intake hashes recorded in `statement-blocker.json` |
| `python3 -m json.tool Stage1_Instances/THM-M-1410/statement-blocker.json` | 0 | structured blocker is valid JSON |
| `LC_ALL=C TZ=UTC rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque)[[:space:]]' Stage1_Instances/THM-M-1410 --glob '*.lean'` | 1 | expected no-match exit; target Lean sources contain no prohibited proof construct |
| for each new blocker file, `git diff --no-index --check -- /dev/null PATH` | 1 | expected added-file diff exit with empty diagnostics; no whitespace error |

There is no applicable `lake env lean <canonical-statement>.lean` command. Creating that file now
would manufacture the missing target rather than validate the assigned statement.

## Retry condition and boundary

An accountable reviewer must preserve and hash an immutable primary or authoritative source,
select and transcribe one exact proposition with a pinpoint locator and incorporated definitions,
audit errata and the 1948/1949 boundary, and independently approve the source-statement mapping.
That review must freeze the measure space, atomlessness and normalization assumptions,
transformation representation, preservation or nonsingularity condition, aperiodicity predicate,
height and indexing, base measurability, image/preimage direction, disjointness semantics, coverage
inequality, and every boundary case. A later statement worker can then encode that same claim,
minimize its pinned imports, serialize and hash the elaborated expression, check all credited
transports, and run the four required mutation classes.

This is the first failed statement gate. The root remains `[H5, M4, R4]` as proposed by intake,
with `audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. It
does not complete the statement node or any downstream node, accept a receipt, or alter the
master-owned execution state. Because the assigned phase is not genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted.
