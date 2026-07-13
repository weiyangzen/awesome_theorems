# THM-M-0271 exact-statement gate: blocked

Item: `S56-M-0271-STATEMENT`

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40` (tree
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`). Attempt date: 2026-07-13
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0271-INTAKE` has only provisional
worker state `[_]`: `intake-receipt.json` is unaccepted and non-content-addressed, has no accepted
receipt ID, and binds an older repository revision. There is no master-accepted dependency
receipt. Rev-5.6 section 10.2 permits provisional inspection of a later node, but master closure
remains dependency ordered.

Independently and decisively, the exact-source-statement gate fails. The complete catalog claim is
the name Fubini's theorem, the Guido Fubini / 1907 attribution, and the gloss `重积分与累次积分的关系`
(`the relationship between multiple and iterated integrals`). It supplies no formula, integral
model, region, measure spaces, finiteness assumptions, scalar or vector codomain, ordered binders,
measurability or integrability hypotheses, exact equality, exceptional-section convention, or
boundary cases. `Docs/Stage0_Blueprint.md` explicitly leaves the precise definitions and premises
open.

The intake's historical source lead does not remove those choices. The zbMATH/JFM record for Guido
Fubini's 1907 paper *Sugli integrali multipli*, pages 608-614, preserves a contemporary secondary
review of a planar scalar Lebesgue formulation. The primary Italian theorem, its incorporated
definitions, integration bounds and conventions, complete proof boundary, corrections and errata,
and an independent review have not been admitted. The secondary review therefore supports the
intake's `H1` classification but cannot select a source-exact root.

These omissions change the proposition. In particular, the pinned abstract Bochner theorem over
product measurable spaces with s-finite measures is not definitionally the historical planar
scalar statement. Nor does the catalog decide whether the root is product integral equals one
iterated order, equals both orders, or equality of the two iterated integrals. Choosing
`MeasureTheory.integral_prod`, `integral_prod_symm`, `integral_integral_swap`, or a package of them
would silently narrow, broaden, or substitute the received claim.

The integrated intake consequently leaves the canonical mathematical claim, Lean declaration,
expression fingerprint, and target environment fingerprint null. Rev-5.6 sections 5 and 5.1 make
that ambiguity a hard blocker. There is no honest canonical expression for which minimal imports,
checked transports, or the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. Those mutations are undefined, not passed. The root
vector remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. Its sole direct
import, `Mathlib.MeasureTheory.Integral.Prod`, exposes ten relevant interfaces:
`integrable_prod_iff`, the almost-everywhere section-integrability lemmas, integrability of the
inner-integral functions, the two product-to-iterated formulas, their reversed forms, and the
iterated-order swap theorem. All checks elaborate. The three candidate axiom reports contain only
`propext`, `Classical.choice`, and `Quot.sound`.

This is real pinned feasibility evidence, but the probe declares no canonical target, checked
historical-to-modern transport, mutation, or proof body. Its import is appropriate for the
candidate-family probe; it cannot be certified as the minimal import of an absent canonical
target. A bounded search located this exact-topic mathlib family and no target-owned Fubini
declaration in the searched repo-local Lean roots. This observation is not the downstream anchor
audit and makes no global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symbolic link was used read-only. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0271` | 0 | rank 1278; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| repository catalog, Stage0, intake dossier, source crosswalk, and Fubini source-lead inspection | 0 | confirmed that the gloss does not select one proposition and the primary-source statement and mapping remain unreviewed |
| `sha256sum` over authority, intake, toolchain, probe, and pinned `Prod.lean` inputs | 0 | exact current fingerprints are recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/MeasureTheory/Integral/Prod.lean'` and package status | 0 | pinned revision/tree and source blob recorded in the JSON blocker; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0271/IntakeProbe.lean` | 0 | ten candidate interfaces elaborated; three axiom reports listed the axioms above; stdout SHA-256 `f11c2335158b8a4a5dba42d5601e820a1914f182432a420148704d7e7d31ef83`; no target declaration |
| bounded exact-topic search over repo-local Lean and pinned mathlib | 0 | located the pinned Fubini candidate family and no target-owned source-identical declaration in the searched roots; discovery only |
| `python3 -B Stage1_Instances/THM-M-0271/check_intake.py` | 1 | the historical intake checker expects authoritative intake `[ ]` / attempt 0, while integration now records provisional `[_]` / attempt 1; intake evidence was not rewritten |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration; diagnostic `#print axioms` commands are permitted |
| `python3 -m json.tool Stage1_Instances/THM-M-0271/statement-blocker.json` plus scoped blocker assertions | 0 | JSON parses; identity, open blocked state, null target/imports, unchanged vector, undefined mutations, false completion flags, exact two-file scope, and absent self-test agree |
| scoped `git diff --check` plus no-index checks for both new files | 0 wrapper result | no whitespace, missing-newline, carriage-return, or NUL diagnostic; raw no-index commands returned only the expected new-file status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact statement did not elaborate |

The root packet remains absent by design; a blocker observation is not a self-tested completion.

## Retry Condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash a lawful immutable primary or approved authoritative source and independently
select one exact proposition. They must map every incorporated definition, ordered binder,
hypothesis, conclusion, proof boundary, correction, erratum, translation convention, and boundary
case, including the integral model, planar region or product measures, finiteness, scalar or
codomain convention, product integrability, exceptional sections, and one-order, both-orders, or
order-swap conclusion.

A fresh statement worker may then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`; no debt-vector
change is proposed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
