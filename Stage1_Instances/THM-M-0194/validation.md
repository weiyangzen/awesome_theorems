# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2` (tree
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source and scope crosswalk, open task DAG, structured
intake invariants, and pinned Lean candidate probe. It does not validate a canonical inscribed-angle
proposition or proof because source, angle, arc, and boundary choices remain open. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no update,
build, clone, fetch, or other dependency mutation was performed. Dirty worker evidence is
nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0194` | exit 0; rank 1223, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `tmp=$(mktemp); curl -L --fail --silent --show-error --max-time 30 https://mathcs.clarku.edu/~djoyce/java/elements/bookIII/propIII20.html -o "$tmp"; sha256sum "$tmp"; wc -c "$tmp"; rm -f "$tmp"` | exit 0; 3,343-byte matching HTML source lead observed at SHA-256 `da95719836c9460d640343db776cea2f893411e3f582544b668829158208dfe2`; no H0 admission |
| `(cd Formalizations/Lean && lake env lean --version && lake env lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `rg -n -i 'thales\|inscribed angle\|angle at the center.*twice\|center.*twice.*circumference' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Euclidean/Angle/Sphere.lean` | exit 0; exact-topic oriented candidates and distinct semicircle alias located; this is intake discovery, not the exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0194/IntakeProbe.lean)` | exit 0; six exact-topic and semicircle interfaces elaborated; both diagnostic axiom reports were `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `bd47379182d6ed664001745c31bf5912b1e47d192e85fe809272c6c581ead899` |
| `python3 -m json.tool Stage1_Instances/THM-M-0194/instance.json >/dev/null` | exit 0 after finalization |
| `python3 -m json.tool Stage1_Instances/THM-M-0194/task-dag.json >/dev/null` | exit 0 after finalization |
| `python3 -m json.tool Stage1_Instances/THM-M-0194/intake-receipt.json >/dev/null` | exit 0 after finalization |
| `python3 -m json.tool .stage1-worker-selftest.json >/dev/null` | exit 0 after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0194-pycache python3 -m py_compile Stage1_Instances/THM-M-0194/check_intake.py` | exit 0; checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0194/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; manifest/DAG identity, null target, H1/M3/R4 boundary, source and dependency pins, artifact hashes, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0194/check_intake.py` | exit 0; public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0194` | exit 1 as expected; no declaration-token match in the API-only probe; this intentionally permits the diagnostic command `#print axioms` |
| public-Markdown private-path and completion-claim scan, using the exact expression recorded in the worker packet | exit 1 as expected; no private absolute path or completion overclaim in public Markdown; the literal scan tokens are kept out of the public files so the check does not match its own record |
| `git diff --check -- Stage1_Instances/THM-M-0194 .stage1-worker-selftest.json` | exit 0; no tracked whitespace diagnostic |
| `find Stage1_Instances/THM-M-0194 -maxdepth 1 -type f -print0 \| xargs -0 awk 'BEGIN{bad=0} /[ \t]$/{print FILENAME ":" FNR ": trailing whitespace"; bad=1} END{exit bad}'` | exit 0; every untracked owned file passed the scoped whitespace check |
| `awk 'BEGIN{bad=0} /[ \t]$/{print FILENAME ":" FNR ": trailing whitespace"; bad=1} END{exit bad}' .stage1-worker-selftest.json` | exit 0; worker packet passed the scoped whitespace check |

## Known open gates

Canonical root selection, complete source definition/case reconstruction, translation and
attribution review, correction/errata audit, and independent source review remain open. So do the
canonical Lean expression and environment fingerprint, checked ordinary/oriented and half/double
transports, statement mutations, exhaustive anchor and provenance audit, discovery protocol,
obligation registry, typed graphs, proof and composition, trust closure, readable reconstruction,
hermetic replay, deterministic bundle, independent verification, master acceptance, audit
completion, and theorem completion. These failures do not invalidate a truthful self-tested
`planned` intake.
