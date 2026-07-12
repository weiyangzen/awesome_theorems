# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `图灵机`, attributes it to Alan Turing in 1936, and gives
only `图灵机的计算模型` ("the computational model of a Turing machine"). Stage0 repeats that gloss
while marking exact definitions, assumptions, proof process, axioms, and existing formal artifacts
as open. The manifest preserves `已验证` solely as `source_status_untrusted`. None of these records
states a proposition.

Separate repository entries cover the universal Turing machine, recognizable languages, the
halting problem, and equivalence with other computation models. Their proximity cannot supply a
missing statement for this target.

## Historical primary-source locator

Alan M. Turing, "On Computable Numbers, with an Application to the Entscheidungsproblem",
*Proceedings of the London Mathematical Society*, second series 42 (1936-1937), pp. 230-265, is the
historical source candidate. In section 1 (starting at p. 231), Turing introduces automatic
machines, configurations, scanned squares, and machine behavior; later sections develop computable
sequences and numbers. This is a source locator, not an `H0` theorem crosswalk: the repository gloss
does not identify a numbered result or passage whose full claim is the target, and no edition/errata
or assumption review has been accepted.

## Crosswalk

| Repository phrase | Possible mathematical component | Pinned Lean component | Intake status |
|---|---|---|---|
| "machine" | finite control plus symbol-dependent transition | `Turing.TM0.Machine`, `Turing.FinTM2` | APIs probed; intended model open |
| "configuration" | control state and tape/storage contents | `Turing.TM0.Cfg`, `Turing.FinTM2.Cfg` | APIs probed; representation open |
| "computation" | repeated transition from encoded input | `Turing.TM0.step`, `Turing.TM0.eval`, `Turing.FinTM2.step` | APIs probed; behavioral claim absent |
| "model" | operational conventions and effective finiteness | `Turing.TM0.Supports`, fields of `Turing.FinTM2` | candidate ingredients only |
| unstated theorem | simulation, correctness, equivalence, or existence | exact proposition and checked transports | absent from repository source |
| `已验证` | untrusted inventory status | no declaration and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Computability.TuringMachine.PostTuringMachine` defines `TM0` and `TM1`, including machine,
configuration, step, reachability, evaluation, support, and translation interfaces.
`StackTuringMachine` adds `TM2`, and `Computable` supplies a finite bundled `TM2` and predicates for
output and function computation. `IntakeProbe.lean` checks representative declarations from this
surface. These are encoding ingredients and candidate formal anchors only; the later anchor audit
must freeze its queries and inspect any candidate against the exact selected statement.
