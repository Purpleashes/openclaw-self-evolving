#!/usr/bin/env python3
"""
Signal Capture System - Automatic signal capture at key interaction points
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from enum import Enum

class SignalType(Enum):
    TASK_COMPLETE = "task_complete"
    TOOL_USAGE = "tool_usage"
    USER_FEEDBACK = "user_feedback"

class SignalCapture:
    def __init__(self, workspace_root="/root/.openclaw/workspace"):
        self.workspace_root = Path(workspace_root)
        self.signals_dir = self.workspace_root / "memory" / "signals"
        
        # Create signals directory if it doesn't exist
        self.signals_dir.mkdir(parents=True, exist_ok=True)
    
    def _save_signal(self, signal_type: SignalType, signal_data: dict):
        """Save a signal to the signals directory"""
        timestamp = int(time.time() * 1000)
        signal_file = self.signals_dir / f"{signal_type.value}-{timestamp}.jsonl"
        
        # Add metadata to signal data
        signal_data["signal_type"] = signal_type.value
        signal_data["timestamp"] = timestamp
        signal_data["datetime"] = datetime.now().isoformat()
        
        with open(signal_file, 'w', encoding='utf-8') as f:
            json.dump(signal_data, f, ensure_ascii=False, indent=2)
        
        return signal_file
    
    def capture_task_complete(self, task_id: str, task_title: str, success: bool, 
                              duration_ms: int, output_summary: str = "", 
                              output_quality: str = "unknown"):
        """Capture task completion signal"""
        signal_data = {
            "task_id": task_id,
            "task_title": task_title,
            "success": success,
            "duration_ms": duration_ms,
            "output_summary": output_summary,
            "output_quality": output_quality
        }
        
        return self._save_signal(SignalType.TASK_COMPLETE, signal_data)
    
    def capture_tool_usage(self, tool_name: str, execution_time_ms: int, 
                           return_code: int, output_length: int, 
                           success: bool):
        """Capture tool usage signal"""
        signal_data = {
            "tool_name": tool_name,
            "execution_time_ms": execution_time_ms,
            "return_code": return_code,
            "output_length": output_length,
            "success": success
        }
        
        return self._save_signal(SignalType.TOOL_USAGE, signal_data)
    
    def capture_user_feedback(self, task_id: str, satisfied: bool, 
                              feedback_text: str = ""):
        """Capture user feedback signal"""
        signal_data = {
            "task_id": task_id,
            "satisfied": satisfied,
            "feedback_text": feedback_text
        }
        
        return self._save_signal(SignalType.USER_FEEDBACK, signal_data)
    
    def get_recent_signals(self, signal_type: SignalType = None, limit: int = 20):
        """Get recent signals, optionally filtered by type"""
        signal_files = list(self.signals_dir.glob("*.jsonl"))
        
        # Sort by timestamp (newest first)
        signal_files.sort(key=lambda x: int(x.stem.split("-")[-1]), reverse=True)
        
        # Filter by type if specified
        if signal_type:
            signal_files = [f for f in signal_files if f.stem.startswith(signal_type.value)]
        
        # Load and return signals
        signals = []
        for signal_file in signal_files[:limit]:
            try:
                with open(signal_file, 'r', encoding='utf-8') as f:
                    signal = json.load(f)
                    signals.append(signal)
            except Exception as e:
                print(f"⚠️  Warning: Could not load {signal_file}: {e}")
        
        return signals

def main():
    """Test the signal capture system"""
    print("🧪 Testing Signal Capture System...")
    print("=" * 60)
    
    signal_capture = SignalCapture()
    
    # Test task complete signal
    print("\n📋 Testing task complete signal...")
    task_signal_file = signal_capture.capture_task_complete(
        task_id="task-test-001",
        task_title="测试信号捕获",
        success=True,
        duration_ms=12345,
        output_summary="测试任务完成",
        output_quality="good"
    )
    print(f"✅ Task complete signal saved to: {task_signal_file}")
    
    # Test tool usage signal
    print("\n🔧 Testing tool usage signal...")
    tool_signal_file = signal_capture.capture_tool_usage(
        tool_name="read",
        execution_time_ms=567,
        return_code=0,
        output_length=1234,
        success=True
    )
    print(f"✅ Tool usage signal saved to: {tool_signal_file}")
    
    # Test user feedback signal
    print("\n👍 Testing user feedback signal...")
    feedback_signal_file = signal_capture.capture_user_feedback(
        task_id="task-test-001",
        satisfied=True,
        feedback_text="结果很好，非常满意！"
    )
    print(f"✅ User feedback signal saved to: {feedback_signal_file}")
    
    # Test getting recent signals
    print("\n📊 Testing get recent signals...")
    recent_signals = signal_capture.get_recent_signals(limit=5)
    print(f"✅ Found {len(recent_signals)} recent signals")
    for i, signal in enumerate(recent_signals):
        print(f"  {i+1}. {signal.get('signal_type')} - {signal.get('datetime')}")
    
    print("\n" + "=" * 60)
    print("🎉 Signal Capture System test completed successfully!")

if __name__ == "__main__":
    main()
