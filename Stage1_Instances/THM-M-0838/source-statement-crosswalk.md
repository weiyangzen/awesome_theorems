# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6152-6157` supplies exactly the title
`Gonthier的形式化证明`, Georges Gonthier, 2008, the gloss `四色定理的Coq形式化`, importance
`高`, and status `已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no mathematical formula, definitions,
theorem locator, source edition, correction history, formal revision, toolchain, dependency lock,
axiom report, proof-body boundary, or reviewer.

`Docs/Stage0_Blueprint.md:22874-22899` projects the record while explicitly leaving the formal
system, logical foundation, exact definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. Its process field merely repeats the
artifact gloss. Rev-5.6 therefore retains `已验证` only as untrusted metadata and resets this target
to `L0 / rework_required`.

Repository secondary notes identify the intended work as Gonthier's 2008 Coq formalization of the
Four Color Theorem and cite Georges Gonthier, "Formal Proof--The Four-Color Theorem," *Notices of
the AMS* (2008). They also describe a combination of formal combinatorics and computation. These
notes disambiguate the topic but are not a primary statement crosswalk, kernel receipt, or H0/M0
evidence. The repository separately cites the 2013 Odd Order work, so that theorem is not this
target.

## Located formal source leads

An immutable historical source mirror, `tangentforks/FourColorTheorem` at commit
`eb30720f9e773fdcbf13dc6c61fdb245587cf401`, exposes the final declaration in
`fourcolor.v:21-24`:

```coq
Theorem four_color : forall m : map R, simple_map m -> map_colorable 4 m.
Proof.
exact (compactness_extension four_color_finite).
Qed.
```

The observed 708-byte raw file has SHA-256
`3f825d03dfa2f75d09195a1efc5259de62fb5fb40bd7d49137d86ab7ac71bec3`. In the same immutable
mirror, `realmap.v` has SHA-256
`fc8b86a7c695494d2372d378aaa973a938d7dbb261dd2b90223beee3fc8baa19` and defines `map` at line
34, `simple_map` at lines 81-85, and `map_colorable` at line 110. This yields the faithful scope
translation: for an arbitrary real model and every map in its plane, every simple map is colorable
with at most four colors.

The maintained `rocq-community/fourcolor` project was inspected at immutable release tag `v1.4.2`,
commit `9990abd7a15f80916c14367ac6dec947a836e60e` (tree
`84c3e9460f2e0808e24cc286ed8b06431d565ca7`). Its README identifies Georges Gonthier as the
initial author and says the library contains a formal proof of the Four Color Theorem in Coq. Its
`theories/proof/fourcolor.v` declares:

```coq
Theorem four_color_finite m : finite_simple_map m -> colorable_with 4 m.
Theorem four_color m : simple_map m -> colorable_with 4 m.
```

The observed raw source has SHA-256
`3a8a0aca7d5453fd2e82688bf2fc3dba5bc89d5ff5fda543c1d9c6121b25ca86`. Its final module says the
statement is over an arbitrary model of the real line and notes a separate equivalence with
classical excluded middle. `realplane.v` defines the current map and coloring vocabulary; its
observed SHA-256 is `b03e3c87073f591ccf19e4ea3b27894a17ea5f4db5acc31faa677353cafbfb36`.

These immutable source anchors are exact formal-source discovery (`E3`) only. Neither project is a
pinned repository dependency, no Coq/Rocq executable or compiled artifact is present here, and no
upstream build, transitive dependency, axiom, placeholder, or terminal-body audit was performed.
Consequently they supply no accepted M1 or M0 status. The historical mirror's relationship to the
maintained releases, the authoritative edition, correction history, license and dependency
boundary, and independent review also remain open.

## Clause crosswalk

| Catalog/source component | Exact source meaning | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Gonthier formalization | a particular Coq development and proof provenance | explicit source/provenance claim, not just a proposition name | root kind unresolved |
| arbitrary real model | source abstraction of real-line structure; maintained file notes classical equivalence separately | approved real/plane model and foundation transport | absent |
| `map R` | relation from plane points to regions | source-faithful map encoding or checked representation | absent |
| `simple_map m` | proper map whose regions are open and connected | exact predicate and every incorporated definition | absent |
| `map_colorable 4 m` / `colorable_with 4 m` | a proper coloring map with at most four regions, consistent with map regions and adjacency | map/face-coloring conclusion | absent |
| finite root | `finite_simple_map m -> ...` | finite-map branch | exact upstream lead only |
| arbitrary root | compactness extends the finite theorem to `simple_map m` | final canonical candidate and composition | exact upstream lead only |
| hypermap core | `planar_bridgeless G -> four_colorable G` | combinatorial intermediate plus discretization | not a final-root substitute |
| generic planar graph | familiar graph-theoretic formulation | `SimpleGraph.Colorable 4` plus a planarity predicate | only after checked bidirectional transports |
| `已验证` | untrusted inventory value | accepted source and kernel evidence would be required | no H/M credit |

## Human-source boundary

The exact formal declaration and definitions materially improve intake scope, but H0 still requires
an approved primary human proof source with edition, pinpoint statement, assumptions, proof nodes,
corrections/errata, and independent review. The repository's Notices citation and the maintained
project's publication links are source leads only. No article text was accepted or mapped here.
The current `H5` applies to the catalog's ambiguous artifact label, not to the truth of the Four
Color Theorem or the existence of Gonthier's formal development.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`SimpleGraph.Coloring`, `SimpleGraph.Colorable`, and
`SimpleGraph.chromaticNumber_le_iff_colorable`. It also elaborates a schema parameterized by an
uninterpreted `Planar` predicate. The parameter is deliberate: a bounded search found no exact
Four Color declaration, and the coloring module lists planar graphs under TODO. No source map
model, planarity definition, duality/representation bridge, target declaration, or proof body is
credited. This is narrow feasibility evidence, not a global absence result or downstream anchor
audit.

## First blocker and retry condition

Independent reviewers must decide whether the canonical root is the source mathematical theorem,
the upstream artifact-closure claim, or an explicit conjunction; admit an immutable authoritative
source edition and formal revision; map every incorporated definition, binder, hypothesis,
conclusion, computation, proof node, foundation assumption, and degenerate case; reconcile neighbor
ownership; and approve the source-to-Lean transport policy. Only then may the statement phase
select minimal imports, elaborate an exact Lean expression, serialize its fingerprints, check
alternate encodings, and run the required hypothesis, domain, binder-scope, and boundary mutations.
