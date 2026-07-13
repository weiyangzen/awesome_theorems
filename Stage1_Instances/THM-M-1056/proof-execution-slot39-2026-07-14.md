# THM-M-1056 proof execution blocker (slot 39)

Item: `S56-M-1056-PROOF`

Base revision: `915698958f008ab3454659b876ec7da319a5a0e5`

Base tree: `5963a5839e72734d6a2b8b65a5dfe9898513d0c4`

Attempt date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`; no proof body was added and no frozen obligation was closed. The
first failed gate remains `M1056-T-CORE`: there is no placeholder-free
inhabitant of `OseledetsCorePackage` in this repository or its pinned Lake
closure. That package is definitionally the full universal target, so
`root_of_oseledetsCorePackage` is only conditional composition.

The exact target requires an Oseledets splitting for every positive-dimensional
finite-dimensional real normed Borel fiber, with strongly measurable oblique
component projections and simultaneous vector growth. The checked
`SanityInstance.lean` proves only that the identity cocycle on a one-point base
is an admissible inhabited instance; it neither makes the hypotheses
inconsistent nor proves the universal theorem.

No state change or receipt is proposed. Because the proof phase is not complete,
the root `.stage1-worker-selftest.json` is deliberately absent.

## External candidate execution

The immutable cached source
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
contains `ErgodicTheory.oseledets_splitting`. Its theorem is substantive, but it
accepts a matrix cocycle on `EuclideanSpace Real (Fin d)` and returns measurable
submodules plus `DirectSum.IsInternal`, not this target's projection structure
over arbitrary `E`.

The candidate is pinned to Lean `4.30.0-rc2` and mathlib
`34f7a6cd150fd7a166958d989d5abab56e9e3d15`; this clone uses Lean `4.29.0` and
mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`. Its theorem's transitive local
source closure contains 62 Lean files (1,498,045 bytes, 27,325 lines). A
read-only scratch port probe compiled `Cocycle/Basic.lean`,
`Cocycle/Norm.lean`, and `TwoSided/Invertible.lean` with this clone's pinned
toolchain. The next dependency, `Ergodic/MaximalErgodic.lean`, failed at line
104 because upstream uses `integrable_finsetSum`, while pinned mathlib exposes
`integrable_finset_sum`. This first rename is small, but it establishes that the
62-file development is not directly importable.

Even after a backport, checked bridges would still be required to:

- choose continuous linear coordinates for arbitrary `E` and conjugate the
  cocycle;
- transfer strong measurability, determinant/invertibility, both log-norm
  integrability assumptions, cocycle recursion, and norm growth;
- turn a measurable internal family of generally nonorthogonal submodules into
  strongly measurable pairwise-annihilating idempotent projections summing to
  identity;
- prove the transported projections' equivariance and derive positive count.

Orthogonal projectors are not component projectors for a nonorthogonal direct
sum. One possible new construction is the frame operator
`S = sum_i P_i` and oblique maps `Q_i = P_i comp S^-1`, but neither its
measurability nor the necessary identities and transports are implemented in
the candidate. Importing only the matrix/submodule theorem would therefore be
a substituted theorem, not exact root closure.

No dependency was installed or added to Lake, and the pre-existing `.lake`
symlink was used read-only. The immutable source archive was already cached
under `/tmp` when this execution was resumed; no network command was used in
the recorded validation. Scratch outputs were written only below `/tmp`.

## Fresh validation

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | 19 obligations and 49 typed edges passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root open M3 and core M4. |
| From `Formalizations/Lean`, copy `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` to a fresh `/tmp` directory; elaborate them in order with `LEAN_NUM_THREADS=1 lake env lean`, supplying the temporary directory through `LEAN_PATH`; remove the directory | 0 | All three modules elaborated. `#print axioms` reported exactly `[propext, Classical.choice, Quot.sound]` for conditional composition and the sanity conclusion. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx\|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| `rg -n -i '(^\|[^A-Za-z])(oseledets\|multiplicative ergodic\|kingman)([^A-Za-z]\|$)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match exit; pinned mathlib has no named terminal Oseledets or Kingman theorem. |
| From `Formalizations/Lean`, run `LEAN_NUM_THREADS=1 LEAN_PATH=/tmp/m1056-portcheck.RuNI6t:$(lake env printenv LEAN_PATH) lake env lean --root=<cached-upstream> -o <scratch-olean> <source>` for each scratch port probe | 0, 0, 0, 1 | `Basic`, `Norm`, and `Invertible` elaborated; `MaximalErgodic` stopped at unknown `integrable_finsetSum` (line 104). |
| `python3 -m json.tool Stage1_Instances/THM-M-1056/proof-execution-slot39-2026-07-14.json >/dev/null` | 0 | Structured blocker evidence parsed as valid JSON. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1056/proof-execution-slot39-2026-07-14.md` and the same command for the JSON artifact | 1, 1 | Expected new-file difference exits with no whitespace diagnostics. |

Toolchain evidence: Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Reopen condition

Resume after placeholder-free bodies exist for the frozen core packages, or
after the immutable external development is compatibly ported together with
kernel-checked coordinate, measurable-oblique-projection, exact-type,
provenance, and trust transports. Until then the root vector remains
`[H1, M3, R3]`, the minimal open cut is `M1056-T-CORE`, and this proof item
cannot truthfully receive `[_]` or theorem-completion credit.
