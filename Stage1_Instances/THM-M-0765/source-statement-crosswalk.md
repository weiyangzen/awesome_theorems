# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:5633-5638` supplies exactly the title
`图灵机可识别语言`, attribution Alan Turing, year 1936, gloss `递归可枚举语言`, importance
`高`, and status `已验证`. All six uncited catalog lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, definition,
bibliographic work, edition, theorem or page, assumptions, proof, correction history, or formal
artifact.

`Docs/Stage0_Blueprint.md:20893-20918` repeats those fields while explicitly leaving the formal
system, precise definitions and premises, proof process, dependencies, equivalent forms, axioms,
machine status, and artifact links open. Its generic statement that a closed result is known is
planning metadata, not source evidence. Rev-5.6 therefore retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The computer-science inventory at `Docs/researches/cs_theorems.md:265` separately lists
`递归可枚举语言性质`, glossed as closure and undecidability properties of r.e. languages. That
record is a neighboring discovery lead, not an exact statement for this target and not a source
of transferred proof credit.

## Literal crosswalk

| Repository element | Mathematical component to identify | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `语言` (language) | alphabet, finite words, extensional membership | an alphabet type, `List`/encoding, and `Set` or predicate | absent |
| `图灵机` | exact effective machine model and valid program encoding | `Turing.TM0`, `TM1`, `TM2`, or a checked equivalent | source does not select one |
| `可识别` (recognizable) | acceptance, halting, rejection, and off-language behavior | reachability or partial-evaluation domain | semantics open |
| `递归可枚举` | domain, range, enumerator, or semidecision definition | `REPred`, `Partrec`, or a checked enumerator relation | one pinned definition exists; identity open |
| juxtaposition of the two phrases | definition, equality, implication, or characterization | exact ordered proposition and checked transports | no conclusion is stated |
| Alan Turing, 1936 | historical discovery key | immutable source locator and node mapping | catalog metadata only |
| `已验证` | untrusted inventory status | accepted source and kernel receipts would be required | no H or M credit |

## Human-source boundary

Alan M. Turing's 1936 work is an obvious historical discovery direction, but the catalog cites no
work or passage. This intake does not invent a title, theorem number, page, modern translation, or
claim that Turing stated the catalog's modern language-class equivalence verbatim. A source audit
must preserve a lawful immutable edition, locate the intended proposition and all incorporated
definitions, map its machine and enumerability conventions, audit corrections and errata, and
obtain independent review. Until then the received wording remains `H5`, not `H0` or `H1`.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.Halting` defines `REPred p` using the domain of a partial-recursive
computation and provides `Partrec.dom_re` and `ComputablePred.to_re`. Module
`Mathlib.Computability.PartrecCode` exposes partial-recursive codes, `Code.eval`, and
`Code.exists_code`. Module `Mathlib.Computability.TuringMachine.ToPartrec` constructs a `TM2`
machine for a partial-recursive code and proves `PartrecToTM2.tr_eval` and finite-support theorem
`tr_supports`.

These are substantive adjacent formal components. They do not, at intake, identify the catalog's
alphabet, word encoding, recognizer semantics, recursive-enumerability definition, quantifier
order, or desired direction. A bounded search found no declaration explicitly named as a
Turing-recognizable-language equivalence. That observation is not an exhaustive downstream anchor
audit and does not establish absence outside the searched pinned sources.

Before statement credit, reviewers must select the exact source proposition, elaborate and hash
the canonical Lean expression with minimal imports, and check every credited conversion. Before
machine credit, the anchor and proof phases must audit both directions required by that selected
root, terminal proof-body provenance, axioms, dependencies, trust, and composition.
