# THM-M-0330 proof-phase blocker

Item: `S56-M-0330-PROOF`  
Attempt date: 2026-07-12  
Base revision: `230f719da7724afb27c761dcb8c62a327557fe63`

## Result

The proof phase is blocked and is not self-tested as complete. No
`.stage1-worker-selftest.json` is emitted. The exact frozen root remains
`H3/M4/R4`; neither `ForwardPackage` nor `ConversePackage` has an inhabitant.
The minimal open root cut therefore remains:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

The forward package requires formal proofs that the strong right-derivative
generator is densely defined and closed, followed by a Bochner/Laplace
resolvent construction, both inverse identities, and the `1/a` norm bound.
The converse package requires bounded Yosida approximants, their exponential
semigroups, uniform contraction estimates, strong convergence to a C0
semigroup, and equality of its generator graph with `A`. These analytic
results are not present in the pinned mathlib source.

The bounded anchor audit found only `mrdouglasny/hille-yosida` at immutable
commit `680e9499ee866763e737c8d888c1248684ced667`. Its inspected declarations cover
only part of the forward resolvent construction. They do not prove generator
density or closedness, the left inverse on the whole domain, or any converse
generation theorem. The project is not in the pinned Lake dependency closure,
and the worker rules prohibit fetching it or otherwise mutating `.lake`.
Consequently there is no exact terminal body available to pin or import.

`ObligationTree.lean` proves only the conditional composition of the two open
direction packages. Its axiom report is for that composition theorem and does
not constitute an inhabitant of either premise. Introducing constants for the
packages, weakening the equivalence, or replacing the analytic predicates by
abstract fields would be an axiom or a substituted theorem and was rejected.

## Commands and exact results

All commands ran in this worker clone using existing pinned artifacts. No Lake
update, build, dependency clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups and `1546` uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets with ranks `1..1546` pass |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | rank `823`, lifecycle `planned`, `theorem_complete: false` |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 0 | expression SHA-256 `5696285042abd39e340c7e72b2c2855d17e2e335106b1aa6a724056fd68bd75e`; all three mutations killed |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | anchor-audit invariants pass; exact root has no proof anchor |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | `19` obligations and `40` typed edges pass; root and both packages remain `M4` |
| `rg -n -i 'Hille.?Yosida\|HilleYosida\|Yosida\|strongly continuous semigroup\|C.?0 semigroup\|infinitesimal generator' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching terminal Hille-Yosida theorem in pinned mathlib source |

The narrow Lean elaboration check was:

```bash
cd Stage1_Instances/THM-M-0330
LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd ../../Formalizations/Lean && lake env which lean) \
    -o /tmp/THM-M-0330-Statement.olean Statement.lean
cp /tmp/THM-M-0330-Statement.olean /tmp/Statement.olean
LEAN_PATH=/tmp:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) \
  $(cd ../../Formalizations/Lean && lake env which lean) ObligationTree.lean
rm -f /tmp/THM-M-0330-Statement.olean /tmp/Statement.olean
```

It exited `0`, elaborated the exact statement and conditional composition, and
reported that `root_of_direction_packages` uses only `propext`,
`Classical.choice`, and `Quot.sound`. It supplies no kernel evidence for the
two open direction packages.

## First failed gate

`M0330-L-FWD-DENSE` is the first unresolved forward leaf, and
`M0330-C-YOSIDA` is the first unresolved converse construction. No repo-local
or pinned exact proof body exists for either. Proof-phase completion and a
worker `[_]` receipt would therefore be false.
