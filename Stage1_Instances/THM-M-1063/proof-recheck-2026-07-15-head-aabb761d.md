# THM-M-1063 proof recheck at current base

Item: `S56-M-1063-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T05:59:25+08:00`

Base revision: `aabb761d975829b09920d981edc8220edb90e8c3`

Base tree: `a988020866eb03a08cd23d18d5e7711cb5d03742`

## Verdict

`blocked`. The proof phase remains `[ ]`; no proof body or proof credit was added.

The frozen target is the full finite-variance Donsker invariance principle in continuous path
space. The current repository and pinned dependency closure contain no theorem with that result.
The only target-local declarations are the definitional expansion
`target_iff_expandedSourceShape` and `ObligationTree.exactRoot_of_exactRoot`, which assumes the
complete target and returns it unchanged. Neither inhabits the root or a substantive frozen
obligation.

Pinned mathlib provides scalar central limit theorems and generic Gaussian-process,
Levy-Prokhorov, tightness, and convergence-in-distribution infrastructure. Exact source searches
found no Donsker or functional central limit declaration in any pinned Lake package. The only
repository hits outside this dossier are metadata strings explicitly classifying functional
Donsker work as separate and open; Git history contains no hidden proof body. The previously
audited `facebookresearch/atlas-lean` candidate proves only parts of a Rademacher
finite-dimensional route, has `sorry` in decisive CLT/Slutsky bodies, and contains no continuous
path-space tightness or convergence theorem. It is ineligible for import or proof credit.

All 29 machine-required obligations still have null terminal proof-body IDs. The first failed gate
remains `M1063-C-PATH`: no checked construction packages the frozen clipped-floor interpolation as
a continuous path. The substantive root cut remains `M1063-L-CLT`, `M1063-L-MODULUS`,
`M1063-L-ASCOLI`, `M1063-L-PROKHOROV`, `M1063-L-LAW-UNIQUE`, and `M1063-T-API`.
Assuming any missing package, strengthening the moment hypothesis, or substituting scalar or
finite-dimensional convergence would change the theorem and is forbidden.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1063` | 0 | Rank 506; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1063/check_obligation_tree.py` | 0 | 31 obligations and 125 typed edges passed; denominator `a55c3e2...26a7703`; root open at M4. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/DonskerTarget.lean` | 0 | The exact target and definitional expansion elaborated; output identified `DonskerInvariancePrinciple : Prop`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/ObligationTree.lean` | 0 | The identity interface elaborated and displayed the complete Donsker target as both input and output. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/AnchorAudit.lean` | 0 | Scalar CLT and generic convergence anchors resolved; axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg` for Donsker/FCLT terms in every pinned Lake package | 1 | Expected no-match exit; the pinned closure contains no topical declaration. |
| `rg` for Donsker/FCLT terms in other repository Lean sources | 0 | Only metadata strings saying functional/Donsker work is separate and open; no declaration. |
| `git grep` for Donsker/FCLT terms across repository history | 0 | Only the same metadata strings and this target's statement/audit/interface files; no proof body. |
| `rg` for prohibited constructs in owned Lean sources | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `unsafe`, `opaque`, `extern`, `implemented_by`, or `native_decide` construct exists. |
| scoped JSON assertion over `obligation-registry.json` | 0 | 31 obligations, 29 machine-required, and every `terminal_proof_body_id` is null. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at `98dc76e...`; Lake 5.0.0-src at the same Lean revision. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib revision `8a178386...` and tree `bdc39a3...`; source tree clean. |
| `sha256sum` over the target, tree, audit, registry, graph, toolchain, and manifest inputs | 0 | Source/input hashes match the structured blocker record. |
| `python3 -m json.tool Stage1_Instances/THM-M-1063/proof-recheck-2026-07-15-head-aabb761d.json` plus blocker assertions | 0 | JSON parsed; identity, base/tree, input hashes, open-state flags, empty proof-credit arrays, null terminal bodies, cut set, and absent self-test agree. |
| `git diff --no-index --check /dev/null` for each fresh artifact | 1 | Expected new-file differences with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof phase is incomplete. |

## Boundary and retry condition

Lifecycle stays `planned`; `audit_complete=false` and `theorem_complete=false`. The intake-era
manifest says M3 while the later frozen closure says M4, so this recheck reports the fail-closed
vector `[H2, M4, R4]` with no delta and makes no authoritative state edit. There are no accepted
receipt IDs. This current-base artifact is nonrelease blocker evidence, not a proof receipt, and it
does not satisfy `S56-M-1063-PROOF` or support master acceptance.

Resume only after continuous-path construction and measurability, finite-dimensional convergence,
finite-second-moment tightness, subsequential limit identification, Brownian-law uniqueness, and
the final API composition are implemented without placeholders, or after an immutable exact Lean 4
proof can be pinned, imported, exact-type checked, and provenance validated. Because the assigned
proof deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
