# External FLT candidate and source ledger

Audit date: `2026-07-10` (`Asia/Shanghai`). This ledger records search evidence
and reproducibility boundaries. It is not a dependency manifest and does not
claim that any candidate proves FLT in this repository.

## ImperialCollegeLondon/FLT

| field | audited value |
|---|---|
| repository | `ImperialCollegeLondon/FLT` |
| immutable revision | `44df7744a2a65cdc111875dc1b6f0db85477348f` |
| commit time | `2026-07-10T08:28:49Z` |
| toolchain | Lean `4.32.0-rc1` |
| mathlib pin | `8bba4200986270d3b30be2bb2f8840af47a7854f` |
| checkdecls pin | `3d425859e73fcfbef85b9638c2a91708ef4a22d4` |
| repository toolchain here | Lean `4.29.0`, mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| compatibility | different Lean and mathlib revisions; not in the local dependency closure |

### Terminal candidate: M0387-X-IMPERIAL.1

The upstream terminal chain in `FLT/Proof.lean` includes:

```lean
def B1 : Prop := FermatLastTheorem
theorem B4_proof : B4 := sorry
theorem B1_proof : B1 := B2_implies_B1 B2_proof
theorem flt : FermatLastTheorem := B1_proof
```

The positive-natural presentation in `FermatsLastTheorem.lean` is:

```lean
theorem PNat.pow_add_pow_ne_pow
    (x y z : ℕ+) (n : ℕ) (hn : n > 2) :
    x^n + y^n ≠ z^n
```

The terminal axiom output reported by the audited source is:

```text
[knownin1980s, propext, sorryAx, Classical.choice, Quot.sound]
```

The repository defines an unrestricted custom axiom:

```lean
axiom knownin1980s {P : Prop} : P
```

The source audit counted `86` `sorry` occurrences in `25` Lean files and also
found explicit axioms named `Mazur_statement` and `Odlyzko_statement`. Thus the
exact-root candidate is `[H1, M5, R0]`, evidence tier `E3`, not `M1` or
`M0-P`. A declaration with the right type is not a machine proof when its
transitive proof term contains `sorryAx` or a proposition-producing custom
axiom.

### Placeholder and custom-axiom boundaries

- `M0387-X-IMPERIAL.2`: `B4_proof : B4 := sorry` is a direct placeholder
  blocker.
- `M0387-X-IMPERIAL.3`: `knownin1980s {P : Prop} : P` can prove an arbitrary
  proposition and is outside the accepted axiom policy.
- `sorryAx`, `knownin1980s`, and the named statement axioms all prevent an exact
  root closure claim even if an upstream aggregate build happens to finish.
- Reopening condition: a newer immutable revision must be independently built,
  expose an exact root type, pass a transitive `#print axioms` report without
  disallowed axioms, and pass a complete placeholder scan. It must then be
  pinned and imported into this repository before it can reach `M0-P`.

### Source-only partial anchors

The following declarations were located in files whose local lexical scan did
not find `sorry`:

| overlay node | source anchors | status and boundary |
|---|---|---|
| `M0387-X-IMPERIAL.4` | `FreyPackage.of_not_FermatLastTheoremFor_p_ge_5`, `FreyPackage.fermatLastTheoremFor_p_ge_5`, `freyCurveInt`, `freyCurve`, `map`, `Δ`, `c₄`, `j`, `j_valuation_of_bad_prime` | `M3/E3`: definitions and source theorems located, but no independent kernel build, transitive axiom report, compatible pin, or repo-local wrapper |
| `M0387-X-IMPERIAL.5` | abstract patching declaration `ker_RtoT_le_nilradical` | `M3/E3`: useful algebraic source anchor, not an instantiated modularity-lifting theorem, historical `R=T`, or FLT root |

These anchors are a **modern candidate overlay**. The Imperial project describes
a route through hardly ramified representations, lifting, compatible families,
switching to characteristic `3`, and Chebotarev/Brauer--Nesbitt. It explicitly
does not implement the historical Ribet level-lowering route represented by
`M0387-WTW-W05` and `W06`. The anchors therefore must not be relabeled as
historical Wiles--Ribet leaves.

### Reproducibility result

A fresh upstream kernel build was attempted but the pinned Lean
`4.32.0-rc1` toolchain could not be downloaded because the elan download ended
with an HTTP/2 error. The immutable source archive was obtained and audited,
but this did not produce `E2` build evidence. Consequently even a
placeholder-free-looking leaf remains `E3/M3` until independently checked.

## Additional repositories and false positives

| project | immutable revision | result |
|---|---|---|
| `leanprover-community/flt-regular` | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | pinned, locally checked partial FLT project: regular primes and selected small exponents; not a complete arbitrary-prime FLT proof |
| `pitmonticone/FLT3` / archived exponent-three source | `a199fa0467f86504a9d2f6164b0456608e586821` | exponent `3` only; cannot close the all-odd-prime family |
| `eluckydog/flt-from-scratch` | `0e14fc0fe1c5ec41e405815be19fac16b8e7fc9c` | README says it is not a complete compilable formalization; Serre/Ribet/Wiles `R=T` portions contain `by sorry`; `M5` candidate |
| `encryptedsalad/fermat_theorem` | `99943f8bc2e90ef013cbd1ef55fb79c2abc90dff` | false positive: Fermat's little theorem, statement mismatch |

Repository search also located the official Imperial and `flt-regular`
projects and the exponent-three archive. These results mean only that no other
usable candidate appeared on the searched surface, not that none can exist.

## Search access limits

- Anonymous GitHub code-search API requests returned HTTP `401`.
- GitHub repository API queries subsequently encountered the anonymous rate
  limit.
- HTML code search required authentication.
- A general web search did not yield another exact Lean 4 terminal candidate.

Because source-code search was not authenticated, the negative result is
deliberately scoped: **no further candidate was found in the audited search
surface as of 2026-07-10**. It is not an exhaustive nonexistence theorem.

## Current decision

No located public project satisfies all four required gates simultaneously:
exact `FermatLastTheorem` type, placeholder-free transitive proof, accepted
axiom report, and reproducible kernel check in or integrable into this
repository. The repo-local root therefore remains `M2`. The Imperial exact
candidate remains `M5`; its selected source-only components remain `M3`.
