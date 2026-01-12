#!/usr/bin/env python3
"""
K-MAD Snapshot System
コード状態の「保険」システム

目的: governance_gate.py 合格時の状態を自動記録
効果: いつでも「正常だった過去」へ戻れる保険

人間の役割: 「スナップショットを撮って」と指示するだけ
AIの役割: 実装・拡張
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SnapshotMetadata:
    """スナップショット情報"""
    snapshot_id: str
    timestamp: float
    datetime_str: str
    reason: str
    git_commit_hash: Optional[str]
    golden_test_accuracy: Optional[float]
    total_files: int
    total_lines: int


class SnapshotSystem:
    """K-MAD スナップショットシステム"""
    
    def __init__(self, snapshot_dir: str = ".snapshots"):
        """
        Args:
            snapshot_dir: スナップショット保存ディレクトリ
        """
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    # ========================================
    # スナップショット保存
    # ========================================
    def save_snapshot(
        self, 
        reason: str = "manual",
        metadata: Optional[Dict[str, Any]] = None
    ) -> SnapshotMetadata:
        """
        現在の状態をスナップショット保存
        
        Args:
            reason: 保存理由（"governance_gate_passed", "golden_test_100%"等）
            metadata: 追加情報
        
        Returns:
            SnapshotMetadata: 保存されたスナップショット情報
        
        AIの実装内容:
        1. タイムスタンプ生成
        2. 全Pythonファイルを収集
        3. Git commit hashを取得
        4. Golden Test精度を記録（あれば）
        5. JSONファイルとして保存
        """
        timestamp = time.time()
        snapshot_id = self._generate_snapshot_id(timestamp, reason)
        
        # TODO: AIが実装すべき箇所
        # ========================================
        # 実装ガイド:
        # 
        # 1. 全Pythonファイルを収集
        #    files = {}
        #    for py_file in Path("src").rglob("*.py"):
        #        with open(py_file, 'r', encoding='utf-8') as f:
        #            content = f.read()
        #            files[str(py_file)] = {
        #                "content": content,
        #                "lines": len(content.splitlines()),
        #                "modified_time": py_file.stat().st_mtime
        #            }
        # 
        # 2. Git commit hashを取得
        #    import subprocess
        #    try:
        #        git_hash = subprocess.check_output(
        #            ["git", "rev-parse", "HEAD"],
        #            text=True
        #        ).strip()
        #    except:
        #        git_hash = None
        # 
        # 3. Golden Test精度を記録
        #    accuracy = None
        #    if Path("quality_reports").exists():
        #        # 最新のレポートから精度を抽出
        #        reports = sorted(Path("quality_reports").glob("*.txt"))
        #        if reports:
        #            accuracy = extract_accuracy_from_report(reports[-1])
        # 
        # 4. スナップショットデータ作成
        #    snapshot_data = {
        #        "metadata": {
        #            "snapshot_id": snapshot_id,
        #            "timestamp": timestamp,
        #            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
        #            "reason": reason,
        #            "git_commit_hash": git_hash,
        #            "golden_test_accuracy": accuracy,
        #            "total_files": len(files),
        #            "total_lines": sum(f["lines"] for f in files.values())
        #        },
        #        "files": files,
        #        "custom_metadata": metadata or {}
        #    }
        # 
        # 5. JSONファイルとして保存
        #    snapshot_file = self.snapshot_dir / f"{snapshot_id}.json"
        #    with open(snapshot_file, 'w', encoding='utf-8') as f:
        #        json.dump(snapshot_data, f, indent=2, ensure_ascii=False)
        # 
        # ========================================
        
        # 暫定: スケルトン段階では最小限の情報
        snapshot_metadata = SnapshotMetadata(
            snapshot_id=snapshot_id,
            timestamp=timestamp,
            datetime_str=datetime.fromtimestamp(timestamp).isoformat(),
            reason=reason,
            git_commit_hash=None,  # TODO: AIが実装
            golden_test_accuracy=None,  # TODO: AIが実装
            total_files=0,  # TODO: AIが実装
            total_lines=0  # TODO: AIが実装
        )
        
        print(f"📸 スナップショット保存: {snapshot_id}")
        print(f"   理由: {reason}")
        print(f"   時刻: {snapshot_metadata.datetime_str}")
        
        return snapshot_metadata
    
    # ========================================
    # スナップショット復元
    # ========================================
    def restore_snapshot(self, snapshot_id: str) -> bool:
        """
        スナップショットから復元
        
        Args:
            snapshot_id: 復元するスナップショットID
        
        Returns:
            bool: 復元成功/失敗
        
        AIの実装内容:
        1. スナップショットファイルを読み込み
        2. 各ファイルを元の場所に書き戻す
        3. 復元完了を報告
        """
        snapshot_file = self.snapshot_dir / f"{snapshot_id}.json"
        
        if not snapshot_file.exists():
            print(f"❌ スナップショットが見つかりません: {snapshot_id}")
            return False
        
        # TODO: AIが実装すべき箇所
        # ========================================
        # 実装ガイド:
        # 
        # 1. スナップショットファイルを読み込み
        #    with open(snapshot_file, 'r', encoding='utf-8') as f:
        #        snapshot_data = json.load(f)
        # 
        # 2. 各ファイルを復元
        #    for file_path, file_info in snapshot_data["files"].items():
        #        file = Path(file_path)
        #        file.parent.mkdir(parents=True, exist_ok=True)
        #        with open(file, 'w', encoding='utf-8') as f:
        #            f.write(file_info["content"])
        # 
        # 3. 復元完了を報告
        #    print(f"✅ スナップショット復元完了: {snapshot_id}")
        #    print(f"   復元ファイル数: {len(snapshot_data['files'])}")
        #    print(f"   元の精度: {snapshot_data['metadata']['golden_test_accuracy']}%")
        # 
        # ========================================
        
        print(f"✅ スナップショット復元: {snapshot_id}")
        return True
    
    # ========================================
    # スナップショット一覧
    # ========================================
    def list_snapshots(self) -> List[SnapshotMetadata]:
        """
        保存されているスナップショット一覧
        
        Returns:
            List[SnapshotMetadata]: スナップショット情報リスト
        """
        snapshots = []
        
        # TODO: AIが実装すべき箇所
        # ========================================
        # 実装ガイド:
        # 
        # 1. 全スナップショットファイルを取得
        #    for snapshot_file in sorted(self.snapshot_dir.glob("*.json")):
        #        with open(snapshot_file, 'r', encoding='utf-8') as f:
        #            data = json.load(f)
        #            metadata = data["metadata"]
        #            
        #            snapshots.append(SnapshotMetadata(
        #                snapshot_id=metadata["snapshot_id"],
        #                timestamp=metadata["timestamp"],
        #                datetime_str=metadata["datetime"],
        #                reason=metadata["reason"],
        #                git_commit_hash=metadata.get("git_commit_hash"),
        #                golden_test_accuracy=metadata.get("golden_test_accuracy"),
        #                total_files=metadata["total_files"],
        #                total_lines=metadata["total_lines"]
        #            ))
        # 
        # 2. 新しい順にソート
        #    snapshots.sort(key=lambda x: x.timestamp, reverse=True)
        # 
        # ========================================
        
        return snapshots
    
    # ========================================
    # ヘルパーメソッド
    # ========================================
    def _generate_snapshot_id(self, timestamp: float, reason: str) -> str:
        """
        スナップショットID生成
        
        例: "snapshot_20251231_195022_governance_gate_passed"
        """
        dt = datetime.fromtimestamp(timestamp)
        date_str = dt.strftime("%Y%m%d_%H%M%S")
        safe_reason = reason.replace(" ", "_").replace("/", "_")
        return f"snapshot_{date_str}_{safe_reason}"
    
    def get_latest_snapshot(self) -> Optional[SnapshotMetadata]:
        """最新のスナップショット取得"""
        snapshots = self.list_snapshots()
        return snapshots[0] if snapshots else None


def main():
    """CLIエントリーポイント（人間が直接実行可能）"""
    import sys
    
    if len(sys.argv) < 2:
        print("使い方:")
        print("  python snapshot_system.py save [理由]")
        print("  python snapshot_system.py list")
        print("  python snapshot_system.py restore <snapshot_id>")
        return
    
    system = SnapshotSystem()
    command = sys.argv[1]
    
    if command == "save":
        reason = sys.argv[2] if len(sys.argv) > 2 else "manual"
        system.save_snapshot(reason=reason)
    
    elif command == "list":
        snapshots = system.list_snapshots()
        print(f"保存されているスナップショット: {len(snapshots)}件")
        for snap in snapshots:
            print(f"  {snap.snapshot_id}")
            print(f"    時刻: {snap.datetime_str}")
            print(f"    理由: {snap.reason}")
            if snap.golden_test_accuracy:
                print(f"    精度: {snap.golden_test_accuracy}%")
    
    elif command == "restore":
        if len(sys.argv) < 3:
            print("❌ snapshot_idを指定してください")
            return
        snapshot_id = sys.argv[2]
        system.restore_snapshot(snapshot_id)
    
    else:
        print(f"❌ 不明なコマンド: {command}")


if __name__ == "__main__":
    main()
