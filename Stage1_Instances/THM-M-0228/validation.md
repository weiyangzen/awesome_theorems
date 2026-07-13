# Intake validation

Base revision: `c6fd6dad8fcfe5fd464416cd452f50286b546978`; base tree:
`5a80b61d8fa09336779f8d1453dcfe4299c9472f`.

This validation covers target membership, the planned dossier and open task DAG, source-record
provenance, JSON/scoped invariants, a narrow pinned Lean substrate probe, prohibited-construct
hygiene, and whitespace. It does not validate a canonical theorem statement or proof. The initial
worktree contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink; it
was used read-only and not modified.

## Source discovery boundary

Immutable Encyclopedia of Mathematics revision `48178` was inspected as a secondary statement and
primary-bibliography lead. A live HTML response was hashed, but wrapper bytes changed on repeat
access; the revision ID and reported MediaWiki content SHA-1, not the live wrapper bytes, identify
the article content. The cited Picard primary proof passage was not retrieved or inspected.

The NUMDAM archival PDF for Picard's distinct 1879 article "Sur une classe de fonctions non
uniformes" was retrieved outside the repository, text-extracted, and inspected. It is not a source
for Little Picard and is recorded only to reject a plausible same-author/year mismatch. No remote
file was added to the repository and no H0 source review is claimed.

## Commands and results

All commands ran at repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0228` | 0 | rank 1240; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD`; `git rev-parse HEAD^{tree}` | 0 each | base revision and tree shown above |
| `git blame -L 1647,1652 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 60 -sS 'https://encyclopediaofmath.org/index.php?title=Picard_theorem&oldid=48178' -o /tmp/eom-picard.html`; `wc -c`; `sha256sum`; bounded `rg` inspection | 0 | revision 48178 states Little Picard and the omitted-two-points formulation and lists the 1879 Picard primary-source lead; one 22,207-byte dynamic response had SHA-256 `a8dfc1c...09d7`, with repeat wrapper drift explicitly recorded |
| `curl -L --fail --retry 3 --retry-delay 2 --max-time 120 -sS 'https://www.numdam.org/item/10.24033/bsmf.163.pdf' -o /tmp/picard1879-full.pdf`; `file`; `wc -c`; `sha256sum`; `pdfinfo`; `pdftotext -layout`; `sed -n '1,260p'` | 0 each | four-page, 241,452-byte archival PDF, SHA-256 `e2f43381...63af`; inspected text concerns multivalued functions near branch points and was rejected as the target source |
| `rg -n -i 'picard.*theorem\|little picard\|omitted.*value\|entire.*one.*exception\|takes every complex\|surjective.*entire' Formalizations/Lean/.lake/packages/flt-regular Formalizations/Lean/.lake/packages/mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean' --glob '*.md'` | 0 | only unrelated Picard-Lindelof/Picard-group material; no exact Little Picard terminal result in the bounded local search |
| `find Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Complex/ValueDistribution -type f`; bounded topic `rg` in that tree | 0 | first-main/value-distribution substrate present; no second-main or Little Picard declaration found in the bounded tree inspection |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD`; `git -C ... rev-parse HEAD^{tree}` | 0 each | pinned mathlib revision `8a178386...a95`, tree `bdc39a31...15e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...85b1d2` and `321626c8...d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0228/IntakeProbe.lean)` | 0 | fourteen adjacent pinned complex-analysis, omitted-set encoding, value-distribution, and exponential sharpness APIs elaborated; 24-line output SHA-256 `0a16d17c...1bdf`; no target theorem declared |
| `python3 -m json.tool` on the three owned JSON records and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0228-pycache python3 -m py_compile Stage1_Instances/THM-M-0228/check_intake.py` | 0 | scoped checker compiles outside the owned path |
| `python3 Stage1_Instances/THM-M-0228/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned lifecycle, H1/M4/R3 boundary, null formal target, exact hashed artifact inventory, worker packet, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0228/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0228` | 1 (expected) | no prohibited Lean proof escape or declaration |
| new-file `git diff --no-index --check` loop over the owned files and root packet | 0 | no whitespace diagnostics; per-file exit 1 is accepted only as the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0228 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0228-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Pinpoint primary proof inspection and independent
source review, canonical Lean elaboration and mutations, anchor audit, discovery and obligation
freezes, typed graphs, proof, composition, trust closure, hermetic replay, release bundling, and
independent validation remain open. They prevent theorem completion but do not invalidate intake.
