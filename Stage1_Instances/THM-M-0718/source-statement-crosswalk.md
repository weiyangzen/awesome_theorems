# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `通用图灵机`, attributes it to Alan Turing in 1936, and
states only `通用计算模型` ("universal computation model"). Stage0 repeats that metadata. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`. None supplies a quantified
claim, machine definition, encoding, simulation criterion, proof source, edition, section, page,
assumption list, or errata record.

The computer-science inventory independently contains `THM-C-0003` with the gloss "there exists a
universal Turing machine that can simulate any other Turing machine". This is useful discovery
evidence for a likely reading, but it is a separate target and secondary metadata. It cannot safely
determine the exact statement or transfer proof credit to `THM-M-0718`.

## Historical source boundary

The attribution points to Alan M. Turing, *On Computable Numbers, with an Application to the
Entscheidungsproblem* (received 1936; Proceedings of the London Mathematical Society, series 2,
volume 42) as a primary-source search target. Intake has not accepted an immutable scan, exact
section/page, machine convention, correction, or errata audit. The source phase must locate and
independently review the passage that constructs the universal machine, then map every encoding and
simulation premise. Until that work is done, the historical certainty of the usual theorem
supports at most `H1`, not `H0`.

## Crosswalk

| Repository phrase | Required mathematical component | Pinned Lean candidate | Intake status |
|---|---|---|---|
| "computation model" | program and machine semantics | `Nat.Partrec.Code`, `Turing.TM2.step` | API probed; model choice open |
| "universal" | one interpreter consuming encoded programs | `Turing.PartrecToTM2.tr`, `init` | strong candidate; identity unproved |
| "simulate" (separate inventory clue) | preservation of partial outputs or execution | `Turing.PartrecToTM2.tr_eval` | exact evaluation theorem probed; crosswalk open |
| "Turing machine" | finite/effectively finite control | `Turing.PartrecToTM2.tr_supports` | candidate finiteness witness probed |
| divergence | equality in partial computation semantics | `Part` equality in `tr_eval` | candidate only |
| `已验证` | untrusted inventory label | no proposition or proof object | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe imports
`Mathlib.Computability.TuringMachine.ToPartrec`. The declaration `tr_eval` states that evaluation of
the TM2 transition function `tr` from `init c v` equals the encoded halt configuration mapped over
`Nat.Partrec.Code.eval c v`; `tr_supports` supplies finite reachable label support for each code and
continuation. These are substantive formal artifacts and motivate `M3`, but intake does not claim
that this program-dependent support formulation is the exact classical one-machine theorem.
