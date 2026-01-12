#!/usr/bin/env python3
"""
K-MAD セットアップスクリプト
初期セットアップを自動化（非エンジニア向け）

実行方法:
  python -m AI_Controller.setup

やること:
1. Git リポジトリルート検出
2. .gitignore に .snapshots/ 追記
3. .git/hooks/pre-commit を生成
4. governance_rules.json のテンプレート生成（未存在時のみ）
"""

import os
import sys
import subprocess
from pathlib import Path

# ========================================
# 出力関数（setup.py では絵文字を使わないので通常のprintでOK）
# ========================================

def safe_print(msg: str):
    """出力（setup.py では絵文字なし、日本語そのまま出力）"""
    print(msg)


# ========================================
# セットアップ処理
# ========================================

def detect_repo_root() -> Path | None:
    """Git リポジトリルートを検出"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        repo_root = Path(result.stdout.strip())
        safe_print(f"[OK] Git リポジトリ検出: {repo_root}")
        return repo_root
    except subprocess.CalledProcessError:
        safe_print("[WARN] Git リポジトリが見つかりません")
        safe_print("       カレントディレクトリをプロジェクトルートとして使用します")
        return Path.cwd()
    except FileNotFoundError:
        safe_print("[ERROR] Git コマンドが見つかりません")
        safe_print("        Git をインストールしてください")
        return None


def update_gitignore(repo_root: Path):
    """.gitignore に .snapshots/ を追記"""
    gitignore_path = repo_root / ".gitignore"
    
    # .gitignore が存在するか確認
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding="utf-8")
        if ".snapshots/" in content:
            safe_print("[OK] .gitignore に .snapshots/ は既に存在します")
            return
    else:
        content = ""
    
    # 追記
    with open(gitignore_path, "a", encoding="utf-8") as f:
        if content and not content.endswith("\n"):
            f.write("\n")
        f.write("# K-MAD Snapshots\n")
        f.write(".snapshots/\n")
    
    safe_print("[OK] .gitignore に .snapshots/ を追加しました")


def create_pre_commit_hook(repo_root: Path):
    """.git/hooks/pre-commit を生成"""
    hooks_dir = repo_root / ".git" / "hooks"
    
    if not hooks_dir.exists():
        safe_print("[WARN] .git/hooks/ が見つかりません（Git リポジトリではない？）")
        return
    
    hook_path = hooks_dir / "pre-commit"
    
    # 既存のフックがある場合は上書き確認
    if hook_path.exists():
        safe_print(f"[WARN] 既存の pre-commit フックが存在します: {hook_path}")
        response = input("      上書きしますか？ (y/n): ")
        if response.lower() != "y":
            safe_print("[SKIP] pre-commit フックの作成をスキップしました")
            return
    
    # フック内容（シェルスクリプト）
    hook_content = """#!/bin/sh
# K-MAD Governance Gate Hook
# 自動生成されました（AI_Controller/setup.py）

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
  echo "[ERROR] Cannot detect repo root."
  exit 1
fi

cd "$REPO_ROOT" || exit 1

# Governance Gate 実行
python AI_Controller/governance_gate.py
EXIT_CODE=$?

# 合格時のみスナップショット保存
if [ $EXIT_CODE -eq 0 ]; then
  python AI_Controller/snapshot_system.py save --reason "governance_gate_passed" || true
fi

exit $EXIT_CODE
"""
    
    # フック作成
    hook_path.write_text(hook_content, encoding="utf-8")
    
    # 実行権限付与（Unix系のみ）
    if os.name != "nt":  # Windows以外
        os.chmod(hook_path, 0o755)
    
    safe_print(f"[OK] pre-commit フックを作成しました: {hook_path}")


def create_governance_rules_template(repo_root: Path):
    """governance_rules.json のテンプレート生成"""
    ai_controller_dir = repo_root / "AI_Controller"
    rules_path = ai_controller_dir / "governance_rules.json"
    
    if rules_path.exists():
        safe_print("[OK] governance_rules.json は既に存在します（スキップ）")
        return
    
    # テンプレート内容（最小限）
    template = {
        "layer1": {
            "negative_list": [
                "eval(",
                "exec(",
                "os.system("
            ],
            "positive_list": [],
            "mandatory_patterns": []
        },
        "layer2": {
            "pipeline_phases": [],
            "required_calls": []
        },
        "layer3": {
            "domain_rules": {}
        },
        "layer4": {
            "architecture_checks": []
        }
    }
    
    # JSON保存
    import json
    with open(rules_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    safe_print(f"[OK] governance_rules.json テンプレートを作成しました: {rules_path}")
    safe_print("     このファイルを編集してルールを追加してください")


def main():
    """メイン処理"""
    safe_print("=" * 60)
    safe_print("K-MAD セットアップ開始")
    safe_print("=" * 60)
    
    # 1. リポジトリルート検出
    repo_root = detect_repo_root()
    if repo_root is None:
        safe_print("[ERROR] セットアップを中断しました")
        sys.exit(1)
    
    safe_print("")
    
    # 2. .gitignore 更新
    safe_print("[Step 1/3] .gitignore 更新...")
    update_gitignore(repo_root)
    
    safe_print("")
    
    # 3. pre-commit フック作成
    safe_print("[Step 2/3] pre-commit フック作成...")
    create_pre_commit_hook(repo_root)
    
    safe_print("")
    
    # 4. governance_rules.json テンプレート作成
    safe_print("[Step 3/3] governance_rules.json テンプレート作成...")
    create_governance_rules_template(repo_root)
    
    safe_print("")
    safe_print("=" * 60)
    safe_print("[OK] セットアップ完了！")
    safe_print("=" * 60)
    safe_print("")
    safe_print("次のステップ:")
    safe_print("1. AI_Controller/governance_rules.json を編集")
    safe_print("2. git commit を実行すると自動的に Governance Gate が動きます")


if __name__ == "__main__":
    main()
