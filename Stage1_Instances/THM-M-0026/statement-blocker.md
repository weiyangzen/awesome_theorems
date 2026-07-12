# Exact-statement gate: blocked

Item: `S56-M-0026-STATEMENT`

Theorem: `THM-M-0026`

Base revision: `936bf2b9e968abd3b79b5b36d32f2f2bff648c7e` (tree
`8c9d3261b0ba9a81deb5bfc19a335a02cb80f962`).

## Decision

The statement item remains `[ ]`. The repository identifies Hilbert's Nullstellensatz only by the
gloss "correspondence between maximal ideals of a polynomial ring over an algebraically closed
field and points of the algebraic set." It does not provide a binder-complete proposition or cite
one exact source proposition. In particular, it does not fix:

- the finite variable presentation or the empty-variable case;
- whether the coefficient field and field of points are identical;
- whether a point is an affine tuple, a zero-locus member, or a maximal-spectrum point;
- whether the conclusion is existence, an `Iff`, a bundled bijection, or the strong radical
  identity; or
- the equality encoding, uniqueness convention, and top/bottom, empty-zero-locus, and zero-ring
  boundaries.

These choices change the proposition. Selecting the closest pinned mathlib declaration from
mathematical familiarity would therefore substitute an encoding for the missing source-selected
claim. Rev-5.6 section 5 makes ambiguity and a missing elaborated-expression fingerprint hard
blockers. No canonical expression exists for which minimal imports, checked transports, or the
four required statement mutations can be certified. The first failed gate is exact source
statement identity and its definition chain. The root vector remains `[H1, M3, R4]`.

The prerequisite intake is recorded as provisional `[_]`; its receipt is expressly unaccepted and
content-unaddressed. Rev-5.6 permits this dependency-ordered attempt, but master acceptance would
still be required after any future statement self-test.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` re-elaborates with the sole direct import
`Mathlib.RingTheory.Nullstellensatz`. In the pinned environment it exposes three different nearby
results:

1. `MvPolynomial.eq_vanishingIdeal_singleton_of_isMaximal`, a weak direction whose coefficient and
   point fields may differ;
2. `MvPolynomial.isMaximal_iff_eq_vanishingIdeal_singleton`, a same-field finite-index `Iff`; and
3. `MvPolynomial.vanishingIdeal_zeroLocus_eq_radical`, the strong Nullstellensatz.

The second is closest to the catalog gloss, but proximity is not exact statement identity. The
probe declares no target theorem or proof body, and its import cannot be certified minimal for an
absent canonical target. A bounded local search found these declarations only in pinned mathlib's
Nullstellensatz module and no repo-local target wrapper. This is discovery evidence, not the later
anchor audit or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No `lake update`, `lake build`, clone,
fetch, or other dependency mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0026` | 0 | rank 1071; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | before edits, only the automation `.lake` link was untracked; base revision/tree are recorded above |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| pinned mathlib `git rev-parse HEAD 'HEAD^{tree}'` and `git status --short` | 0 | revision/tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0026/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout SHA-256 `f6f297b818be88c4cccbb38d7c2e981ef3b0698056a48e10837902abf2367ecf` |
| bounded `rg` search for the exact topic in repo-local Lean and pinned `Nullstellensatz.lean` | 0 | no repo-local wrapper; the three neighboring declarations above were found in the pinned module |
| `python3 -B Stage1_Instances/THM-M-0026/check_intake.py` before these artifacts | 1 | historical intake evidence is stale against the current regenerated blueprint/DAG hashes; it is not rewritten by this statement run |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0026/statement-blocker.json` | 0 | blocker parsed as valid JSON |
| `jq -e '<identity/null-target/H1-M3-R4/mutation/completion invariants>' Stage1_Instances/THM-M-0026/statement-blocker.json` | 0 | identity, null target/imports, unchanged H1/M3/R4, undefined mutations, false completion flags, and no self-test claim agree; the full filter is recorded in the JSON command ledger |
| `git diff --check -- Stage1_Instances/THM-M-0026` | 0 | no tracked whitespace diagnostics |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0026/statement-blocker.json` and the same command for `statement-blocker.md` | 1 each | empty diagnostic output; exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the statement gate did not pass |

## Retry Condition And Status Boundary

An accountable source reviewer must preserve and hash an immutable primary or authoritative source,
select one exact proposition, transcribe all incorporated definitions, ordered binders, hypotheses,
conclusion, proof boundary, corrections, and boundary cases, and independently approve its identity
with `THM-M-0026`. A later statement run can then encode that same claim, minimize its pinned
imports, serialize the elaborated expression and environment, compile every credited transport,
and run removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations.

This blocker is the assigned phase's truthful result, not completion. Lifecycle remains `planned`;
`audit_complete: false` and `theorem_complete: false`. No exact statement, minimal-import claim,
statement fingerprint, checked transport, mutation certificate, proof credit, node receipt, worker
`[_]`, master acceptance, or debt-vector change is claimed. Because the assigned deliverable did
not self-test, `.stage1-worker-selftest.json` remains absent.
