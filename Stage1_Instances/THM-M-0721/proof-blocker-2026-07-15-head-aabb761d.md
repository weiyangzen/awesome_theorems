# THM-M-0721 proof recheck at `aabb761d`

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T06:02:39+08:00`

Base revision: `aabb761d975829b09920d981edc8220edb90e8c3`

Base tree: `a988020866eb03a08cd23d18d5e7711cb5d03742`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The target requires a binary-word language in the frozen verifier-based `InNP`
and polynomial-time many-one hardness for every such language. The checked
`root_of_candidate_packages` declaration only composes two hypotheses. It does
not construct either required package:

- `M0721-T-SAT-IN-NP`: a faithful encoded SAT language, verifier, correctness,
  certificate bound, and `TM2ComputableInPolyTime` witness;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin
  tableau construction, both correctness directions, and a polynomial-time TM2
  reduction witness.

No shortcut is available from the frozen definitions. Empty, universal,
constant, and identity candidates do not establish universal hardness, while
`InNP` and every reduction demand actual polynomial-time TM2 witnesses. Pinned
mathlib supplies the TM2 substrate and identity machine, but no NP, SAT, or
Cook-Levin endpoint. Its composition declaration is explicitly `proof_wanted`,
and ordinary computable `ManyOneReducible` is not the frozen reduction notion.

The immutable candidate replay passed at this base. It confirmed that one
external candidate supplies fixed-tableau support only, while the two headline
NP-completeness endpoints remain placeholder- or contract-dependent and lack a
checked transport to this binary-word TM2 formulation.

The first failed gate is `M0721-N-SAT-ENCODING`. The full missing development is
the eleven frozen SAT encoding, verifier, correctness, runtime, normalization,
tableau, reduction, and terminal packages. Because the positive proof phase is
incomplete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No dependency update, build,
clone, fetch, or `.lake` mutation was performed. Temporary Lean input was
created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all` | 0 | Base `aabb761d...e8c3`, tree `a9880208...3742`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 360s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression hash `758b1033...204`; all four structural mutations were distinguished; pinned Lean and mathlib identities matched. Two earlier overlapping invocations were stopped without diagnostics before this successful serialized rerun. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root open M3 and both terminal packages M4. |
| Trust-zero replay of a temporary copy of `Statement.lean` | 0 | The exact current statement module elaborated and printed `ExistsNPCompleteLanguage` as an existential language satisfying `NPComplete`. |
| Trust-zero temporary replay of the declaration-bearing portions of `Statement.lean` and `ObligationTree.lean` | 0 | Exact statement and conditional composition elaborated; axioms were exactly `propext` and `Quot.sound`; no terminal package was produced. |
| Scoped pinned-mathlib search for NP-completeness, SAT-language, and Cook-Levin endpoints | 1 expected | No matching endpoint was found. |
| Prohibited-device scans over owned Lean files and pinned `Computable.lean` | 0 overall | Owned files had no match; the sole pinned substrate hit was `proof_wanted TM2ComputableInPolyTime.comp`. |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins/hashes and all three immutable candidates matched; the root candidate classification remained M2. |
| Pinned mathlib identity and cleanliness check | 0 | Revision `8a178386...ea95`, tree `bdc39a31...c2b`, clean dependency worktree. |
| `python3 -m json.tool` on the fresh structured blocker | 0 | The JSON artifact parsed successfully. |
| No-index whitespace checks on both fresh blocker artifacts | 0 | Both returned the expected new-file difference exit without a whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof phase is blocked. |

Two earlier overlapping statement-harness attempts were stopped under host-wide
Lean saturation. The serialized rerun, smaller trust-zero replays, and the
structural obligation check all succeeded and establish the blocker boundary.

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and
Cook-Levin packages, or after an immutable compatible Lean 4 proof can be
pinned, exact-type checked, transported to the frozen encodings, and
provenance-audited. Until then the minimal root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`.

This is current-base nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, or claim audit completion, theorem
completion, validation, release, receipt acceptance, or master acceptance.
