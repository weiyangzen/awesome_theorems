# THM-M-0918 intake validation

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675`; base tree:
`7b1b5269d7da840fd086da731d6f92903c209c35`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-statement discrimination, JSON and scoped invariants, a narrow pinned Lean
substrate probe, bounded repository/mathlib search, prohibited-construct hygiene, and whitespace.
It does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

NIST DLMF sections 17.2(vi) and 26.10(iv), their four exact equation permalinks, and their stated
references were inspected on 2026-07-13 as mutable discovery inputs. The observed section HTML
hashes were recorded during the run, but no remote file is part of the replay recipe or repository.
Crossref metadata for Rogers's original paper was also inspected; the publisher text was blocked.
These observations justify the H1 scope classification, not H0 admission, exact source freeze, or
proof credit.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0918` | 0 | rank 1460, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the canonical `.lake` symlink; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git log --all -S'**Rogers-Ramanujan identities**' -- Docs/researches/math_theorems.md` and blob checks | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 30 https://dlmf.nist.gov/17.2.vi` and exact E49/E50 TeX endpoints | 0 | both analytic identities inspected; 414,571-byte section HTML observed with SHA-256 `a1dc9479...7b3524`; mutable discovery only |
| `curl -L --fail --max-time 30 https://dlmf.nist.gov/26.10.iv` and exact E13/E14 TeX endpoints | 0 | both combinatorial identities and DLMF's explicit family label inspected; 203,471-byte section HTML observed with SHA-256 `8775a171...9a97`; mutable discovery only |
| Crossref title query for Rogers's second memoir | 0 | matching DOI `10.1112/plms/s1-25.1.318`, pages 318-343, and November 1893 metadata; no publisher theorem text; mutable discovery only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0918/IntakeProbe.lean)` | 0 | sixteen adjacent partition/power-series/sum/product interfaces elaborated and three axiom reports printed; output SHA-256 `dd94c452...66ae5` |
| bounded search for Rogers-Ramanujan and q-Pochhammer terms in repo-local Lean and pinned mathlib | 0 | only this probe's explanatory comments and a q-Pochhammer future-work bullet; no target declaration; bounded intake discovery only |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0918-pycache python3 -m py_compile Stage1_Instances/THM-M-0918/check_intake.py` | 0 | validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0918/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H1/M4/R4 boundary, pins, receipt, packet, and six open tasks agree |
| prohibited-construct scan over the owned Lean file | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check` and per-file `git diff --no-index --check /dev/null` | 0 aggregate | no whitespace diagnostics; no-index difference statuses were only the expected new-file differences |

## Known downstream failures

- The catalog does not select the first identity, second identity, conjunction, analytic form,
  formal power-series form, combinatorial form, or checked equivalences among them.
- Exact source edition, incorporated definitions, assumptions, proof boundary, historical date,
  corrections or errata, immutable source admission, and independent review remain open.
- Complex/formal coefficient domain, convergence and product semantics, partition representation,
  difference and residue predicates, binder order, and boundary cases remain open.
- No canonical Lean expression, minimal imports, expression or environment fingerprint, checked
  alternate encoding, or statement mutation result exists.
- Full source and anchor audits, discovery freeze, obligation registry and typed graphs, proof,
  composition and trust checks, readable reconstruction, hermetic replay, deterministic evidence
  bundle, independent verification, audit completion, theorem completion, and master acceptance
  remain open.

These failures block statement and theorem execution, but they do not invalidate a truthful,
self-tested `planned` intake that preserves the pair boundary, ambiguity, crosswalk, and open DAG.
Only the integration lane may accept the provisional worker receipt.
