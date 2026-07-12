# Statement gate blocker

Item: `S56-M-0453-STATEMENT`  
Theorem: `THM-M-0453`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record gives only the name "Selmer group" and the gloss "the Selmer group of
an elliptic curve". It contains no proposition. In particular, it fixes neither a base global
field and elliptic curve nor a descent parameter (an integer, prime, or isogeny), local conditions,
cohomology model, or conclusion. A definition, finiteness theorem, descent exact sequence, and rank
bound are distinct possible targets. Selecting any one would add mathematics absent from the
source and violate the rev-5.6 prohibition on broadened or substituted theorems.

The pinned mathlib revision does contain `IsDedekindDomain.selmerGroup`, exposed by the minimal
import `Mathlib.RingTheory.DedekindDomain.SelmerGroup`. It is a subgroup of the unit group of a
fraction field modulo powers, cut out by valuations away from a set of height-one primes. Its
module documentation explicitly leaves the fundamental exact sequence and global-field finiteness
as future work. This is not an elliptic-curve Selmer group, and its checked monotonicity theorem is
not a source-faithful replacement for the missing THM-M-0453 proposition. The owned
`StatementDiscovery.lean` probe elaborates only these discovery anchors and assigns them no target
or proof credit.

Consequently the ordered binders, hypotheses, conclusion, excluded cases, canonical expression,
expression fingerprint, checked alternate transports, and removed-hypothesis, changed-domain,
changed-scope, and boundary mutations required by rev-5.6 section 5.1 cannot truthfully be
produced. No declaration, proxy predicate, proof, or substituted special case was introduced. The
machine state remains `M4`; statement acceptance and theorem completion are false.

## Environment fingerprint

- Repository base revision: `e0e1658c48365b041b302468a8238be1e1f30f20`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from this worker clone using only the existing canonical pinned `.lake` artifacts.
No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0453/StatementDiscovery.lean` | 0 | Minimal-import discovery probe elaborated both Dedekind-domain declarations; it declares no THM-M-0453 target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'selmer' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Matches are confined to the Dedekind-domain Selmer module and unrelated comments; no elliptic-curve Selmer declaration was located |
| `rg -n -i 'selmer' Formalizations/Lean/.lake/packages/mathlib/Mathlib/AlgebraicGeometry/EllipticCurve --glob '*.lean'` | 1 | No elliptic-curve Selmer declaration or reference; exit 1 is the no-match result |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0453` | 0 | Rank 302, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Retry condition

Provide an immutable primary-source edition and exact theorem/page pinpoint that selects a specific
elliptic-curve Selmer proposition. Its transcription must fix the base field and elliptic curve,
descent datum, local and cohomological conventions, every ordered binder and hypothesis, the exact
conclusion, and boundary cases. The statement phase can then encode that claim with minimal pinned
imports, serialize its elaborated expression, check any alternate transports, and execute all four
required mutation classes.

Until those conditions are met, this phase is not genuinely self-tested to its completion gate.
Accordingly no `.stage1-worker-selftest.json` is emitted.
