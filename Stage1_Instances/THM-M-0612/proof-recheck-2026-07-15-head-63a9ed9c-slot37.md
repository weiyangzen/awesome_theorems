# THM-M-0612 proof recheck at `63a9ed9c` (slot37)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T13:04:00+08:00`

Base revision: `63a9ed9c4aae594da31423142b0658129d5452a7`

Base tree: `7bee4fac4489bad36fd615a023df13bb294d1781`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact target
`Stage1.THM_M_0612.StatementShape`. The frozen immediate root cut remains
`M0612-T-SQUARED`, represented by
`Stage1.THM_M_0612.RadiusSquaredObstruction`: the canonical local smooth
symplectic embedding and cylinder hypotheses must imply `r ^ 2 <= R ^ 2`.

The first deep unavailable package is `M0612-C-CAPACITY`. Neither this
repository nor the available pinned Lean package sources construct a compatible
symplectic capacity with the invariance, monotonicity, conformality, ball, and
cylinder results required by the frozen route. The alternative frozen branch
also lacks the needed almost-complex structures and pseudoholomorphic-curve
existence, compactness, energy, and monotonicity results.

`ObligationTree.lean` supplies the real ordered-field transport
`radius_le_of_sq_le` and the conditional composition
`root_of_radiusSquaredObstruction`. The latter accepts the complete missing
geometric obstruction as a premise. The eight additional local-encoding and
sanity declarations establish nonvacuity, openness, differentiability, form
nondegeneracy, and derivative injectivity, but none closes the frozen root cut.
Introducing the geometric premise as an axiom, bodyless declaration, or theorem
hypothesis would be a prohibited placeholder rather than a proof.

A current source audit found no terminal declaration in the repo-local or
pinned Lean sources. The legacy `S1_M_256.lean` file uses a different global
embedding interface and proves only definitions, order lemmas, and conditional
reductions. The prerequisite audit's only external Lean 4 theorem named
`gromovNonsqueezing`, at immutable commit
`acc509702046aaae6a3c9be4546d5735ad7450cf`, has an admitted body and admitted
support, so it is ineligible for pinning or proof credit.

The proof-relevant Lean sources, frozen registry, and typed graphs are
byte-identical to the preceding `3a40b196` recheck. The only intervening target
changes are that preceding blocker JSON and Markdown. Thus there is no new
proof body or dependency candidate to credit at the current base.

The shared automation cache also prevents the prescribed Lake recipe from
starting: `.lake/packages/flt-regular/.git/HEAD` is
`refs/heads/.invalid`. The manifest-pinned commit object is present, but this
worker did not repair, check out, fetch, clone, or otherwise mutate `.lake`.
For scoped diagnostic evidence, the pinned Lean 4.29.0 binary was run with an
explicit read-only `LEAN_PATH` over the existing package build artifacts. All
four owned Lean modules elaborated at trust level 0; the ten printed declaration
reports each named exactly `propext`, `Classical.choice`, and `Quot.sound`. This
does not make the prescribed `lake env lean` recipe pass and does not supply the
missing nonlinear geometry.

No proof source or positive receipt was added. The root vector remains
`[H2, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. Because the
assigned positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. No `lake update`, `lake build`, dependency
clone/fetch, checkout, repair, or other `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | `PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges`; denominator `2cad29b7...a4bc8`; root open M3. |
| prescribed scoped `lake env lean --trust=0 -t0` replay | 1 | Lake stopped before invoking Lean because the shared `flt-regular` checkout cannot resolve `HEAD`. |
| explicit-path pinned Lean `--trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, `LocalEncoding.lean`, and `EncodingSanityProbe.lean` | 0 | All four modules elaborated; all ten axiom reports were exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle construct, or native-decision shortcut occurs. |
| available pinned-package topical scan | 1 | Expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| proof-input diff against `3a40b196` | 0 | Proof sources, registry, and graphs are unchanged; only the prior blocker pair entered the target path. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 128 | `HEAD` is `refs/heads/.invalid` and cannot be resolved. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular cat-file -t 56161b6e...a27` | 0 | The manifest-pinned object is present and has type `commit`. |
| pinned environment and SHA-256 checks | 0 | Lean 4.29.0 commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; all recorded input and pin hashes matched. |
| blocker JSON parse, current-head fail-closed assertions, source-hash checks, fresh-file whitespace checks, and `test ! -e .stage1-worker-selftest.json` | 0 | `PASS current-head blocker identity, hashes, fail-closed state, changed paths, whitespace, and absent completion selftest`. |

The explicit replay compiled `Statement.lean` to a temporary `Statement.olean`,
prepended that directory to the read-only package build paths while checking the
three importing modules, and removed all temporary output. The untracked `.lake`
symlink points outside this clone, so this remains dirty nonrelease evidence.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or discovery of an immutable compatible Lean 4
terminal proof that can be pinned, exact-type transported, and checked without
changing the dependency lock. Prescribed Lake replay additionally requires the
automation cache to expose manifest-pinned `flt-regular` commit
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` through a valid checkout.

This is fresh owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0612-PROOF`, propose checklist state, or support audit completion,
theorem completion, validation, release, or master acceptance.
