# THM-M-0721 proof recheck at `874745ff`

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T06:43:36+08:00`

Base revision: `874745ff39044c1e45ed30a04111d3d84aa0e348`

Base tree: `6e4fd01c84ebee3b7e65ad42efcfe307b2f88fc4`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked declaration `root_of_candidate_packages` only composes hypotheses. It does not
construct either required root package:

- `M0721-T-SAT-IN-NP`: an encoded SAT language, verifier, correctness proof, certificate bound,
  and a `TM2ComputableInPolyTime` verifier witness;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableaux, both
  correctness directions, and a polynomial-time TM2 reduction witness.

No definitional shortcut closes the target. The alphabet equivalences in
`TM2ComputableInPolyTime` rename individual symbols only; they cannot change list length or encode
an arbitrary whole-word function. Thus the pinned identity machine cannot bridge the
`encodePair` verifier input to the one-bit `encodeBool` output or implement arbitrary reductions.
Empty, universal, constant, and identity language candidates do not establish hardness for every
frozen `InNP` source.

Pinned mathlib supplies the TM2 substrate and its identity machine, but no NP, SAT, or Cook-Levin
endpoint. Its polynomial-time composition declaration is explicitly `proof_wanted`, so it cannot
receive proof credit. The frozen immutable anchor audit likewise records the three external
candidates as supporting-only, placeholder-dependent, or contract-incompatible and without a
checked transport to the binary-word target. A fresh remote replay was attempted but timed out;
therefore no network result is credited by this recheck.

The first failed gate is `M0721-N-SAT-ENCODING`. The remaining minimal root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the proof phase is incomplete, no
proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned
artifacts was reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short` | 0 | Base `874745ff...348`, tree `6e4fd01c...fc4`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root open M3 and both terminal packages M4. |
| From `Formalizations/Lean`, concatenate the declaration-bearing portions of `Statement.lean` and `ObligationTree.lean`, then run `LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 --stdin` | 0 | The exact statement and conditional composition elaborated; axioms were exactly `propext` and `Quot.sound`; no terminal-package inhabitant was produced. |
| `lake env lean --version`; `lake env lake --version`; pinned mathlib revision/tree checks | 0 | Lean 4.29.0 at `98dc76e...40`, Lake 5.0.0, mathlib `8a178386...ea95`, tree `bdc39a31...c2b`. |
| Scoped local and pinned-mathlib search for NP-completeness, SAT-language, and Cook-Levin endpoints | 0 | Matches were confined to this target's statement and conditional interface; no usable proof endpoint was found. |
| Prohibited-device scan over owned Lean files and pinned `Computable.lean` | 0 | Owned files had no match; the sole pinned substrate hit was `proof_wanted TM2ComputableInPolyTime.comp`. |
| `timeout 20 git ls-remote` for each of the three audited external repositories | 124 each | All three immutable-source replay attempts timed out with no output; no remote evidence is credited. |
| `python3 -m json.tool` on the structured blocker; `git diff --no-index --check /dev/null` on both blocker files | 0 overall | JSON parsed; both no-index checks returned the expected new-file exit 1 without whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof phase is blocked. |

The statement checker was also started, but machine-wide concurrent Lean load prevented it from
finishing in the command runner's 30-second observation window. Its temporary owned files and
processes were removed, and this interrupted run is not counted as passing evidence.

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof can be pinned, exact-type checked, transported to the
frozen encodings, and provenance-audited without changing the dependency lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
