import Mathlib.ModelTheory.Equivalence

/-!
# S1-M-298 / THM-M-0652: Craig interpolation theorem statement boundary

This Stage1 artifact records a conservative Lean 4 statement shape for the
first-order interpolation theorem.  The local mathlib snapshot provides
first-order languages, sentences, theories, semantic realization, language maps,
satisfiability, compactness, and semantic implication wrappers.  A terminal
Craig interpolation theorem was not located in the pinned mathlib dependency.

The file therefore keeps the theorem as a precise `StatementShape : Prop` and
checks only low-risk wrappers around available model-theory infrastructure.
-/

noncomputable section

open FirstOrder
open FirstOrder.Language

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_298

universe u v w

/--
Semantic consequence for sentences over a theory, using the same model universe
as mathlib's satisfiability definition for a language.
-/
def SemanticConsequence {L : Language.{u, v}} (T : L.Theory) (φ ψ : L.Sentence) : Prop :=
  ∀ ⦃M : Type (max u v)⦄ [Nonempty M] [L.Structure M] [M ⊨ T], M ⊨ φ → M ⊨ ψ

/--
Data for one Craig-interpolation instance.

`Lcommon` is the common language in which the interpolant must live.  `Lleft`
and `Lright` are the languages of the antecedent and consequent.  `Ltotal` is a
joint language where the original entailment is checked.  The commuting square
records that the two routes from the common language into the joint language
identify the same symbols.
-/
structure CraigInterpolationProblem
    (Lcommon Lleft Lright Ltotal : Language.{u, v}) : Type (max (u + 1) (v + 1)) where
  toLeft : Lcommon →ᴸ Lleft
  toRight : Lcommon →ᴸ Lright
  embedLeft : Lleft →ᴸ Ltotal
  embedRight : Lright →ᴸ Ltotal
  common_commutes : embedLeft.comp toLeft = embedRight.comp toRight
  leftSentence : Lleft.Sentence
  rightSentence : Lright.Sentence
  premise :
    SemanticConsequence (∅ : Ltotal.Theory)
      (embedLeft.onSentence leftSentence)
      (embedRight.onSentence rightSentence)

/--
A common-language sentence is an interpolant when the left sentence implies its
left-language translation and its right-language translation implies the right
sentence.
-/
def IsInterpolant {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal)
    (θ : Lcommon.Sentence) : Prop :=
  SemanticConsequence (∅ : Lleft.Theory) P.leftSentence (P.toLeft.onSentence θ) ∧
    SemanticConsequence (∅ : Lright.Theory) (P.toRight.onSentence θ) P.rightSentence

/--
Stage1 normalized statement-shape candidate for the first-order Craig
interpolation theorem: every semantic entailment between two sentences, after
embedding their languages into a common total language with a specified shared
sub-language, admits an interpolating sentence over the shared language.
-/
def StatementShape : Prop :=
  ∀ (Lcommon Lleft Lright Ltotal : Language.{u, v}),
    ∀ P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal,
      ∃ θ : Lcommon.Sentence, IsInterpolant P θ

/-- The normalized statement shape unfolds to the explicit interpolant-existence statement. -/
theorem statementShape_iff :
    StatementShape.{u, v} ↔
      ∀ (Lcommon Lleft Lright Ltotal : Language.{u, v}),
        ∀ P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal,
          ∃ θ : Lcommon.Sentence, IsInterpolant P θ :=
  Iff.rfl

/-- Semantic consequence is reflexive. -/
theorem semanticConsequence_refl {L : Language.{u, v}} (T : L.Theory) (φ : L.Sentence) :
    SemanticConsequence T φ φ := by
  intro M _ _ _ hφ
  exact hφ

/-- Semantic consequence is transitive. -/
theorem semanticConsequence_trans {L : Language.{u, v}} {T : L.Theory}
    {φ ψ θ : L.Sentence} (hφψ : SemanticConsequence T φ ψ)
    (hψθ : SemanticConsequence T ψ θ) :
    SemanticConsequence T φ θ := by
  intro M _ _ _ hφ
  exact hψθ (hφψ hφ)

/-- Project the left half of a supplied interpolant certificate. -/
theorem interpolant_left {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    {P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal} {θ : Lcommon.Sentence}
    (h : IsInterpolant P θ) :
    SemanticConsequence (∅ : Lleft.Theory) P.leftSentence (P.toLeft.onSentence θ) :=
  h.1

/-- Project the right half of a supplied interpolant certificate. -/
theorem interpolant_right {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    {P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal} {θ : Lcommon.Sentence}
    (h : IsInterpolant P θ) :
    SemanticConsequence (∅ : Lright.Theory) (P.toRight.onSentence θ) P.rightSentence :=
  h.2

/-- Checked mathlib anchor: the empty theory is satisfiable. -/
theorem emptyTheory_isSatisfiable (L : Language.{u, v}) :
    (∅ : L.Theory).IsSatisfiable :=
  Theory.isSatisfiable_empty L

/-- Checked mathlib anchor: first-order compactness for satisfiability. -/
theorem compactness_wrapper {L : Language.{u, v}} (T : L.Theory) :
    T.IsSatisfiable ↔ T.IsFinitelySatisfiable :=
  Theory.isSatisfiable_iff_isFinitelySatisfiable

/-- Checked mathlib anchor: sentence realization is preserved by language-map expansion. -/
theorem realize_onSentence_wrapper {L L' : Language.{u, v}} (M : Type (max u v))
    [L.Structure M] [L'.Structure M] (φ : L →ᴸ L') [φ.IsExpansionOn M]
    (ψ : L.Sentence) :
    M ⊨ φ.onSentence ψ ↔ M ⊨ ψ :=
  φ.realize_onSentence M ψ

/-- Checked mathlib anchor: the left coproduct injection of languages is injective. -/
theorem sumInl_injective (L L' : Language.{u, v}) :
    (LHom.sumInl : L →ᴸ L.sum L').Injective :=
  LHom.sumInl_injective

/-- Checked mathlib anchor: the right coproduct injection of languages is injective. -/
theorem sumInr_injective (L L' : Language.{u, v}) :
    (LHom.sumInr : L' →ᴸ L.sum L').Injective :=
  LHom.sumInr_injective

/-! ## Language/signature support for the common-symbol boundary. -/

namespace LanguageSupport

/--
A support predicate for the function and relation symbols of a language.

This is deliberately syntactic: it records which symbols may occur in a term or
formula, independently of semantics.  The interpolation extraction tasks can use
it to state that a candidate interpolant only uses symbols coming from the
specified common language.
-/
structure SymbolSupport (L : Language.{u, v}) : Type (max (u + 1) (v + 1)) where
  functions : ∀ n : ℕ, Set (L.Functions n)
  relations : ∀ n : ℕ, Set (L.Relations n)

namespace SymbolSupport

/-- Push a symbol-support predicate forward along a language homomorphism. -/
def map {L L' : Language.{u, v}} (g : L →ᴸ L') (S : SymbolSupport L) :
    SymbolSupport L' where
  functions n := (fun f : L.Functions n => g.onFunction f) '' S.functions n
  relations n := (fun R : L.Relations n => g.onRelation R) '' S.relations n

/-- The support in the codomain consisting exactly of symbols in the image of a language map. -/
def range {L L' : Language.{u, v}} (g : L →ᴸ L') : SymbolSupport L' where
  functions n := Set.range fun f : L.Functions n => g.onFunction f
  relations n := Set.range fun R : L.Relations n => g.onRelation R

@[simp] theorem map_functions {L L' : Language.{u, v}} (g : L →ᴸ L')
    (S : SymbolSupport L) (n : ℕ) :
    (S.map g).functions n = (fun f : L.Functions n => g.onFunction f) '' S.functions n :=
  rfl

@[simp] theorem map_relations {L L' : Language.{u, v}} (g : L →ᴸ L')
    (S : SymbolSupport L) (n : ℕ) :
    (S.map g).relations n = (fun R : L.Relations n => g.onRelation R) '' S.relations n :=
  rfl

@[simp] theorem range_functions {L L' : Language.{u, v}} (g : L →ᴸ L') (n : ℕ) :
    (range g).functions n = Set.range (fun f : L.Functions n => g.onFunction f) :=
  rfl

@[simp] theorem range_relations {L L' : Language.{u, v}} (g : L →ᴸ L') (n : ℕ) :
    (range g).relations n = Set.range (fun R : L.Relations n => g.onRelation R) :=
  rfl

/-- Equal language maps determine the same image support. -/
theorem range_congr {L L' : Language.{u, v}} {g h : L →ᴸ L'} (hgh : g = h) :
    range g = range h := by
  subst hgh
  rfl

end SymbolSupport

/-- A term is supported by `S` when each function symbol occurring in it is allowed by `S`. -/
def TermSupported {L : Language.{u, v}} {α : Type w} (S : SymbolSupport L) :
    L.Term α → Prop
  | Term.var _ => True
  | Term.func f ts => f ∈ S.functions _ ∧ ∀ i, TermSupported S (ts i)

/--
A bounded formula is supported by `S` when all function and relation symbols
occurring in it are allowed by `S`.
-/
def BoundedFormulaSupported {L : Language.{u, v}} {α : Type w} (S : SymbolSupport L) :
    ∀ {n : ℕ}, L.BoundedFormula α n → Prop
  | _, BoundedFormula.falsum => True
  | _, BoundedFormula.equal t₁ t₂ => TermSupported S t₁ ∧ TermSupported S t₂
  | _, BoundedFormula.rel R ts => R ∈ S.relations _ ∧ ∀ i, TermSupported S (ts i)
  | _, BoundedFormula.imp φ ψ => BoundedFormulaSupported S φ ∧ BoundedFormulaSupported S ψ
  | _, BoundedFormula.all φ => BoundedFormulaSupported S φ

/-- Sentence-level specialization of formula support. -/
abbrev SentenceSupported {L : Language.{u, v}} (S : SymbolSupport L) (φ : L.Sentence) : Prop :=
  BoundedFormulaSupported S φ

@[simp] theorem termSupported_var {L : Language.{u, v}} {α : Type w}
    (S : SymbolSupport L) (a : α) :
    TermSupported S (Term.var a : L.Term α) :=
  trivial

@[simp] theorem termSupported_func {L : Language.{u, v}} {α : Type w}
    (S : SymbolSupport L) {n : ℕ} (f : L.Functions n) (ts : Fin n → L.Term α) :
    TermSupported S (Term.func f ts) ↔ f ∈ S.functions n ∧ ∀ i, TermSupported S (ts i) :=
  Iff.rfl

@[simp] theorem boundedFormulaSupported_falsum {L : Language.{u, v}} {α : Type w}
    {n : ℕ} (S : SymbolSupport L) :
    BoundedFormulaSupported S (BoundedFormula.falsum : L.BoundedFormula α n) :=
  trivial

@[simp] theorem boundedFormulaSupported_equal {L : Language.{u, v}} {α : Type w}
    {n : ℕ} (S : SymbolSupport L) (t₁ t₂ : L.Term (α ⊕ Fin n)) :
    BoundedFormulaSupported S (BoundedFormula.equal t₁ t₂ : L.BoundedFormula α n) ↔
      TermSupported S t₁ ∧ TermSupported S t₂ :=
  Iff.rfl

@[simp] theorem boundedFormulaSupported_rel {L : Language.{u, v}} {α : Type w}
    {n l : ℕ} (S : SymbolSupport L) (R : L.Relations l)
    (ts : Fin l → L.Term (α ⊕ Fin n)) :
    BoundedFormulaSupported S (BoundedFormula.rel R ts : L.BoundedFormula α n) ↔
      R ∈ S.relations l ∧ ∀ i, TermSupported S (ts i) :=
  Iff.rfl

@[simp] theorem boundedFormulaSupported_imp {L : Language.{u, v}} {α : Type w}
    {n : ℕ} (S : SymbolSupport L) (φ ψ : L.BoundedFormula α n) :
    BoundedFormulaSupported S (φ.imp ψ) ↔
      BoundedFormulaSupported S φ ∧ BoundedFormulaSupported S ψ :=
  Iff.rfl

@[simp] theorem boundedFormulaSupported_all {L : Language.{u, v}} {α : Type w}
    {n : ℕ} (S : SymbolSupport L) (φ : L.BoundedFormula α (n + 1)) :
    BoundedFormulaSupported S φ.all ↔ BoundedFormulaSupported S φ :=
  Iff.rfl

/-- Language-map translation sends supported terms to terms supported by the pushed-forward support. -/
theorem termSupported_map {L L' : Language.{u, v}} {α : Type w} (g : L →ᴸ L')
    {S : SymbolSupport L} :
    ∀ t : L.Term α, TermSupported S t → TermSupported (S.map g) (g.onTerm t)
  | Term.var _, _ => trivial
  | Term.func f ts, h =>
      ⟨by
        simpa [SymbolSupport.map] using
          (Set.mem_image_of_mem (fun f : L.Functions _ => g.onFunction f) h.1),
        fun i => termSupported_map g (ts i) (h.2 i)⟩

/--
Every translated term is supported by the image of the translating language
homomorphism.
-/
theorem termSupported_range {L L' : Language.{u, v}} {α : Type w} (g : L →ᴸ L') :
    ∀ t : L.Term α, TermSupported (SymbolSupport.range g) (g.onTerm t)
  | Term.var _ => trivial
  | Term.func f ts =>
      ⟨⟨f, rfl⟩, fun i => termSupported_range g (ts i)⟩

/-- Language-map translation preserves bounded-formula support under pushed-forward supports. -/
theorem boundedFormulaSupported_map {L L' : Language.{u, v}} {α : Type w}
    (g : L →ᴸ L') {S : SymbolSupport L} :
    ∀ {n : ℕ} (φ : L.BoundedFormula α n),
      BoundedFormulaSupported S φ → BoundedFormulaSupported (S.map g) (g.onBoundedFormula φ)
  | _, BoundedFormula.falsum, _ => trivial
  | _, BoundedFormula.equal t₁ t₂, h =>
      ⟨termSupported_map g t₁ h.1, termSupported_map g t₂ h.2⟩
  | _, BoundedFormula.rel R ts, h =>
      ⟨by
        simpa [SymbolSupport.map] using
          (Set.mem_image_of_mem (fun R : L.Relations _ => g.onRelation R) h.1),
        fun i => termSupported_map g (ts i) (h.2 i)⟩
  | _, BoundedFormula.imp φ ψ, h =>
      ⟨boundedFormulaSupported_map g φ h.1, boundedFormulaSupported_map g ψ h.2⟩
  | _, BoundedFormula.all φ, h =>
      boundedFormulaSupported_map g φ h

/-- Every translated bounded formula is supported by the image of its language homomorphism. -/
theorem boundedFormulaSupported_range {L L' : Language.{u, v}} {α : Type w}
    (g : L →ᴸ L') :
    ∀ {n : ℕ} (φ : L.BoundedFormula α n),
      BoundedFormulaSupported (SymbolSupport.range g) (g.onBoundedFormula φ)
  | _, BoundedFormula.falsum => trivial
  | _, BoundedFormula.equal t₁ t₂ =>
      ⟨termSupported_range g t₁, termSupported_range g t₂⟩
  | _, BoundedFormula.rel R ts =>
      ⟨⟨R, rfl⟩, fun i => termSupported_range g (ts i)⟩
  | _, BoundedFormula.imp φ ψ =>
      ⟨boundedFormulaSupported_range g φ, boundedFormulaSupported_range g ψ⟩
  | _, BoundedFormula.all φ =>
      boundedFormulaSupported_range g φ

/-- Sentence translation preserves support under pushed-forward supports. -/
theorem sentenceSupported_map {L L' : Language.{u, v}} (g : L →ᴸ L')
    {S : SymbolSupport L} {φ : L.Sentence} (h : SentenceSupported S φ) :
    SentenceSupported (S.map g) (g.onSentence φ) :=
  boundedFormulaSupported_map g φ h

/-- Every translated sentence is supported by the image of the translating language map. -/
theorem sentenceSupported_range {L L' : Language.{u, v}} (g : L →ᴸ L') (φ : L.Sentence) :
    SentenceSupported (SymbolSupport.range g) (g.onSentence φ) :=
  boundedFormulaSupported_range g φ

/-- The two total-language images of common symbols in a Craig problem are the same boundary. -/
theorem commonBoundary_eq {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal) :
    SymbolSupport.range (P.embedLeft.comp P.toLeft) =
      SymbolSupport.range (P.embedRight.comp P.toRight) :=
  SymbolSupport.range_congr P.common_commutes

/-- A common sentence translated through the left route is supported by the common total boundary. -/
theorem common_leftRoute_supported {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal) (θ : Lcommon.Sentence) :
    SentenceSupported (SymbolSupport.range (P.embedLeft.comp P.toLeft))
      ((P.embedLeft.comp P.toLeft).onSentence θ) :=
  sentenceSupported_range (P.embedLeft.comp P.toLeft) θ

/-- A common sentence translated through the right route is supported by the same total boundary. -/
theorem common_rightRoute_supported_by_leftBoundary
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal) (θ : Lcommon.Sentence) :
    SentenceSupported (SymbolSupport.range (P.embedLeft.comp P.toLeft))
      ((P.embedRight.comp P.toRight).onSentence θ) := by
  rw [← P.common_commutes]
  exact common_leftRoute_supported P θ

/-- The same boundary statement, oriented through the right route. -/
theorem common_leftRoute_supported_by_rightBoundary
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal) (θ : Lcommon.Sentence) :
    SentenceSupported (SymbolSupport.range (P.embedRight.comp P.toRight))
      ((P.embedLeft.comp P.toLeft).onSentence θ) := by
  rw [P.common_commutes]
  exact sentenceSupported_range (P.embedRight.comp P.toRight) θ

end LanguageSupport

/-! ## Proof-calculus API selected for the interpolation route. -/

namespace ProofCalculus

/--
Contexts for the selected first-order proof calculus.

The calculus works directly with mathlib's locally nameless
`BoundedFormula`, so quantifier rules can move between the `n` and `n + 1`
bound-variable levels without introducing a second syntax tree.
-/
abbrev Context (L : Language.{u, v}) (α : Type w) (n : ℕ) : Type (max u v w) :=
  List (L.BoundedFormula α n)

/--
A small natural-deduction kernel for first-order formulas.

This is the Stage1 API choice, not a completeness theorem.  The rule set is
kept intentionally compact: hypothesis, falsum elimination, implication
introduction/elimination, and universal introduction.  Later child tasks can
extend this kernel or connect it to a fuller sequent calculus while preserving
the same finite-context and leaf-budget interfaces below.
-/
inductive Derivation (L : Language.{u, v}) {α : Type w} :
    ∀ {n : ℕ}, Context L α n → L.BoundedFormula α n → Type (max u v w)
  | hyp {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α n} (hφ : φ ∈ Γ) :
      Derivation L Γ φ
  | falsum_elim {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α n} :
      Derivation L Γ ⊥ → Derivation L Γ φ
  | imp_intro {n : ℕ} {Γ : Context L α n} {φ ψ : L.BoundedFormula α n} :
      Derivation L (φ :: Γ) ψ → Derivation L Γ (φ.imp ψ)
  | imp_elim {n : ℕ} {Γ : Context L α n} {φ ψ : L.BoundedFormula α n} :
      Derivation L Γ (φ.imp ψ) → Derivation L Γ φ → Derivation L Γ ψ
  | all_intro {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α (n + 1)} :
      Derivation L (Γ.map fun ψ => ψ.liftAt 1 n) φ →
        Derivation L Γ φ.all

namespace Derivation

/-- Number of open hypothesis leaves used by a derivation tree. -/
def leafCount {L : Language.{u, v}} {α : Type w} :
    ∀ {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α n},
      Derivation L Γ φ → ℕ
  | _, _, _, hyp _ => 1
  | _, _, _, falsum_elim d => leafCount d
  | _, _, _, imp_intro d => leafCount d
  | _, _, _, imp_elim dφψ dφ => leafCount dφψ + leafCount dφ
  | _, _, _, all_intro d => leafCount d

@[simp] theorem leafCount_hyp {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ : L.BoundedFormula α n} (hφ : φ ∈ Γ) :
    (hyp hφ).leafCount = 1 :=
  rfl

@[simp] theorem leafCount_falsum_elim {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ : L.BoundedFormula α n} (d : Derivation L Γ ⊥) :
    (falsum_elim (φ := φ) d).leafCount = d.leafCount :=
  rfl

@[simp] theorem leafCount_imp_intro {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ ψ : L.BoundedFormula α n}
    (d : Derivation L (φ :: Γ) ψ) :
    (imp_intro d).leafCount = d.leafCount :=
  rfl

@[simp] theorem leafCount_imp_elim {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ ψ : L.BoundedFormula α n}
    (dφψ : Derivation L Γ (φ.imp ψ)) (dφ : Derivation L Γ φ) :
    (imp_elim dφψ dφ).leafCount = dφψ.leafCount + dφ.leafCount :=
  rfl

@[simp] theorem leafCount_all_intro {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ : L.BoundedFormula α (n + 1)}
    (d : Derivation L (Γ.map fun ψ => ψ.liftAt 1 n) φ) :
    (all_intro d).leafCount = d.leafCount :=
  rfl

end Derivation

/--
Derivations that already satisfy the M0387-style local leaf budget for this
Stage1 route.
-/
structure SmallDerivation {L : Language.{u, v}} {α : Type w} {n : ℕ}
    (Γ : Context L α n) (φ : L.BoundedFormula α n) : Type (max u v w) where
  proof : Derivation L Γ φ
  leafCount_le_100 : proof.leafCount ≤ 100

namespace SmallDerivation

/-- Hypothesis leaves are valid small derivations. -/
def hyp {L : Language.{u, v}} {α : Type w} {n : ℕ} {Γ : Context L α n}
    {φ : L.BoundedFormula α n} (hφ : φ ∈ Γ) : SmallDerivation Γ φ where
  proof := Derivation.hyp hφ
  leafCount_le_100 := by simp

/-- Implication introduction preserves the leaf budget. -/
def impIntro {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ ψ : L.BoundedFormula α n}
    (d : SmallDerivation (φ :: Γ) ψ) : SmallDerivation Γ (φ.imp ψ) where
  proof := Derivation.imp_intro d.proof
  leafCount_le_100 := by simpa using d.leafCount_le_100

/--
Implication elimination is budget-preserving when the caller supplies the
combined leaf-count bound.  This keeps the budget accounting explicit at each
branching point.
-/
def impElim {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ ψ : L.BoundedFormula α n}
    (dφψ : SmallDerivation Γ (φ.imp ψ)) (dφ : SmallDerivation Γ φ)
    (hbudget : dφψ.proof.leafCount + dφ.proof.leafCount ≤ 100) :
    SmallDerivation Γ ψ where
  proof := Derivation.imp_elim dφψ.proof dφ.proof
  leafCount_le_100 := by simpa using hbudget

/-- Universal introduction preserves the leaf budget. -/
def allIntro {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ : L.BoundedFormula α (n + 1)}
    (d : SmallDerivation (Γ.map fun ψ => ψ.liftAt 1 n) φ) :
    SmallDerivation Γ φ.all where
  proof := Derivation.all_intro d.proof
  leafCount_le_100 := by simpa using d.leafCount_le_100

end SmallDerivation

/-- Sentence-level contexts used by Craig-interpolation derivability objects. -/
abbrev SentenceContext (L : Language.{u, v}) : Type (max u v) :=
  Context L Empty 0

/-- Sentence-level derivations are the closed-fragment specialization of the API. -/
abbrev SentenceDerivation {L : Language.{u, v}} (Γ : SentenceContext L)
    (φ : L.Sentence) : Type (max u v) :=
  Derivation L Γ φ

/-- Budgeted sentence derivations for local proof leaves. -/
abbrev SmallSentenceDerivation {L : Language.{u, v}} (Γ : SentenceContext L)
    (φ : L.Sentence) : Type (max u v) :=
  SmallDerivation Γ φ

/--
Finite-support derivability from a theory.

The context field is a finite list of theory sentences; the derivation field is
already bounded by `≤ 100` open leaves.  This is the object intended for child
proof leaves in the Craig-interpolation tree.
-/
structure TheoryDerivation {L : Language.{u, v}} (T : L.Theory) (φ : L.Sentence) :
    Type (max u v) where
  context : SentenceContext L
  context_subset : ∀ ⦃ψ : L.Sentence⦄, ψ ∈ context → ψ ∈ T
  derivation : SmallSentenceDerivation context φ

/-- Translate a finite sentence context through a language homomorphism. -/
def mapSentenceContext {L L' : Language.{u, v}} (g : L →ᴸ L')
    (Γ : SentenceContext L) : SentenceContext L' :=
  Γ.map g.onSentence

@[simp] theorem length_mapSentenceContext {L L' : Language.{u, v}} (g : L →ᴸ L')
    (Γ : SentenceContext L) :
    (mapSentenceContext g Γ).length = Γ.length := by
  simp [mapSentenceContext]

theorem mem_mapSentenceContext {L L' : Language.{u, v}} (g : L →ᴸ L')
    (Γ : SentenceContext L) {φ' : L'.Sentence} :
    φ' ∈ mapSentenceContext g Γ ↔
      ∃ φ : L.Sentence, φ ∈ Γ ∧ g.onSentence φ = φ' := by
  simp [mapSentenceContext]

/-- A hypothesis from a sentence context gives a one-leaf small derivation. -/
def smallSentenceHyp {L : Language.{u, v}} {Γ : SentenceContext L} {φ : L.Sentence}
    (hφ : φ ∈ Γ) : SmallSentenceDerivation Γ φ :=
  SmallDerivation.hyp hφ

/-! ### Soundness of the selected local calculus. -/

/-- A finite context is realized by a valuation and bound-variable environment. -/
def ContextRealized {L : Language.{u, v}} {α : Type w} {n : ℕ} {M : Type (max u v)}
    [L.Structure M] (Γ : Context L α n) (val : α → M) (xs : Fin n → M) : Prop :=
  ∀ ⦃φ : L.BoundedFormula α n⦄, φ ∈ Γ → φ.Realize val xs

/--
Weakening a realized context across the fresh bound-variable slot used by
universal introduction.
-/
theorem contextRealized_liftAt_one {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {M : Type (max u v)} [L.Structure M] {Γ : Context L α n} {val : α → M}
    {xs : Fin n → M} (hΓ : ContextRealized Γ val xs) (x : M) :
    ContextRealized (Γ.map fun ψ => ψ.liftAt 1 n) val (Fin.snoc xs x) := by
  intro φ hφ
  rw [List.mem_map] at hφ
  rcases hφ with ⟨ψ, hψ, rfl⟩
  simpa [ContextRealized] using hΓ hψ

namespace Derivation

/--
Soundness of the local natural-deduction kernel for bounded formulas: every
derivation preserves realization in every structure under any realized finite
context.
-/
theorem sound {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ : L.BoundedFormula α n} (d : Derivation L Γ φ)
    {M : Type (max u v)} [L.Structure M] :
    ∀ (val : α → M) (xs : Fin n → M), ContextRealized Γ val xs → φ.Realize val xs := by
  induction d with
  | hyp hφ =>
      intro val xs hΓ
      exact hΓ hφ
  | falsum_elim _ ih =>
      intro val xs hΓ
      exact False.elim (ih val xs hΓ)
  | imp_intro _ ih =>
      intro val xs hΓ hφ
      exact ih val xs (by
        intro θ hθ
        simp only [List.mem_cons] at hθ
        rcases hθ with rfl | hθ
        · exact hφ
        · exact hΓ hθ)
  | imp_elim _ _ ihφψ ihφ =>
      intro val xs hΓ
      exact (ihφψ val xs hΓ) (ihφ val xs hΓ)
  | all_intro _ ih =>
      intro val xs hΓ x
      exact ih val (Fin.snoc xs x) (contextRealized_liftAt_one hΓ x)

end Derivation

/-- Budgeted derivations inherit the soundness theorem of their proof tree. -/
theorem SmallDerivation.sound {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ : L.BoundedFormula α n} (d : SmallDerivation Γ φ)
    {M : Type (max u v)} [L.Structure M] :
    ∀ (val : α → M) (xs : Fin n → M), ContextRealized Γ val xs → φ.Realize val xs :=
  d.proof.sound

/-- Sentence-level soundness for finite contexts. -/
theorem smallSentenceDerivation_sound {L : Language.{u, v}} {Γ : SentenceContext L}
    {φ : L.Sentence} (d : SmallSentenceDerivation Γ φ) {M : Type (max u v)}
    [L.Structure M] (hΓ : ∀ ⦃ψ : L.Sentence⦄, ψ ∈ Γ → M ⊨ ψ) :
    M ⊨ φ := by
  simpa [Sentence.Realize, Formula.Realize, ContextRealized] using
    d.sound (M := M) (default : Empty → M) (default : Fin 0 → M) hΓ

/-- Theory derivations are sound in every nonempty model of the theory. -/
theorem theoryDerivation_realize {L : Language.{u, v}} {T : L.Theory} {φ : L.Sentence}
    (d : TheoryDerivation T φ) {M : Type (max u v)} [Nonempty M] [L.Structure M]
    [M ⊨ T] : M ⊨ φ :=
  smallSentenceDerivation_sound d.derivation (fun {ψ} hψ =>
    (Theory.model_iff T).1 inferInstance ψ (d.context_subset hψ))

/--
Soundness against `SemanticConsequence`: a derivation from a theory proves a
sentence semantically entailed by that theory, independently of the chosen
antecedent sentence.
-/
theorem theoryDerivation_semanticConsequence {L : Language.{u, v}} {T : L.Theory}
    {ψ : L.Sentence} (d : TheoryDerivation T ψ) (φ : L.Sentence) :
    SemanticConsequence T φ ψ := by
  intro M _ _ _ _
  exact theoryDerivation_realize d

/-- A one-assumption sentence derivation is sound as an empty-theory semantic implication. -/
theorem smallSentenceDerivation_semanticConsequence_singleton {L : Language.{u, v}}
    {φ ψ : L.Sentence} (d : SmallSentenceDerivation [φ] ψ) :
    SemanticConsequence (∅ : L.Theory) φ ψ := by
  intro M _ _ _ hφ
  exact smallSentenceDerivation_sound d (by
    intro θ hθ
    simp only [List.mem_singleton] at hθ
    subst hθ
    exact hφ)

/-! ### Completeness bridge boundary for the selected local calculus. -/

/--
The repo-local semantic consequence predicate agrees with mathlib's
`Theory.Imp` semantic implication wrapper at sentence level.

This is not a proof-completeness theorem: both sides are semantic.  It records
the exact checked handoff between the local statement shape and mathlib's
model-theory implication API.
-/
theorem semanticConsequence_iff_theoryImp {L : Language.{u, v}} {T : L.Theory}
    {φ ψ : L.Sentence} :
    SemanticConsequence T φ ψ ↔ FirstOrder.Language.Theory.Imp T φ ψ := by
  constructor
  · intro h M val xs hφ
    have hval : val = (default : Empty → M) := funext fun x => Empty.elim x
    have hxs : xs = (default : Fin 0 → M) := funext fun x => Fin.elim0 x
    subst val
    subst xs
    exact h (M := M) (by simpa [Sentence.Realize, Formula.Realize] using hφ)
  · intro h M _ _ _ hφ
    simpa [Sentence.Realize, Formula.Realize] using
      h (Theory.ModelType.of T M) (default : Empty → M) (default : Fin 0 → M) hφ

/--
A non-axiomatic interface for the missing semantic-to-derivability step.

Supplying an inhabitant of this structure is exactly the local completeness
work still missing for the selected finite-context calculus.  The structure is
ordinary data: this file only proves how such a bridge would be consumed.
-/
structure SemanticToDerivabilityBridge (L : Language.{u, v}) : Type (max (u + 1) (v + 1)) where
  derive_of_semantic :
    ∀ {φ ψ : L.Sentence},
      SemanticConsequence (∅ : L.Theory) φ ψ → SmallSentenceDerivation [φ] ψ

/--
The semantic premise of a Craig-interpolation problem converts to a one-assump-
tion derivation once the missing completeness bridge is provided for the total
language.
-/
def SemanticToDerivabilityBridge.derivationOfCraigPremise
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (bridge : SemanticToDerivabilityBridge Ltotal)
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal) :
    SmallSentenceDerivation [P.embedLeft.onSentence P.leftSentence]
      (P.embedRight.onSentence P.rightSentence) :=
  bridge.derive_of_semantic P.premise

/--
The same conversion expressed as a finite theory derivation from the singleton
theory containing the embedded antecedent.
-/
def SemanticToDerivabilityBridge.theoryDerivationOfCraigPremise
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (bridge : SemanticToDerivabilityBridge Ltotal)
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal) :
    TheoryDerivation ({P.embedLeft.onSentence P.leftSentence} : Ltotal.Theory)
      (P.embedRight.onSentence P.rightSentence) where
  context := [P.embedLeft.onSentence P.leftSentence]
  context_subset := by
    intro ψ hψ
    simp only [List.mem_singleton] at hψ
    subst hψ
    exact Set.mem_singleton _
  derivation := bridge.derivationOfCraigPremise P

/--
C004 status marker: repo-local Lean now has the checked consumption interface
for completeness, but no inhabitant of `SemanticToDerivabilityBridge` is
provided here.
-/
def c004CompletenessBridgeStatus : String :=
  "checked conditional bridge API; terminal semantic-to-derivability proof remains formalization_debt"

/-- Checked marker for the C004 completeness bridge boundary status. -/
theorem c004CompletenessBridgeStatus_eq :
    c004CompletenessBridgeStatus =
      "checked conditional bridge API; terminal semantic-to-derivability proof remains formalization_debt" :=
  rfl

/-! ### Cut-free structural interface for the selected local calculus. -/

namespace Derivation

/--
`CutFree d` records that a derivation uses no cut rule.

For the selected local natural-deduction kernel there is no explicit cut
constructor, so the predicate only recurses through the existing introduction,
elimination, and quantifier rules.  This gives later interpolation-extraction
work a named cut-free interface without pretending that a separate sequent
calculus cut-elimination theorem has been proved.
-/
def CutFree {L : Language.{u, v}} {α : Type w} :
    ∀ {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α n},
      Derivation L Γ φ → Prop
  | _, _, _, hyp _ => True
  | _, _, _, falsum_elim d => CutFree d
  | _, _, _, imp_intro d => CutFree d
  | _, _, _, imp_elim dφψ dφ => CutFree dφψ ∧ CutFree dφ
  | _, _, _, all_intro d => CutFree d

/-- Every derivation in the selected local kernel is cut-free by construction. -/
theorem cutFree {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ : L.BoundedFormula α n} (d : Derivation L Γ φ) :
    d.CutFree := by
  induction d with
  | hyp _ =>
      trivial
  | falsum_elim _ ih =>
      exact ih
  | imp_intro _ ih =>
      exact ih
  | imp_elim _ _ ihφψ ihφ =>
      exact ⟨ihφψ, ihφ⟩
  | all_intro _ ih =>
      exact ih

/--
Named structural induction principle for cut-free proof consumers.

Lean already generates a recursor for `Derivation`; this theorem freezes the
constructor-by-constructor API that the later interpolant extraction recursion
can target.
-/
theorem cutFreeStructuralInduction {L : Language.{u, v}} {α : Type w}
    (motive : ∀ {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α n},
      Derivation L Γ φ → Prop)
    (hhyp :
      ∀ {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α n}
        (hφ : φ ∈ Γ), motive (hyp hφ))
    (hfalsum :
      ∀ {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α n}
        (d : Derivation L Γ ⊥), motive d → motive (falsum_elim (φ := φ) d))
    (himpIntro :
      ∀ {n : ℕ} {Γ : Context L α n} {φ ψ : L.BoundedFormula α n}
        (d : Derivation L (φ :: Γ) ψ), motive d → motive (imp_intro d))
    (himpElim :
      ∀ {n : ℕ} {Γ : Context L α n} {φ ψ : L.BoundedFormula α n}
        (dφψ : Derivation L Γ (φ.imp ψ)) (dφ : Derivation L Γ φ),
          motive dφψ → motive dφ → motive (imp_elim dφψ dφ))
    (hallIntro :
      ∀ {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α (n + 1)}
        (d : Derivation L (Γ.map fun ψ => ψ.liftAt 1 n) φ),
          motive d → motive (all_intro d)) :
    ∀ {n : ℕ} {Γ : Context L α n} {φ : L.BoundedFormula α n}
      (d : Derivation L Γ φ), motive d := by
  intro n Γ φ d
  induction d with
  | hyp hφ =>
      exact hhyp hφ
  | falsum_elim d ih =>
      exact hfalsum d ih
  | imp_intro d ih =>
      exact himpIntro d ih
  | imp_elim dφψ dφ ihφψ ihφ =>
      exact himpElim dφψ dφ ihφψ ihφ
  | all_intro d ih =>
      exact hallIntro d ih

end Derivation

/-- A derivation bundled with the checked cut-free invariant for this local kernel. -/
structure CutFreeDerivation {L : Language.{u, v}} {α : Type w} {n : ℕ}
    (Γ : Context L α n) (φ : L.BoundedFormula α n) : Type (max u v w) where
  proof : Derivation L Γ φ
  cutFree : proof.CutFree

namespace Derivation

/-- Convert any selected-kernel derivation to the bundled cut-free form. -/
def toCutFree {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ : L.BoundedFormula α n}
    (d : Derivation L Γ φ) : CutFreeDerivation Γ φ where
  proof := d
  cutFree := d.cutFree

/-- The cut-free bundling step preserves the proof tree and therefore its leaf count. -/
theorem leafCount_toCutFree {L : Language.{u, v}} {α : Type w} {n : ℕ}
    {Γ : Context L α n} {φ : L.BoundedFormula α n} (d : Derivation L Γ φ) :
    d.toCutFree.proof.leafCount = d.leafCount :=
  rfl

end Derivation

/--
C005 status marker: repo-local Lean has a checked cut-free structural interface
for the selected no-cut natural-deduction kernel.  A separate sequent-calculus
cut-elimination theorem, if later selected for extraction, remains
formalization debt.
-/
def c005CutStructuralStatus : String :=
  "checked no-cut structural interface for selected calculus; terminal Craig extraction cut theorem remains formalization_debt"

/-- Checked marker for the C005 cut/structural branch boundary status. -/
theorem c005CutStructuralStatus_eq :
    c005CutStructuralStatus =
      "checked no-cut structural interface for selected calculus; terminal Craig extraction cut theorem remains formalization_debt" :=
  rfl

/-! ### Interpolant extraction recursion boundary. -/

/--
Constructor-by-constructor choices for extracting a common-language formula from
a derivation over a source language.

This is deliberately an algebra of extraction rules rather than a claimed Craig
interpolation algorithm.  A later proof branch must instantiate these choices
with the actual Craig construction for the final selected calculus.
-/
structure InterpolantExtractionRules (Lsrc Lcommon : Language.{u, v}) (alpha : Type w) :
    Type (max (u + 1) (v + 1) w) where
  hyp :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n} {formula : Lsrc.BoundedFormula alpha n},
      formula ∈ Gamma → Lcommon.BoundedFormula alpha n
  falsumElim :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n},
      Derivation Lsrc Gamma ⊥ → Lcommon.BoundedFormula alpha n →
        Lcommon.BoundedFormula alpha n
  impIntro :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n}
      {formula consequent : Lsrc.BoundedFormula alpha n},
      Derivation Lsrc (formula :: Gamma) consequent →
        Lcommon.BoundedFormula alpha n → Lcommon.BoundedFormula alpha n
  impElim :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n}
      {formula consequent : Lsrc.BoundedFormula alpha n},
      Derivation Lsrc Gamma (formula.imp consequent) → Derivation Lsrc Gamma formula →
        Lcommon.BoundedFormula alpha n → Lcommon.BoundedFormula alpha n →
          Lcommon.BoundedFormula alpha n
  allIntro :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n} {formula : Lsrc.BoundedFormula alpha (n + 1)},
      Derivation Lsrc (Gamma.map fun psi => psi.liftAt 1 n) formula →
        Lcommon.BoundedFormula alpha (n + 1) → Lcommon.BoundedFormula alpha n

namespace InterpolantExtractionRules

/-- Structural interpolant-extraction recursion over the selected proof kernel. -/
def extract {Lsrc Lcommon : Language.{u, v}} {alpha : Type w}
    (rules : InterpolantExtractionRules Lsrc Lcommon alpha) :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n} {formula : Lsrc.BoundedFormula alpha n},
      Derivation Lsrc Gamma formula → Lcommon.BoundedFormula alpha n
  | _, _, _, Derivation.hyp hformula => rules.hyp hformula
  | _, _, _, Derivation.falsum_elim d =>
      rules.falsumElim d (extract rules d)
  | _, _, _, Derivation.imp_intro d =>
      rules.impIntro d (extract rules d)
  | _, _, _, Derivation.imp_elim dImp dArg =>
      rules.impElim dImp dArg (extract rules dImp) (extract rules dArg)
  | _, _, _, Derivation.all_intro d =>
      rules.allIntro d (extract rules d)

end InterpolantExtractionRules

/--
Support-preservation contract for an extraction rule algebra.

If each rule returns a formula supported by `support` whenever its recursive
inputs are supported by `support`, then the full extraction recursion preserves
that common-language support invariant.
-/
structure InterpolantExtractionSupportInvariant
    {Lsrc Lcommon : Language.{u, v}} {alpha : Type w}
    (support : LanguageSupport.SymbolSupport Lcommon)
    (rules : InterpolantExtractionRules Lsrc Lcommon alpha) : Prop where
  hyp :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n} {formula : Lsrc.BoundedFormula alpha n}
      (hformula : formula ∈ Gamma),
        LanguageSupport.BoundedFormulaSupported support (rules.hyp hformula)
  falsumElim :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n}
      (d : Derivation Lsrc Gamma ⊥) {commonFormula : Lcommon.BoundedFormula alpha n},
      LanguageSupport.BoundedFormulaSupported support commonFormula →
        LanguageSupport.BoundedFormulaSupported support (rules.falsumElim d commonFormula)
  impIntro :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n}
      {formula consequent : Lsrc.BoundedFormula alpha n}
      (d : Derivation Lsrc (formula :: Gamma) consequent)
      {commonFormula : Lcommon.BoundedFormula alpha n},
      LanguageSupport.BoundedFormulaSupported support commonFormula →
        LanguageSupport.BoundedFormulaSupported support (rules.impIntro d commonFormula)
  impElim :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n}
      {formula consequent : Lsrc.BoundedFormula alpha n}
      (dImp : Derivation Lsrc Gamma (formula.imp consequent))
      (dArg : Derivation Lsrc Gamma formula)
      {commonImp commonArg : Lcommon.BoundedFormula alpha n},
      LanguageSupport.BoundedFormulaSupported support commonImp →
        LanguageSupport.BoundedFormulaSupported support commonArg →
          LanguageSupport.BoundedFormulaSupported support
            (rules.impElim dImp dArg commonImp commonArg)
  allIntro :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n} {formula : Lsrc.BoundedFormula alpha (n + 1)}
      (d : Derivation Lsrc (Gamma.map fun psi => psi.liftAt 1 n) formula)
      {commonFormula : Lcommon.BoundedFormula alpha (n + 1)},
      LanguageSupport.BoundedFormulaSupported support commonFormula →
        LanguageSupport.BoundedFormulaSupported support (rules.allIntro d commonFormula)

namespace InterpolantExtractionRules

/-- The extraction recursion preserves any support invariant supplied by its rule algebra. -/
theorem extract_supported {Lsrc Lcommon : Language.{u, v}} {alpha : Type w}
    {support : LanguageSupport.SymbolSupport Lcommon}
    {rules : InterpolantExtractionRules Lsrc Lcommon alpha}
    (hrules : InterpolantExtractionSupportInvariant support rules) :
    ∀ {n : ℕ} {Gamma : Context Lsrc alpha n} {formula : Lsrc.BoundedFormula alpha n}
      (d : Derivation Lsrc Gamma formula),
      LanguageSupport.BoundedFormulaSupported support (extract rules d)
  | _, _, _, Derivation.hyp hformula => hrules.hyp hformula
  | _, _, _, Derivation.falsum_elim d =>
      hrules.falsumElim d (extract_supported hrules d)
  | _, _, _, Derivation.imp_intro d =>
      hrules.impIntro d (extract_supported hrules d)
  | _, _, _, Derivation.imp_elim dImp dArg =>
      hrules.impElim dImp dArg (extract_supported hrules dImp) (extract_supported hrules dArg)
  | _, _, _, Derivation.all_intro d =>
      hrules.allIntro d (extract_supported hrules d)

/--
A conservative checked rule algebra that always extracts falsum.

This is useful as a compile-time sanity check for the recursion and support
invariant.  It is not a Craig interpolant construction and is not used to claim
the parent theorem.
-/
def bottom (Lsrc Lcommon : Language.{u, v}) (alpha : Type w) :
    InterpolantExtractionRules Lsrc Lcommon alpha where
  hyp := by
    intro n Gamma formula hformula
    exact ⊥
  falsumElim := by
    intro n Gamma d commonFormula
    exact ⊥
  impIntro := by
    intro n Gamma formula consequent d commonFormula
    exact ⊥
  impElim := by
    intro n Gamma formula consequent dImp dArg commonImp commonArg
    exact ⊥
  allIntro := by
    intro n Gamma formula d commonFormula
    exact ⊥

/-- The conservative bottom extraction algebra preserves every syntactic support predicate. -/
theorem bottom_supportInvariant {Lsrc Lcommon : Language.{u, v}} {alpha : Type w}
    (support : LanguageSupport.SymbolSupport Lcommon) :
    InterpolantExtractionSupportInvariant support (bottom Lsrc Lcommon alpha) := by
  constructor <;> intros <;> exact LanguageSupport.boundedFormulaSupported_falsum support

/-- Bottom extraction is supported for every derivation and every support predicate. -/
theorem extract_bottom_supported {Lsrc Lcommon : Language.{u, v}} {alpha : Type w}
    (support : LanguageSupport.SymbolSupport Lcommon)
    {n : ℕ} {Gamma : Context Lsrc alpha n} {formula : Lsrc.BoundedFormula alpha n}
    (d : Derivation Lsrc Gamma formula) :
    LanguageSupport.BoundedFormulaSupported support (extract (bottom Lsrc Lcommon alpha) d) :=
  extract_supported (bottom_supportInvariant support) d

/-- Extract from a budgeted derivation by forgetting only the budget certificate. -/
def extractSmall {Lsrc Lcommon : Language.{u, v}} {alpha : Type w}
    (rules : InterpolantExtractionRules Lsrc Lcommon alpha)
    {n : ℕ} {Gamma : Context Lsrc alpha n} {formula : Lsrc.BoundedFormula alpha n}
    (d : SmallDerivation Gamma formula) : Lcommon.BoundedFormula alpha n :=
  extract rules d.proof

/-- Support preservation for extraction from a budgeted derivation. -/
theorem extractSmall_supported {Lsrc Lcommon : Language.{u, v}} {alpha : Type w}
    {support : LanguageSupport.SymbolSupport Lcommon}
    {rules : InterpolantExtractionRules Lsrc Lcommon alpha}
    (hrules : InterpolantExtractionSupportInvariant support rules)
    {n : ℕ} {Gamma : Context Lsrc alpha n} {formula : Lsrc.BoundedFormula alpha n}
    (d : SmallDerivation Gamma formula) :
    LanguageSupport.BoundedFormulaSupported support (extractSmall rules d) :=
  extract_supported hrules d.proof

/-- Sentence-level interpolant extraction from a budgeted sentence derivation. -/
def extractSentence {Lsrc Lcommon : Language.{u, v}}
    (rules : InterpolantExtractionRules Lsrc Lcommon Empty)
    {Gamma : SentenceContext Lsrc} {formula : Lsrc.Sentence}
    (d : SmallSentenceDerivation Gamma formula) : Lcommon.Sentence :=
  extractSmall rules d

/-- Sentence-level support invariant for the extraction recursion. -/
theorem extractSentence_supported {Lsrc Lcommon : Language.{u, v}}
    {support : LanguageSupport.SymbolSupport Lcommon}
    {rules : InterpolantExtractionRules Lsrc Lcommon Empty}
    (hrules : InterpolantExtractionSupportInvariant support rules)
    {Gamma : SentenceContext Lsrc} {formula : Lsrc.Sentence}
    (d : SmallSentenceDerivation Gamma formula) :
    LanguageSupport.SentenceSupported support (extractSentence rules d) :=
  extractSmall_supported hrules d

/-- The left-language translation of any extracted common sentence uses only common symbols. -/
theorem extractSentence_leftRoute_supported
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal)
    (rules : InterpolantExtractionRules Ltotal Lcommon Empty)
    {Gamma : SentenceContext Ltotal} {formula : Ltotal.Sentence}
    (d : SmallSentenceDerivation Gamma formula) :
    LanguageSupport.SentenceSupported (LanguageSupport.SymbolSupport.range P.toLeft)
      (P.toLeft.onSentence (extractSentence rules d)) :=
  LanguageSupport.sentenceSupported_range P.toLeft (extractSentence rules d)

/-- The right-language translation of any extracted common sentence uses only common symbols. -/
theorem extractSentence_rightRoute_supported
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal)
    (rules : InterpolantExtractionRules Ltotal Lcommon Empty)
    {Gamma : SentenceContext Ltotal} {formula : Ltotal.Sentence}
    (d : SmallSentenceDerivation Gamma formula) :
    LanguageSupport.SentenceSupported (LanguageSupport.SymbolSupport.range P.toRight)
      (P.toRight.onSentence (extractSentence rules d)) :=
  LanguageSupport.sentenceSupported_range P.toRight (extractSentence rules d)

/--
The total-language left route of any extracted common sentence is supported by
the Craig common boundary.
-/
theorem extractSentence_totalLeftBoundary_supported
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal)
    (rules : InterpolantExtractionRules Ltotal Lcommon Empty)
    {Gamma : SentenceContext Ltotal} {formula : Ltotal.Sentence}
    (d : SmallSentenceDerivation Gamma formula) :
    LanguageSupport.SentenceSupported
      (LanguageSupport.SymbolSupport.range (P.embedLeft.comp P.toLeft))
      ((P.embedLeft.comp P.toLeft).onSentence (extractSentence rules d)) :=
  LanguageSupport.common_leftRoute_supported P (extractSentence rules d)

/--
The total-language right route of any extracted common sentence is supported by
the same Craig common boundary as the left route.
-/
theorem extractSentence_totalRightBoundary_supported
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal)
    (rules : InterpolantExtractionRules Ltotal Lcommon Empty)
    {Gamma : SentenceContext Ltotal} {formula : Ltotal.Sentence}
    (d : SmallSentenceDerivation Gamma formula) :
    LanguageSupport.SentenceSupported
      (LanguageSupport.SymbolSupport.range (P.embedLeft.comp P.toLeft))
      ((P.embedRight.comp P.toRight).onSentence (extractSentence rules d)) :=
  LanguageSupport.common_rightRoute_supported_by_leftBoundary P (extractSentence rules d)

end InterpolantExtractionRules

/--
C006 status marker: repo-local Lean now has a checked extraction recursion and
a common-language support invariant, but the rule algebra is not yet the
terminal Craig interpolation construction.
-/
def c006ExtractionStatus : String :=
  "checked structural extraction recursion and support invariant; terminal Craig extraction rules remain formalization_debt"

/-- Checked marker for the C006 extraction/support boundary status. -/
theorem c006ExtractionStatus_eq :
    c006ExtractionStatus =
      "checked structural extraction recursion and support invariant; terminal Craig extraction rules remain formalization_debt" :=
  rfl

/-! ### Terminal `IsInterpolant` obligation boundary. -/

/--
The common-language candidate produced by applying the current extraction API to
the derivation obtained from a supplied semantic-to-derivability bridge.

This is only a candidate: the actual Craig proof must still prove the two
semantic implications packaged below.
-/
def extractedInterpolantCandidate {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (bridge : SemanticToDerivabilityBridge Ltotal)
    (rules : InterpolantExtractionRules Ltotal Lcommon Empty)
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal) : Lcommon.Sentence :=
  InterpolantExtractionRules.extractSentence rules (bridge.derivationOfCraigPremise P)

/-- `IsInterpolant` is exactly the conjunction of its two terminal semantic obligations. -/
theorem isInterpolant_iff_left_right {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal) (θ : Lcommon.Sentence) :
    IsInterpolant P θ ↔
      SemanticConsequence (∅ : Lleft.Theory) P.leftSentence (P.toLeft.onSentence θ) ∧
        SemanticConsequence (∅ : Lright.Theory) (P.toRight.onSentence θ) P.rightSentence :=
  Iff.rfl

/-- Build an interpolant certificate from the two terminal semantic obligations. -/
theorem isInterpolant_of_left_right {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    {P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal} {θ : Lcommon.Sentence}
    (hleft :
      SemanticConsequence (∅ : Lleft.Theory) P.leftSentence (P.toLeft.onSentence θ))
    (hright :
      SemanticConsequence (∅ : Lright.Theory) (P.toRight.onSentence θ) P.rightSentence) :
    IsInterpolant P θ :=
  ⟨hleft, hright⟩

/--
Terminal proof obligations for the extracted Craig candidate.

This structure records the exact two semantic implications that remain after an
extraction rule algebra and semantic-to-derivability bridge have produced a
candidate common sentence.  It is ordinary proof data, not a postulate.
-/
structure ExtractedInterpolantTerminalObligations
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    (bridge : SemanticToDerivabilityBridge Ltotal)
    (rules : InterpolantExtractionRules Ltotal Lcommon Empty)
    (P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal) : Prop where
  antecedent_implies_interpolant :
    SemanticConsequence (∅ : Lleft.Theory) P.leftSentence
      (P.toLeft.onSentence (extractedInterpolantCandidate bridge rules P))
  interpolant_implies_consequent :
    SemanticConsequence (∅ : Lright.Theory)
      (P.toRight.onSentence (extractedInterpolantCandidate bridge rules P)) P.rightSentence

/--
Once the two terminal obligations are proved for the extracted candidate, the
candidate is an `IsInterpolant`.
-/
theorem extractedInterpolantCandidate_isInterpolant
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    {bridge : SemanticToDerivabilityBridge Ltotal}
    {rules : InterpolantExtractionRules Ltotal Lcommon Empty}
    {P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal}
    (h : ExtractedInterpolantTerminalObligations bridge rules P) :
    IsInterpolant P (extractedInterpolantCandidate bridge rules P) :=
  isInterpolant_of_left_right h.antecedent_implies_interpolant
    h.interpolant_implies_consequent

/-- Project the antecedent-to-interpolant terminal obligation for the extracted candidate. -/
theorem extractedInterpolantCandidate_left
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    {bridge : SemanticToDerivabilityBridge Ltotal}
    {rules : InterpolantExtractionRules Ltotal Lcommon Empty}
    {P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal}
    (h : ExtractedInterpolantTerminalObligations bridge rules P) :
    SemanticConsequence (∅ : Lleft.Theory) P.leftSentence
      (P.toLeft.onSentence (extractedInterpolantCandidate bridge rules P)) :=
  (extractedInterpolantCandidate_isInterpolant h).1

/-- Project the interpolant-to-consequent terminal obligation for the extracted candidate. -/
theorem extractedInterpolantCandidate_right
    {Lcommon Lleft Lright Ltotal : Language.{u, v}}
    {bridge : SemanticToDerivabilityBridge Ltotal}
    {rules : InterpolantExtractionRules Ltotal Lcommon Empty}
    {P : CraigInterpolationProblem Lcommon Lleft Lright Ltotal}
    (h : ExtractedInterpolantTerminalObligations bridge rules P) :
    SemanticConsequence (∅ : Lright.Theory)
      (P.toRight.onSentence (extractedInterpolantCandidate bridge rules P)) P.rightSentence :=
  (extractedInterpolantCandidate_isInterpolant h).2

/--
C007 status marker: the final `IsInterpolant` introduction/projection surface is
checked, but the actual Craig proofs of the two semantic implications remain
formalization debt until real extraction rules and their left/right correctness
proofs are supplied.
-/
def c007TerminalObligationsStatus : String :=
  "checked IsInterpolant terminal obligation interface; left/right Craig correctness remains formalization_debt"

/-- Checked marker for the C007 terminal-obligation boundary status. -/
theorem c007TerminalObligationsStatus_eq :
    c007TerminalObligationsStatus =
      "checked IsInterpolant terminal obligation interface; left/right Craig correctness remains formalization_debt" :=
  rfl

end ProofCalculus

/-! ## Audit probes retained in the checked file. -/

#check FirstOrder.Language
#check FirstOrder.Language.Sentence
#check FirstOrder.Language.Theory
#check FirstOrder.Language.Theory.Imp
#check FirstOrder.Language.Theory.IsSatisfiable
#check FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#check FirstOrder.Language.LHom
#check FirstOrder.Language.LHom.onBoundedFormula
#check FirstOrder.Language.LHom.onSentence
#check FirstOrder.Language.LHom.realize_onSentence
#check FirstOrder.Language.LHom.sumInl
#check FirstOrder.Language.LHom.sumInr
#check FirstOrder.Language.LHom.sumMap
#check LanguageSupport.SymbolSupport
#check LanguageSupport.TermSupported
#check LanguageSupport.BoundedFormulaSupported
#check LanguageSupport.sentenceSupported_range
#check LanguageSupport.commonBoundary_eq
#check ProofCalculus.Derivation
#check ProofCalculus.SmallDerivation
#check ProofCalculus.TheoryDerivation
#check ProofCalculus.Derivation.sound
#check ProofCalculus.theoryDerivation_semanticConsequence
#check ProofCalculus.smallSentenceDerivation_semanticConsequence_singleton
#check ProofCalculus.semanticConsequence_iff_theoryImp
#check ProofCalculus.SemanticToDerivabilityBridge
#check ProofCalculus.SemanticToDerivabilityBridge.derivationOfCraigPremise
#check ProofCalculus.SemanticToDerivabilityBridge.theoryDerivationOfCraigPremise
#check ProofCalculus.c004CompletenessBridgeStatus_eq
#check ProofCalculus.Derivation.CutFree
#check ProofCalculus.Derivation.cutFree
#check ProofCalculus.Derivation.cutFreeStructuralInduction
#check ProofCalculus.CutFreeDerivation
#check ProofCalculus.Derivation.toCutFree
#check ProofCalculus.Derivation.leafCount_toCutFree
#check ProofCalculus.c005CutStructuralStatus_eq
#check ProofCalculus.InterpolantExtractionRules
#check ProofCalculus.InterpolantExtractionRules.extract
#check ProofCalculus.InterpolantExtractionSupportInvariant
#check ProofCalculus.InterpolantExtractionRules.extract_supported
#check ProofCalculus.InterpolantExtractionRules.extractSentence_supported
#check ProofCalculus.InterpolantExtractionRules.extractSentence_totalRightBoundary_supported
#check ProofCalculus.c006ExtractionStatus_eq
#check ProofCalculus.extractedInterpolantCandidate
#check ProofCalculus.isInterpolant_iff_left_right
#check ProofCalculus.isInterpolant_of_left_right
#check ProofCalculus.ExtractedInterpolantTerminalObligations
#check ProofCalculus.extractedInterpolantCandidate_isInterpolant
#check ProofCalculus.extractedInterpolantCandidate_left
#check ProofCalculus.extractedInterpolantCandidate_right
#check ProofCalculus.c007TerminalObligationsStatus_eq

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.ModelTheory.Syntax",
  "Mathlib.ModelTheory.Semantics",
  "Mathlib.ModelTheory.LanguageMap",
  "Mathlib.ModelTheory.Satisfiability",
  "Mathlib.ModelTheory.Equivalence",
  "Mathlib.ModelTheory.Types",
  "Mathlib.ModelTheory.Ultraproducts",
  "Mathlib.ModelTheory.Skolem",
  "Mathlib.ModelTheory.Definability"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "FirstOrder.Language",
  "FirstOrder.Language.Sentence",
  "FirstOrder.Language.Theory",
  "FirstOrder.Language.Theory.Imp",
  "FirstOrder.Language.Theory.IsSatisfiable",
  "FirstOrder.Language.Theory.IsFinitelySatisfiable",
  "FirstOrder.Language.Theory.ModelsBoundedFormula",
  "FirstOrder.Language.Theory.ModelType",
  "FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable",
  "FirstOrder.Language.LHom",
  "FirstOrder.Language.LHom.onBoundedFormula",
  "FirstOrder.Language.LHom.onSentence",
  "FirstOrder.Language.LHom.realize_onSentence",
  "FirstOrder.Language.LHom.sumInl",
  "FirstOrder.Language.LHom.sumInr",
  "FirstOrder.Language.LHom.sumMap"
]

/-- Search terms that did not locate a terminal Craig interpolation theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "Craig",
  "Interpolation",
  "interpol",
  "Robinson",
  "Beth",
  "cut elimination",
  "sequent",
  "proof system",
  "interpolant"
]

end S1_M_298
end Stage1
end AwesomeTheorems
