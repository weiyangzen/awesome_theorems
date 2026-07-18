# THM-M-0387 historical proof outline

This is the short reader route through the proof tree required by
`Docs/Stage1_Blueprint_v2.md`, using retained historical gate vocabulary. It reports mathematical evidence (`H`),
kernel evidence (`M`), and readable reconstruction (`R`) independently. The
long Wiles--Taylor--Wiles plan is in
`THM-M-0387/readable/wiles_taylor_wiles_process.md`; machine-closed entries are
in `THM-M-0387/readable/machine_closed_nodes.md`; external candidates are in
`THM-M-0387/readable/external_candidate_ledger.md`.

## Exact statement and boundary

The selected natural-number root is mathlib's exact proposition

```lean
def FermatLastTheorem : Prop :=
  ∀ n : ℕ, n ≥ 3 →
    ∀ a b c : ℕ, a ≠ 0 → b ≠ 0 → c ≠ 0 →
      a ^ n + b ^ n ≠ c ^ n
```

The repo-local alias `fermatLastTheoremRootStatement` is definitionally this
proposition. The currently checked root-shaped theorem is only conditional:

```lean
fermatLastTheoremRootOfOddPrimesPath :
  (∀ p : ℕ, Nat.Prime p → Odd p → FermatLastTheoremFor p) →
  fermatLastTheoremRootStatement
```

There is no repo-local, placeholder-free proof of its premise for every odd
prime. Therefore `M0387-ROOT = [H1, M2, R0]` in the conservative source audit:
the theorem is historically proved, but the primary-source-to-leaf crosswalk
is not complete; only some formal branches are closed; this document makes the
boundary readable. This vector is not a theorem-completion claim.

Across the full manifest, tree classification is `132/132`, exact machine
closure is `29/93 (31.18%)`, readable closure is `132/132`, and human-source
`H0` closure is `0/113`. The zero `H0` numerator means exact primary-source
section/theorem/page and assumption crosswalks remain incomplete; it does not
deny the accepted historical proof. All nodes therefore retain `H1` in this
run rather than borrowing human-proof closure from Lean evidence.

Accepted machine dependencies are Lean's kernel plus the audited occurrences
of `propext`, `Classical.choice`, and `Quot.sound`. `sorryAx`, `admit`, and
unreviewed custom axioms are disallowed. A wrapper records a checked conclusion
but never relocates its upstream proof body.

## Root composition

The checked mathlib theorem `FermatLastTheorem.of_odd_primes` performs the
entire exponent recomposition:

1. For `n ≥ 3`, `Nat.four_dvd_or_exists_odd_prime_and_dvd_of_two_lt` gives
   either `4 ∣ n` or an odd prime `p ∣ n`.
2. The first case uses `fermatLastTheoremFour`; the second requests the missing
   all-odd-prime premise.
3. `FermatLastTheoremWith.mono` transports a fixed-exponent theorem along the
   divisor in either case.

Thus `n = 4` plus **all** odd-prime exponents is sufficient, and all required
branches really are represented. The exact open edge is `M0387-R04`, not an
unspecified final line.

## Whole-tree map

| node | role | historical vector and exact boundary |
|---|---|---|
| `M0387-S` | `FermatLastTheoremWith`, fixed-exponent and full statements; primitive and `ℕ/ℤ/ℚ` transports; axiom policy | individual APIs are locally checked, while the structural package inherits `[H1, M2, R0]`; definitions and equivalences do not prove FLT |
| `M0387-R` | exponent boundaries, divisor monotonicity, composite-exponent split, odd-prime interface, conditional root assembly | checked reductions surround the open `M0387-R04`; package `[H1, M2, R0]` |
| `M0387-B3` | mod-9 boundary, generalized cubic statement, solution normalization, multiplicity descent, terminal `n = 3` wrapper | `[H1, M0-W, R0]`; proof body is pinned mathlib, not repo-local; exact primary human-source crosswalk remains open |
| `M0387-B4` | bridge equation, minimal primitive normalization, two Pythagorean classifications, coprimality and square extraction, strict descent, transports | `[H1, M0-W, R0]`; proof body is pinned mathlib, not repo-local; exact primary human-source crosswalk remains open |
| `M0387-RP` | regular-prime setup, primitive reduction, Kummer Case I and Case II, terminal `flt_regular` | `[H1, M0-P, R0]`; checked through pinned `flt-regular`, whose proof body is external and not vendored |
| `M0387-SMALL` | `p = 5,7,11,13` and all `3 ≤ n ≤ 16` | `[H1, M0-P, R0]`; pinned `flt-regular` plus mathlib, not an arbitrary-exponent family |
| `M0387-WTW` | general odd-prime route: Frey curve, representation, semistable modularity, level lowering, level-2 contradiction | `[H1, M4, R0]`; readable implementation plan only, no local proof body |
| `M0387-X-IMPERIAL` | modern external formalization candidate | terminal candidate is `M5`; selected source declarations are only `M3/E3`; it is evidence overlay, not the historical branch |
| `M0387-T` | branch terminals, odd-prime composition boundary, exact root gate | root terminal stays `[H1, M2, R0]`; the root gate is not met |

## Historical W01--W09 route

`M0387-WTW` is the historical contradiction route used here for proof-tree
architecture, not a description of completed local Lean code.

| package | readable obligation | machine status |
|---|---|---|
| `W01` | reduce a hypothetical solution to primitive, sign/parity-normalized odd prime exponent `p ≥ 5` | open plan (`M4`) |
| `W02` | construct the Frey curve, prove nonsingularity, compute invariants and minimal/local data, prove semistability and conductor formula | open plan (`M4`) |
| `W03` | construct `E[p]`, prove determinant, ramification, irreducibility/exception handling, and compatibility with Frey data | open plan (`M4`) |
| `W04` | prove semistable elliptic curves over `ℚ` modular through residual modularity, deformation rings, Taylor--Wiles primes, patching, minimal `R=T`, and nonminimal lifting | open plan (`M4`) |
| `W05` | apply Ribet's representation theorem/level-lowering hypotheses and lower the Frey representation to weight `2`, level `2` | open plan (`M4`) |
| `W06` | identify the required form in `S_2(Γ_0(2))`, calculate that this space is zero, and exclude the form | open plan (`M4`) |
| `W07` | compose modularity, level lowering, and level-2 impossibility into a contradiction | open because `W02--W06` are open |
| `W08` | quantify over every odd prime, combining `p = 3` with `p ≥ 5` | open because `W07` is open |
| `W09` | feed `W08` to `FermatLastTheorem.of_odd_primes`, whose `n = 4` branch is already checked | conditional assembly is checked; its all-prime input is open |

The published proof package is Andrew Wiles, *Modular elliptic curves and
Fermat's Last Theorem*, Annals of Mathematics 141 (1995), 443--551,
DOI [`10.2307/2118559`](https://doi.org/10.2307/2118559), together with Richard
Taylor and Andrew Wiles, *Ring-theoretic properties of certain Hecke
algebras*, 141 (1995), 553--572, DOI
[`10.2307/2118560`](https://doi.org/10.2307/2118560). The companion paper is
part of the corrected proof, not an optional historical footnote: the 1993
Euler-system argument had a gap, and the published route replaces that step
with Taylor--Wiles auxiliary primes and ring-theoretic control.

## Imperial modern candidate overlay

The audited Imperial candidate at revision
`44df7744a2a65cdc111875dc1b6f0db85477348f` follows a different modern route:
roughly, hardly ramified representations are lifted, placed in compatible
families, switched to characteristic `3`, and compared using
Chebotarev/Brauer--Nesbitt. It explicitly does not formalize the historical
Ribet `W05--W06` route. Its source has a declaration `flt :
FermatLastTheorem`, but the dependency chain contains `B4_proof : B4 := sorry`,
86 `sorry` occurrences in 25 Lean files, and the unrestricted custom axiom
`knownin1980s {P : Prop} : P`. Its terminal axiom report includes both
`sorryAx` and `knownin1980s`. Consequently it is `M5`, not `M1` or `M0-P`.

Its source-only Frey and abstract patching declarations are useful `E3/M3`
anchors. They do not close `W02`, `W04`, or the root, and they are kept in the
external overlay rather than silently spliced into the historical route.

## Final boundary

The strongest local statement is therefore precise but partial: statement and
reduction APIs, `n = 3`, `n = 4`, the selected small exponents, and every
regular-prime exponent are checked under pinned dependencies. No exact local
kernel-checked declaration proves `FermatLastTheorem` without assuming the
missing all-odd-prime family. Audit readability and historical mathematical
acceptance do not discharge that machine debt.
