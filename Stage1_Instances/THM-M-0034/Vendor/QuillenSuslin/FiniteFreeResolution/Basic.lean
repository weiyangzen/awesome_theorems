/-
Copyright (c) 2026 Yongle Hu. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Yongle Hu
-/
/- Port notice: modified for the repository's pinned Lean 4.29/mathlib APIs.
The exact compatibility edits are recorded in `../../../PORT_PROVENANCE.md`. -/
import Mathlib.RingTheory.Finiteness.Prod
import Mathlib.RingTheory.PicardGroup

universe u v w

variable {R : Type u} [CommRing R]

/-- `HasFiniteFreeResolutionLength R P n` means `P` admits a free resolution of length `n`
by finitely generated free modules. We use the convention that length `0` means `P` itself is
finitely generated and free, and the successor step is given by a surjection from a finitely
generated free module with kernel admitting a shorter resolution. -/
inductive HasFiniteFreeResolutionLength (R : Type u) [CommRing R] :
    ∀ (P : Type u), [AddCommGroup P] → [Module R P] → ℕ → Prop
  | zero (P : Type u) [AddCommGroup P] [Module R P] [Module.Finite R P] [Module.Free R P] :
      HasFiniteFreeResolutionLength R P 0
  | succ (P : Type u) [AddCommGroup P] [Module R P] (n : ℕ)
      (F : Type u) [AddCommGroup F] [Module R F] [Module.Finite R F] [Module.Free R F]
      (f : F →ₗ[R] P) (hf : Function.Surjective f)
      (hker : HasFiniteFreeResolutionLength R (LinearMap.ker f) n) :
      HasFiniteFreeResolutionLength R P (n + 1)

theorem module_finite_of_hasFiniteFreeResolutionLength {P : Type u} [AddCommGroup P] [Module R P]
    {n : ℕ} (hn : HasFiniteFreeResolutionLength R P n) : Module.Finite R P := by
  induction hn with
  | zero P => infer_instance
  | succ P n F f hf hker ih => exact Module.Finite.of_surjective f hf

/-- A module `P` over a commutative ring `R` has a finite free resolution if it has a resolution
of some finite length by finitely generated free `R`-modules. -/
def HasFiniteFreeResolution (R : Type u) (P : Type v)
    [CommRing R] [AddCommGroup P] [Module R P] : Prop :=
  ∃ (F : Type u) ( _ : AddCommGroup F) (_ : Module R F) (_ : Module.Finite R F)
    (_ : Module.Free R F) (f : F →ₗ[R] P) (_ : Function.Surjective f) (n : ℕ),
      HasFiniteFreeResolutionLength R (LinearMap.ker f) n

/-- A finitely generated free module has a finite free resolution (of length `0`). -/
theorem hasFiniteFreeResolution_of_finite_of_free (P : Type v) [AddCommGroup P] [Module R P]
    [Module.Finite R P] [Module.Free R P] : HasFiniteFreeResolution R P := by
  let ι := Module.Free.ChooseBasisIndex R P
  let b : Module.Basis ι R P := Module.Free.chooseBasis R P
  let n : ℕ := Fintype.card ι
  let eι : Fin n ≃ ι := (Fintype.equivFin ι).symm
  have ePi : (ι → R) ≃ₗ[R] (Fin n → R) := (LinearEquiv.piCongrLeft R (fun _ : ι => R) eι).symm
  have eP : (Fin n → R) ≃ₗ[R] P := (b.equivFun.trans ePi).symm
  have : Subsingleton eP.toLinearMap.ker := Submodule.subsingleton_iff_eq_bot.mpr eP.ker
  exact ⟨Fin n → R, inferInstance, inferInstance, inferInstance, inferInstance, eP.toLinearMap,
    eP.surjective, 0, HasFiniteFreeResolutionLength.zero eP.toLinearMap.ker⟩

private theorem hasFiniteFreeResolutionLength_of_linearEquiv_aux (P : Type u) [AddCommGroup P]
    [Module R P] {n : ℕ} (hn : HasFiniteFreeResolutionLength R P n) :
    ∀ {Q : Type u} [AddCommGroup Q] [Module R Q], (e : P ≃ₗ[R] Q) →
      HasFiniteFreeResolutionLength R Q n := by
  induction hn with
  | zero P =>
      intro Q _ _ e
      let : Module.Finite R Q := Module.Finite.of_surjective e.toLinearMap e.surjective
      let : Module.Free R Q := Module.Free.of_equiv e
      exact HasFiniteFreeResolutionLength.zero Q
  | succ P n F π hπ hker ih =>
      intro Q _ _ e
      exact HasFiniteFreeResolutionLength.succ Q n F (e.toLinearMap.comp π) (e.surjective.comp hπ)
        <| ih (LinearEquiv.ofEq (e.toLinearMap.comp π).ker π.ker (e.ker_comp π)).symm

theorem hasFiniteFreeResolutionLength_of_linearEquiv {P Q : Type u}
    [AddCommGroup P] [Module R P]
    [AddCommGroup Q] [Module R Q] (e : P ≃ₗ[R] Q)
    {n : ℕ} (hn : HasFiniteFreeResolutionLength R P n) : HasFiniteFreeResolutionLength R Q n :=
  hasFiniteFreeResolutionLength_of_linearEquiv_aux P hn e

/-- Transport `HasFiniteFreeResolution` along an `R`-linear equivalence. -/
theorem hasFiniteFreeResolution_of_linearEquiv {P : Type v} {Q : Type w} [AddCommGroup P]
    [Module R P] [AddCommGroup Q] [Module R Q]
    (e : P ≃ₗ[R] Q) (h : HasFiniteFreeResolution R P) : HasFiniteFreeResolution R Q := by
  rcases h with ⟨F, _, _, _, _, f, hf, n, hn⟩
  exact ⟨F, inferInstance, inferInstance, inferInstance, inferInstance, e.toLinearMap.comp f,
    e.surjective.comp hf, n,
      hasFiniteFreeResolutionLength_of_linearEquiv (LinearEquiv.ofEq _ _ (e.ker_comp f).symm) hn⟩

theorem hasFiniteFreeResolutionLength_of_hasFiniteFreeResolution
    (P : Type u) [AddCommGroup P] [Module R P] :
    HasFiniteFreeResolution R P → ∃ n : ℕ, HasFiniteFreeResolutionLength R P n := by
  rintro ⟨F, _, _, _, _, f, hf, n, hn⟩
  exact ⟨n + 1, HasFiniteFreeResolutionLength.succ P n F f hf hn⟩

-- add a lemma : P HasFiniteFreeResolution ↔ Shrink.{u} P HasFiniteFreeResolution
theorem hasFiniteFreeResolution_iff_shrink (P : Type v) [AddCommGroup P] [Module R P] [Small.{u} P] :
    HasFiniteFreeResolution R P ↔ HasFiniteFreeResolution R (Shrink.{u} P) :=
  ⟨hasFiniteFreeResolution_of_linearEquiv (Shrink.linearEquiv R P).symm,
    hasFiniteFreeResolution_of_linearEquiv (Shrink.linearEquiv R P)⟩

section ringEquiv

variable {A : Type u} {B : Type u} [CommRing A] [CommRing B]

attribute [local instance] RingHomInvPair.of_ringEquiv

noncomputable def semilinearEquiv_compHom (e : A ≃+* B) (M : Type v) [AddCommGroup M]
    [Module B M] :
    let : Module A M := Module.compHom M (e : A →+* B)
    M ≃ₛₗ[(e : A →+* B)] M := by
  let : Module A M := Module.compHom M (e : A →+* B)
  refine
    { toEquiv := Equiv.refl M
      map_add' := fun _ _ => rfl
      map_smul' := fun _ _ => rfl }

theorem moduleFinite_of_ringEquiv (e : A ≃+* B) (M : Type v) [AddCommGroup M] [Module B M]
    [Module.Finite B M] :
    let : Module A M := Module.compHom M e.toRingHom
    Module.Finite A M := by
  let : Module A M := Module.compHom M (e : A →+* B)
  have hfgB : (⊤ : Submodule B M).FG := Module.Finite.fg_top
  rcases (Submodule.fg_def.mp hfgB) with ⟨S, hSfin, hSspan⟩
  refine Module.Finite.of_fg_top <| (Submodule.fg_def).2 ⟨S, hSfin, ?_⟩
  apply le_antisymm le_top
  show (⊤ : Submodule A M) ≤ Submodule.span A S
  intro x hx
  have hxB : x ∈ Submodule.span B S := by simp [hSspan]
  have hBA : (Submodule.span B S : Set M) ⊆ (Submodule.span A S : Set M) := by
    intro y
    refine Submodule.span_induction
      (fun z hz => Submodule.subset_span hz) (by simp)
        (fun _ _ _ _ hz₁ hz₂ => by simpa using Submodule.add_mem (Submodule.span A S) hz₁ hz₂) ?_
    intro b z _ hz
    rcases e.surjective b with ⟨a, rfl⟩
    simpa [Module.compHom] using Submodule.smul_mem (Submodule.span A S) a hz
  exact hBA hxB

theorem hasFiniteFreeResolutionLength_of_ringEquiv (e : A ≃+* B) (P : Type u) [AddCommGroup P]
    [Module B P] {n : ℕ} (hn : HasFiniteFreeResolutionLength B P n) :
    let : Module A P := Module.compHom P e.toRingHom
    HasFiniteFreeResolutionLength A P n := by
  let : Module A P := Module.compHom P e.toRingHom
  induction hn with
  | zero P =>
      have : Module.Finite A P := moduleFinite_of_ringEquiv e P
      have : Module.Free A P :=
        (Module.Free.iff_of_equiv (semilinearEquiv_compHom e P)).2 inferInstance
      exact HasFiniteFreeResolutionLength.zero P
  | succ P n F f hf hker ih =>
      let : Module A F := Module.compHom F e.toRingHom
      have : Module.Finite A F := moduleFinite_of_ringEquiv e F
      have : Module.Free A F :=
        (Module.Free.iff_of_equiv (semilinearEquiv_compHom e F)).2 inferInstance
      let fA : F →ₗ[A] P :=
        { toFun := f
          map_add' := fun _ _ => by simp
          map_smul' := by
            intro a x
            show f ((e a) • x) = (e a) • f x
            simp }
      have hkerA : HasFiniteFreeResolutionLength A (LinearMap.ker fA) n := by simpa [fA] using ih
      exact HasFiniteFreeResolutionLength.succ P n F fA hf hkerA

theorem hasFiniteFreeResolution_of_ringEquiv (e : A ≃+* B) (P : Type v) [AddCommGroup P]
    [Module B P] (h : HasFiniteFreeResolution B P) :
    let : Module A P := Module.compHom P e.toRingHom
    HasFiniteFreeResolution A P := by
  let : Module A P := Module.compHom P e.toRingHom
  rcases h with ⟨F, _, _, _, _, f, hf, n, hn⟩
  let : Module A F := Module.compHom F e.toRingHom
  have : Module.Finite A F := moduleFinite_of_ringEquiv e F
  have : Module.Free A F :=
    (Module.Free.iff_of_equiv (semilinearEquiv_compHom e F)).2 inferInstance
  let fA : F →ₗ[A] P :=
    { toFun := f
      map_add' := fun _ _ => by simp
      map_smul' := by
        intro a x
        show f ((e a) • x) = (e a) • f x
        simp }
  have hnA : HasFiniteFreeResolutionLength A (LinearMap.ker fA) n := by
    simpa [fA] using hasFiniteFreeResolutionLength_of_ringEquiv e _ hn
  exact ⟨F, inferInstance, inferInstance, inferInstance, inferInstance, fA, hf, n, hnA⟩

theorem hasFiniteFreeResolution_of_ringEquiv_left (e : A ≃+* B) (P : Type v) [AddCommGroup P]
    [Module A P]
    (h : (let : Module B P := Module.compHom P e.symm.toRingHom; HasFiniteFreeResolution B P)) :
    HasFiniteFreeResolution A P := by
  let instA₀ : Module A P := inferInstance
  let instB : Module B P := Module.compHom P e.symm.toRingHom
  have hB : HasFiniteFreeResolution B P := by simpa using h
  let instA₁ : Module A P := Module.compHom P e.toRingHom
  have hA₁ : @HasFiniteFreeResolution A P _ _ instA₁ := by
    simpa [instA₁] using hasFiniteFreeResolution_of_ringEquiv e P hB
  have hinst : instA₁ = instA₀ := by
    refine Module.ext' instA₁ instA₀ ?_
    intro a x
    show (have := instA₀; (e.symm (e a)) • x) = _
    simp
  rw [hinst] at hA₁
  exact hA₁

theorem hasFiniteFreeResolution_of_ringEquiv_right (e : A ≃+* B) (P : Type v) [AddCommGroup P]
    [Module B P]
    (h : (let : Module A P := Module.compHom P e.toRingHom; HasFiniteFreeResolution A P)) :
    HasFiniteFreeResolution B P := by
  let instB₀ : Module B P := inferInstance
  let instA : Module A P := Module.compHom P e.toRingHom
  have hA : HasFiniteFreeResolution A P := by simpa using h
  let instB₁ : Module B P := Module.compHom P e.symm.toRingHom
  have hB₁ : @HasFiniteFreeResolution B P _ _ instB₁ := by
    simpa [instB₁] using hasFiniteFreeResolution_of_ringEquiv e.symm P hA
  have hinst : instB₁ = instB₀ := by
    refine Module.ext' instB₁ instB₀ ?_
    intro b x
    show (have := instB₀; (e (e.symm b)) • x) = _
    simp
  rw [hinst] at hB₁
  exact hB₁

variable {S : Type u} [CommRing S]

noncomputable def ringEquivULift : ULift.{w} S ≃+* S :=
  { toEquiv := Equiv.ulift
    map_mul' := fun _ _ => rfl
    map_add' := fun _ _ => rfl }

noncomputable def semilinearEquivULift (M : Type u) [AddCommGroup M] [Module S M] :
    ULift.{w} M ≃ₛₗ[(ringEquivULift (S := S) : ULift.{w} S →+* S)] M :=
  { toEquiv := Equiv.ulift
    map_add' := fun _ _ => rfl
    map_smul' := fun _ _ => rfl }

noncomputable def linearEquivULift (M : Type u) [AddCommGroup M] [Module S M] :
    ULift.{w} M ≃ₗ[S] M :=
  { toEquiv := Equiv.ulift
    map_add' := fun _ _ => rfl
    map_smul' := fun _ _ => rfl }

theorem moduleFinite_of_ringEquiv' {A : Type u} {B : Type v} [CommRing A] [CommRing B]
    (e : A ≃+* B) (M : Type w) [AddCommGroup M] [Module B M] [Module.Finite B M] :
    let : Module A M := Module.compHom M e.toRingHom
    Module.Finite A M := by
  let : Module A M := Module.compHom M e.toRingHom
  have hfgB : (⊤ : Submodule B M).FG := Module.Finite.fg_top
  rcases (Submodule.fg_def.mp hfgB) with ⟨T, hTfin, hTspan⟩
  refine Module.Finite.of_fg_top <| (Submodule.fg_def).2 ⟨T, hTfin, ?_⟩
  apply le_antisymm le_top
  show (⊤ : Submodule A M) ≤ Submodule.span A T
  intro x hx
  have hxB : x ∈ Submodule.span B T := by simp [hTspan]
  have hBA : (Submodule.span B T : Set M) ⊆ (Submodule.span A T : Set M) := by
    intro y
    refine Submodule.span_induction
      (fun z hz => Submodule.subset_span hz) (by simp)
        (fun _ _ _ _ hz₁ hz₂ => by simpa using Submodule.add_mem (Submodule.span A T) hz₁ hz₂) ?_
    intro b z _ hz
    rcases e.surjective b with ⟨a, rfl⟩
    simpa [Module.compHom] using Submodule.smul_mem (Submodule.span A T) a hz
  exact hBA hxB

theorem hasFiniteFreeResolutionLength_ulift {P : Type u} [AddCommGroup P] [Module S P] {n : ℕ}
    (hn : HasFiniteFreeResolutionLength S P n) :
    HasFiniteFreeResolutionLength (ULift.{w} S) (ULift.{w} P) n := by
  induction hn with
  | zero P =>
      have : Module.Free (ULift.{w} S) (ULift.{w} P) :=
        (Module.Free.iff_of_equiv (semilinearEquivULift P)).2 inferInstance
      have : Module.Finite (ULift.{w} S) (ULift.{w} P) := by
        have : Module.Finite S (ULift.{w} P) :=
          Module.Finite.equiv (linearEquivULift P).symm
        simpa using moduleFinite_of_ringEquiv' (B := S) ringEquivULift (ULift.{w} P)
      exact HasFiniteFreeResolutionLength.zero (ULift.{w} P)
  | succ P n F f hf hker ih =>
      let f' : ULift.{w} F →ₗ[ULift.{w} S] ULift.{w} P :=
        { toFun := fun x => ULift.up (f x.down)
          map_add' := by
            intro x y
            ext
            simp [f.map_add]
          map_smul' := by
            intro a x
            ext
            simp [f.map_smul] }
      have hf' : Function.Surjective f' := by
        intro y
        rcases hf y.down with ⟨x, hx⟩
        refine ⟨ULift.up x, ?_⟩
        ext
        simp [f', hx]
      have : Module.Free (ULift.{w} S) (ULift.{w} F) :=
        (Module.Free.iff_of_equiv (semilinearEquivULift F)).2 inferInstance
      have : Module.Finite (ULift.{w} S) (ULift.{w} F) := by
        have : Module.Finite S (ULift.{w} F) :=
          Module.Finite.equiv (linearEquivULift F).symm
        simpa using moduleFinite_of_ringEquiv' (B := S) ringEquivULift (ULift.{w} F)
      have hk' : HasFiniteFreeResolutionLength (ULift.{w} S) (LinearMap.ker f') n := by
        have hk0 :
            HasFiniteFreeResolutionLength (ULift.{w} S) (ULift.{w} (LinearMap.ker f)) n := by
          simpa using ih
        let eKer : ULift.{w} (LinearMap.ker f) ≃ₗ[ULift.{w} S] LinearMap.ker f' :=
          { toEquiv :=
              { toFun := fun x => ⟨ULift.up x.down.1, by
                  ext
                  simp [f']⟩
                invFun := fun y =>
                  ULift.up ⟨y.1.down, by
                    have hy : f' y.1 = 0 := (LinearMap.mem_ker).1 y.2
                    dsimp [f'] at hy
                    have hy' : f y.1.down = 0 := by simpa using congrArg ULift.down hy
                    exact (LinearMap.mem_ker).2 hy'⟩
                left_inv := fun _ => by congr
                right_inv := fun y => by congr }
            map_add' := fun _ _ => by congr
            map_smul' := fun _ _ => by congr }
        exact hasFiniteFreeResolutionLength_of_linearEquiv eKer hk0
      exact HasFiniteFreeResolutionLength.succ (ULift.{w} P) n (ULift.{w} F) f' hf' hk'

theorem hasFiniteFreeResolution_ulift (P : Type v) [AddCommGroup P] [Module S P]
    (h : HasFiniteFreeResolution S P) : HasFiniteFreeResolution (ULift.{w} S) P := by
  rcases h with ⟨F, _, _, _, _, f, hf, n, hn⟩
  let f' : ULift.{w} F →ₗ[ULift.{w} S] P :=
    { toFun := fun x => f x.down
      map_add' := fun _ _ => by simp
      map_smul' := fun _ _ => by simp }
  have hf' : Function.Surjective f' := by
    intro y
    rcases hf y with ⟨x, rfl⟩
    exact ⟨ULift.up x, rfl⟩
  have hn' : HasFiniteFreeResolutionLength (ULift.{w} S) (LinearMap.ker f') n := by
    have hk0 : HasFiniteFreeResolutionLength (ULift.{w} S) (ULift.{w} (LinearMap.ker f)) n := by
      simpa using hasFiniteFreeResolutionLength_ulift hn
    let eKer :
        ULift.{w} (LinearMap.ker f) ≃ₗ[ULift.{w} S] LinearMap.ker f' :=
      { toEquiv :=
          { toFun := fun x => ⟨ULift.up x.down.1, by simp [f']⟩
            invFun := fun y =>
            ULift.up ⟨y.1.down, by
              have hy : f' y.1 = 0 := (LinearMap.mem_ker).1 y.2
              dsimp [f'] at hy
              exact (LinearMap.mem_ker).2 hy⟩
            left_inv := fun _ => by congr
            right_inv := fun _ => by congr }
        map_add' := fun _ _ => by congr
        map_smul' := fun _ _ => by congr }
    exact hasFiniteFreeResolutionLength_of_linearEquiv eKer hk0
  have : Module.Free (ULift.{w} S) (ULift.{w} F) :=
    (Module.Free.iff_of_equiv (semilinearEquivULift F)).2 inferInstance
  have : Module.Finite (ULift.{w} S) (ULift.{w} F) := by
    have : Module.Finite S (ULift.{w} F) := Module.Finite.equiv (linearEquivULift F).symm
    simpa using moduleFinite_of_ringEquiv' (B := S) ringEquivULift (ULift.{w} F)
  exact ⟨ULift.{w} F, inferInstance, inferInstance, inferInstance, inferInstance, f', hf', n, hn'⟩

end ringEquiv

section exact_seq

/-- Extract a surjection `F →ₗ[R] P` from a finite free resolution of `P`.
For length `0` we use the identity map. -/
theorem exists_surjective_of_hasFiniteFreeResolutionLength (P : Type u)
    [AddCommGroup P] [Module R P] {n : ℕ} (hn : HasFiniteFreeResolutionLength R P n) :
      ∃ (F : Type u) (_ : AddCommGroup F) (_ : Module R F) (_ : Module.Finite R F)
        (_ : Module.Free R F) (π : F →ₗ[R] P), Function.Surjective π ∧
          HasFiniteFreeResolutionLength R (LinearMap.ker π) (Nat.pred n) := by
  cases hn with
  | zero P =>
      refine ⟨P, inferInstance, inferInstance, inferInstance, inferInstance, LinearMap.id,
          Function.surjective_id, ?_⟩
      simpa using (HasFiniteFreeResolutionLength.zero (⊥ : Submodule R P))
  | succ P n F π hπ hker =>
      refine ⟨F, inferInstance, inferInstance, inferInstance, inferInstance, π, hπ, ?_⟩
      simpa using hker

theorem hasFiniteFreeResolution_of_hasFiniteFreeResolutionLength
    (P : Type u) [AddCommGroup P] [Module R P] :
    (∃ n : ℕ, HasFiniteFreeResolutionLength R P n) → HasFiniteFreeResolution R P := by
  rintro ⟨n, hn⟩
  rcases exists_surjective_of_hasFiniteFreeResolutionLength P hn with
    ⟨F, _, _, _, _, π, hπ, hker⟩
  exact ⟨F, inferInstance, inferInstance, inferInstance, inferInstance, π, hπ, Nat.pred n, hker⟩

/-- Horseshoe lemma for finite free resolutions (2-out-of-3: left + right ⇒ middle). -/
theorem hasFiniteFreeResolution_of_shortExact_of_left_of_right_length (P₁ P₂ P₃ : Type u)
    [AddCommGroup P₁] [Module R P₁] [AddCommGroup P₂] [Module R P₂] [AddCommGroup P₃] [Module R P₃]
    {f : P₁ →ₗ[R] P₂} {g : P₂ →ₗ[R] P₃} (hf : Function.Injective f) (hg : Function.Surjective g)
    (h : Function.Exact f g) {n₁ n₃ : ℕ} (h₁ : HasFiniteFreeResolutionLength R P₁ n₁)
      (h₃ : HasFiniteFreeResolutionLength R P₃ n₃) : HasFiniteFreeResolution R P₂ := by
  induction h₁ generalizing P₂ P₃ g n₃ with
  | zero P₁ =>
      rcases exists_surjective_of_hasFiniteFreeResolutionLength P₃ h₃ with
        ⟨F₃, _, _, _, _, π₃, hπ₃, hK₃⟩
      obtain ⟨l, hl⟩ := Module.projective_lifting_property g π₃ hg
      let φ : (P₁ × F₃) →ₗ[R] P₂ := f.coprod l
      have hφsurj : Function.Surjective φ := by
        intro p₂
        rcases hπ₃ (g p₂) with ⟨y₃, hy₃⟩
        have hg0 : g (p₂ - l y₃) = 0 := by
          have hgl : g (l y₃) = π₃ y₃ := by
            simpa [LinearMap.comp_apply] using congrArg (fun m => m y₃) hl
          simp [map_sub, hgl, hy₃]
        have : p₂ - l y₃ ∈ LinearMap.ker g := hg0
        have hker : LinearMap.ker g = LinearMap.range f := h.linearMap_ker_eq
        rcases (show p₂ - l y₃ ∈ LinearMap.range f by simpa [hker] using this) with ⟨x₁, hx₁⟩
        exact ⟨(x₁, y₃), by simp [φ, LinearMap.coprod_apply, hx₁]⟩
      let p : (LinearMap.ker φ) →ₗ[R] (LinearMap.ker π₃) :=
        LinearMap.codRestrict (LinearMap.ker π₃)
          ((LinearMap.snd R P₁ F₃).comp (Submodule.subtype (LinearMap.ker φ))) (by
            intro y
            have hy : φ y.1 = 0 := y.2
            have hgf : g.comp f = 0 := h.linearMap_comp_eq_zero
            have hgf' : g (f y.1.1) = 0 := by
              simpa [LinearMap.comp_apply] using congrArg (fun m => m y.1.1) hgf
            have hgl : g (l y.1.2) = π₃ y.1.2 := by
              simpa [LinearMap.comp_apply] using congrArg (fun m => m y.1.2) hl
            have hgy : g (φ y.1) = 0 := by simp [hy]
            have hgl0 : g (l y.1.2) = 0 := by
              simpa [hgf'] using (g.map_add (f y.1.1) (l y.1.2)).symm.trans hgy
            have : π₃ y.1.2 = 0 := by
              calc _ = g (l y.1.2) := by simpa using hgl.symm
                _ = 0 := hgl0
            simpa [LinearMap.mem_ker] using this)
      have hp_surj : Function.Surjective p := by
        intro z
        have hz : π₃ z.1 = 0 := z.2
        have : g (l z.1) = 0 := by
          have : g (l z.1) = π₃ z.1 := by
            simpa [LinearMap.comp_apply] using congrArg (fun m => m z.1) hl
          simp [this, hz]
        have hker : LinearMap.ker g = LinearMap.range f := h.linearMap_ker_eq
        have : l z.1 ∈ LinearMap.ker g := by simpa [LinearMap.mem_ker] using this
        rcases (show l z.1 ∈ LinearMap.range f by simpa [hker] using this) with ⟨x₁, hx₁⟩
        refine ⟨⟨(-x₁, z.1), ?_⟩, ?_⟩
        · have : f (-x₁) + l z.1 = 0 := by simp [map_neg, hx₁]
          simpa [φ, LinearMap.mem_ker, LinearMap.coprod_apply] using this
        · apply Subtype.ext
          simp [p]
      have hp_inj : Function.Injective p := by
        intro x y hxy
        apply Subtype.ext
        have h2 : x.1.2 = y.1.2 := by simpa [p] using congrArg Subtype.val hxy
        have h1 : x.1.1 = y.1.1 := by
          have hx : φ x.1 = 0 := x.2
          have hy : φ y.1 = 0 := y.2
          have : f x.1.1 = f y.1.1 := by
            calc _ = -l x.1.2 := (eq_neg_iff_add_eq_zero).2 hx
              _ = -l y.1.2 := by simp [h2]
              _ = f y.1.1 := ((eq_neg_iff_add_eq_zero).2 hy).symm
          exact hf this
        exact Prod.ext h1 h2
      exact hasFiniteFreeResolution_of_hasFiniteFreeResolutionLength P₂
        ⟨Nat.pred n₃ + 1,
          HasFiniteFreeResolutionLength.succ P₂ (Nat.pred n₃) (P₁ × F₃) φ hφsurj <|
            hasFiniteFreeResolutionLength_of_linearEquiv
              (LinearEquiv.ofBijective p ⟨hp_inj, hp_surj⟩).symm hK₃⟩
  | succ P₁ n F₁ π₁ hπ₁ hK₁ ih =>
      rcases exists_surjective_of_hasFiniteFreeResolutionLength P₃ h₃ with
        ⟨F₃, _, _, _, _, π₃, hπ₃, hK₃⟩
      obtain ⟨l, hl⟩ := Module.projective_lifting_property g π₃ hg
      let φ : (F₁ × F₃) →ₗ[R] P₂ := (f.comp π₁).coprod l
      have hφsurj : Function.Surjective φ := by
        intro p₂
        rcases hπ₃ (g p₂) with ⟨y₃, hy₃⟩
        have hg0 : g (p₂ - l y₃) = 0 := by
          have hgl : g (l y₃) = π₃ y₃ := by
            simpa [LinearMap.comp_apply] using congrArg (fun m => m y₃) hl
          simp [map_sub, hgl, hy₃]
        have : p₂ - l y₃ ∈ LinearMap.ker g := hg0
        have hker : LinearMap.ker g = LinearMap.range f := h.linearMap_ker_eq
        rcases (show p₂ - l y₃ ∈ LinearMap.range f by simpa [hker] using this) with ⟨x₁, hx₁⟩
        rcases hπ₁ x₁ with ⟨y₁, rfl⟩
        refine ⟨(y₁, y₃), ?_⟩
        simp [φ, LinearMap.coprod_apply, LinearMap.comp_apply, hx₁]
      -- Define the short exact sequence `ker π₁ → ker φ → ker π₃`.
      let i : (LinearMap.ker π₁) →ₗ[R] (LinearMap.ker φ) :=
        LinearMap.codRestrict (LinearMap.ker φ)
          ((LinearMap.inl R F₁ F₃).comp (Submodule.subtype (LinearMap.ker π₁))) (by
            intro x
            have hx : π₁ x.1 = 0 := x.2
            simp [φ, LinearMap.mem_ker, LinearMap.coprod_apply, LinearMap.comp_apply, hx])
      let p : (LinearMap.ker φ) →ₗ[R] (LinearMap.ker π₃) :=
        LinearMap.codRestrict (LinearMap.ker π₃)
          ((LinearMap.snd R F₁ F₃).comp (Submodule.subtype (LinearMap.ker φ))) (by
            intro y
            have hgf : g.comp f = 0 := h.linearMap_comp_eq_zero
            have hgf' : g (f (π₁ y.1.1)) = 0 := by
              simpa [LinearMap.comp_apply] using congrArg (fun m => m (π₁ y.1.1)) hgf
            have hgl : g (l y.1.2) = π₃ y.1.2 := by
              simpa [LinearMap.comp_apply] using congrArg (fun m => m y.1.2) hl
            have hgy : g (φ y.1) = 0 := by simp
            have hsum : g (f (π₁ y.1.1)) + g (l y.1.2) = 0 := by
              calc _ = g (f (π₁ y.1.1) + l y.1.2) := (g.map_add (f (π₁ y.1.1)) (l y.1.2)).symm
                _ = 0 := hgy
            have hgl0 : g (l y.1.2) = 0 := by simpa [hgf'] using hsum
            have : π₃ y.1.2 = 0 := by
              calc _ = g (l y.1.2) := by simpa using hgl.symm
                _ = 0 := hgl0
            simpa [LinearMap.mem_ker] using this)
      have hi : Function.Injective i := by
        intro x y hxy
        apply Subtype.ext
        exact congrArg Prod.fst (congrArg Subtype.val hxy)
      have hp : Function.Surjective p := by
        intro z
        have hz : π₃ z.1 = 0 := z.2
        have : g (l z.1) = 0 := by
          have : g (l z.1) = π₃ z.1 := by
            simpa [LinearMap.comp_apply] using congrArg (fun m => m z.1) hl
          simp [this, hz]
        have hker : LinearMap.ker g = LinearMap.range f := h.linearMap_ker_eq
        have : l z.1 ∈ LinearMap.ker g := by simpa [LinearMap.mem_ker] using this
        rcases (show l z.1 ∈ LinearMap.range f by simpa [hker] using this) with ⟨x₁, hx₁⟩
        rcases hπ₁ (-x₁) with ⟨y₁, hy₁⟩
        refine ⟨⟨(y₁, z.1), ?_⟩, ?_⟩
        · have : f (π₁ y₁) + l z.1 = 0 := by
            have : f (π₁ y₁) = -l z.1 := by
              simpa [hy₁, map_neg] using congrArg Neg.neg hx₁
            simp [this]
          simpa [φ, LinearMap.mem_ker, LinearMap.coprod_apply, LinearMap.comp_apply] using this
        · apply Subtype.ext
          simp [p]
      have hexact : Function.Exact i p := by
        rw [LinearMap.exact_iff]
        ext x
        constructor
        · intro hx
          have hx2 : x.1.2 = 0 := by
            have : p x = 0 := by simpa [LinearMap.mem_ker] using hx
            have : (p x).1 = 0 := congrArg Subtype.val this
            simpa [p] using this
          have hx1 : π₁ x.1.1 = 0 := by
            have hxφ : φ x.1 = 0 := x.2
            have hxφ' : f (π₁ x.1.1) + l x.1.2 = 0 := by
              have hxφ'' := hxφ
              dsimp [φ] at hxφ''
              simpa using hxφ''
            have hfEq : f (π₁ x.1.1) = -l x.1.2 := (eq_neg_iff_add_eq_zero).2 hxφ'
            have hf0 : f (π₁ x.1.1) = 0 := by simpa [hx2] using hfEq
            exact hf (by simpa using hf0)
          refine ⟨⟨x.1.1, hx1⟩, ?_⟩
          apply Subtype.ext
          ext
          · simp [i]
          · simp [i, hx2]
        · rintro ⟨x₁, rfl⟩
          apply Subtype.ext
          simp [p, i, LinearMap.codRestrict_apply]
      obtain ⟨m, hm⟩ := hasFiniteFreeResolutionLength_of_hasFiniteFreeResolution (LinearMap.ker φ) <|
        ih (LinearMap.ker φ) (LinearMap.ker π₃) hi hp hexact hK₃
      exact hasFiniteFreeResolution_of_hasFiniteFreeResolutionLength P₂
        ⟨m + 1, HasFiniteFreeResolutionLength.succ P₂ m (F₁ × F₃) φ hφsurj hm⟩

/-- In a short exact sequence `0 → P₁ → P₂ → P₃ → 0`, if `P₁` and `P₃` have finite free
resolutions, then so does `P₂`. -/
theorem hasFiniteFreeResolution_of_shortExact_of_left_of_right (P₁ P₂ P₃ : Type*)
    [AddCommGroup P₁] [Module R P₁] [AddCommGroup P₂] [Module R P₂] [AddCommGroup P₃] [Module R P₃]
    {f : P₁ →ₗ[R] P₂} {g : P₂ →ₗ[R] P₃} (hf : Function.Injective f) (hg : Function.Surjective g)
    (h : Function.Exact f g) (h₁ : HasFiniteFreeResolution R P₁)
    (h₃ : HasFiniteFreeResolution R P₃) : HasFiniteFreeResolution R P₂ := by
  rcases h₁ with ⟨F₁, _, _, _, _, π₁, hπ₁, n₁, hK₁⟩
  rcases h₃ with ⟨F₃, _, _, _, _, π₃, hπ₃, n₃, hK₃⟩
  obtain ⟨l, hl⟩ := Module.projective_lifting_property g π₃ hg
  let φ : (F₁ × F₃) →ₗ[R] P₂ := (f.comp π₁).coprod l
  have hφsurj : Function.Surjective φ := by
    intro p₂
    rcases hπ₃ (g p₂) with ⟨y₃, hy₃⟩
    have hg0 : g (p₂ - l y₃) = 0 := by
      have hgl : g (l y₃) = π₃ y₃ := by
        simpa [LinearMap.comp_apply] using congrArg (fun m => m y₃) hl
      simp [map_sub, hgl, hy₃]
    have : p₂ - l y₃ ∈ LinearMap.ker g := hg0
    have hker : LinearMap.ker g = LinearMap.range f := h.linearMap_ker_eq
    rcases (show p₂ - l y₃ ∈ LinearMap.range f by simpa [hker] using this) with ⟨x₁, hx₁⟩
    rcases hπ₁ x₁ with ⟨y₁, rfl⟩
    refine ⟨(y₁, y₃), ?_⟩
    simp [φ, LinearMap.coprod_apply, LinearMap.comp_apply, hx₁]
  -- Define the short exact sequence `ker π₁ → ker φ → ker π₃`.
  let i : (LinearMap.ker π₁) →ₗ[R] (LinearMap.ker φ) :=
    LinearMap.codRestrict (LinearMap.ker φ)
      ((LinearMap.inl R F₁ F₃).comp (Submodule.subtype (LinearMap.ker π₁))) (by
        intro x
        have hx : π₁ x.1 = 0 := x.2
        simp [φ, LinearMap.mem_ker, LinearMap.coprod_apply, LinearMap.comp_apply, hx])
  let p : (LinearMap.ker φ) →ₗ[R] (LinearMap.ker π₃) :=
    LinearMap.codRestrict (LinearMap.ker π₃)
      ((LinearMap.snd R F₁ F₃).comp (Submodule.subtype (LinearMap.ker φ))) (by
        intro y
        have hgf : g.comp f = 0 := h.linearMap_comp_eq_zero
        have hgf' : g (f (π₁ y.1.1)) = 0 := by
          simpa [LinearMap.comp_apply] using congrArg (fun m => m (π₁ y.1.1)) hgf
        have hgl : g (l y.1.2) = π₃ y.1.2 := by
          simpa [LinearMap.comp_apply] using congrArg (fun m => m y.1.2) hl
        have hgy : g (φ y.1) = 0 := by simp
        have hsum : g (f (π₁ y.1.1)) + g (l y.1.2) = 0 := by
          calc _ = g (f (π₁ y.1.1) + l y.1.2) := (g.map_add (f (π₁ y.1.1)) (l y.1.2)).symm
            _ = 0 := hgy
        have hgl0 : g (l y.1.2) = 0 := by simpa [hgf'] using hsum
        have : π₃ y.1.2 = 0 := by
          calc _ = g (l y.1.2) := by simpa using hgl.symm
            _ = 0 := hgl0
        simpa [LinearMap.mem_ker] using this)
  have hi : Function.Injective i := by
    intro x y hxy
    apply Subtype.ext
    exact congrArg Prod.fst (congrArg Subtype.val hxy)
  have hp : Function.Surjective p := by
    intro z
    have hz : π₃ z.1 = 0 := z.2
    have : g (l z.1) = 0 := by
      have : g (l z.1) = π₃ z.1 := by
        simpa [LinearMap.comp_apply] using congrArg (fun m => m z.1) hl
      simp [this, hz]
    have hker : LinearMap.ker g = LinearMap.range f := h.linearMap_ker_eq
    have : l z.1 ∈ LinearMap.ker g := by simpa [LinearMap.mem_ker] using this
    rcases (show l z.1 ∈ LinearMap.range f by simpa [hker] using this) with ⟨x₁, hx₁⟩
    rcases hπ₁ (-x₁) with ⟨y₁, hy₁⟩
    refine ⟨⟨(y₁, z.1), ?_⟩, ?_⟩
    · have : f (π₁ y₁) + l z.1 = 0 := by
        have : f (π₁ y₁) = -l z.1 := by
          simpa [hy₁, map_neg] using congrArg Neg.neg hx₁
        simp [this]
      simpa [φ, LinearMap.mem_ker, LinearMap.coprod_apply, LinearMap.comp_apply] using this
    · apply Subtype.ext
      simp [p]
  have hexact : Function.Exact i p := by
    rw [LinearMap.exact_iff]
    ext x
    constructor
    · intro hx
      have hx2 : x.1.2 = 0 := by
        have : p x = 0 := by simpa [LinearMap.mem_ker] using hx
        have : (p x).1 = 0 := congrArg Subtype.val this
        simpa [p] using this
      have hx1 : π₁ x.1.1 = 0 := by
        have hxφ : φ x.1 = 0 := x.2
        have hxφ' : f (π₁ x.1.1) + l x.1.2 = 0 := by
          have hxφ'' := hxφ
          dsimp [φ] at hxφ''
          simpa using hxφ''
        have hfEq : f (π₁ x.1.1) = -l x.1.2 := (eq_neg_iff_add_eq_zero).2 hxφ'
        have hf0 : f (π₁ x.1.1) = 0 := by simpa [hx2] using hfEq
        exact hf (by simpa using hf0)
      refine ⟨⟨x.1.1, hx1⟩, ?_⟩
      apply Subtype.ext
      ext
      · simp [i]
      · simp [i, hx2]
    · rintro ⟨x₁, rfl⟩
      apply Subtype.ext
      simp [p, i, LinearMap.codRestrict_apply]
  have hK₂ : HasFiniteFreeResolution R (LinearMap.ker φ) :=
    hasFiniteFreeResolution_of_shortExact_of_left_of_right_length
      (LinearMap.ker π₁) (LinearMap.ker φ) (LinearMap.ker π₃) hi hp hexact hK₁ hK₃
  rcases hasFiniteFreeResolutionLength_of_hasFiniteFreeResolution (LinearMap.ker φ) hK₂ with ⟨m, hm⟩
  exact ⟨F₁ × F₃, inferInstance, inferInstance, inferInstance, inferInstance, φ, hφsurj, m, hm⟩

/-- In a short exact sequence `0 → P₁ → P₂ → P₃ → 0`, if `P₁` and `P₂` have finite free
resolutions, then so does `P₃`. -/
theorem hasFiniteFreeResolution_of_shortExact_of_left_of_middle (P₁ P₂ P₃ : Type*)
    [AddCommGroup P₁] [Module R P₁] [AddCommGroup P₂] [Module R P₂] [AddCommGroup P₃] [Module R P₃]
    {f : P₁ →ₗ[R] P₂} {g : P₂ →ₗ[R] P₃} (hf : Function.Injective f) (hg : Function.Surjective g)
    (h : Function.Exact f g) (h₁ : HasFiniteFreeResolution R P₁)
    (h₂ : HasFiniteFreeResolution R P₂) : HasFiniteFreeResolution R P₃ := by
  rcases h₂ with ⟨F₂, _, _, _, _, π₂, hπ₂, n₂, hK₂len⟩
  have hK₂ : HasFiniteFreeResolution R (LinearMap.ker π₂) :=
    hasFiniteFreeResolution_of_hasFiniteFreeResolutionLength (LinearMap.ker π₂) ⟨n₂, hK₂len⟩
  let q : F₂ →ₗ[R] P₃ := g.comp π₂
  have hq : Function.Surjective q := hg.comp hπ₂
  -- Define the short exact sequence `ker π₂ → ker q → P₁`.
  let i : (LinearMap.ker π₂) →ₗ[R] (LinearMap.ker q) :=
    LinearMap.codRestrict (LinearMap.ker q) (Submodule.subtype (LinearMap.ker π₂)) (by
      intro x
      have hx : π₂ x.1 = 0 := x.2
      simp [q, LinearMap.mem_ker, LinearMap.comp_apply, hx])
  let e : P₁ ≃ₗ[R] LinearMap.range f := LinearEquiv.ofInjective f hf
  let toRange : (LinearMap.ker q) →ₗ[R] (LinearMap.range f) :=
    LinearMap.codRestrict (LinearMap.range f) (π₂.comp (Submodule.subtype (LinearMap.ker q))) <| by
      simpa using fun y hy => (h _).mp hy
  let p : (LinearMap.ker q) →ₗ[R] P₁ := e.symm.toLinearMap.comp toRange
  have hi : Function.Injective i := by
    intro x y hxy
    apply Subtype.ext
    simpa [i] using congrArg Subtype.val hxy
  have hp : Function.Surjective p := by
    intro x₁
    rcases hπ₂ (f x₁) with ⟨x, hx⟩
    have hgf : g.comp f = 0 := h.linearMap_comp_eq_zero
    have : g (f x₁) = 0 := by
      simpa [LinearMap.comp_apply] using congrArg (fun m => m x₁) hgf
    have hxL : x ∈ LinearMap.ker q := by
      simp [LinearMap.mem_ker, q, LinearMap.comp_apply, hx, this]
    refine ⟨⟨x, hxL⟩, e.injective <| Subtype.ext ?_⟩
    simp [p, toRange, e, hx, LinearMap.codRestrict_apply, LinearMap.comp_apply]
  have hexact : Function.Exact i p := by
    rw [LinearMap.exact_iff]
    ext y
    constructor
    · intro hy
      have hy0 : p y = 0 := by simpa [LinearMap.mem_ker] using hy
      have hyTo : toRange y = 0 := by
        have : e (p y) = e 0 := by simp [hy0]
        simp [p] at this
        exact this
      have hyπ : π₂ y.1 = 0 := by
        have : (toRange y).1 = 0 := congrArg Subtype.val hyTo
        simpa [toRange, LinearMap.codRestrict_apply, LinearMap.comp_apply] using this
      refine ⟨⟨y.1, hyπ⟩, ?_⟩
      apply Subtype.ext
      simp [i]
    · rintro ⟨x, rfl⟩
      have : π₂ x.1 = 0 := x.2
      show p (i x) = 0
      have hto : toRange (i x) = 0 := by
        apply Subtype.ext
        simp [toRange, i, this, LinearMap.codRestrict_apply, LinearMap.comp_apply]
      simp [p, hto]
  have hL : HasFiniteFreeResolution R (LinearMap.ker q) :=
    hasFiniteFreeResolution_of_shortExact_of_left_of_right (LinearMap.ker π₂) (LinearMap.ker q) P₁
      hi hp hexact hK₂ h₁
  rcases hasFiniteFreeResolutionLength_of_hasFiniteFreeResolution (LinearMap.ker q) hL with ⟨m, hm⟩
  exact ⟨F₂, inferInstance, inferInstance, inferInstance, inferInstance, q, hq, m, hm⟩

/-- In a short exact sequence `0 → P₁ → P₂ → P₃ → 0`, if `P₂` and `P₃` have finite free
resolutions, then so does `P₁`. -/
theorem hasFiniteFreeResolution_of_shortExact_of_middle_of_right (P₁ P₂ P₃ : Type*)
    [AddCommGroup P₁] [Module R P₁] [AddCommGroup P₂] [Module R P₂] [AddCommGroup P₃] [Module R P₃]
    {f : P₁ →ₗ[R] P₂} {g : P₂ →ₗ[R] P₃} (hf : Function.Injective f) (hg : Function.Surjective g)
    (h : Function.Exact f g) (h₂ : HasFiniteFreeResolution R P₂)
    (h₃ : HasFiniteFreeResolution R P₃) : HasFiniteFreeResolution R P₁ := by
  rcases h₂ with ⟨F₂, _, _, _, _, π₂, hπ₂, n₂, hK₂len⟩
  have hK₂ : HasFiniteFreeResolution R (LinearMap.ker π₂) :=
    hasFiniteFreeResolution_of_hasFiniteFreeResolutionLength (LinearMap.ker π₂) ⟨n₂, hK₂len⟩
  have hF₂ : HasFiniteFreeResolution R F₂ := hasFiniteFreeResolution_of_finite_of_free F₂
  let q : F₂ →ₗ[R] P₃ := g.comp π₂
  have hq : Function.Surjective q := hg.comp hπ₂
  rcases h₃ with ⟨F₃, _, _, _, _, π₃, hπ₃, n₃, hK₃len⟩
  have hK₃ : HasFiniteFreeResolution R (LinearMap.ker π₃) :=
    hasFiniteFreeResolution_of_hasFiniteFreeResolutionLength (LinearMap.ker π₃) ⟨n₃, hK₃len⟩
  have hF₃ : HasFiniteFreeResolution R F₃ := hasFiniteFreeResolution_of_finite_of_free F₃
  let d : (F₂ × F₃) →ₗ[R] P₃ := q.coprod (-π₃)
  let Kd := LinearMap.ker d
  -- Short exact sequence `ker π₃ → ker d → F₂`.
  let j : (LinearMap.ker π₃) →ₗ[R] Kd :=
    LinearMap.codRestrict Kd ((LinearMap.inr R F₂ F₃).comp (Submodule.subtype π₃.ker)) <| by
      intro y
      show d ((0 : F₂), y.1) = 0
      simp [d, LinearMap.coprod_apply]
  let pr₁ : Kd →ₗ[R] F₂ := (LinearMap.fst R F₂ F₃).comp (Submodule.subtype Kd)
  have hj : Function.Injective j := by
    intro x y hxy
    apply Subtype.ext
    simpa [j] using congrArg Prod.snd (congrArg Subtype.val hxy)
  have hpr₁ : Function.Surjective pr₁ := by
    intro x₂
    rcases hπ₃ (q x₂) with ⟨y₃, hy₃⟩
    have hx : d (x₂, y₃) = 0 := by simp [d, LinearMap.coprod_apply, hy₃]
    exact ⟨⟨(x₂, y₃), by simpa [LinearMap.mem_ker] using hx⟩, rfl⟩
  have hexact₁ : Function.Exact j pr₁ := by
    rw [LinearMap.exact_iff]
    ext x
    constructor
    · intro hx
      have hx0 : pr₁ x = 0 := by simpa [LinearMap.mem_ker] using hx
      have hxF₂ : x.1.1 = 0 := by simpa [pr₁] using hx0
      refine ⟨⟨x.1.2, ?_⟩, ?_⟩
      · have hxker : d x.1 = 0 := x.2
        have : π₃ x.1.2 = 0 := by
          have hxpair : x.1 = (0, x.1.2) := by
            ext <;> simp [hxF₂]
          have hxker' := hxker
          rw [hxpair] at hxker'
          have : d (0, x.1.2) = 0 := hxker'
          simpa [d, LinearMap.coprod_apply] using this
        simpa [LinearMap.mem_ker] using this
      · apply Subtype.ext
        ext <;> simp [j, hxF₂]
    · rintro ⟨y, rfl⟩
      show pr₁ (j y) = 0
      simp [pr₁, j, LinearMap.codRestrict_apply]
  have hKd : HasFiniteFreeResolution R Kd :=
    hasFiniteFreeResolution_of_shortExact_of_left_of_right (LinearMap.ker π₃) Kd F₂ hj hpr₁
      hexact₁ hK₃ hF₂
  obtain ⟨s, hs⟩ := Module.projective_lifting_property q π₃ hq
  -- Short exact sequence `F₃ → ker d → ker q`.
  let k : F₃ →ₗ[R] Kd := LinearMap.codRestrict Kd (LinearMap.prod s LinearMap.id) <| by
    intro y
    have hs' : q (s y) = π₃ y := by
      simpa [LinearMap.comp_apply] using congrArg (fun m => m y) hs
    show d (s y, y) = 0
    simp [d, LinearMap.coprod_apply, hs']
  let r0 : Kd →ₗ[R] F₂ := ((LinearMap.fst R F₂ F₃).comp (Submodule.subtype Kd)) -
    (s.comp ((LinearMap.snd R F₂ F₃).comp (Submodule.subtype Kd)))
  let r : Kd →ₗ[R] (LinearMap.ker q) := LinearMap.codRestrict (LinearMap.ker q) r0 <| by
    intro x
    have hxker : d x.1 = 0 := x.2
    have hxEq : q x.1.1 = π₃ x.1.2 := by
      dsimp [d] at hxker
      exact sub_eq_zero.mp (by simpa [sub_eq_add_neg, LinearMap.neg_apply] using hxker)
    have hs' : q (s x.1.2) = π₃ x.1.2 := by
      simpa [LinearMap.comp_apply] using congrArg (fun m => m x.1.2) hs
    simp [LinearMap.mem_ker, r0, map_sub, hxEq, hs', LinearMap.comp_apply]
  have hk : Function.Injective k := by
    intro x y hxy
    have : (k x).1.2 = (k y).1.2 := congrArg Prod.snd (congrArg Subtype.val hxy)
    simpa [k] using this
  have hr : Function.Surjective r := by
    intro z
    refine ⟨⟨(z.1, 0), ?_⟩, ?_⟩
    · have hz : q z.1 = 0 := z.2
      have : d (z.1, 0) = 0 := by simp [d, LinearMap.coprod_apply, hz]
      simpa [LinearMap.mem_ker] using this
    · apply Subtype.ext
      simp [r, r0, LinearMap.codRestrict_apply, LinearMap.comp_apply]
  have hexact₂ : Function.Exact k r := by
    rw [LinearMap.exact_iff]
    ext x
    constructor
    · intro hx
      have hx0 : r x = 0 := by simpa [LinearMap.mem_ker] using hx
      have hx0' : r0 x = 0 := congrArg Subtype.val hx0
      have hxEq : x.1.1 = s x.1.2 := by
        -- from `x.1.1 - s x.1.2 = 0`.
        have : x.1.1 - s x.1.2 = 0 := by
          simpa [r0, LinearMap.sub_apply, LinearMap.comp_apply] using hx0'
        exact sub_eq_zero.mp this
      refine ⟨x.1.2, ?_⟩
      apply Subtype.ext
      ext <;> simp [k, hxEq]
    · rintro ⟨y, rfl⟩
      apply Subtype.ext
      simp [r, r0, k, LinearMap.codRestrict_apply, LinearMap.comp_apply]
  have hL : HasFiniteFreeResolution R (LinearMap.ker q) :=
    hasFiniteFreeResolution_of_shortExact_of_left_of_middle F₃ Kd (LinearMap.ker q) hk hr hexact₂
      hF₃ hKd
  -- Finally, use the short exact sequence `ker π₂ → ker q → P₁`.
  let i : (LinearMap.ker π₂) →ₗ[R] (LinearMap.ker q) :=
    LinearMap.codRestrict (LinearMap.ker q) (Submodule.subtype (LinearMap.ker π₂)) <| by
      simp [q, LinearMap.mem_ker, LinearMap.comp_apply]
  let e : P₁ ≃ₗ[R] LinearMap.range f := LinearEquiv.ofInjective f hf
  let toRange : (LinearMap.ker q) →ₗ[R] (LinearMap.range f) :=
    LinearMap.codRestrict (LinearMap.range f) (π₂.comp (Submodule.subtype q.ker)) <| by
      simpa using fun y hy => (h _).mp hy
  let p : (LinearMap.ker q) →ₗ[R] P₁ := e.symm.toLinearMap.comp toRange
  have hi : Function.Injective i := by
    intro x y hxy
    apply Subtype.ext
    simpa [i] using congrArg Subtype.val hxy
  have hp : Function.Surjective p := by
    intro x₁
    rcases hπ₂ (f x₁) with ⟨x, hx⟩
    have hgf : g.comp f = 0 := h.linearMap_comp_eq_zero
    have : g (f x₁) = 0 := by simpa [LinearMap.comp_apply] using congrArg (fun m => m x₁) hgf
    have hxL : x ∈ LinearMap.ker q := by simp [q, LinearMap.comp_apply, hx, this]
    refine ⟨⟨x, hxL⟩, ?_⟩
    apply e.injective
    apply Subtype.ext
    simp [p, toRange, e, hx, LinearMap.codRestrict_apply, LinearMap.comp_apply]
  have hexact₃ : Function.Exact i p := by
    rw [LinearMap.exact_iff]
    ext y
    constructor
    · intro hy
      have hy0 : p y = 0 := by simpa [LinearMap.mem_ker] using hy
      have hyTo : toRange y = 0 := by
        have : e (p y) = e 0 := by simp [hy0]
        simp [p] at this
        exact this
      have hyπ : π₂ y.1 = 0 := by
        have : (toRange y).1 = 0 := congrArg Subtype.val hyTo
        simpa [toRange, LinearMap.codRestrict_apply, LinearMap.comp_apply] using this
      refine ⟨⟨y.1, hyπ⟩, ?_⟩
      apply Subtype.ext
      simp [i]
    · rintro ⟨x, rfl⟩
      have : π₂ x.1 = 0 := x.2
      show p (i x) = 0
      have hto : toRange (i x) = 0 := by
        apply Subtype.ext
        simp [toRange, i, this, LinearMap.codRestrict_apply, LinearMap.comp_apply]
      simp [p, hto]
  exact hasFiniteFreeResolution_of_shortExact_of_left_of_middle π₂.ker q.ker P₁ hi hp hexact₃ hK₂ hL

end exact_seq
