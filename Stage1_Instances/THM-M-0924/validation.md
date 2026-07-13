# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation covers target membership, the planned dossier and six-task open DAG, repository-source
provenance, JSON syntax and scoped invariants, exact owned-file inventory, a narrow pinned Lean
substrate probe, bounded exact-topic search, prohibited-construct hygiene, and whitespace. It does
not validate a canonical theorem statement or proof because the catalog supplies no truth-valued
proposition.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source and formal boundary

All six catalog lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; they provide no citation or proposition. A
bibliographic metadata lead for Lucas's 1878 *Theorie des Fonctions Numeriques Simplement
Periodiques* was recorded, but no article text, exact definition, theorem, proof, correction record,
or independent review was admitted. It grants no H0 credit.

Pinned mathlib has generic linear-recurrence and Fibonacci interfaces but no exact Lucas-number
declaration in the bounded package search. The only exact-phrase package hit is a prose mention of
Lucas sequences in the elliptic-divisibility-sequence module. The repo-local `lucasSequence P Q`
is a foreign legacy `U`-sequence object for `THM-M-0405`, begins `0,1`, and receives no target or
proof credit.

## Commands and results

Commands ran from the repository root unless a different working directory is stated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0924` | 0 | rank 1544; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | initially only pre-existing automation symlink `Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git blame -L 6756,6761 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa...` |
| `rg -n -i --glob '*.lean' 'Lucas numbers\|Lucas number\|Lucas sequence' Formalizations/Lean/.lake/packages` | 0 | one prose-only hit in `EllipticDivisibilitySequence.lean`; no Lucas-number definition or theorem found |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision `8a178386...`, tree `bdc39a31...`, clean package worktree |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0924/IntakeProbe.lean` | 0 | generic recurrence/Fibonacci interfaces and candidate axiom reports elaborated; 1,587-byte stdout SHA-256 `2860e9bc98e492ac65d7b24ca8a322694a7c4e304b20347cc1fa2738480d5429`; no target or proof declared |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all JSON documents parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0924-pycache python3 -m py_compile Stage1_Instances/THM-M-0924/check_intake.py` | 0 | scoped validator compiled without adding generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0924/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, planned H5/M4/R4 boundary, null target, source/pin/artifact hashes, exact probe output, handoff, and six open tasks agree |
| `rg -n --glob '*.lean' 'sorry\|admit\|sorryAx\|(^\|[^A-Za-z])(axiom\|constant\|opaque\|unsafe\|theorem\|lemma\|example)[[:space:]]' Stage1_Instances/THM-M-0924/IntakeProbe.lean` | 1 | expected no-match: no prohibited declaration or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0924 .stage1-worker-selftest.json` plus a scoped newline/CR/NUL/trailing-space Python check | 0 | no whitespace or file-hygiene defect |

The probe reports `[propext, Classical.choice, Quot.sound]` for the generic recurrence construction
and uniqueness candidates and `[propext, Quot.sound]` for `Nat.fib_add_two`. These are candidate
trust observations only, not an axiom audit of an absent canonical target.

## Known downstream failures

- No stable mathematical proposition is selected. Classical `L` versus general `U/V`, parameters,
  initialization, recurrence convention, domains, binders, conclusion, source, proof boundary,
  corrections, and independent reviews remain open.
- No canonical Lean expression, expression or environment fingerprint, minimal imports, checked
  alternate encoding, or statement mutation certificate exists.
- The API probe establishes generic pinned substrate only. The foreign legacy `U`-sequence and
  bounded search neither identify nor prove the catalog root; machine status remains `M4`.
- Formal anchor audit, obligation registry, typed graphs, proof, composition, provenance and trust
  closure, readable reconstruction, hermetic replay, deterministic evidence bundle, independent
  verification, release, and master acceptance remain open.

These failures block statement and theorem execution but do not invalidate a truthful, self-tested
`planned` intake. Only the integration lane may accept the provisional worker receipt.
