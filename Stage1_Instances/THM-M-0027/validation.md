# Intake validation

Base revision: `b09b188fbf6e0e288ddccb92314ef863d473ebad` (tree
`d64707bb77427b4e8569657bcd92a2c7f5713dc9`).

All commands ran from the isolated worker clone on 2026-07-13. Initial status contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink; it was preserved. The shared
canonical pinned `.lake` artifacts were used read-only. No update, build, fetch, clone, or
dependency mutation was run.

Validation covers manifest membership, planned-dossier structure, JSON integrity, a narrow pinned
Lean candidate probe, axiom reporting, source provenance, prohibited-token hygiene, and
whitespace. Because the catalogue does not identify an exact truth-valued formulation, it
establishes no canonical statement, expression fingerprint, mutation certificate, source
acceptance, or proof.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0027` | 0 | rank 1072; planned; L0/rework_required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short` | 0 | initial status recorded only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git blame -L 214,219 -- Docs/researches/math_theorems.md` | 0 | all six catalogue lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 857,882 -- Docs/Stage0_Blueprint.md` | 0 | catalogue fields and later generic tree/debt annotations identified; exact definitions, premises, equivalents, axioms, and artifacts remain open |
| `sha256sum` over normative, source, toolchain, lock, probed mathlib, and foreign legacy inputs | 0 | hashes recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0027/IntakeProbe.lean)` | 0 | five Wedderburn-Artin family candidates elaborated; the forward and iff candidate axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `rg -n -i 'wedderburn.?artin\|artin.?wedderburn' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 0 | bounded pinned-mathlib name search located the intended module and algebraically closed specialization; not a comprehensive anchor audit |
| `curl -L --fail --silent --show-error --max-time 30 https://api.crossref.org/works/10.1112%2Fplms%2Fs2-6.1.77` | 0 | metadata confirms Wedderburn, 1908, volume s2-6, pages 77-118, and DOI; no full paper or theorem passage inspected |
| `curl -L --fail --silent --show-error --max-time 30 https://api.crossref.org/works/10.1007%2FBF02952526` | 0 | metadata confirms Artin, 1927, volume 5, pages 251-260, and DOI; no full paper or theorem passage inspected |
| `python3 -m json.tool Stage1_Instances/THM-M-0027/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0027/task-dag.json` | 0 | valid JSON |

The final receipt JSON checks, scoped invariant checker, provisional packet linkage, prohibited
Lean construct scan, and whitespace checks are recorded after receipt finalization in
`intake-receipt.json`. Known downstream failures remain deliberately open: pinpoint primary-source
inspection and independent review; exact ring, handedness, direction, uniqueness, factor,
matrix-size, universe, and boundary choices; canonical Lean elaboration and mutation tests;
discovery and obligation freezes; complete candidate and provenance audit; proof and composition;
hermetic replay; deterministic release bundle; and independent master acceptance. They prevent
theorem completion but do not invalidate this truthful `planned` intake.
