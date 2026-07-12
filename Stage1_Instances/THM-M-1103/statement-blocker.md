# Statement gate: blocked

Item: `S56-M-1103-STATEMENT`

Base revision: `3ba2d9fd086e5b49bf2ca5268e302f89ef4a2b03`.

## First failed gate

The rev-5.6 exact-statement gate fails before Lean elaboration. The complete repository claim for
this target is the Chinese phrase `HMC算法` ("HMC algorithm") in
`Docs/researches/math_theorems.md`, repeated in `Docs/Stage0_Blueprint.md`. It contains no domains,
ordered binders, hypotheses, or conclusion and is not a proposition. The manifest adds only the
English topic name "Hamiltonian Monte Carlo" and untrusted metadata; it supplies no mathematical
statement.

Consequently there is no source-determined canonical `Prop` to put in a Lean file, no principled
minimal import set, and no expression whose elaborated kernel form can be hashed. Choosing any of
the following would broaden or substitute the target:

- preservation of a canonical phase-space measure by an exact Hamiltonian flow;
- detailed balance or stationarity of a Metropolized HMC transition kernel;
- correctness properties of leapfrog integration;
- irreducibility, ergodicity, or a convergence rate for an HMC chain.

These candidates have materially different definitions, assumptions, boundary cases, and
conclusions. A vacuous wrapper around an abstract assumption of invariance would also assume the
claimed result rather than encode HMC correctness. No `.lean` target was created, and no
elaboration, mutation-test, proof, audit-completion, or theorem-completion claim is made.

## Retry condition

An accountable source reviewer must identify and inspect a stable edition of a primary source,
select one exact numbered or pinpointed proposition, and record its complete definitions,
assumptions, conclusion, page range, and errata status. The statement phase can then freeze its
domains, quantifiers, degenerate cases, foundation/TCB/computation profiles, translate it without
strengthening or weakening, and run the required Lean elaboration and four mutation classes.

Until that happens, the truthful machine classification remains `M4` and
`S56-M-1103-STATEMENT` remains blocked. The intake dependency is present but does not cure the
source ambiguity already recorded in the dossier.

## Narrow validation evidence

All commands ran from the repository root unless the command contains an explicit `cd`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard reports 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1103` | exit 0; rank 543, planned, `theorem_complete: false` |
| `rg -n -C 8 'Hamiltonian Monte Carlo\|HMC算法\|HMC algorithm\|Radford Neal' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md README.md Formalizations Stage1` | exit 2 because some optional search roots do not exist; matches in the two authoritative repository source files confirm only the topic phrase and open fields |
| `rg -n -C 8 'Hamiltonian Monte Carlo\|HMC算法\|HMC algorithm\|Radford Neal' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md` | exit 0; the scoped rerun confirms only the topic phrase, author/year metadata, and open statement fields |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-1103` | exit 0; no whitespace errors after this record was added |

The available Lean toolchain does not resolve the preceding mathematical ambiguity. Running Lean
on an invented proposition would be a successful check of a substituted target, not valid evidence
for this item. Because the assigned phase is not self-tested, no `.stage1-worker-selftest.json` is
emitted.
