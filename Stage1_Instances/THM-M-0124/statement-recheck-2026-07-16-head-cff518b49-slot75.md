# THM-M-0124 statement recheck: blocked

Item: `S56-M-0124-STATEMENT`

Base revision: `cff518b49c10dc043854d984bb38a0748aa4f3a0` (tree
`751ce4527826593f7fccac18160af616cf18b8cf`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 75.

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

The predecessor intake is only provisional `[_]`, not master-accepted `[x]`. Since the preceding
same-slot recheck, the target manifest, catalog, Stage0 and legacy Stage1 records, execution skill,
guidelines, intake dossier, legacy Lean module, toolchain, and dependency lock remain unchanged.
The prior recheck is now integrated; blueprint and execution-DAG changes concern only unrelated
`THM-M-0122`. Normalized `THM-M-0124` authority records are unchanged.

The pinned Lean surface supplies congruence subgroups, cusps, cusp orbits, and finiteness of those
orbits, but the bounded local search found no associated compactified modular curve, curve Jacobian
or degree-zero Picard group, cuspidal divisor-class construction, Abel-Jacobi map, or exact
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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0124` | 0 | rank 43; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base identity matches this record |
| scoped authority/source/intake/legacy inspection and prior-to-current diff | 0 | failed exact-statement gate unchanged; only unrelated `THM-M-0122` scheduler state changed |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0124/StatementProbe.lean` | 0 | four lines, 310 bytes, SHA-256 `2d31e6...93547`; empty stderr; cusp substrate only |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_043.lean` | 0 | 17 lines, 1,296 bytes, SHA-256 `0f9cf6...fe11`; empty stderr; abstract discovery surface only |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` | 1 per tree, expected no match | zero output; no exact target or required concrete construction found |
| JSON parsing, scoped invariants, prohibited-construct scan, and whitespace checks | expected exits passed | blocked fields, two-file scope, absent self-test, no prohibited construct, and clean whitespace agree |
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
