# Source-statement crosswalk

## Repository record

The canonical catalog occurrence at `Docs/researches/math_theorems.md:2041-2046` records:

| Field | Literal value | Intake interpretation |
|---|---|---|
| Title | `柯尔莫哥洛夫零一律` | Selects the Kolmogorov zero-one family, not an expression. |
| Attribution | Andrey Kolmogorov | Historical metadata without a theorem locator. |
| Year | 1933 | Suggests the foundational probability monograph, but is not a statement fingerprint. |
| Gloss | `尾事件的零一性质` | Names tail events and the zero-one conclusion while omitting all definitions and premises. |
| Status | `已验证` | Explicitly untrusted under rev-5.6; grants no H/M/R or proof credit. |

The duplicate source-corpus occurrence at lines 7392-7397 repeats the same six fields. Stage0
deduplicates them as `THM-M-0284` but leaves precise definitions, premises, proof history,
equivalent formulations, axioms, machine status, and artifact links open. All catalog lines trace
to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

## Historical source lead

A. N. Kolmogorov's 1933 *Grundbegriffe der Wahrscheinlichkeitsrechnung* and later English
translation *Foundations of the Theory of Probability* are plausible primary-source families for
the catalog attribution and date. No immutable lawful copy, edition, exact theorem/section/page,
incorporated definition chain, premise/conclusion passage, proof boundary, translation comparison,
correction or erratum, or independent review was admitted during this intake. Network searches for
a stable copy timed out and are not evidence.

This is therefore `H1`, not `H0`. Before source closure, an independently assigned probability
reviewer must select the exact edition and map every definition, assumption, conclusion, proof
node, translation choice, and known correction.

## Source-to-claim nodes

| Claim component | Repository evidence | Pinned Lean candidate | Required statement decision |
|---|---|---|---|
| Independent input | absent | `iIndep s mu` for sub-sigma-algebras | Select sub-sigma-algebras or random variables and check any generated-sigma-algebra transport. |
| Index set | only "tail" | general ordered `iota` with `atTop` | Fix `Nat` or the source order and tail direction. |
| Ambient structure | absent | `forall n, s n <= m0` | Determine the source ambient measurable-space premise and its Lean encoding. |
| Measure model | zero-one language only | ordinary `Measure`, with independence supplying probability behavior | Fix probability/finite/general measure assumptions and rule out an unjustified kernel substitution. |
| Tail sigma-algebra | named only | `Filter.limsup s Filter.atTop` | Map the source intersection of future sigma-algebras to mathlib's limsup encoding by checked equality or iff. |
| Tail event | named only | `MeasurableSet[limsup s atTop] t` | Fix event carrier, ambient measurability, and scoped measurability conventions. |
| Conclusion | "zero-one property" | `mu t = 0 or mu t = 1` | Freeze equality codomain and any equivalent set-membership form. |
| Boundary cases | absent | includes trivial events and general nonempty no-max index orders | Audit zero measure, trivial sigma-algebras, empty carrier, constant variables, and order edge cases. |

## Formal candidate crosswalk

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Probability.Independence.ZeroOne`, explicitly documents and proves
`ProbabilityTheory.measure_zero_or_one_of_measurableSet_limsup_atTop` as Kolmogorov's zero-one law.
The declaration and seven adjacent APIs elaborate in `IntakeProbe.lean`. The source file is
Apache-2.0 and its current proof body is in the local pinned dependency closure.

This is strong `E3` discovery evidence and supports `M3`: a usable exact-topic declaration exists.
It is not yet `M0-W`. The exact source proposition has not been selected; no normalized expression,
environment fingerprint, source-to-Lean transport, mutation suite, terminal-body provenance graph,
transitive dependency or trust audit, wrapper, or accepted receipt has been frozen. The observed
axiom report `[propext, Classical.choice, Quot.sound]` is intake information, not accepted trust
closure.

The pinned `docs/overview.yaml` and `docs/undergrad.yaml` also index the same declaration as the
zero-one law. Those documentation entries confirm discoverability only and add no independent
proof credit.
