# Source-statement crosswalk

## Located repository source

`Docs/researches/math_theorems.md` names Axel Harnack, gives the year 1887, and summarizes the claim
as `正调和函数的比较` (comparison of positive harmonic functions). `Docs/Stage0_Blueprint.md`
repeats that summary but explicitly leaves definitions, hypotheses, proof, axioms, and machine
artifact open. The metadata label `已验证` is not primary-source evidence.

## Selected exact modern source

Sheldon Axler, Paul Bourdon, and Wade Ramey, *Harmonic Function Theory*, second edition,
Theorem 3.6, numbered page 48, states: if `Omega` is connected and `K` is a compact subset of
`Omega`, then some `C in (1, infinity)` satisfies `1/C <= u(y)/u(x) <= C` for all `x,y in K` and
all positive harmonic `u` on `Omega`. The following note says that `C` may depend on `Omega` and
`K` but is independent of `x`, `y`, and `u`. The authors' PDF downloaded from
`https://www.axler.net/HFT.pdf` had SHA-256
`4e64124f7e36993ee784e575a024505f99d484ccf959d2d3864eae9232af8bf1` on 2026-07-12.

The book's standing convention treats a domain as open, so `IsOpen Omega` is explicit in Lean.
Its `R^n` is encoded as `EuclideanSpace Real (Fin n)`, positive means pointwise strict positivity,
and mathlib's `InnerProductSpace.HarmonicOnNhd` supplies the classical harmonicity predicate.

## Historical-source work still requiring inspection

- Axel Harnack's 1887 work on logarithmic potential theory is the historical-source lead supplied
  by the repository metadata. Exact title, edition, theorem/page, wording, and errata have not been
  verified and must not be inferred from the name.
The modern theorem selects the formal target but does not establish the exact 1887 genealogy or
H0. An independent reviewer must still audit the historical source, the modern edition and errata,
and every source-to-Lean mapping below.

## Crosswalk

| Repository phrase | Mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| positive harmonic functions | real-valued `u`, harmonic and strictly positive on `Omega` | `u : Space n -> Real`; `HarmonicOnNhd u Omega`; `forall z in Omega, 0 < u z` | frozen and elaborated |
| comparison | `1/C <= u(y)/u(x) <= C` for all `x,y in K` | nested universal binders and real division | frozen and elaborated |
| domain | connected open subset of Euclidean space | `IsOpen Omega`; `IsConnected Omega` | frozen and elaborated |
| compact interior set | compact `K` contained in `Omega` | `IsCompact K`; `K ⊆ Omega` | frozen and elaborated |
| constant | `C > 1`, dependent only on `Omega,K` | `exists C, 1 < C` outside binders for `u,x,y` | frozen and elaborated |

Before `H0`, an independent reviewer must verify the edition, theorem/page, definitions, all
hypotheses, constant dependencies, dimensional edge cases, and errata, and approve this mapping.
Those source debts do not prevent the selected exact Lean proposition from elaborating.
