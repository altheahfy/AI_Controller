#!/usr/bin/env python3
"""
K-MAD Central Layer & Claim Arbiter
中央管理体制・調停者システム（容量管理型タスクスケジューラー用）

目的: 
- 全体の意志決定を一箇所に集約
- 各部署からの提案（Claim）を調停
- 職務分掌（Capabilities）を強制
- 9段階パイプラインの実行

人間の役割: 「何を作るか」を指示するだけ
AIの役割: 各部署の実装、Claim生成、調停ロジックの実装
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path


# ========================================
# Claim（提案）システム
# ========================================

class ClaimType(Enum):
    """
    容量管理型タスクスケジューラーのClaim種類
    
    governance_rules.jsonの各部署のcan_claimと一致させること
    """
    # TaskPlacementProposer
    TASK_INSTANCE = "task_instance"          # タスクインスタンス
    TARGET_SLOT_ID = "target_slot_id"        # 配置先の時間枠ID
    PLACEMENT_PROPOSAL = "placement_proposal"  # 配置提案
    
    # CapacityValidator
    CAPACITY_CHECK_RESULT = "capacity_check_result"  # 容量チェック結果
    REMAINING_CAPACITY = "remaining_capacity"        # 残り容量
    CAN_FIT = "can_fit"                             # 配置可能か
    
    # ConsistencyValidator
    CONSISTENCY_CHECK_RESULT = "consistency_check_result"  # 整合性チェック結果
    VALIDATION_ERRORS = "validation_errors"                # 検証エラー
    
    # AutoReplacementProposer
    ALTERNATIVE_SLOTS = "alternative_slots"      # 代替時間枠
    REPLACEMENT_PROPOSAL = "replacement_proposal"  # 再配置提案
    
    # TaskTemplateManager
    TEMPLATE_OPERATION = "template_operation"  # テンプレート操作
    
    # TimeSlotManager
    SLOT_OPERATION = "slot_operation"  # 時間枠操作
    
    # TaskCompletionHandler
    COMPLETION_STATUS = "completion_status"  # 完了状態


@dataclass
class Claim:
    """
    提案（Claim）
    
    各部署が生成する「提案」
    CentralController（中央管理機関）が調停して最終決定
    """
    claim_type: ClaimType
    handler_name: str  # 部署名
    value: Any
    confidence: float = 1.0  # 0.0 ~ 1.0
    evidence: Dict[str, Any] = field(default_factory=dict)  # 根拠情報
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            "claim_type": self.claim_type.value,
            "handler_name": self.handler_name,
            "value": self.value,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "metadata": self.metadata
        }


# ========================================
# Central Controller（中央管理体制）
# ========================================

class CentralController:
    """
    K-MAD 中央管理体制（容量管理型タスクスケジューラー用）
    
    責務:
    1. 9段階パイプラインの実行
    2. 各部署の招集
    3. Claimの調停
    4. 最終決定とデータ書き込み（唯一の権限）
    """
    
    def __init__(self, config_path: str = "AI_Controller/governance_rules.json"):
        """
        初期化
        
        Args:
            config_path: governance_rules.jsonのパス
        """
        self.config = self._load_config(config_path)
        self.handlers: Dict[str, Any] = {}
        self.validators: Dict[str, Any] = {}
        self.arbiter = ClaimArbiter(self.config)
    
    def _load_config(self, path: str) -> Dict[str, Any]:
        """設定ファイル読み込み"""
        config_file = Path(path)
        if not config_file.exists():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def register_handler(self, handler_name: str, handler: Any):
        """
        提案部署の登録
        
        Args:
            handler_name: 部署名（例: "TaskPlacementProposer"）
            handler: 部署インスタンス
        """
        self.handlers[handler_name] = handler
        print(f"[登録] 提案部署: {handler_name}")
    
    def register_validator(self, validator_name: str, validator: Any):
        """
        検証部署の登録
        
        Args:
            validator_name: 検証部署名（例: "CapacityValidator"）
            validator: 検証部署インスタンス
        """
        self.validators[validator_name] = validator
        print(f"[登録] 検証部署: {validator_name}")
    
    def process(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        9段階統一汎用パイプラインの実行
        
        Args:
            command: 解析済みコマンドデータ
                例: {"action": "place", "template": "ミーティング", "slot": "9:00"}
        
        Returns:
            Dict: 処理結果
        
        Pipeline:
            Phase ① 入力解析（受付係） - この関数が呼ばれる前に完了
            Phase ② トリガー検出 - この関数内で実行
            Phase ③ 提案部署招集
            Phase ④ 検証部署招集
            Phase ⑤ 検証結果の評価
            Phase ⑥ 容量オーバー時の自動再配置提案
            Phase ⑦ 中央管理機関の最終決裁（このメソッド）
            Phase ⑧ 実行とデータ書き込み
            Phase ⑨ 結果出力
        """
        print(f"\n[開始] 9段階パイプライン処理")
        print(f"コマンド: {command}")
        
        # Phase ② トリガー検出
        action = command.get("action")
        triggered_handlers = self._detect_triggers(action)
        print(f"[Phase 2] トリガー検出: {triggered_handlers}")
        
        # Phase ③ 提案部署招集
        all_claims = self._invoke_handlers(triggered_handlers, command)
        print(f"[Phase 3] Claim収集: {len(all_claims)}件")
        
        # Phase ④ 検証部署招集
        validation_results = self._invoke_validators(all_claims, command)
        print(f"[Phase 4] 検証結果: {validation_results}")
        
        # Phase ⑤ 検証結果の評価
        evaluation = self._evaluate_validations(validation_results)
        print(f"[Phase 5] 評価: {evaluation}")
        
        # Phase ⑥ 容量オーバー時の自動再配置提案
        if not evaluation["capacity_ok"]:
            print(f"[Phase 6] 容量オーバー - 自動再配置を試行")
            replacement_claims = self._invoke_auto_replacement(command, validation_results)
            if replacement_claims:
                # 再配置提案をClaimに追加して Phase ④ に戻る
                all_claims.extend(replacement_claims)
                validation_results = self._invoke_validators(all_claims, command)
                evaluation = self._evaluate_validations(validation_results)
        
        # Phase ⑦ 中央管理機関の最終決裁
        approval = self._final_approval(all_claims, evaluation)
        print(f"[Phase 7] 最終決裁: {approval}")
        
        if not approval["approved"]:
            return {
                "success": False,
                "error": approval["reason"],
                "phase": "approval"
            }
        
        # Phase ⑧ 実行とデータ書き込み（唯一ここだけがデータを変更できる）
        execution_result = self._execute(approval["approved_claims"], command)
        print(f"[Phase 8] 実行完了: {execution_result}")
        
        # Phase ⑨ 結果出力
        return self._format_result(execution_result)
    
    def _detect_triggers(self, action: str) -> List[str]:
        """
        Phase ② トリガー検出
        
        Args:
            action: アクション名
        
        Returns:
            List[str]: 招集すべき部署名のリスト
        """
        trigger_map = {
            "place": ["TaskPlacementProposer"],
            "create_template": ["TaskTemplateManager"],
            "create_slot": ["TimeSlotManager"],
            "complete": ["TaskCompletionHandler"],
            "list": ["DisplayHandler"]
        }
        return trigger_map.get(action, [])
    
    def _invoke_handlers(self, handler_names: List[str], data: Dict[str, Any]) -> List[Claim]:
        """
        Phase ③ 提案部署招集
        
        Args:
            handler_names: 招集する部署名リスト
            data: 入力データ
        
        Returns:
            List[Claim]: 収集されたClaim一覧
        """
        claims = []
        for name in handler_names:
            if name in self.handlers:
                handler = self.handlers[name]
                # 職務分掌チェック
                if self._check_capability(handler, data):
                    handler_claims = handler.process(data)
                    claims.extend(handler_claims)
            else:
                print(f"[警告] 部署が未登録: {name}")
        return claims
    
    def _check_capability(self, handler: Any, data: Dict[str, Any]) -> bool:
        """
        職務分掌チェック
        
        Args:
            handler: ハンドラーインスタンス
            data: 入力データ
        
        Returns:
            bool: 許可されていればTrue
        """
        # TODO: governance_rules.jsonのcapabilitiesをチェック
        # 現状は全て許可
        return True
    
    def _invoke_validators(self, claims: List[Claim], data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase ④ 検証部署招集
        
        Args:
            claims: Claim一覧
            data: 入力データ
        
        Returns:
            Dict: 検証結果
        """
        results = {
            "capacity": None,
            "consistency": None
        }
        
        for name, validator in self.validators.items():
            if name == "CapacityValidator":
                results["capacity"] = validator.validate(claims, data)
            elif name == "ConsistencyValidator":
                results["consistency"] = validator.validate(claims, data)
        
        return results
    
    def _evaluate_validations(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase ⑤ 検証結果の評価
        
        Args:
            validation_results: 検証結果
        
        Returns:
            Dict: 評価結果
        """
        capacity_ok = validation_results.get("capacity", {}).get("passed", True)
        consistency_ok = validation_results.get("consistency", {}).get("passed", True)
        
        return {
            "capacity_ok": capacity_ok,
            "consistency_ok": consistency_ok,
            "all_ok": capacity_ok and consistency_ok
        }
    
    def _invoke_auto_replacement(self, command: Dict[str, Any], validation_results: Dict[str, Any]) -> List[Claim]:
        """
        Phase ⑥ 容量オーバー時の自動再配置提案
        
        Args:
            command: 元のコマンド
            validation_results: 検証結果
        
        Returns:
            List[Claim]: 再配置提案のClaim
        """
        if "AutoReplacementProposer" in self.handlers:
            handler = self.handlers["AutoReplacementProposer"]
            return handler.process(command, validation_results)
        return []
    
    def _final_approval(self, claims: List[Claim], evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase ⑦ 中央管理機関の最終決裁
        
        Args:
            claims: 全Claim
            evaluation: 評価結果
        
        Returns:
            Dict: 承認結果
        """
        if not evaluation["all_ok"]:
            return {
                "approved": False,
                "reason": "検証失敗",
                "details": evaluation
            }
        
        # 職務分掌違反チェック
        violations = self._check_capability_violations(claims)
        if violations:
            return {
                "approved": False,
                "reason": "職務分掌違反",
                "violations": violations
            }
        
        # 承認
        return {
            "approved": True,
            "approved_claims": claims
        }
    
    def _check_capability_violations(self, claims: List[Claim]) -> List[str]:
        """
        職務分掌違反のチェック
        
        Args:
            claims: Claim一覧
        
        Returns:
            List[str]: 違反リスト
        """
        violations = []
        # TODO: governance_rules.jsonのcapabilitiesと照合
        # 各claimのclaim_typeが、そのhandlerのcan_claimに含まれているかチェック
        return violations
    
    def _execute(self, claims: List[Claim], command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase ⑧ 実行とデータ書き込み
        
        重要: 唯一ここだけがデータを書き込める
        
        Args:
            claims: 承認されたClaim
            command: コマンド
        
        Returns:
            Dict: 実行結果
        """
        # TODO: 実際のデータ書き込み
        # - タスクの配置
        # - テンプレートの作成
        # - 時間枠の作成
        # etc.
        return {
            "executed": True,
            "claims_processed": len(claims)
        }
    
    def _format_result(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase ⑨ 結果出力
        
        Args:
            execution_result: 実行結果
        
        Returns:
            Dict: 整形された結果
        """
        return {
            "success": True,
            "result": execution_result,
            "message": "処理が完了しました"
        }


# ========================================
# Claim Arbiter（調停者）
# ========================================

class ClaimArbiter:
    """
    Claim調停者
    
    責務:
    - 各モジュールからの複数のClaimを調停
    - スコアリングシステムで最適なClaimを選択
    - 職務分掌違反のClaimを却下
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        初期化
        
        Args:
            config: governance_rules.jsonから読み込んだ設定
        """
        self.config = config
    
    def arbitrate(self, claims: List[Claim]) -> Dict[str, Any]:
        """
        Claim調停
        
        Args:
            claims: 各ハンドラーからのClaim一覧
        
        Returns:
            Dict: 最終的なフィールド割り当て
        
        処理:
        1. 同じClaimTypeのClaimをグループ化
        2. スコアリングシステムで最高点のClaimを選択
        3. 職務分掌違反のClaimを却下
        4. 最終フィールド割り当てを確定
        """
        print(f"[調停] Claim調停開始: {len(claims)}件")
        
        # Step 1: Claimのグループ化
        grouped_claims = {}
        for claim in claims:
            if claim.claim_type not in grouped_claims:
                grouped_claims[claim.claim_type] = []
            grouped_claims[claim.claim_type].append(claim)
        
        # Step 2: 職務分掌チェック
        validated_claims = []
        for claim in claims:
            if self._validate_capability(claim):
                validated_claims.append(claim)
            else:
                print(f"[ERROR] Claim却下（職務分掌違反）: {claim.handler_name} -> {claim.claim_type}")
        
        # Step 3: スコアリング - 各ClaimTypeごとに最高点のClaimを選択
        final_fields = {}
        for claim_type, claim_list in grouped_claims.items():
            if not claim_list:
                continue
            
            # スコアリングシステム
            best_claim = max(claim_list, key=lambda c: self._calculate_score(c))
            
            # フィールドに割り当て
            field_name = self._claim_type_to_field_name(claim_type)
            final_fields[field_name] = best_claim.value
        
        return final_fields
    
    def _calculate_score(self, claim: Claim) -> float:
        """
        Claimのスコア計算
        
        Args:
            claim: Claim
        
        Returns:
            float: スコア（高いほど優先）
        
        スコアリング:
        - confidence（信頼度）: 最大50点
        - ドメイン辞書マッチ: +30点
        - ルールマッチ: +20点
        - ハンドラー優先度
        """
        score = 0.0
        
        # confidence（信頼度）
        score += claim.confidence * 50
        
        # evidence（根拠）による加点
        if claim.evidence.get("domain_dictionary_match"):
            score += 30
        if claim.evidence.get("rule_match"):
            score += 20
        
        return score
    
    def _validate_capability(self, claim: Claim) -> bool:
        """
        職務分掌チェック
        
        Args:
            claim: Claim
        
        Returns:
            bool: 職務分掌に違反していなければTrue
        """
        # governance_rules.jsonから該当部署のcapabilitiesを取得
        capabilities = self.config.get("capabilities", {})
        handler_rules = capabilities.get(claim.handler_name, {})
        allowed_claim_types = handler_rules.get("can_claim", [])
        
        # claim_typeが許可されているかチェック
        if claim.claim_type.value not in allowed_claim_types:
            print(f"[ERROR] 職務分掌違反: {claim.handler_name} が {claim.claim_type} をclaimしています")
            print(f"   許可されているのは: {allowed_claim_types}")
            return False
        
        return True
    
    def _claim_type_to_field_name(self, claim_type: ClaimType) -> str:
        """
        ClaimType → フィールド名変換
        
        Args:
            claim_type: ClaimType
        
        Returns:
            str: フィールド名
        """
        mapping = {
            ClaimType.TASK_INSTANCE: "task_instance",
            ClaimType.TARGET_SLOT_ID: "target_slot_id",
            ClaimType.PLACEMENT_PROPOSAL: "placement_proposal",
            ClaimType.CAPACITY_CHECK_RESULT: "capacity_check_result",
            ClaimType.REMAINING_CAPACITY: "remaining_capacity",
            ClaimType.CAN_FIT: "can_fit",
            ClaimType.CONSISTENCY_CHECK_RESULT: "consistency_check_result",
            ClaimType.VALIDATION_ERRORS: "validation_errors",
            ClaimType.ALTERNATIVE_SLOTS: "alternative_slots",
            ClaimType.REPLACEMENT_PROPOSAL: "replacement_proposal",
            ClaimType.TEMPLATE_OPERATION: "template_operation",
            ClaimType.SLOT_OPERATION: "slot_operation",
            ClaimType.COMPLETION_STATUS: "completion_status",
        }
        return mapping.get(claim_type, "UNKNOWN")


# ========================================
# 使用例
# ========================================

def example_usage():
    """
    使用例（人間向けのデモンストレーション）
    
    実際の使い方:
    1. CentralControllerを作成
    2. 各部署（ハンドラー、バリデーター）を登録
    3. コマンドを処理
    """
    # Central Controller作成
    controller = CentralController()
    
    # TODO: ハンドラー登録
    # controller.register_handler("TaskPlacementProposer", TaskPlacementProposer())
    # controller.register_validator("CapacityValidator", CapacityValidator())
    # etc.
    
    # TODO: 処理実行
    # command = {"action": "place", "template": "ミーティング", "slot": "9:00"}
    # result = controller.process(command)
    # print(result)
    
    print("[OK] スケルトン動作確認")
    print("各部署を実装して登録してください")


if __name__ == "__main__":
    example_usage()

