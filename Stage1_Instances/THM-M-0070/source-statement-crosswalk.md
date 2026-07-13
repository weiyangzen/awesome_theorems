# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:519-524` supplies the Chinese title, Walter Feit/John Thompson,
1963, the gloss `奇数阶群可解`, importance "high," and status `已验证`. Git history traces all six
uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
paper title, theorem/page locator, definitions, proof boundary, corrections, errata, or reviewer.

`Docs/Stage0_Blueprint.md:2028-2053` repeats the gloss but explicitly leaves definitions,
premises, formal system, foundations, proof route, dependencies, and evidence open. The Stage1
manifest therefore correctly resets the target to `L0 / rework_required` and records `已验证` only
as `source_status_untrusted`.

## Primary source candidate

Walter Feit and John G. Thompson, "Solvability of Groups of Odd Order," *Pacific Journal of
Mathematics* 13 (1963), no. 3, 775-1029, DOI `10.2140/pjm.1963.13.775` is the matching primary
paper. The journal-hosted Chapter I PDF was inspected. On printed page 775, Chapter I, section 1,
the authors write: "The purpose of this paper is to prove the following result: THEOREM. All finite
groups of odd order are solvable." Section 2 then states that all groups considered in the paper
are finite unless explicitly stated otherwise.

The inspected PDF had 742,729 bytes and SHA-256
`47e5127ef40e915bc8588a169df432ebab14a68a0f85fbd5b768abc0ca01b574`. This is discovery
evidence, not a vendored source. Only Chapter I pages available through that endpoint were checked;
the complete 255-page proof, incorporated definitions, correction and errata history, source-to-node
mapping, and independent review remain open. Consequently source status is H1, not H0.

## Statement-token crosswalk

| Source token | Content that must survive | Candidate Lean representation | Intake status |
|---|---|---|---|
| `All` | universal quantification over group carriers | `(G : Type u)` | frozen explicit binder |
| `finite groups` | group structure plus finite carrier | `[Group G] [Finite G]` | frozen ordered binders |
| `order` | cardinality of the group carrier | `Nat.card G` | frozen; checked `Fintype.card` alternate |
| `odd` | natural-number oddness of that cardinality | `Odd (Nat.card G)` | frozen; checked modulo-two alternate |
| `solvable` | derived series eventually becomes trivial | `IsSolvable G` | frozen; checked explicit witness alternate |

The canonical declaration is `Stage1Instances.THM_M_0070.OddOrderSolvabilityTarget` with shape
`(G : Type u) -> [Group G] -> [Finite G] -> Odd (Nat.card G) -> IsSolvable G`.
`Statement.lean` elaborates and serializes its fully explicit expression. This is statement
identity evidence only, not an inhabitant or proof of the declaration.

## Formalization record and Lean boundary

`Docs/researches/classified_theorems.md:521-541` describes a Coq/MathComp formalization completed
by Gonthier and collaborators and its references name the 2013 paper "A Machine-Checked Proof of
the Odd Order Theorem." Bibliographic discovery corroborates Georges Gonthier et al., *Interactive
Theorem Proving* 2013, pages 163-179, DOI `10.1007/978-3-642-39634-2_14`. Neither the external Coq
source tree nor a Coq toolchain is in this worker's Lean validation closure. At observed upstream
revision `6afa795b9018c64ab5c7cd2f9b3c9ab5dd45d93f`, `theories/PFsection14.v` declares
`Feit_Thompson` with type `odd #|G| -> solvable G`; the raw source SHA-256 was
`8153cf86d39adc9d9486a3044e1adeef1d523525d3757346fd0992feb571f9ef`. The same revision's
`stripped_odd_order_theorem.v` exposes a bare-Coq statement with explicit group axioms, finite order,
oddness, and solvability; its raw SHA-256 was
`47348f81909ca27ec7618577349acb4da315f0e8ec48a15cb503c1a9917a90ad`. These observations
strengthen the external lead, but no Coq build, dependency/trust audit, or repo-local integration
ran. It remains downstream external-candidate evidence only, not M0 or accepted M1 status.

Pinned mathlib provides `IsSolvable`, `isSolvable_def`, `derivedSeries`, and special solvability
results such as `CommGroup.isSolvable`. Its `docs/1000.yaml` contains the Feit-Thompson title but
no declaration. The probe's commutative-group theorem reports `[propext, Classical.choice,
Quot.sound]`; that report belongs only to the adjacent API. It neither proves the odd-order root
nor fixes the exact root's future foundation and TCB profiles.

## Downstream crosswalk gaps

- accept the complete primary edition and proof boundary, assumptions, corrections, errata, and
  source-to-obligation map under independent review;
- obtain master acceptance of the worker-self-tested statement expression, transports, mutations,
  boundary implications, and minimal-import evidence;
- perform immutable repo-local, mathlib, and external Lean 4 discovery, while separately deciding
  whether and how the Coq artifact can be pinned or translated without false Lean proof credit;
- freeze the obligation registry and typed graphs before measuring closure;
- implement or integrate exact placeholder-free proof bodies, composition certificates, trust
  closure, readable reconstruction, hermetic replay, and independent release validation.
