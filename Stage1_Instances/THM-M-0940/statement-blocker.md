# THM-M-0940 exact-statement gate: blocked

- Item: `S56-M-0940-STATEMENT`
- Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a`
- Base tree: `cc5285432a02107fadffb68c698690d1b98ac5f2`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; statement state remains `[ ]`

## First Failed Gate

The exact-source statement identity and scope freeze required by sections 5 and 5.1 of
`Docs/Stage1_Blueprint_rev-5.6.md` cannot pass. The complete claim-bearing catalog record gives
only the title `加法组合学基本定理` ("fundamental theorem of additive combinatorics"), collective
attribution to many mathematicians in the twentieth century, and the gloss `加法组合的核心结果`
("a core result of additive combinatorics"). It supplies no bibliography, stable theorem
identity, carrier, operation, finite-set or measurable-set representation, ordered binders,
hypotheses, constants, conclusion, proof boundary, correction history, or boundary conventions.
The catalog's `已验证` value is untrusted metadata under rev-5.6. Stage0 explicitly leaves the
formal system, definitions, premises, proof route, alternate forms, axioms, machine status, and
artifacts open.

The wording names a subject umbrella, not one truth-valued proposition. It does not select a
Cauchy-Davenport lower bound, Kneser or Kemperman structure theorem, a Freiman inverse theorem,
Ruzsa covering, a Ruzsa triangle inequality, a Pluennecke-Ruzsa growth inequality, an
additive-energy theorem, or a density/progression theorem. These alternatives have materially
different domains, assumptions, binders, conclusions, constants, and degenerate cases. Several
are separately owned neighboring targets. Choosing one familiar result, or conjoining convenient
pinned declarations, would invent, narrow, broaden, or substitute proposition-changing
mathematics rather than elaborate the exact received target.

Consequently there is no canonical Lean expression for which imports can be minimized, no
serialized expression or canonical-target environment fingerprint, and no credited alternate
encoding. Removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined, not passed. No `Statement.lean`, theorem declaration, axiom, placeholder, desired
property stored in a premise, weakened special case, or broadened interface was added. The intake's
provisional `[H5, M4, R4]` proposal remains unchanged and receives no new acceptance.

The prerequisite `S56-M-0940-INTAKE` is also only provisional `[_]`. Its worker receipt has
`accepted: false`, is not content-addressed, and contains no accepted receipt ID. Section 10.2
permits this dependency-ordered blocker investigation, but statement-node closure remains
dependency ordered. The historical intake checker now stops at its frozen expectation that intake
has authoritative state `[ ]`; the current execution DAG records the integrated provisional state
`[_]`. This statement attempt records that stale replay boundary and does not rewrite intake
evidence or any generated state authority.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). Its seven `#check` commands expose mutually
different Cauchy-Davenport, Freiman-homomorphism, Ruzsa-covering, Ruzsa-triangle, and
Pluennecke-Ruzsa APIs. The probe declares no canonical target, source transport, or proof body.
Its four combined imports are discovery-only and cannot be certified as minimal for an
unidentified target.

A bounded exact-topic search of tracked project Lean and pinned mathlib found no declaration named
for `THM-M-0940` or the generic "fundamental theorem of additive combinatorics" label. A second
bounded query located the distinct adjacent APIs represented by the probe. These are narrow
statement-feasibility observations, not the downstream immutable anchor audit and not a global
absence claim.

The automation-provided `Formalizations/Lean/.lake` link to canonical pinned artifacts was used
read-only. Pinned mathlib remained clean. No `lake update`, `lake build`, dependency clone or fetch,
or other `.lake` mutation was run.

## Validation Evidence

Commands ran in this isolated worker clone on 2026-07-13 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean`; other commands ran from the repository root unless stated otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0940` | 0 | rank 1479; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| source, authority, intake, toolchain, lockfile, and pinned-module SHA-256 checks | 0 | exact current digests are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0940/check_intake.py` | 1 | historical intake checker expected intake state `[ ]`; current authority records provisional `[_]`; no intake artifact was changed |
| `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| pinned mathlib revision, tree, and worktree checks | 0 | revision and tree match the lock; package worktree was clean |
| `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0940/IntakeProbe.lean` | 0 | seven adjacent APIs elaborated; stdout was 1470 bytes with SHA-256 `135604d648557af41647c3c0ff39b1b3c0b567196c00b2eb9222ef1097bb8711`; no target was declared |
| bounded exact-topic search in tracked project Lean and pinned mathlib | 1 | expected no-match result; no declaration for the generic catalog label was located |
| bounded adjacent-API search | 0 | distinct Cauchy-Davenport, Freiman, Ruzsa, and Pluennecke-Ruzsa declarations were located; no source selected one as this target |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| final JSON parse, scoped blocker invariants, and whitespace checks | 0 | identity, null target/imports, four undefined mutations, unchanged debt, false completion flags, exact two-file change scope, final newlines, and absent self-test agreed |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must first revalidate and master-accept refreshed intake evidence. Accountable
reviewers must preserve and hash one lawful immutable primary or approved authoritative source,
select one exact proposition with a pinpoint locator, audit corrections and errata, reconcile its
ownership with the neighboring additive-combinatorics targets, and independently approve the
source-to-statement crosswalk. That decision must freeze the carrier and algebraic structure;
input representation and finiteness assumptions; ordered binders and hypotheses; constants and
exact conclusion; alternate encodings; proof and computation boundaries; and every empty,
singleton, trivial-carrier, torsion, stabilizer, zero-density, zero-denominator, and exponent or
rank boundary case that applies.

A fresh statement worker can then encode precisely that accepted claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
Lifecycle remains `planned`; `audit_complete` and `theorem_complete` remain false. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, audit completion,
theorem completion, or master acceptance is claimed.
