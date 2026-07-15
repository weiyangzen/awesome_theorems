# THM-M-0612 proof recheck at `728f3f0e` (slot42)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T11:56:32+08:00`

Base revision: `728f3f0ec187c9cbc62ff9b16f77018433a57c27`

Base tree: `57eac4a7a903020d852432d3aef2039a70683a4b`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact
target `Stage1.THM_M_0612.StatementShape`. The frozen immediate root cut is
still `M0612-T-SQUARED`, whose exact interface is
`Stage1.THM_M_0612.RadiusSquaredObstruction`: derive `r ^ 2 <= R ^ 2` from
the canonical local smooth symplectic embedding and cylinder hypotheses.

The first deep unavailable package is `M0612-C-CAPACITY`. The repository and
present pinned package sources do not construct a capacity on the canonical
local-domain model together with invariance, monotonicity, conformality, and
the ball and cylinder computations. The frozen alternative branch likewise
lacks compatible almost-complex structures and the pseudoholomorphic-curve
existence, compactness, energy, and monotonicity results.

`ObligationTree.lean` contains two real but nonterminal bodies.
`radius_le_of_sq_le` proves the ordered-field transport from squared radii,
and `root_of_radiusSquaredObstruction` checks the final composition only after
accepting the entire missing geometric obstruction as a premise. The ten
existing local statement, composition, encoding, and diagnostic declarations
replayed with `--trust=0`; each axiom report was exactly
`[propext, Classical.choice, Quot.sound]`. None constructs
`RadiusSquaredObstruction`, so none closes the root cut.

The legacy `S1_M_256.lean` uses a different global embedding interface. Its
Gromov-width definitions, supremum lemma, and conditional reductions do not
prove either the required nonlinear capacity computations or the canonical
local-domain theorem. The prerequisite anchor audit found a named external
Lean 4 nonsqueezing declaration only with admissions, and a fresh scan of the
available pinned package sources found no eligible terminal declaration.

The automation-provided top-level Lake environment remains malformed:
`.lake/packages/flt-regular/.git/HEAD` is `refs/heads/.invalid`, so the
prescribed top-level `lake env` commands stop before invoking Lean. Unlike the
preceding slot42 receipt, the manifest-pinned commit object
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` is now present. This worker did not
repair or check out the dependency. As a diagnostic fallback only, the pinned
Lean binary was run with an explicit read-only path assembled from the
already-present build artifacts; all four owned Lean sources elaborated.
That fallback is current kernel evidence for those exact files, but it is not
a successful replay of the recorded top-level Lake recipe and is nonrelease
evidence.

No proof source or positive receipt was added. The root vector remains
`[H2, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. The
prerequisite obligation-tree item is still worker-provisional `[_]`, not
master-accepted `[x]`. Because the assigned proof phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`,
dependency clone/fetch, checkout, repair, or other `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | `PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges`; denominator `2cad29b7...a4bc8`; root open M3 because the squared-radius package remains M4. |
| `cd Formalizations/Lean && lake env lean --version` | 1 | Lake could not resolve `flt-regular` `HEAD` and did not invoke Lean. |
| `cd Formalizations/Lean && lake env printenv LEAN_PATH` | 1 | Same invalid-`HEAD` failure. |
| explicit-path pinned Lean `--trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, `LocalEncoding.lean`, and `EncodingSanityProbe.lean` | 0 | All four sources elaborated. The ten printed declaration reports were exactly `[propext, Classical.choice, Quot.sound]`. Outputs were created only under `/tmp` and removed. |
| `cd Formalizations/Lean && lake --version && elan show && elan which lean` | 0 | Lake `5.0.0-src+98dc76e`; active Lean `4.29.0`, commit `98dc76e...16740`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | `HEAD` cannot be resolved; `.git/HEAD` contains `ref: refs/heads/.invalid`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular cat-file -t 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` | 0 | The manifest-pinned object is present and has type `commit`; it is not checked out at valid `HEAD`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Mathlib revision `8a178386...ea95`, tree `bdc39a31...1c2b`. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle construct, or native decision shortcut occurs. |
| available pinned-package topical scan | 1 | Expected no-match exit for a terminal nonsqueezing, Gromov-width, symplectic-capacity, or pseudoholomorphic declaration. |
| source and frozen-artifact SHA-256 check | 0 | Statement `2de623b5...f919`; obligation composition `0392a18a...07007`; registry file `635af26d...8850`; typed graphs `def70532...50b2`; pins unchanged. |
| paired JSON parse and blocker-invariant assertions | 0 | `PASS current-head blocker identity, hashes, fail-closed state, cut set, changed paths, and absent selftest`. |
| per-new-file whitespace checks | 0 aggregate | Both fresh evidence files passed `git diff --no-index --check`; exit 1 from each raw diff means only that `/dev/null` and the new file differ. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The diagnostic replay selected the pinned Lean executable with `elan which
lean`, assembled `LEAN_PATH` exclusively from the existing root and pinned
package `.lake/build/lib/lean` directories, compiled a temporary
`Statement.olean`, and used that temporary directory when replaying the three
imports of `Statement`. Output SHA-256 values were `e3b0c442...b855` for the
statement, `039f16b7...35a` for the obligation tree,
`4515cf76...0a3c5` for local encoding, and `94de4565...81e` for the encoding
probe.

The immutable repository input is HEAD `728f3f0e...a57c27`, tree
`57eac4a7...3a4b`. The untracked `.lake` symlink points outside the clone to
the canonical automation cache, so the evidence is dirty/nonrelease. Its link
target hashes to `e8714e9e...f59826`.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or discovery of an immutable compatible Lean 4
terminal proof that can be pinned, exact-type transported, and checked without
changing the dependency lock. A future recorded Lake replay additionally
requires the automation cache to expose the manifest-pinned `flt-regular`
commit through a valid checkout.

This is fresh owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0612-PROOF`, propose checklist state, or support audit completion,
theorem completion, validation, release, or master acceptance.
