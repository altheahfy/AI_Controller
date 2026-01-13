**Language / 言語**
- [English](#English)
- [日本語](#日本語)

## English
# AI_Controller (K-MAD)

> **“Code generation speed has finally overtaken human comprehension speed.”**

**AI_Controller** is a reference implementation of **K-MAD**  
(*Knowledge-Constrained Method for AI-Driven Development*).

K-MAD is for engineers who can no longer rely on traditional manual code reviews—  
because **generation has finally overtaken comprehension**.

This repository demonstrates how to keep AI-assisted development **governable,
reviewable, and accountable** when humans can no longer read or fully understand
all generated code.

---

## What this repository *is*

- A **governance-first control layer** for AI-assisted development
- A concrete demonstration of K-MAD principles in practice
- A human-in-the-loop workflow where:
  - AI performs generation and modification
  - Humans perform **explicit approval and responsibility**
- A minimal, inspectable implementation focused on **decision structure**, not automation tricks

This repository exists to show **how AI should be constrained**, not how fast it can generate code.

---

## What this repository is *not*

- Not a framework or library
- Not a turnkey automation tool
- Not an AI coding assistant
- Not a replacement for engineering judgment

AI_Controller does **not** try to make AI “smarter.”  
It exists to make **human responsibility explicit**.

---

## Core idea: governance-first AI development

K-MAD starts from a simple observation:

> Reviewing every line of AI-generated code is no longer realistic.

Instead of attempting exhaustive code-level review, K-MAD shifts the focus to
**decision-level governance**:

- Humans approve *decisions and boundaries*, not raw output
- Constraints and rules are treated as executable system logic
- AI operates only within explicitly defined limits
- Responsibility is never delegated to the AI

This repository shows how those principles can be enforced **structurally**.

---

## How this repository is intended to be used (high level)

- Engineers explore the structure and flow of governance-first AI control
- Users provide tutorial documents to an AI assistant
- The AI reads predefined constraints before performing generation
- Humans review outcomes at **explicit approval points**

Detailed operational steps are documented separately and are intended to be
*read by the AI itself*, not memorized by humans.

---

## Repository structure (high-level)

- `src/`  
  Executable logic, including pipeline definitions and governance rules.  
  **Key concept:** these files are treated as **system logic for the AI**, not merely
  documentation for humans. The AI reads them to understand what it is *allowed* to do.

- `docs/`  
  Tutorials and contextual explanations intended to be provided to AI assistants.

---

## Where to learn more

A full conceptual explanation of K-MAD—including its motivation, design philosophy,
and implications at scale—is available in the main article:

👉 **[Full article URL — (https://altheahfy.github.io/k-mad-en-engineers/)]**

Title:  
**“K-MAD is for those who can no longer rely on manual code reviews—because Generation has finally overtaken Comprehension.”**

## Related Projects

The following repositories demonstrate practical outcomes and supporting systems related to K-MAD.

- **RephraseUI**  
  A grammar-aware UI built on structured sentence decomposition.  
  UI: https://altheahfy.github.io/Rephrase_ui_public/training/index.html
  Repository: https://github.com/altheahfy/Rephrase_ui_public

- **Sentence Auto-Structuring System (Documentation)**  
  Materials and architectural notes for the sentence analysis system used in Rephrase.  
  UI: https://altheahfy.github.io/The-Automated-Sentence-Structuring-System_Public/
  Repository: https://github.com/yourname/sentence-structuring-docs

---

## Trademark & License

**“K-MAD”** is a trademark currently under application.  
This repository does not grant any rights to use the trademark in commercial products,
services, or branding.

This repository is provided under a restricted license.  
See the `LICENSE` file for details.


## 日本語

**AI_Controller** は、**K-MAD**  
（*Knowledge-Constrained Method for AI-Driven Development*）の考え方を示すためのリファレンス実装です。

エンジニアは、もはや従来の手作業によるコードレビューに頼ることができなくなってきています。なぜなら、**コード生成速度が人間の理解速度を明確に上回ってしまった**からです。K-MAD は、そんなエンジニアのための方法論です。

本リポジトリは、  
人間がすべての生成コードを読み切れない状況においても、  
AI支援開発を **統治可能（governable）・検証可能（reviewable）・責任所在が明確な状態（accountable）**
に保つための考え方と構造を示します。

---

## このリポジトリは何を示すものか？

- AI支援開発における **ガバナンス優先（governance-first）** の制御レイヤ
- K-MAD の思想を具体的な構造として示す最小限の実装
- 次の役割分担を前提とした人間参加型ワークフロー：
  - AI：生成・修正を行う
  - 人間：**明示的な承認と責任判断**を行う
- 自動化の巧妙さではなく、**意思決定構造**に焦点を当てた設計

本リポジトリの目的は、  
「AIをより賢くすること」ではなく、  
**AIをどのように制約すべきかを示すこと**にあります。

---

## このリポジトリが該当しないもの

- フレームワークやライブラリではありません
- そのまま使える自動化ツールではありません
- AIコーディング支援ツールではありません
- エンジニアの判断を置き換えるものではありません

AI_Controller は、  
**人間の責任を明示的に残すため**に存在します。

---

## 中核となる考え方：ガバナンス優先のAI開発

K-MAD は、次の観察から出発しています。

> AIが生成するコード量に対して、  
> 人間がそれをすべて確認することは、もはや現実的ではありません。

そこで K-MAD は、  
**コード単位の網羅的レビュー**ではなく、  
**意思決定単位のガバナンス**へと重心を移します。

- 人間が承認するのは、生成物そのものではなく「判断と境界」
- 制約やルールは、実行可能なシステムロジックとして扱う
- AIは、明示的に定義された範囲内でのみ動作する
- 責任は決してAIに委譲されない

本リポジトリは、これらの原則を  
**構造として実装する一つの方法**を示します。

---

## 想定される利用方法（概要）

- エンジニアは、ガバナンス優先型AI制御の構造を確認する
- ユーザーは、チュートリアル文書をAIに与える
- AIは、生成前に定義済みの制約を読み込む
- 人間は、**明示的な承認ポイント**で結果を判断する

詳細な手順は別途ドキュメント化されており、  
それらは **人間が記憶するためではなく、AIに読ませること**を前提としています。

---

## リポジトリ構成（概要）

- `src/`  
  パイプライン定義やガバナンスルールを含む実行ロジック。  
  **重要な点として、これらは人間向けの説明資料ではなく、AIにとっての「許可範囲」を定義するシステムロジックとして扱われることを前提としています。**

- `docs/`  
  AIに与えることを想定したチュートリアルや補足説明。

---

## 詳細について

K-MAD の背景、設計思想、そしてスケールしたAI開発における課題については、
以下の本稿で詳しく解説しています。

👉 **[本稿URL: (https://altheahfy.github.io/k-mad-jp-engineers/)]**

タイトル：  
**従来の手作業によるコードレビューに頼ることができなくなったエンジニアのための方法論「K-MAD」～コード生成速度が人間の理解速度を上回る時代へ向けて～**

---

## 商標・ライセンスについて

**「K-MAD」** は現在、商標出願中です。  
本リポジトリは、商標の商用利用権を付与するものではありません。

本リポジトリは制限付きライセンスのもとで提供されています。  
詳細は `LICENSE` ファイルを参照してください。