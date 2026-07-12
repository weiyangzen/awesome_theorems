# Source-statement crosswalk

## Repository evidence

`Docs/Stage0_Blueprint.md` identifies the authors Jonathan Pila and Umberto Zannier, gives 2008,
and says only "special points in o-minimal structures". `Docs/researches/math_theorems.md` repeats
that wording. Neither record supplies a theorem number, domains, hypotheses, or conclusion. The
same repository also contains `THM-M-0465`, with the identical Chinese name but the distinct gloss
"proof of the Manin-Mumford conjecture". That difference is a material ambiguity, not permission
to merge the targets.

## Candidate primary source

Jonathan Pila and Umberto Zannier, "Rational points in periodic analytic sets and the
Manin-Mumford conjecture", *Rendiconti Lincei. Matematica e Applicazioni* 19 (2008), 149-162,
DOI `10.4171/RLM/514`.

The authors, year, and Pila-Zannier method match the metadata, and this is the primary candidate
already identified for `THM-M-0465`. It is only a discovery anchor here. A stable copy has not been
inspected in this intake, and its Manin-Mumford target does not by itself explain why this separate
record says "special points in o-minimal structures". No `H0` credit is assigned.

## Metadata-to-source crosswalk

| Repository component | Candidate interpretation | Required formal component | Intake disposition |
|---|---|---|---|
| "Pila-Zannier theorem" | either the 2008 Manin-Mumford result or the broader Pila-Zannier strategy | one pinpoint source theorem, not an eponym | unresolved |
| "o-minimal structures" | tame definability used for point counting | language/structure, definability, o-minimality, and the exact counting input | ingredient family only |
| "special points" | torsion, CM, Shimura-special, or another unlikely-intersection locus | concrete ambient object and a source-defined specialness predicate | unresolved |
| 2008 | agrees with the candidate Manin-Mumford paper | immutable source edition and theorem/page | candidate identified |
| `已验证` | untrusted Stage0 screening label | none | rejected as evidence |

## Required next crosswalk

Before an exact statement may be claimed, a source reviewer must select and inspect an immutable
primary source; record theorem/page, incorporated definitions, assumptions, equivalent forms, and
errata; explain whether this target duplicates or differs from `THM-M-0465`; and obtain independent
approval. The Lean-side crosswalk must then map every ambient structure, special-point predicate,
height, algebraic part, orbit bound, and conclusion to exact types and declarations, recording
missing APIs rather than replacing them with assumptions.

No target-specific Lean module was located at intake. Nearby Pila-Wilkie and o-minimal artifacts
are discovery surfaces only and cannot establish statement identity or proof closure for this
target.
