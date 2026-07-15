# THM-M-0578 proof-phase recheck at base 6bf9ee93 (slot42)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-16 (Asia/Shanghai)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. The exact frozen proposition
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
proof body was added. The proof item remains `[ ]`, the root vector remains
`[H3, M4, R4]`, and root closure, validation, release, audit completion, and
theorem completion remain false.

The frozen immediate root cut remains:

- `M0578-C-BUNDLE`: construct the selected smooth Milnor bundle total space;
- `M0578-T-HOMEO`: identify it with the fixed unit seven-sphere by a homeomorphism;
- `M0578-O-NONDIFF`: exclude every smooth diffeomorphism to that sphere.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The checked theorem
`ObligationTree.root_of_exoticWitnessPackage` is conditional composition only:
its premise already contains the smooth manifold, homeomorphism, and
nondiffeomorphism certificate. It constructs none of the open packages and
cannot receive root proof credit.

## Dependency And Reuse Audit

The new v2 dependency overlay was audited before proof search. The observed
theorem DAG SHA-256 is
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
and the stable target context SHA-256 is
`cdf6c9f8de36e769dba3868e130e3dbcced7e1e38e0429fb4b3a728c4b787aff`.
The target has no direct hard parents, transitive hard ancestors, hard edges,
or reuse hints, so the required inspection closure is empty.

The one shared group, `SHARED-MODULE-b3a9d89c683d7166`, is explicitly a weak
co-import cluster for `Mathlib.Geometry.Manifold.PoincareConjecture`, not a
common lemma or proof body. The closest member, `THM-M-0605`, was inspected:
its proof state is `[ ]`, and its only theorem
`exoticSevenSphereExists_of_witness` conditionally assembles a result from the
complete manifold, homeomorphism, and `IsEmpty Diffeomorph` certificate. Its
frozen structure also uses analytic regularity `omega`, while this target fixes
infinity-smooth regularity. There is no inhabitant to transport. The ledger
therefore records `not_applicable`, no unresolved compatibility work, and no
transferred proof credit. The repository's schema-1.1 ledger validator passes.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as the discarded source marker
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. Batteries
elaborates this syntax under `withoutModifyingEnv` and removes the declaration.
The trust-zero owned probe confirms that the name is unknown after import.

A current-base search across repository formalizations and all 9,676 Lean
files in the pinned packages found 13 relevant files. Every hit was a
statement, conditional composition, audit probe, legacy metadata module,
analogous-target probe, or the discarded marker. No retained declaration
inhabits the exact target or complete `ExoticWitnessPackage`; no Milnor bundle,
clutching construction, homotopy-sphere bridge, Eells-Kuiper invariant, or
Kervaire-Milnor implementation was found.

The owned `ProofBlockerProbe.lean` rejects invalid shortcuts at trust level
zero. `Diffeomorph.refl` inhabits the standard sphere's infinity-smooth
self-diffeomorphism type, so the standard sphere cannot be the requested
witness. Choosing a different atlas and proving the required emptiness
certificate would itself be the missing exotic-smooth-structure theorem.

The base advanced from `57fa141a` by adding the dependency orchestration and
integrating evidence, but no canonical proof input or Lean dependency pin
changed. Fresh structural and kernel checks reproduce the same mathematical
blocker. The new target-owned reuse ledger is the only new proof gate artifact;
it is complete and identifies no reusable terminal body.

## Validation

All successful commands ran in this worker clone. The automation-provided
untracked `Formalizations/Lean/.lake` symlink points at shared canonical pinned
artifacts and was reused read-only. No `lake update`, `lake build`, dependency
clone or fetch, checkout repair, network request, or dependency mutation
command was issued. Lean outputs were confined to a disposable `/tmp`
directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem incomplete. |
| direct call to `validate_dependency_reuse_ledger` with exact graph/base bindings | 0 | Schema 1.1 ledger passed with zero hard-parent inspections and one weak-group decision. |
| `timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-0578/check_statement.py` | 0 | Exact target elaborated; four mutations were distinguished; expression digest `c9d29902fc3b1bd25c4a83aa5daaa4ce201798576d7b5e16e9bbc05e76a9d32c`. |
| `timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact source marker and discard semantics passed at the pins; root remains M4 formalization debt. |
| `timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| isolated pinned `lake env lean` trust-zero replay of `Statement.lean`, `ObligationTree.lean`, and `ProofBlockerProbe.lean` | 0 | Statement, conditional composition, standard-sphere rejection, and discarded-name rejection elaborated; both nonroot theorems use exactly `propext`, `Classical.choice`, and `Quot.sound`; statement olean SHA-256 `83dcfaec38f0d842614531d19db521eb5f8496fa2d891fe59c6e2fc189d3d3a7`. |
| scoped retained-body search across repository and 9,676 pinned-package Lean files | 0 | The 13 relevant files were statements, conditional bodies, audits, metadata, probes, the analogous open target, or the discarded marker; no eligible terminal body was found. |
| pinned implementation search for clutching, homotopy/exotic sphere, Eells-Kuiper, Kervaire-Milnor, or Milnor-sphere code | 1 | Expected no-match exit; no implementation of the frozen construction, topology, or smooth-obstruction packages was found. |
| forbidden-proof-device scan of owned Lean files | 1 | Expected no-match exit; no `sorry`, `admit`, axiom declaration, `sorryAx`, `native_decide`, unsafe declaration, or equivalent proof escape was found. |
| proof-input whitelist diff from `57fa141a` to `HEAD` | 0 | Empty: no canonical proof input or Lean dependency pin changed. |

The full standard validator was also attempted, but severe concurrent runner
load prevented its parent process from returning a capturable final result in
this worker turn, so no pass is claimed. The v2 DAG checker was rerun after the
new blocker JSON/MD existed and returned its expected worker-side failure: its
fresh inventory includes those new files while the checked-in graph does not.
A worker may not regenerate or edit that authoritative graph; the integration
lane does so after merging blocked evidence. The target manifest commands,
pre-edit graph digest, schema-specific reuse validator, all three target
validators, and trust-zero Lean replay completed as recorded.

## Exact Recipe

The isolated kernel replay used the pinned Lake environment:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0578-proof-lakeenv-6bf9ee93-slot42.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
cp Stage1_Instances/THM-M-0578/ProofBlockerProbe.lean "$tmp/ProofBlockerProbe.lean"
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(
  cd Formalizations/Lean
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground --kill-after=5s 600s \
    lake env lean --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground --kill-after=5s 600s \
    lake env lean --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground --kill-after=5s 600s \
    lake env lean --trust=0 -t0 -R "$tmp" "$tmp/ProofBlockerProbe.lean"
)
sha256sum "$tmp/Statement.olean"
```

The reuse and source checks were:

```bash
python3 - <<'PY'
import scripts.stage1_execution_cron as c
from pathlib import Path
c.validate_dependency_reuse_ledger(
    Path('Stage1_Instances/THM-M-0578/dependency-reuse-ledger.json'),
    'THM-M-0578',
    expected_observed_graph_sha256=c.graph_sha256(),
    expected_repository_revision='6bf9ee93a322e7d25cf9249226222095f95d1cff',
    evidence_root=c.ROOT,
    authoritative_root=c.ROOT,
)
PY

find -L Formalizations/Lean/.lake/packages -type f -name '*.lean' | wc -l
rg -l -i --glob '*.lean' \
  '(MilnorExoticSphereTarget|exists_homeomorph_isEmpty_diffeomorph_sphere_seven|ExoticWitnessPackage|ExoticSevenSphereExists|Milnor.{0,40}sphere|exotic.{0,40}(7.?sphere|seven.?sphere)|Eells.?Kuiper|Kervaire.?Milnor|sphere.{0,30}bundle.{0,30}sphere)' \
  Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages
rg -n -i --glob '*.lean' \
  '(clutching|homotopy.?sphere|exotic.?sphere|eells.?kuiper|kervaire.?milnor|milnor.?sphere)' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib \
  Formalizations/Lean/.lake/packages/batteries/Batteries
rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern|external)([[:space:]]|$)' \
  Stage1_Instances/THM-M-0578 --glob '*.lean'
```

## Retry Boundary

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock, license record,
and terminal-body provenance, then rerun exact-type, trust, provenance, and
composition checks.

Repeated root-level attempts exceed the rev-5.6 five-tick split threshold.
The integration lane should schedule dedicated child proof tasks for the seven
substantive packages; this worker does not edit the authoritative DAG.

This is a current-base nonrelease blocker record. It is not a proof receipt,
does not satisfy `S56-M-0578-PROOF`, proposes no state promotion, and supports
neither root closure nor theorem completion. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` remains intentionally absent.
