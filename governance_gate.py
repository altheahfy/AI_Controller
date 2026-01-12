#!/usr/bin/env python3
"""
K-MAD Governance Gate
コミット時の統治ゲート（Layer 1-4統合検証システム）

人間の役割: governance_rules.json で「何を守るか」を定義
AIの役割: 各Layerの検証ロジックを実装

Exit Code:
  0: すべて合格（コミット許可）
  1: 違反検出（コミット拒否）
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
import time


@dataclass
class ValidationResult:
    """検証結果"""
    layer: str
    passed: bool
    violations: List[str]
    warnings: List[str]
    execution_time: float


class GovernanceGate:
    """K-MAD統治ゲート"""
    
    def __init__(self, config_path: str = "AI_Controller/governance_rules.json"):
        """
        Args:
            config_path: 設定ファイルパス（人間が編集）
        """
        self.config = self._load_config(config_path)
        self.results: List[ValidationResult] = []
    
    def _load_config(self, path: str) -> Dict[str, Any]:
        """設定ファイル読み込み"""
        config_file = Path(path)
        if not config_file.exists():
            print(f"[ERROR] 設定ファイルが見つかりません: {path}")
            print("ヒント: governance_rules.json をプロジェクトルートに配置してください")
            sys.exit(1)
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # ========================================
    # Layer 1: Static Structural Enforcement
    # ========================================
    def run_layer1_static_analysis(self) -> ValidationResult:
        """
        Layer 1: 静的AST検査
        
        人間の指示（governance_rules.json）:
        {
          "layer1": {
            "enabled": true,
            "rules": [
              "no_direct_spacy_access",
              "no_hardcoded_slot_names",
              ...
            ]
          }
        }
        
        AIの実装:
        - ASTパース
        - ネガティブリスト/ポジティブリスト検証
        - 違反箇所の特定
        """
        start_time = time.time()
        
        if not self.config.get("layer1", {}).get("enabled", False):
            return ValidationResult(
                "Layer 1: Static Analysis", 
                True, 
                [], 
                ["スキップ（無効化）"], 
                0.0
            )
        
        violations = []
        warnings = []
        
        # TODO: AIが実装すべき箇所
        # ========================================
        # 実装ガイド:
        # 1. Python AST解析
        #    import ast
        #    for py_file in Path("src").rglob("*.py"):
        #        with open(py_file) as f:
        #            tree = ast.parse(f.read())
        # 
        # 2. 禁止パターン検出（ネガティブリスト）
        #    例: "doc.token" のような直接アクセス検出
        #    for node in ast.walk(tree):
        #        if isinstance(node, ast.Attribute):
        #            if node.attr == "token":
        #                violations.append(f"{py_file}:{node.lineno}: 禁止: 直接spaCyアクセス")
        # 
        # 3. 必須パターン検証（ポジティブリスト）
        #    例: ハンドラーに必ず "CAPABILITIES" 定義があるか
        #    if "Handler" in class_name:
        #        if not has_capabilities_definition(node):
        #            violations.append(f"{py_file}:{node.lineno}: 必須: CAPABILITIES定義が欠落")
        # ========================================
        
        # 暫定: スケルトン段階ではすべて合格
        # AIが実装を追加すると、実際の検証結果が返される
        
        execution_time = time.time() - start_time
        
        return ValidationResult(
            layer="Layer 1: Static Analysis",
            passed=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            execution_time=execution_time
        )
    
    # ========================================
    # Layer 2: Dynamic Flow Validation
    # ========================================
    def run_layer2_flow_validation(self) -> ValidationResult:
        """
        Layer 2: 動的フロー検査
        
        人間の指示（pipeline_definition.md）:
        - データフロー定義
        - 処理順序の期待値
        
        AIの実装:
        - pipeline_definition.md の読み取り
        - 実行時のトレース記録との照合
        - 期待フローとの整合性検証
        """
        start_time = time.time()
        
        if not self.config.get("layer2", {}).get("enabled", False):
            return ValidationResult(
                "Layer 2: Flow Validation", 
                True, 
                [], 
                ["スキップ（無効化）"], 
                0.0
            )
        
        violations = []
        warnings = []
        
        # TODO: AIが実装すべき箇所（② Geminiアドバイス反映）
        # ========================================
        # 実装ガイド:
        # 
        # 1. pipeline_definition.md を読み取る
        #    pipeline_file = Path(self.config.get("layer2", {}).get("flow_definition", "pipeline_definition.md"))
        #    if not pipeline_file.exists():
        #        violations.append(f"pipeline_definition.md が見つかりません: {pipeline_file}")
        #        return ValidationResult(...)
        #    
        #    with open(pipeline_file, 'r', encoding='utf-8') as f:
        #        pipeline_content = f.read()
        # 
        # 2. パイプライン定義を解析
        #    # 例: "Phase ① → Phase ② → Phase ③" のような順序定義を抽出
        #    expected_phases = extract_phase_order(pipeline_content)
        # 
        # 3. 実行ログを読み取る
        #    log_file = Path(self.config.get("layer2", {}).get("execution_log", "logs/execution_trace.json"))
        #    if not log_file.exists():
        #        warnings.append("実行ログが見つかりません。動的検証をスキップします")
        #        return ValidationResult(...)
        #    
        #    with open(log_file, 'r', encoding='utf-8') as f:
        #        execution_log = json.load(f)
        # 
        # 4. フロー整合性を検証
        #    actual_phases = execution_log.get("phase_execution_order", [])
        #    
        #    if actual_phases != expected_phases:
        #        violations.append(
        #            f"フロー順序違反: 期待={expected_phases}, 実際={actual_phases}"
        #        )
        #    
        #    # 必須フェーズの実行確認
        #    for required_phase in expected_phases:
        #        if required_phase not in actual_phases:
        #            violations.append(f"必須フェーズ未実行: {required_phase}")
        # 
        # 5. データ変換の検証
        #    # 例: "Phase ② でチャンク合体が行われたか"
        #    if "chunk_merge" in pipeline_content:
        #        if not execution_log.get("chunk_merge_executed", False):
        #            violations.append("必須処理が実行されませんでした: チャンク合体")
        # 
        # ========================================
        
        execution_time = time.time() - start_time
        
        return ValidationResult(
            layer="Layer 2: Flow Validation",
            passed=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            execution_time=execution_time
        )
    
    # ========================================
    # Layer 3: Domain Library Inspection
    # ========================================
    def run_layer3_domain_inspection(self) -> ValidationResult:
        """
        Layer 3: 専門知識検査
        
        人間の指示（governance_rules.json）:
        {
          "layer3": {
            "enabled": true,
            "domain_specific_rules": [
              "adverb_flexibility_check",
              "nested_clause_pattern_check",
              ...
            ]
          }
        }
        
        AIの実装:
        - ドメイン固有ルールの検証
        - パターンライブラリの整合性チェック
        """
        start_time = time.time()
        
        if not self.config.get("layer3", {}).get("enabled", False):
            return ValidationResult(
                "Layer 3: Domain Inspection", 
                True, 
                [], 
                ["スキップ（無効化）"], 
                0.0
            )
        
        violations = []
        warnings = []
        
        # TODO: AIが実装すべき箇所
        # ========================================
        # 実装ガイド:
        # 1. ドメインルール読み込み
        #    domain_rules = self.config["layer3"]["domain_specific_rules"]
        # 
        # 2. パターンライブラリ検証
        #    例: 副詞許容力チェック
        #    for pattern in rephrase_patterns:
        #        if "ADV_CHUNK" in pattern["pattern_key"]:
        #            violations.append(f"副詞許容力違反: パターンキーにADV_CHUNKが含まれています")
        # 
        # 3. 重複・欠損チェック
        #    if has_duplicate_patterns(rephrase_lib):
        #        violations.append("パターン重複: 同一文型に複数パターンが登録されています")
        # ========================================
        
        execution_time = time.time() - start_time
        
        return ValidationResult(
            layer="Layer 3: Domain Inspection",
            passed=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            execution_time=execution_time
        )
    
    # ========================================
    # Layer 4: Architecture Preservation
    # ========================================
    def run_layer4_architecture_guard(self) -> ValidationResult:
        """
        Layer 4: アーキテクチャ保護
        
        人間の指示（governance_rules.json）:
        {
          "layer4": {
            "enabled": true,
            "snapshot_comparison": true,
            "pattern_degradation_check": true
          }
        }
        
        AIの実装:
        - スナップショット比較
        - パターン数退化検知
        - 破壊的変更検出
        """
        start_time = time.time()
        
        if not self.config.get("layer4", {}).get("enabled", False):
            return ValidationResult(
                "Layer 4: Architecture Guard", 
                True, 
                [], 
                ["スキップ（無効化）"], 
                0.0
            )
        
        violations = []
        warnings = []
        
        # TODO: AIが実装すべき箇所
        # ========================================
        # 実装ガイド:
        # 1. スナップショット読み込み
        #    with open(".snapshots/latest_snapshot.json") as f:
        #        snapshot = json.load(f)
        # 
        # 2. 現在状態との差分計算
        #    current_pattern_count = count_rephrase_patterns()
        #    snapshot_pattern_count = snapshot["rephrase_pattern_count"]
        #    
        #    if current_pattern_count < snapshot_pattern_count:
        #        violations.append(
        #            f"パターン退化: {snapshot_pattern_count} → {current_pattern_count} "
        #            f"({snapshot_pattern_count - current_pattern_count}パターン減少)"
        #        )
        # 
        # 3. 破壊的変更検出
        #    for file, methods in snapshot["method_signatures"].items():
        #        current_methods = get_current_method_signatures(file)
        #        if methods != current_methods:
        #            violations.append(f"破壊的変更: {file} のメソッドシグネチャが変更されました")
        # ========================================
        
        execution_time = time.time() - start_time
        
        return ValidationResult(
            layer="Layer 4: Architecture Guard",
            passed=len(violations) == 0,
            violations=violations,
            warnings=warnings,
            execution_time=execution_time
        )
    
    # ========================================
    # 統合実行・レポート
    # ========================================
    def execute_all_layers(self) -> bool:
        """全Layer実行"""
        print("=" * 60)
        print("K-MAD Governance Gate - 統治検証開始")
        print("=" * 60)
        
        # Layer 1-4を順次実行
        self.results.append(self.run_layer1_static_analysis())
        self.results.append(self.run_layer2_flow_validation())
        self.results.append(self.run_layer3_domain_inspection())
        self.results.append(self.run_layer4_architecture_guard())
        
        # 結果集約
        all_passed = all(r.passed for r in self.results)
        
        # レポート出力
        self._print_report()
        
        # ① スナップショット連動（Geminiアドバイス反映）
        # 合格時のみスナップショットを撮る
        if all_passed:
            self._trigger_snapshot()
        
        return all_passed
    
    def _trigger_snapshot(self):
        """
        合格時のスナップショット保存
        
        AIへの実装指示例:
        「snapshot_system.py を呼び出して、現在の状態を保存してください」
        
        実装ガイド:
        1. snapshot_system.py をインポート
           from snapshot_system import SnapshotSystem
        
        2. スナップショットを撮る
           snapshot = SnapshotSystem()
           snapshot.save_snapshot(
               reason="governance_gate_passed",
               metadata={"timestamp": time.time()}
           )
        
        3. 成功メッセージ
           print("[OK] スナップショット保存完了（保険作成）")
        """
        # 最小実装（ChatGPTレビュー反映）
        # snapshot_system.pyがなくてもエラーにならない
        try:
            from snapshot_system import SnapshotSystem
            snapshot = SnapshotSystem()
            snapshot.save_snapshot(
                reason="governance_gate_passed",
                metadata={"timestamp": time.time()}
            )
            print("[OK] スナップショット保存完了（保険作成）")
        except ImportError:
            print("[WARN] snapshot_system.py が見つかりません（スキップ）")
        except Exception as e:
            print(f"[WARN] スナップショット保存失敗: {e}（継続）")
    
    def _print_report(self):
        """結果レポート"""
        print("\n" + "=" * 60)
        print("検証結果サマリー")
        print("=" * 60)
        
        for result in self.results:
            status = "[OK] 合格" if result.passed else "[NG] 違反"
            print(f"\n{status} {result.layer} ({result.execution_time:.2f}s)")
            
            if result.violations:
                print("  違反:")
                for v in result.violations:
                    print(f"    - {v}")
            
            if result.warnings:
                print("  警告:")
                for w in result.warnings:
                    print(f"    - {w}")
        
        print("\n" + "=" * 60)
        total_violations = sum(len(r.violations) for r in self.results)
        if total_violations == 0:
            print("[OK] すべての検証に合格しました。コミットを許可します。")
        else:
            print(f"[NG] {total_violations}件の違反が検出されました。")
            print("コミットは拒否されます。")
            print("\nヒント: 「governance_gate.pyのエラーを修正して」とAIに指示してください。")
        print("=" * 60)


def main():
    """エントリーポイント（Git pre-commitフックから呼ばれる）"""
    gate = GovernanceGate()
    
    try:
        all_passed = gate.execute_all_layers()
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"[ERROR] 統治ゲート実行エラー: {e}")
        print("緊急停止: コミットを拒否します")
        sys.exit(1)


if __name__ == "__main__":
    main()
