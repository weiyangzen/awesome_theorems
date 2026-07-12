# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` contains two identical inventory entries. Each gives the Chinese
title `切博塔廖夫密度定理`, attributes it to Nikolai Chebotaryov, dates it 1922, and supplies only
`素理想分解的密度分布` ("density distribution of prime-ideal splitting").
`Docs/Stage0_Blueprint.md` repeats that gloss and explicitly leaves exact definitions, hypotheses,
equivalent formulations, axioms, proof path, and machine artifacts open. The rev-5.6 manifest
retains `已验证` only as `source_status_untrusted`.

Those records do not identify an edition, theorem/page, density convention, or formal artifact.
The 1922 date is preserved as repository metadata but is not accepted as a publication locator.

## Primary-source candidate

A bibliographic candidate for the original proof is N. Tschebotareff, "Die Bestimmung der
Dichtigkeit einer Menge von Primzahlen, welche zu einer gegebenen Substitutionsklasse gehoeren,"
*Mathematische Annalen* **95** (1926), 191-228. Intake does not claim `H0`: an immutable copy has
not been archived or hashed, the exact statement and assumptions have not been transcribed from a
pinpoint passage, errata have not been audited, and no independent source reviewer has approved the
mapping. These are required source-audit tasks rather than facts inferred from the famous name.

## Crosswalk

| Source element | Standard-family interpretation | Exact Lean obligation | Intake status |
|---|---|---|---|
| prime ideals | nonzero primes of the base number field's integers | ring of integers, ideal predicate, norm/enumeration | domain open |
| splitting | decomposition behavior represented by Frobenius | unramified predicate and Frobenius conjugacy class | convention open |
| density | limiting proportion of the selected primes | natural or Dirichlet density expression | definition open |
| prescribed class | a conjugacy class in a finite Galois group | `ConjClasses` or conjugacy-stable set | source wording absent |
| density value | expected class-size/group-size ratio | finite cardinalities coerced to the density codomain | not source-checked |
| `已验证` | untrusted inventory metadata | no proposition or proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded local name
search found no occurrence of `Chebotarev` in `Mathlib`. `IntakeProbe.lean` checks nearby APIs for
number fields, prime ideals lying over a base ideal, relative norm, inertia degree, conjugacy
classes, and conjugacy-class cardinality. These are encoding ingredients only. The probe neither
defines Frobenius classes or prime-ideal density nor locates a theorem candidate; comprehensive
repo-local and external discovery belongs to `S56-M-0019-ANCHOR_AUDIT` after statement freeze.
