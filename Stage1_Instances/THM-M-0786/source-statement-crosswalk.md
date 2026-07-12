# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` identifies "Martin theorem," attributes it to Donald Martin in
1975, and gives only `波雷尔博弈的决定性` ("determinacy of Borel games").
`Docs/Stage0_Blueprint.md` repeats that phrase but leaves definitions, premises, proof route,
dependencies, axioms, and formal artifacts open. The rev-5.6 manifest deliberately records the old
`已验证` label as `source_status_untrusted`.

## Primary source candidate

Donald A. Martin, "Borel Determinacy," *Annals of Mathematics*, Second Series, volume 102,
number 2 (September 1975), pages 363-371, DOI `10.2307/1971035`.

This is a bibliographic discovery anchor, not accepted `H0` evidence. An immutable copy has not
been archived here, and an independent reviewer has not yet verified the exact theorem text,
definitions, page-by-page proof dependencies, foundation assumptions, later corrections, or
errata. The provisional English statement in `instance.json` is therefore not presented as a
verbatim quotation.

## Crosswalk

| Repository/source component | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| Borel game | infinite perfect-information game with a Borel payoff | game record or predicates over alternating finite histories | provisional; exact source definition open |
| natural-number moves | each move is in `omega` | `Nat`; plays represented provisionally by `Nat -> Nat` | carrier probe elaborated; exact encoding open |
| Baire space | `omega^omega` with product topology | topology on `Nat -> Nat` and its Borel measurable structure | pinned API vocabulary probed only |
| Borel payoff | payoff belongs to the Borel sigma algebra | `MeasurableSet A` only after topology/measurable-space equality is checked | vocabulary probed; statement identity open |
| strategy | move selected from a finite position for the correct player | parity-sensitive history function and compatibility predicate | not selected |
| winning strategy | every compatible counterplay produces a winning outcome | universal quantification over opponent strategies or induced plays | not selected |
| determined | one player has a winning strategy | disjunction of the two exact winning predicates | not selected |
| all Borel games | arbitrary Borel rank, not an easier subclass | outer quantification over payoff and Borel witness | included boundary; no Lean target yet |

## Source gate

Before statement acceptance, a source reviewer must inspect a stable edition and pin the theorem's
exact wording and pages, all referenced game/topology definitions, assumptions and conventions,
proof dependencies, and any errata. Each premise must map to an ordered Lean binder or a checked
derived fact. A later anchor audit must independently search pinned mathlib and credible immutable
Lean 4 projects; this intake makes no claim that a formal Borel determinacy theorem exists.
