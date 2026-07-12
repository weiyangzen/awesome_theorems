# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `迭代力迫`, attributes it to "many mathematicians",
dates it only to the twentieth century, and gives the statement `力迫的迭代技术` ("the iteration
technique of forcing"). `Docs/Stage0_Blueprint.md` repeats the gloss and leaves exact definitions,
assumptions, equivalent formulations, axioms, and machine artifacts open. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`.

These records identify a subject but provide no proposition, ordered binders, hypotheses,
conclusion, theorem number, page, proof, or formal declaration. They cannot support `H0` or an exact
Lean target.

## Candidate source families

| Source anchor | Relevant family | Intake boundary |
|---|---|---|
| Thomas Jech, *Set Theory*, third millennium edition, revised and expanded, Springer, 2003, chapters on forcing and iterated forcing | finite/countable/transfinite iteration machinery and preservation applications | authoritative discovery locator only; exact theorem/page, assumptions, edition text, and errata are not yet crosswalked |
| Kenneth Kunen, *Set Theory*, College Publications, 2011, forcing/iteration development | standard set-forcing and iteration formulations | candidate reference only; no passage has been accepted as the repository claim |
| Saharon Shelah, *Proper and Improper Forcing*, second edition, Springer, 1998 | countable-support iterations and preservation of properness | specialized preservation family; cannot silently define the general repository target |

## Statement crosswalk

| Repository phrase | Possible component | Lean requirement | Status |
|---|---|---|---|
| "forcing" | a forcing preorder in a ground-model setting | exact forcing/model/name/generic APIs | absent |
| "iteration" | stage family plus successor and limit constructions | index, stage names, restriction maps, and coherence | absent |
| "support" | finite/countable/revised/full/mixed support | exact support predicate and limit condition type | absent |
| "technique" | a construction method rather than a truth-valued claim | one source-selected proposition | absent |
| `已验证` | untrusted inventory label | no proof credit | rejected as evidence |

## Required source decision

The statement phase is blocked until an immutable, independently reviewed passage fixes one exact
claim and crosswalks the iteration length, support, stage hypotheses, ground-model/foundation
setting, boundary cases, and conclusion. The later source audit must record edition, theorem and
page, premise mapping, proof boundary, and errata. The citations above are discovery anchors, not
accepted receipts.
