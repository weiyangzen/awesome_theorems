# Statement phase blocker

Item: `S56-M-0122-STATEMENT`  
Theorem: `THM-M-0122`  
Date: 2026-07-12

## Result

The exact Lean 4 target cannot be elaborated against the repository's pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` without inventing
mathematical data. The statement node therefore remains blocked and makes no
exact-statement, proof, audit-completion, or theorem-completion claim.

The frozen intake requires a smooth, projective, geometrically connected curve
over a number field, its geometric genus greater than one, and finiteness of
the full rational-point type. Repository-wide searches of the pinned mathlib
source found:

- native `SmoothOfRelativeDimension`, `IsProper`, and
  `GeometricallyIntegral` predicates;
- a construction and properness theorem for particular `Proj` schemes, but no
  general projective-morphism predicate suitable for the quantified curve;
- no geometric-genus or arithmetic-genus invariant for a general smooth proper
  curve;
- no native geometrically-connected scheme predicate in the algebraic-geometry
  tree at this revision.

Consequently the legacy `GeometricGenusSlot := Nat` is not acceptable: it is a
free number unrelated to the curve. Likewise, silently replacing projective by
proper or geometrically connected by geometrically integral would require
checked equivalence implications not present in the pin. Either move would
broaden or substitute the theorem forbidden by the intake scope.

## Checked boundary

`StatementProbe.lean` uses the five narrow imports needed by the available
boundary. It elaborates the number-field, relative-dimension-one smoothness,
properness, geometric-integrality, rational-section, slice-morphism, checked
point-encoding equivalence, and full-type finiteness interfaces. The file
explicitly does not define the canonical Faltings target.

Unblocking requires pinned Lean declarations for a projective curve convention
and a curve-derived geometric-genus invariant, plus checked transports to the
selected connectedness/integrality and rational-point conventions. Fetching a
moving dependency is not valid worker evidence and was not attempted.

## Validation record

Commands were run from the worker repository on 2026-07-12 at base revision
`cf2b907b1d10a3b5c923fc84e10b495a48530690`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0122` | 0 | rank 41, `planned`, `L0`, rework required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0122/StatementProbe.lean` | 0 | the available boundary and rational-point transport elaborated under the pinned toolchain |

The first attempted Lean path used one too many parent traversals and exited 1
with `no such file or directory`; the corrected command above is the actual
elaboration check. No `.lake` update, build, clone, fetch, or write was run.

## Status boundary

- Lifecycle remains `planned` and machine debt remains `M4`.
- No `.stage1-worker-selftest.json` is emitted because the assigned exact
  statement deliverable is not self-tested successfully.
- The dependent anchor-audit node must not treat this probe as an accepted
  statement fingerprint.
