# THM-M-0721 proof recheck at `6cf20c1a`

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T06:27:59+08:00`

Base revision: `6cf20c1ab97fcd6970455baa23022062ebc14fe1`

Base tree: `5fa65edc9a9b91b49f7f925ad524ec374328e14c`

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
receive proof credit. The immutable anchor replay also reconfirmed that the three audited external
candidates are supporting-only, placeholder-dependent, or contract-incompatible and have no
checked transport to the frozen binary-word target.

The first failed gate is `M0721-N-SAT-ENCODING`. The remaining minimal root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the proof phase is incomplete, no
proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned
artifacts was reused read-only. No dependency update, build, clone, fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all` | 0 | Base `6cf20c1a...fe1`, tree `5fa65edc...e14c`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 360s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...204`; all four mutations were distinguished; pinned environment matched. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root open M3 and both terminal packages M4. |
| From `Formalizations/Lean`, concatenate the declaration-bearing portions of `Statement.lean` and `ObligationTree.lean`, then run `lake env lean --trust=0 --stdin` | 0 | The exact statement and conditional composition elaborated; axioms were exactly `propext` and `Quot.sound`; no terminal-package inhabitant was produced. |
| Scoped pinned-mathlib search for NP-completeness, SAT-language, and Cook-Levin endpoints | 1 expected | No matching endpoint was found. |
| Prohibited-device scans over owned Lean files and pinned `Computable.lean` | 0 overall | Owned files had no match; the sole pinned substrate hit was `proof_wanted TM2ComputableInPolyTime.comp`. |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins/hashes and all three immutable candidates matched; root classification remained M2. |
| Pinned mathlib identity and cleanliness check | 0 | Revision `8a178386...ea95`, tree `bdc39a31...c2b`, clean dependency worktree. |
| `python3 -m json.tool` on the fresh structured blocker | 0 | The JSON artifact parsed successfully. |
| No-index whitespace checks on both fresh blocker artifacts | 0 | Both returned the expected new-file difference exit without a whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof phase is blocked. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof can be pinned, exact-type checked, transported to the
frozen encodings, and provenance-audited without changing the dependency lock.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
