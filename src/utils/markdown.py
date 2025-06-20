from datetime import datetime
from typing import List
from src.session import Session


class MarkdownExporter:
    def export_sessions(self, sessions: List[Session]) -> str:
        if not sessions:
            return "# 作業セッション記録\n\nセッションがありません。"
        
        lines = []
        lines.append("# 作業セッション記録")
        lines.append("")
        lines.append(f"**生成日時:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        lines.append("## セッション一覧")
        lines.append("")
        lines.append("| # | タスク名 | 開始時刻 | 終了時刻 | 経過時間 |")
        lines.append("|---|---|---|---|---|")
        
        total_duration = 0.0
        
        for i, session in enumerate(sessions, 1):
            start_time = session.start_time.strftime('%H:%M:%S') if session.start_time else "未設定"
            end_time = session.end_time.strftime('%H:%M:%S') if session.end_time else "未設定"
            duration = session.format_duration()
            total_duration += session.get_duration()
            
            lines.append(f"| {i} | {session.task_name} | {start_time} | {end_time} | {duration} |")
        
        lines.append("")
        lines.append("## サマリー")
        lines.append("")
        
        total_hours = int(total_duration // 3600)
        total_minutes = int((total_duration % 3600) // 60)
        total_seconds = int(total_duration % 60)
        total_formatted = f"{total_hours:02d}:{total_minutes:02d}:{total_seconds:02d}"
        
        lines.append(f"**合計時間:** {total_formatted}")
        lines.append(f"**セッション数:** {len(sessions)}")
        
        return "\n".join(lines)