# THM-M-0936 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6840-6845` names the Cauchy-Davenport theorem, attributes it to
Augustin Cauchy and Harold Davenport, gives the date 1813, and says only `有限域上子集和的下界`:
"a lower bound for subset sums over a finite field." The record entered at repository source
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:25525-25550`
repeats the gloss and explicitly leaves definitions, premises, proof, equivalent statements,
axioms, machine status, and artifact links open. The manifest's `已验证` field is untrusted under
rev-5.6.

The record identifies a stable named theorem family but not a binder-complete proposition. It does
not identify two sets, prime modulus, nonemptiness, pointwise addition, cardinality, the cap, or
the exact lower-bound formula. Its single date reflects Cauchy's part of a history that also
contains Davenport's later independent proof; it is not a pinpoint source citation.

## Human-source lead

Jeffrey Paul Wheeler, *The Cauchy-Davenport Theorem for Finite Groups*, arXiv `1202.1816v1`
(submitted 8 February 2012), states on page 3 as Theorem 1.4:

```text
If A and B are nonempty subsets of Z/pZ, p prime, then
|A + B| >= min{p, |A| + |B| - 1}.
```

Definition 1.1 on page 2 defines `A + B = {a + b | a in A, b in B}`. The paper says that Cauchy
first proved the theorem in 1813, Davenport independently reproved it in 1935, and Davenport noted
the history in 1947. Its references identify Cauchy, *Recherches sur les nombres*, *J. École
Polytechnique* 9 (1813), 99-116; Davenport, *On the addition of residue classes*, *J. London Math.
Soc.* 10 (1935), 30-32; and Davenport, *A historical note*, volume 22 (1947), 100-101.

The versioned arXiv PDF was inspected and observed with SHA-256
`eb4bbc4d75ffab654b43a49495b6a24124da446edd16ff8771603b46b244f4fb`. It is a credible modern
source lead and an explicit component map, but it is not the catalog's cited primary source. The
original works, definition chain, exact historical proof boundary, corrections or errata, and an
independent source review have not been admitted. Consequently this intake remains `H1`, not `H0`.

## Candidate source-to-statement map

| Component | Repository gloss | Wheeler Theorem 1.4 | Pinned Lean candidate | Intake status |
|---|---|---|---|---|
| Modulus/domain | finite field | prime `p`, `Z/pZ` | `{p : Nat}`, `hp : p.Prime`, `ZMod p` | prime-field interpretation open |
| Inputs | "subsets" / ambiguous subset sums | nonempty subsets `A`, `B` | `{s t : Finset (ZMod p)}`, `hs`, `ht` | two-set and Finset choices open |
| Sum operation | unstated | `A + B = {a+b}` | pointwise Finset `s + t` | notation/encoding transport open |
| Measurement | lower bound only | finite cardinality | `#s`, `#t`, `#(s + t)` in `Nat` | exact cardinal encoding open |
| Cap | unstated | `min p` | `min p` | source adoption open |
| Growth term | unstated | `|A| + |B| - 1` | `#s + #t - 1` with Nat subtraction | boundary/mutation checks open |
| Conclusion | lower bound | `|A+B| >= ...` | `min p (...) <= #(s+t)` | orientation agrees as a candidate |

Every component after the repository-gloss column adds proposition-changing information. It must
be adopted from an approved source and connected by checked transports before exact statement
identity can pass.

## Pinned Lean candidates

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains module
`Mathlib.Combinatorics.Additive.CauchyDavenport`. The closest conventional candidate is:

```lean
ZMod.cauchy_davenport
  {p : Nat} (hp : p.Prime)
  {s t : Finset (ZMod p)}
  (hs : s.Nonempty) (ht : t.Nonempty) :
  min p (#s + #t - 1) <= #(s + t)
```

The same module exposes `cauchy_davenport_minOrder_add`, a stronger general group interface whose
cap is the minimum order of a nontrivial element. That interface may explain a valid finite-field
generalization by characteristic, but it must not silently replace the source-selected root.

`IntakeProbe.lean` successfully checks both names and prints their reported axioms. The candidate
is not canonical at intake: minimal imports, normalized expression identity, environment
fingerprint, checked source transport, mutation tests, terminal proof-body provenance, transitive
dependencies, trust closure, and proof credit remain open.

## Evidence and debt boundary

- `H1`: the named classical family and a versioned modern theorem/definition/history lead are
  known; primary-source admission, exact premise/proof/errata mapping, catalog-to-source adoption,
  and independent review are open.
- `M3`: an exact-topic pinned Lean interface elaborates, but no canonical target, checked transport,
  terminal-body audit, or accepted kernel evidence is frozen.
- `R4`: there is no complete source-faithful, node-anchored, independently reviewed reconstruction.

The arXiv source, theorem name, mathlib documentation, and successful API probe are discovery
evidence only. They establish neither `H0` nor `M0`, audit completion, or theorem completion.
