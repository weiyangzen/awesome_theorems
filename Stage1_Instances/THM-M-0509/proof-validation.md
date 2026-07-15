# THM-M-0509 proof-phase validation

Item: `S56-M-0509-PROOF`

Base revision: `1f996d0ba7939acd26bf231689a91751d276bb8c`

Base tree: `ae0448c57d503bd89b62f8f4b753e689abe77e83`

## Implemented bodies

`Proof.lean` adds three exact, unconditional theorem bodies and two finite
definitions:

- `isP2_iff_cardFactors_pos_le_two` proves that the frozen product-based
  `IsP2` predicate is equivalent to having one or two prime factors counted
  with multiplicity;
- `representations` and `representationCount` define the complete finite set
  and count of prime-plus-`P2` representations of a natural number;
- `representationCount_pos_iff` proves that count positivity is exactly the
  canonical existential witness shape; and
- `chenTheoremTarget_iff_eventualPositiveRepresentationCount` proves both
  directions between the exact root and eventual positivity of that count.

These are substantive proof interfaces toward `M0509-C-REPRESENTATION` and
`M0509-T-P2-EXTRACTION`. The frozen nodes remain broader prose-level packages,
so zero frozen obligations are claimed closed. In particular, the final
equivalence does not inhabit `EventualPositiveRepresentationCount`.

## Boundary

The frozen remaining root cut is still `M0509-T-P2-EXTRACTION`: the new exact
interfaces do not prove the broader survivor-extraction package or construct a
positive survivor. The first unavailable analytic leaf below that cut is
`M0509-N-DISTRIBUTION`: neither the
repository nor pinned mathlib contains the quantitative averaged distribution
estimate for primes in progressions required by the weighted-sieve route.
Pinned `Mathlib.NumberTheory.SelbergSieve` supplies an upper-bound sieve only;
it does not supply Chen's lower-bound weighted sieve or switching principle.
Pinned `Mathlib.NumberTheory.LSeries.PrimesInAP` supplies qualitative
Dirichlet infinitude, not the required uniform averaged estimate.

The remaining route also needs exact frozen Lean signatures and bodies for the
sieve setup, weighted lower bound, switching estimate, aggregate remainder,
positivity assembly, and survivor extraction. Assuming eventual positivity or
returning `root_of_sieve_package` would substitute a conditional theorem for
the exact target.

The root remains `[H1, M4, R4]`; `root_kernel_closed=false`,
`audit_complete=false`, and `theorem_complete=false`. This partial proof
handoff is not theorem completion.

## Commands and exact results

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed. The automation-provided `.lake` symlink was used read-only.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0509` | 0 | rank 883; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0509/check_obligation_tree.py` | 0 | 15 obligations and 40 typed edges passed; denominator `74b4c30d...50703bd`; root open M4 |
| `bash Stage1_Instances/THM-M-0509/check_proof.sh` | 0 | isolated `Statement -> Proof` elaboration with `--trust=0` under both direct pinned Lean and mathlib's `lake env lean`; outputs agreed; all three theorem bodies were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`; evidence hashes and open-root boundary passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0509/Statement.lean)` | 1 | root Lake environment could not resolve `HEAD` in the shared `flt-regular` checkout; no fetch/update was attempted |
| `rg` scan for Chen/almost-prime/semiprime aliases in pinned mathlib Lean source | 1 | expected no-match exit; no exact terminal theorem found |
| `rg` scan for Bombieri-Vinogradov/linear-sieve/weighted-sieve/switching-principle aliases in pinned mathlib Lean source | 1 | expected no-match exit; no required analytic package found |
| prohibited-device scan over `Proof.lean` | 1 | expected no-match exit; no `sorry`, `admit`, axiom declaration, unsafe declaration, oracle, or native proof escape |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`, tree `bdc39a31...e5c2b` |
| `git diff --check -- Stage1_Instances/THM-M-0509 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The isolated checker enumerates only existing compiled package directories,
writes all generated oleans and output beneath `/tmp`, invokes the exact
repository toolchain `leanprover/lean4:v4.29.0` directly and through mathlib's
`lake env lean`, requires identical diagnostic output, and removes the
temporary directory. Explicit `LEAN_PATH` and `--root` isolate the narrow Lake
replay from root-project discovery, which currently fails on the unrelated
shared `flt-regular` checkout.

## Reopen condition

Resume root closure after exact typed signatures are frozen and placeholder-free
bodies are implemented for `M0509-N-DISTRIBUTION` and its dependent weighted-
sieve packages, or after an immutable compatible Lean 4 Chen proof is pinned,
exact-type transported, and checked for terminal provenance and trust.
