# Source-statement crosswalk

## Primary source candidate

Jonathan Pila and Umberto Zannier, "Rational points in periodic analytic sets and the
Manin-Mumford conjecture", *Rendiconti Lincei. Matematica e Applicazioni* 19 (2008), 149-162,
DOI `10.4171/RLM/514`.

The title and bibliographic record directly match Stage0's phrase "Manin-Mumford猜想的证明".
This is an identification anchor, not `H0`: a stable copy still must be inspected for exact theorem
number, wording, assumptions, definitions, and errata. The eponym "Pila-Zannier theorem" is not by
itself a unique statement, so the source theorem controls the later formal target.

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Pila-Zannier theorem" | Pila-Zannier proof/result | exact cited theorem | candidate identified, number open |
| Manin-Mumford conjecture | torsion locus in a subvariety of an abelian variety | abelian variety, closed subvariety, torsion points | included, APIs open |
| torsion coset | torsion translate of an abelian subvariety contained in `X` | subgroup/subvariety and translation predicates | included, encoding open |
| finitely many maximal cosets | finite structural description of the torsion locus | finite family plus coverage/maximality | included, equivalent form open |
| characteristic-zero setting | field and geometric-point hypotheses | field typeclasses and scalar extension | source wording open |

No target-specific Lean artifact was found during intake. Before `H0`, an independent reviewer must
check the primary paper's theorem/page, every hypothesis, definitions, equivalent-form transport,
and errata. Before any machine credit, the exact Lean expression must elaborate and the complete
dependency and axiom closure must be audited at pinned revisions.
