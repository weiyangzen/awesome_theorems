# THM-M-0124 statement recheck: blocked

Item: `S56-M-0124-STATEMENT`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff` (tree
`24acf86e69ab2e6fca9480c6269b6429874ba295`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 72.

## Decision

The exact-statement gate remains blocked. The repository catalog names the Manin-Drinfeld theorem
but describes only unspecified properties of Heegner points on elliptic curves. That is a different
topic, not a proposition that can be normalized into this theorem.

The intake instead selects the standard theorem family: a degree-zero divisor supported on the
cusps of a congruence modular curve has torsion class in its Jacobian, with pairwise cusp
differences as an intended generator form. That selection is expressly prose-frozen, not an
accepted canonical source or Lean statement. The cited papers still lack an accepted theorem/page
transcription, exact hypotheses and generality, incorporated definitions, translation and errata
review, and independent source review. The arithmetic base, geometric-versus-rational cusp and
divisor conventions, Jacobian versus `Pic^0`, ordered binders, boundary cases, and checked
equivalence between the pairwise and all-degree-zero-divisor forms remain open. Choosing them here
would invent proposition-changing mathematics.

The intake crosswalk's Drinfeld DOI `10.1007/BF01078845` is inconsistent with the article metadata.
`10.1007/BF01078890` remains a correction candidate requiring accountable correction and
independent review, not accepted source authority in this statement-phase record.

The predecessor intake is only provisional `[_]`, not master-accepted `[x]`. Since the prior
recheck, the target manifest, catalog, Stage0 and legacy Stage1 records, intake dossier, legacy Lean
module, toolchain, and dependency lock remain unchanged. The prior target recheck is integrated.
The v2 orchestration overlay is new relevant authority, but normalized `THM-M-0124` rev-5.6 phase
records are unchanged.

The pinned Lean surface supplies congruence subgroups, cusps, cusp orbits, and finiteness of those
orbits, but a fresh bounded local search found no associated compactified modular curve, curve
Jacobian or degree-zero Picard group, cuspidal divisor-class construction, Abel-Jacobi map, or exact
Manin-Drinfeld declaration. Mathlib's Picard group and elliptic-curve Jacobian-coordinate APIs are
not the required geometric object model.

The historical `AwesomeTheorems.Stage1.S1_M_043.StatementShape` cannot fill the gap. Its caller
supplies an abstract curve-point type, additive target, cusp inclusion, and arbitrary divisor-class
map, thereby assuming away the missing geometry. Fresh elaboration succeeds, but the module labels
itself `statementShapeOnly` and explicitly forbids a theorem-completion claim.

Consequently there is no truthful canonical Lean expression, minimal canonical import set,
expression hash, environment fingerprint, checked alternate-form transport, or meaningful suite
for removed hypotheses, changed domains, changed binder scope, and boundary cases. The first failed
gate remains `exact_source_statement_and_concrete_formal_object_model`. Lifecycle stays `planned`,
root debt stays `H1 / M4 / R4`, and the statement node stays `[ ]`. No receipt, proof, debt change,
audit completion, theorem completion, or master acceptance is claimed.

## Dependency Context

`dependency-reuse-ledger.json` records the required v2 audit under schema
`stage1-dependency-reuse-ledger/1.1`. It binds graph SHA-256
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`, target context
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`, and this base revision.
The authoritative node has no direct hard parents, transitive ancestors, incoming hard edges, reuse
hints, or shared groups, so `inspections`, `reuse_decisions`, and unresolved compatibility
obligations are truthfully empty. The scheduler's ledger validator accepts this exact empty closure.
It conveys no proof credit.

## Pinned Lean Boundary

`StatementProbe.lean`, with the sole direct import
`Mathlib.NumberTheory.ModularForms.Cusps`, elaborated successfully. It emitted four API types, 310
bytes, at SHA-256 `2d31e6ab6b2dd3018738af639c7e84a7dcea236e34a0dbe4fca31b6bffa93547`;
stderr was empty. This validates adjacent substrate, not the canonical theorem. The import is
minimal only for the probe; target-import minimality is undefined without a canonical target.

The legacy discovery module also elaborated successfully, with 17 stdout lines, 1,296 bytes, and
SHA-256 `0f9cf61b87219c06e8e2f14479e2ad675a4f097e0447d7a3bf8434833c01fe11`;
stderr was empty. It receives discovery credit only.

Replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both dependency worktrees were clean. The
automation-provided canonical `.lake` symlink was reused read-only. No update, build, clone, fetch,
or dependency mutation was performed.

## Validation Record

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, v2 theorem DAG, and skill presence passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10,822 legacy states preserved, 2 hard edges, 5 reuse hints, 310 shared groups, acyclic |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0124` | 0 | rank 43; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base identity matches this record |
| scoped authority/source/intake/legacy inspection and prior-to-current diff | 0 | exact-statement blocker unchanged; v2 overlay added; normalized target rev-5.6 records unchanged |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s lake env lean ../../Stage1_Instances/THM-M-0124/StatementProbe.lean` | 0 | four lines, 310 bytes, SHA-256 `2d31e6...93547`; empty stderr; cusp substrate only |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300s lake env lean AwesomeTheorems/Stage1/S1_M_043.lean` | 0 | 17 lines, 1,296 bytes, SHA-256 `0f9cf6...fe11`; empty stderr; abstract discovery surface only |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` | 1, expected no match | zero output, SHA-256 `e3b0c4...b855`; no exact target or required concrete construction found |
| scheduler `validate_dependency_reuse_ledger` on the target-owned ledger | 0 | schema, graph/context/base binding, and exact empty closure passed |
| JSON parsing, scoped invariants, prohibited-construct scan, and whitespace checks | expected exits passed | blocked fields, three-file scope, absent self-test, no prohibited construct, and clean whitespace agree |
| post-write dependency revision/status checks | 0 | mathlib and `flt-regular` remain clean at the recorded revisions |

## Retry Condition And Boundary

Retry after intake master acceptance and accountable reviewers preserve and approve one exact
primary or approved-authoritative statement with stable theorem/page locators, incorporated
definitions, assumptions, corrections, errata disposition, and independent review. Correct and
review the Drinfeld locator. Fix subgroup generality, base, cusp/divisor conventions, Jacobian or
`Pic^0` target, binders, assumptions, boundary cases, and all alternate forms. Concrete pinned Lean
constructions for the associated compactified modular curve, its Jacobian or degree-zero Picard
group, and cuspidal divisor-class map must then exist or be supplied. A later worker can encode only
that reviewed proposition, minimize imports, fingerprint the expression and environment, compile
all transports, and execute all four mutation classes.

This is a current-HEAD blocker handoff, not statement completion. Because the positive deliverable
did not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker `[_]` or master
acceptance is requested.
