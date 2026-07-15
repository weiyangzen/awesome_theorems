# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T12:57:09+08:00`

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

## Verdict

`blocked`. The assigned proof phase remains `[ ]` and is not self-tested as complete.

The integrated `Proof.lean` is genuine partial progress. Under Lean's trust level zero, it checks
the `Lp` representative's `MemLp` certificate, the unit-period and `p = 2` side conditions, an
adapter from a universally quantified upstream-shaped theorem, equality between the dossier-local
upstream-shaped cutoff and `symmetricPartialSum`, and composition of that raw analytic premise into
the exact `Stage1.THM_M_0346.CarlesonTarget`. All six declarations are sorry-free and report only
`propext`, `Classical.choice`, and `Quot.sound`.

Those bodies do not prove `RawCarlesonHunt`. In particular, `upstreamPartialFourierSum` is a local
model of the audited external API; because the external module is not imported, this phase does not
claim a checked equality against the actual external `partialFourierSum'`. Neither
`upstream_carleson_hunt_adapter` nor `carlesonTarget_of_rawCarlesonHunt` closes its explicit
analytic premise, so neither receives root proof credit.

The first failed gate is `M0346-L-CARLESON-HUNT`. Pinned mathlib contains no `carleson_hunt`
declaration or `partialFourierSum'` definition, and no Carleson package is present in the existing
Lake closure. The audited candidate remains `fpvandoorn/carleson` at immutable commit
`80e151dff5ddce2426079ec6392616496a4ec927`, module
`Carleson.Classical.CarlesonHunt`, declaration `carleson_hunt`. It targets Lean
`v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`, while this repository
is pinned to Lean `v4.29.0` and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It is therefore still an anchor, not an imported,
kernel-checked proof body. The external tree also contains textual `sorry` tokens, including one
inside a commented-out declaration in a transitive source file; only an actual import and
declaration-closure audit can decide the theorem's trust boundary, so textual inspection alone is
not proof credit or a definitive dependency claim.

The frozen registry remains authoritative: the root is open at `M3`, and its recorded cut consists
of `M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`,
`M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. The checked local bodies are evidence toward the
four adapter obligations, but this proof worker does not rewrite the frozen pre-proof closure
observation or claim any obligation closed. Assuming `RawCarlesonHunt`, treating a conditional
adapter as closure, or substituting mathlib's `L2`-topology convergence theorem would violate the
exact target.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were written under `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique ordered targets, ranks 1 through 1,546, passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | 11 obligations and 24 typed edges passed; denominator `1ff60884ffc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `Proof.lean` using the existing pinned package paths | 0 | Exact target and all six local declarations elaborated; every declaration was sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`. |
| prohibited-mechanism scan over `Statement.lean` and `Proof.lean` | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless `axiom`/`constant`, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide` occurred. |
| existing-package scan for a directory named `carleson` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| source scan for `theorem carleson_hunt` or `def partialFourierSum'` in repository and pinned Lean sources | 1 | Expected no-match exit; the actual upstream theorem and API are absent. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `cd Formalizations/Lean && timeout 20 lake env lean --version` | 1 | The project frontend stopped before Lean because the shared `flt-regular` checkout had an unresolved `HEAD`; it was not repaired or modified. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof phase is incomplete. |

The isolated replay used `lake env lean` from the existing pinned mathlib checkout because the
project-level Lake frontend could not resolve the unrelated shared `flt-regular` checkout. It
derived `LEAN_PATH` from that checkout, redirected its stale nested package prefixes to the same
canonical package directories, used `LEAN_NUM_THREADS=1`, and removed its temporary directory.
The source SHA-256 values were `a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d`
for `Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. The temporary object SHA-256 values were
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82` and
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`.

## Boundary and retry condition

Lifecycle stays `planned`; the root vector stays `[H3, M3, R4]`;
`audit_complete=false` and `theorem_complete=false`. This is current-base, warm-cache blocker
evidence, not a proof receipt. It changes no scheduler item, accepts no receipt, and supports no
validation, release, audit-completion, theorem-completion, or master-acceptance claim.

Resume after an immutable, license-reviewed Carleson package compatible with the repository pins is
provided, or after a deliberate repository-wide pin migration. Then import the real
`carleson_hunt`, check the exact external partial-sum transport, audit its transitive terminal
bodies and axioms, and compose the exact root. Because that work is unavailable under this worker's
no-fetch and no-`.lake`-mutation constraints, `.stage1-worker-selftest.json` is deliberately
absent.
