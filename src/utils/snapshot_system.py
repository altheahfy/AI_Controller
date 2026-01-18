#!/usr/bin/env python3
"""
K-MAD Snapshot System
コード状態の「保険」システム - 完全復元可能版

目的: governance_gate.py 合格時の状態を自動記録
効果: いつでも「正常だった過去」へ戻れる保険（コード全文を圧縮保存し、7日間保持、指定IDで復元可能）

人間の役割: 「スナップショットを撮って」と指示するだけ
AIの役割: 実装・拡張
"""

import json
import gzip
import base64
import hashlib
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class SnapshotMetadata:
    """スナップショット情報"""
    snapshot_id: str
    timestamp: float
    datetime_str: str
    reason: str
    git_commit_hash: Optional[str]
    git_branch: Optional[str]
    git_is_dirty: bool
    golden_test_accuracy: Optional[float]
    total_files: int
    total_lines: int
    data_hash: str  # データ改ざん検出用


class SnapshotSystem:
    """K-MAD スナップショットシステム - 完全復元可能版"""
    
    # 保持期間（日数）
    RETENTION_DAYS = 7
    
    # 対象ファイル拡張子
    TARGET_EXTENSIONS = {'.py', '.js', '.ts', '.json', '.yaml', '.yml', '.md', '.txt'}
    
    # 除外ディレクトリ
    EXCLUDE_DIRS = {'.git', '.snapshots', 'node_modules', '__pycache__', '.venv', 'venv', '.pytest_cache'}
    
    def __init__(self, snapshot_dir: str = ".snapshots", project_root: Optional[Path] = None):
        """
        Args:
            snapshot_dir: スナップショット保存ディレクトリ
            project_root: プロジェクトルート（Noneの場合は自動検出）
        """
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.project_root = project_root or self._detect_project_root()
    
    def _detect_project_root(self) -> Path:
        """プロジェクトルートを検出（.gitがある場所）"""
        current = Path.cwd()
        while current != current.parent:
            if (current / '.git').exists():
                return current
            current = current.parent
        return Path.cwd()  # 見つからなければカレントディレクトリ
    
    # ========================================
    # スナップショット保存
    # ========================================
    def save_snapshot(
        self, 
        reason: str = "manual",
        metadata: Optional[Dict[str, Any]] = None
    ) -> SnapshotMetadata:
        """
        現在の状態をスナップショット保存（完全復元可能版）
        
        Args:
            reason: 保存理由（"governance_gate_passed", "golden_test_100%"等）
            metadata: 追加情報
        
        Returns:
            SnapshotMetadata: 保存されたスナップショット情報
        """
        timestamp = time.time()
        snapshot_id = self._generate_snapshot_id(timestamp, reason)
        
        print(f"📸 スナップショット作成中: {snapshot_id}")
        
        # 1. 全対象ファイルを収集
        files = self._collect_files()
        print(f"   収集ファイル数: {len(files)}")
        
        # 2. Git状態を取得
        git_info = self._get_git_info()
        
        # 3. Golden Test精度を記録（あれば）
        accuracy = self._get_golden_test_accuracy()
        
        # 4. 総行数を計算
        total_lines = sum(f["lines"] for f in files.values())
        
        # 5. payloadを作成
        payload = {
            "version": 1,
            "files": files,
            "git": git_info,
            "custom_metadata": metadata or {}
        }
        
        # 6. JSON文字列化→gzip圧縮→base64化
        payload_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        payload_json_bytes = payload_json.encode('utf-8')
        payload_gzip = gzip.compress(payload_json_bytes)
        data_b64_gzip = base64.b64encode(payload_gzip).decode('ascii')
        
        # 7. データハッシュ（改ざん検出用）
        data_hash = hashlib.sha256(payload_gzip).hexdigest()
        
        # 8. メタデータ作成
        snapshot_metadata = SnapshotMetadata(
            snapshot_id=snapshot_id,
            timestamp=timestamp,
            datetime_str=datetime.fromtimestamp(timestamp).isoformat(),
            reason=reason,
            git_commit_hash=git_info.get("commit_hash"),
            git_branch=git_info.get("branch"),
            git_is_dirty=git_info.get("is_dirty", False),
            golden_test_accuracy=accuracy,
            total_files=len(files),
            total_lines=total_lines,
            data_hash=data_hash
        )
        
        # 9. 1行JSONとして保存
        snapshot_data = {
            "version": 1,
            "metadata": asdict(snapshot_metadata),
            "data_b64_gzip": data_b64_gzip
        }
        
        snapshot_file = self.snapshot_dir / f"{snapshot_id}.jsonl"
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(snapshot_data, ensure_ascii=False, separators=(",", ":")))
        
        print(f"✅ スナップショット保存完了")
        print(f"   理由: {reason}")
        print(f"   時刻: {snapshot_metadata.datetime_str}")
        print(f"   ファイル数: {len(files)}")
        print(f"   総行数: {total_lines}")
        print(f"   Git commit: {git_info.get('commit_hash', 'N/A')[:8]}")
        print(f"   データハッシュ: {data_hash[:16]}...")
        
        # 10. 期限切れスナップショットを削除
        self._cleanup_old_snapshots()
        
        return snapshot_metadata
    
    def _collect_files(self) -> Dict[str, Dict[str, Any]]:
        """対象ファイルを収集"""
        files = {}
        
        for file_path in self.project_root.rglob('*'):
            # ディレクトリはスキップ
            if file_path.is_dir():
                continue
            
            # 除外ディレクトリ内のファイルはスキップ
            if any(excluded in file_path.parts for excluded in self.EXCLUDE_DIRS):
                continue
            
            # 対象拡張子のみ
            if file_path.suffix not in self.TARGET_EXTENSIONS:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                relative_path = str(file_path.relative_to(self.project_root))
                files[relative_path] = {
                    "content": content,
                    "lines": len(content.splitlines()),
                    "mtime": file_path.stat().st_mtime
                }
            except Exception as e:
                print(f"⚠️  ファイル読み込みエラー: {file_path} - {e}")
        
        return files
    
    def _get_git_info(self) -> Dict[str, Any]:
        """Git状態を取得"""
        git_info = {}
        
        try:
            # HEADコミット
            git_info["commit_hash"] = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            
            # ブランチ名
            git_info["branch"] = subprocess.check_output(
                ["git", "branch", "--show-current"],
                cwd=self.project_root,
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            
            # ワークツリーの状態
            status = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            git_info["is_dirty"] = len(status) > 0
            
            # 未ステージ差分
            try:
                git_info["diff_unstaged"] = subprocess.check_output(
                    ["git", "diff"],
                    cwd=self.project_root,
                    text=True,
                    stderr=subprocess.DEVNULL
                )
            except:
                git_info["diff_unstaged"] = ""
            
            # ステージ差分
            try:
                git_info["diff_staged"] = subprocess.check_output(
                    ["git", "diff", "--cached"],
                    cwd=self.project_root,
                    text=True,
                    stderr=subprocess.DEVNULL
                )
            except:
                git_info["diff_staged"] = ""
            
            # リモート情報（任意）
            try:
                git_info["remotes"] = subprocess.check_output(
                    ["git", "remote", "-v"],
                    cwd=self.project_root,
                    text=True,
                    stderr=subprocess.DEVNULL
                ).strip()
            except:
                git_info["remotes"] = ""
            
        except Exception as e:
            print(f"⚠️  Git情報取得エラー: {e}")
            git_info["error"] = str(e)
        
        return git_info
    
    def _get_golden_test_accuracy(self) -> Optional[float]:
        """Golden Test精度を取得（あれば）"""
        quality_reports = Path("quality_reports")
        if not quality_reports.exists():
            return None
        
        try:
            reports = sorted(quality_reports.glob("*.txt"))
            if not reports:
                return None
            
            # 最新レポートから精度を抽出（簡易実装）
            latest_report = reports[-1]
            with open(latest_report, 'r', encoding='utf-8') as f:
                content = f.read()
                # "精度: XX.X%" のようなパターンを探す
                import re
                match = re.search(r'精度[：:]\s*(\d+\.?\d*)%', content)
                if match:
                    return float(match.group(1))
        except Exception as e:
            print(f"⚠️  Golden Test精度取得エラー: {e}")
        
        return None
    
    def _cleanup_old_snapshots(self):
        """期限切れスナップショットを削除"""
        cutoff_time = time.time() - (self.RETENTION_DAYS * 24 * 60 * 60)
        deleted_count = 0
        
        for snapshot_file in self.snapshot_dir.glob("*.jsonl"):
            try:
                with open(snapshot_file, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                    timestamp = data["metadata"]["timestamp"]
                    
                    if timestamp < cutoff_time:
                        snapshot_file.unlink()
                        deleted_count += 1
                        print(f"🗑️  期限切れスナップショット削除: {snapshot_file.name}")
            except Exception as e:
                print(f"⚠️  スナップショット削除エラー: {snapshot_file.name} - {e}")
        
        if deleted_count > 0:
            print(f"   削除済み: {deleted_count}件")
    
    # ========================================
    # スナップショット復元
    # ========================================
    def restore_snapshot(self, snapshot_id: str) -> bool:
        """
        スナップショットから復元（完全版）
        
        Args:
            snapshot_id: 復元するスナップショットID
        
        Returns:
            bool: 復元成功/失敗
        """
        snapshot_file = self.snapshot_dir / f"{snapshot_id}.jsonl"
        
        if not snapshot_file.exists():
            print(f"❌ スナップショットが見つかりません: {snapshot_id}")
            return False
        
        print(f"🔄 スナップショット復元中: {snapshot_id}")
        
        try:
            # 1. スナップショットファイルを読み込み
            with open(snapshot_file, 'r', encoding='utf-8') as f:
                snapshot_data = json.loads(f.read())
            
            metadata = snapshot_data["metadata"]
            data_b64_gzip = snapshot_data["data_b64_gzip"]
            
            # 2. データを復号・解凍
            payload_gzip = base64.b64decode(data_b64_gzip)
            
            # データハッシュ検証
            actual_hash = hashlib.sha256(payload_gzip).hexdigest()
            expected_hash = metadata.get("data_hash", "")
            if expected_hash and actual_hash != expected_hash:
                print(f"⚠️  警告: データハッシュが一致しません（改ざんの可能性）")
                print(f"   期待値: {expected_hash}")
                print(f"   実際: {actual_hash}")
                response = input("   復元を続行しますか？ (yes/no): ")
                if response.lower() != 'yes':
                    print("❌ 復元をキャンセルしました")
                    return False
            
            payload_json_bytes = gzip.decompress(payload_gzip)
            payload = json.loads(payload_json_bytes.decode('utf-8'))
            
            files = payload["files"]
            git_info = payload.get("git", {})
            
            # 3. 復元前に現在状態をバックアップ
            print("   現在状態をバックアップ中...")
            self.save_snapshot(reason="pre_restore_backup")
            
            # 4. 各ファイルを復元
            restored_count = 0
            for relative_path, file_info in files.items():
                file_path = self.project_root / relative_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                if file_path.exists():
                    print(f"   上書き: {relative_path}")
                else:
                    print(f"   作成: {relative_path}")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info["content"])
                
                restored_count += 1
            
            # 5. 復元完了を報告
            print(f"✅ スナップショット復元完了: {snapshot_id}")
            print(f"   復元ファイル数: {restored_count}")
            print(f"   元の時刻: {metadata['datetime_str']}")
            print(f"   元の理由: {metadata['reason']}")
            if metadata.get('golden_test_accuracy'):
                print(f"   元の精度: {metadata['golden_test_accuracy']}%")
            
            # 6. Git状態の情報を表示（自動checkoutはしない）
            print("\n⚠️  Git状態について:")
            print(f"   当時のコミット: {git_info.get('commit_hash', 'N/A')}")
            print(f"   当時のブランチ: {git_info.get('branch', 'N/A')}")
            print(f"   当時のワークツリー: {'変更あり' if git_info.get('is_dirty') else 'クリーン'}")
            print("\n   注意: Git状態の自動復元は行いません。")
            print("   必要に応じて手動で git checkout を実行してください。")
            
            if git_info.get('diff_unstaged') or git_info.get('diff_staged'):
                print("\n   当時の差分情報が保存されています。")
                print("   詳細は復元されたスナップショットファイルを確認してください。")
            
            return True
            
        except Exception as e:
            print(f"❌ 復元エラー: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # ========================================
    # スナップショット一覧
    # ========================================
    def list_snapshots(self) -> List[SnapshotMetadata]:
        """
        保存されているスナップショット一覧（完全版）
        
        Returns:
            List[SnapshotMetadata]: スナップショット情報リスト（新しい順）
        """
        snapshots = []
        
        for snapshot_file in self.snapshot_dir.glob("*.jsonl"):
            try:
                with open(snapshot_file, 'r', encoding='utf-8') as f:
                    data = json.loads(f.read())
                    metadata = data["metadata"]
                    
                    snapshots.append(SnapshotMetadata(
                        snapshot_id=metadata["snapshot_id"],
                        timestamp=metadata["timestamp"],
                        datetime_str=metadata["datetime_str"],
                        reason=metadata["reason"],
                        git_commit_hash=metadata.get("git_commit_hash"),
                        git_branch=metadata.get("git_branch"),
                        git_is_dirty=metadata.get("git_is_dirty", False),
                        golden_test_accuracy=metadata.get("golden_test_accuracy"),
                        total_files=metadata["total_files"],
                        total_lines=metadata["total_lines"],
                        data_hash=metadata.get("data_hash", "")
                    ))
            except Exception as e:
                print(f"⚠️  スナップショット読み込みエラー: {snapshot_file.name} - {e}")
        
        # 新しい順にソート
        snapshots.sort(key=lambda x: x.timestamp, reverse=True)
        
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
        print("K-MAD スナップショットシステム - 使い方:")
        print("  python snapshot_system.py save [理由]")
        print("  python snapshot_system.py list")
        print("  python snapshot_system.py restore <snapshot_id>")
        print("\n例:")
        print("  python snapshot_system.py save governance_gate_passed")
        print("  python snapshot_system.py list")
        print("  python snapshot_system.py restore snapshot_20260118_120000_governance_gate_passed")
        return
    
    system = SnapshotSystem()
    command = sys.argv[1]
    
    if command == "save":
        reason = sys.argv[2] if len(sys.argv) > 2 else "manual"
        metadata = system.save_snapshot(reason=reason)
        print(f"\n💾 保存場所: {system.snapshot_dir / f'{metadata.snapshot_id}.jsonl'}")
    
    elif command == "list":
        snapshots = system.list_snapshots()
        print(f"\n📋 保存されているスナップショット: {len(snapshots)}件\n")
        
        if not snapshots:
            print("   （スナップショットがありません）")
        else:
            for i, snap in enumerate(snapshots, 1):
                print(f"{i}. {snap.snapshot_id}")
                print(f"   時刻: {snap.datetime_str}")
                print(f"   理由: {snap.reason}")
                print(f"   ファイル数: {snap.total_files}, 総行数: {snap.total_lines}")
                if snap.git_commit_hash:
                    print(f"   Git: {snap.git_commit_hash[:8]} on {snap.git_branch}")
                if snap.golden_test_accuracy:
                    print(f"   精度: {snap.golden_test_accuracy}%")
                print()
    
    elif command == "restore":
        if len(sys.argv) < 3:
            print("❌ snapshot_idを指定してください")
            print("\n使い方: python snapshot_system.py restore <snapshot_id>")
            print("\nスナップショット一覧を表示:")
            print("  python snapshot_system.py list")
            return
        snapshot_id = sys.argv[2]
        success = system.restore_snapshot(snapshot_id)
        if not success:
            sys.exit(1)
    
    else:
        print(f"❌ 不明なコマンド: {command}")
        print("\n使用可能なコマンド: save, list, restore")


if __name__ == "__main__":
    main()
