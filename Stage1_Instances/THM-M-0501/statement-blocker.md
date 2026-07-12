# Exact-statement gate: blocked

Item: `S56-M-0501-STATEMENT`  
Theorem: `THM-M-0501`  
Base revision: `aa55669bb59986e08ea8a0d1d77a1e40343d8142`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the title "Siegel-Walfisz theorem" and the gloss "estimates for
zeros of L-functions", with an attribution to Carl Siegel and Arnold Walfisz and the year 1936.
There is no immutable source copy, theorem or formula/page pinpoint, exact wording, errata record,
ordered binder list, hypotheses, or conclusion.

The standard theorem name usually denotes a uniform prime-number theorem in reduced residue
classes for logarithmically bounded moduli, not merely an estimate about L-function zeros. Even
within that family, materially different statements remain possible:

1. an unweighted prime count `pi(x; q, a)`;
2. a logarithmically weighted prime count `theta(x; q, a)`;
3. a von Mangoldt sum `psi(x; q, a)`;
4. a power-saving error in `log x` or a stronger-looking exponential error form; and
5. natural-cutoff or real-cutoff formulations with different endpoint conventions.

The record also fails to fix the quantifier order and dependence of the modulus-range exponent,
error exponent, constants, cutoff, modulus, and residue class; the exact main term and range; the
effective or ineffective status of constants; or the treatment of `q = 0`, `q = 1`, non-reduced
classes, and small cutoffs. These variants are related mathematically but are not definitionally
identical Lean propositions. Selecting a familiar formulation, or replacing the named conclusion
by a zero-free-region or qualitative infinitude result, would broaden or substitute the target.

Consequently the canonical human-claim identity fails before import minimization, expression
fingerprinting, checked transports, or removed-hypothesis, changed-domain, binder-scope, and
boundary mutations can be meaningful. No Lean declaration, axiom, proof hole, weakened special
case, or assumed proxy predicate was introduced. Machine debt remains `M4`; statement acceptance,
audit completion, and theorem completion remain false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.NumberTheory.LSeries.PrimesInAP` and checks
Dirichlet characters, the von Mangoldt function, Euler's totient, modular congruence, and
mathlib's qualitative prime-in-progressions declarations. It re-elaborates in the pinned
environment, but it is not a canonical Siegel-Walfisz statement and receives no statement or proof
credit. A bounded source search found no declaration named for Siegel-Walfisz in pinned mathlib.

The reused environment is Lean `4.29.0` (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`) with Lake
`5.0.0-src+98dc76e` and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and
`lake-manifest.json` SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
The pre-existing shared `.lake` artifacts were used read-only. No update, build, dependency clone,
fetch, or other dependency mutation was performed.

## Validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0501` | 0 | Rank 878, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0501/IntakeProbe.lean` | 0 | All six nearby pinned APIs elaborated; this is an infrastructure probe only |
| repository `rg` search for the target ID, Chinese title/gloss, and Siegel-Walfisz spellings | 0 | Found only underspecified metadata and the planned intake dossier; no source-frozen proposition |
| `rg -n -i 'Siegel.?Walfisz|Walfisz|SiegelWalfisz' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match result in the bounded pinned-mathlib search |
| `python3 -m json.tool Stage1_Instances/THM-M-0501/statement-blocker.json` | 0 | Structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0501` | 0 | No whitespace errors |

There is no applicable `lake env lean <canonical-target>.lean` command because no exact expression
exists. Compiling an arbitrarily chosen conventional variant would be false statement evidence,
not completion of the assigned deliverable.

## Retry condition and status boundary

An accountable source review must preserve and hash an immutable primary or authoritative edition,
select and transcribe one exact theorem or formula with all referenced definitions and premises,
audit errata, and independently approve the mapping. It must freeze the counting function,
endpoint convention, quantifier order, main term, error bound, uniform modulus range, constant
dependence, coprimality encoding, and every small or degenerate case. A later statement run can then
encode that same claim, minimize pinned imports, serialize and hash the elaborated expression, prove
checked transports, and execute all four required mutation classes.

Verdict: `blocked`. The lifecycle remains `planned`; the root remains `[H3, M4, R4]`;
`audit_complete: false`; `theorem_complete: false`. No statement receipt or acceptance is claimed.
The assigned phase did not pass its completion gate, so no `.stage1-worker-selftest.json` is emitted.
