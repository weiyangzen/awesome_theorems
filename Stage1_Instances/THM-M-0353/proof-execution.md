# THM-M-0353 proof execution history

## Current rev-5.6 execution

The earlier blocked attempt below has been superseded by a provisional exact-root proof packet.
`Proof.lean` now kernel-checks the unchanged complex Hermite completeness target through a
byte-identical, immutable Apache-2.0 Hermite development and a repo-local complex adapter. See
`proof-validation.md`, `proof-receipt.json`, and `VENDOR_PROVENANCE.md` for the current commands,
hashes, axiom results, graph boundary, and non-completion status. This worker does not overwrite the
historical record or promote any accepted state.

## Superseded blocked attempt

Item: `S56-M-0353-PROOF`  
Base revision: `b8a117cd19ae3b30b59087d7bc9c8071ee7212ab`  
Verdict: `blocked`; no worker self-test receipt is issued.

## Implemented proof body

`Proof.lean` proves the exact boundary case
`Stage1Instances.THM_M_0353.hermiteFunction_zero_memLp`.  The proof unfolds the literal zeroth
Hermite function, reduces its squared norm to a Gaussian, and invokes the pinned mathlib theorem
`integrable_exp_neg_mul_sq`.  Kernel axiom reporting is
`[propext, Classical.choice, Quot.sound]`; there is no declared axiom or placeholder.

This closes only the `n = 0` subcase of `M0353-P-MEMLP`.  It does not close that universally
quantified obligation, `M0353-P-BASIS`, or the canonical root, and no theorem-completion credit is
claimed.

## First failed gate and blocker

The first failed proof-phase gate is exact root closure.  The frozen root still requires a proof
that every normalized Hermite function is in `L2` and a `HilbertBasis Nat Complex` whose vectors
are those functions.  The pinned mathlib revision has Hermite-polynomial/Gaussian differentiation
and Gaussian integrability, but no Hermite orthogonality, dense-span, or completeness theorem.  The
audited external Gaussian-Hilbert candidate does not match the target, toolchain, scalar field,
measure, normalization, or basis packaging and therefore cannot be imported as terminal closure.
Inventing either missing analytic package would violate the no-placeholder and exact-theorem gates.

Remaining root cut set: `M0353-P-MEMLP`, `M0353-P-BASIS`.  Machine status remains `M3`; theorem
completion remains false.  Because the assigned proof phase is not genuinely complete, the worker
intentionally leaves `.stage1-worker-selftest.json` absent.

## Validation ledger

All commands ran in the worker clone and reused the existing pinned Lake artifacts.  No Lake
update, build, clone, or fetch was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0353` | 0 | rank 846, lifecycle `planned`, `theorem_complete: false` |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0353 ../../Stage1_Instances/THM-M-0353/Statement.lean -o ../../Stage1_Instances/THM-M-0353/Statement.olean && LEAN_PATH=../../Stage1_Instances/THM-M-0353 lake env lean -R ../../Stage1_Instances/THM-M-0353 ../../Stage1_Instances/THM-M-0353/Proof.lean` | 0 | statement and proof elaborated; axiom report was `[propext, Classical.choice, Quot.sound]` |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0353 -g '*.lean'` | 1, expected | no prohibited placeholder or declared axiom |
| `git diff --check -- Stage1_Instances/THM-M-0353` | 0 | no whitespace errors |
