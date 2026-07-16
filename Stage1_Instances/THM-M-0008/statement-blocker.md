# Statement phase blocker

Item: `S56-M-0008-STATEMENT`
Base revision: `1cc6aa61bb055a5c032297ee457905c849af7608`
Checked: 2026-07-17

## First failed gate

The rev-5.6 exact-statement gate fails before a canonical Lean declaration may be frozen. The only
repository source wording is `Tor函子的性质` ("properties of the Tor functor") in
`Docs/researches/math_theorems.md`. It gives no proposition, domains, ordered binders, hypotheses,
conclusion, boundary cases, author, title, theorem number, or page. The accepted intake correctly
classifies this as `blocked_on_primary_source_and_statement_disambiguation`.

At least the following mutually non-equivalent roots fit the wording: projective/flat vanishing,
balancedness of the two derived tensor variables, a Tor long exact sequence, and a degree-zero
identification. Selecting any one without a source selection rule would broaden or substitute the
unknown claim. Consequently there is no truthful elaborated-expression hash, canonical target,
alternate-encoding transport, or removed-hypothesis/domain/scope/boundary mutation suite to record.

## Audited dependency and reuse context

The v2 graph digest is
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b`, and this node's
dependency-context digest is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The authoritative direct-parent, transitive-ancestor, hard-edge, reuse-hint, and shared-group lists
are all empty. Therefore `parent_inspection_order` is empty and was traversed exactly once as the
empty sequence. `dependency-reuse-ledger.json` records that audited closure with empty inspections,
reuse decisions, and unresolved compatibility obligations. No provider acceptance or proof credit
is transferred.

## Narrow Lean check

`Statement.lean` imports only `Mathlib.CategoryTheory.Monoidal.Tor` and checks that
the pinned environment can elaborate one candidate family, higher Tor vanishing against a
projective object in either derivation variable. This is discovery evidence only and is explicitly
not a canonical statement. The checked toolchain is `leanprover/lean4:v4.29.0`; the manifest pins
mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, which matches the reused local
mathlib checkout. The exact current commands and semantic result are bound in
`statement-receipt.json`; command success does not make the positive statement predicate true.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Authority, target set, v2 DAG, phase contract, and execution skill pass before owned inventory changes. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 phase states, two hard edges, five reuse hints, 310 shared groups, acyclic. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required. |
| `python3 scripts/stage1_target.py show THM-M-0008` | 0 | rank 101; lifecycle `planned`; baseline `L0`; `theorem_complete: false`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0008/Statement.lean` | 0 | Elaborated all four pinned Tor vocabulary checks; no theorem or proof declaration exists. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0008/check_statement.py` | 0 | Exactly one typed JSON result reports `status=blocked`, `phase_accepted=false`. |

## Retry condition and boundary

Retry only after the master supplies or accepts a stable primary-source selection with a pinpoint
theorem and enough text to crosswalk every assumption and conclusion. Then elaborate exactly that
claim with pinned imports and run the four required semantic mutation classes.

This artifact does not complete the positive statement predicate, accept a receipt, alter the
execution DAG, or claim audit/theorem completion. The worker handoff self-tests only the
target-owned negative assessment and proposes `[_]` for integration review; raw blocked semantics
cannot become master acceptance.
