# Statement gate blocker

Item: `S56-M-0774-STATEMENT`  
Base revision: `61f7b7dcf859725be90a66069022323d5a8903e2`

## First failed gate

The exact human statement is not identifiable from the repository source record. The only supplied
wording is "existence of a maximal element in a partially ordered set", with the attribution
Kuratowski/Max Zorn and the year 1922. It omits the chain-boundedness premise and does not choose:

- all chains versus nonempty chains;
- implicit nonemptiness via an upper bound for the empty chain versus an explicit nonempty carrier;
- a maximal element of the whole carrier versus a maximal member of a distinguished subset;
- the precise historical Kuratowski formulation versus the later standard Zorn formulation.

The accepted intake explicitly leaves those choices to an inspected primary edition. Selecting
one now would broaden the literal repository wording by adding a premise and would substitute an
unverified modern formulation for an unidentified source statement. Under rev-5.6 sections 0, 2,
and 5, that is a hard statement-identity failure. Consequently no canonical declaration,
elaborated-expression digest, checked transport, mutation suite, or statement receipt is emitted.

## Narrow diagnostic elaboration

`StatementProbe.lean` records three noncanonical propositions so the ambiguity is executable rather
than merely verbal. They respectively express the whole-poset empty-chain form, the explicitly
nonempty/nonempty-chain form, and the subset-relative form. The probe also checks the corresponding
pinned mathlib declarations `zorn_le`, `zorn_le_nonempty`, and `zorn_le₀`. Elaboration establishes
that the local Lean environment can express each candidate; it does not select one or confer proof
or anchor credit.

The direct import `Mathlib.Order.Zorn` is the smallest pinned public module containing all three
diagnostic declarations. The pinned manifest records mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and toolchain `leanprover/lean4:v4.29.0`.

## Commands and results

All commands ran in this worker clone. Lean ran from `Formalizations/Lean` using the existing pinned
Lake environment; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0774/StatementProbe.lean` | 0 | all three candidate propositions and the three pinned declarations elaborated |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0774` | 0 | rank 581, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0774` | 0 | no whitespace errors |

## Retry condition and status boundary

Retry after an immutable primary edition is inspected and recorded with publication, theorem/page,
exact quantified statement, definitions, assumptions, and errata status, followed by independent
approval of its crosswalk to one Lean proposition. Until then the statement node remains blocked,
the root remains at least `M4`, and all downstream nodes remain open. This artifact claims neither
self-tested statement completion nor theorem completion, so `.stage1-worker-selftest.json` is
intentionally absent.
