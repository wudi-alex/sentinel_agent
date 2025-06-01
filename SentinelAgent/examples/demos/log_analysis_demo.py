#!/usr/bin/env python3
"""
Log Analysis Tool Demo

Demonstrates how to use ExecutionLogAnalyzer and LogAnalysisTool for log analysis
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sentinelagent.core.log_analyzer import ExecutionLogAnalyzer
from sentinelagent.core.tools import LogAnalysisTool

def demo_direct_analysis():
    """Direct analysis using ExecutionLogAnalyzer"""
    print("=== Direct Analysis Demo ===")
    
    # Create analyzer
    analyzer = ExecutionLogAnalyzer()
    
    # Analyze TXT format logs
    txt_log = "../../autogen_magneticone/logs/log_2025-05-17_17-47-03.txt"
    if Path(txt_log).exists():
        print(f"\n📊 Analyzing TXT log: {txt_log}")
        result = analyzer.analyze_log_file(txt_log)
        
        print(f"✅ Analysis complete:")
        print(f"  - Execution paths: {len(result.execution_paths)}")
        print(f"  - Error count: {len(result.errors)}")
        print(f"  - Warning count: {len(result.warnings)}")
        
        if result.errors:
            print("\n❌ Major errors:")
            for i, error in enumerate(result.errors[:3], 1):
                print(f"  {i}. {error.error_type} ({error.severity.value}): {error.description}")
        
        # generatereport
        report = analyzer.generate_report(result, "txt_analysis_report.md")
        print(f"\n📄 Detailed report generated: txt_analysis_report.md")
    
    # Analyze CSV format logs
    csv_log = "../../magentic-one-file-code-execution.csv"
    if Path(csv_log).exists():
        print(f"\n📊 Analyzing CSV log: {csv_log}")
        result = analyzer.analyze_log_file(csv_log)
        
        print(f"✅ Analysis complete:")
        print(f"  - Execution paths: {len(result.execution_paths)}")
        print(f"  - Error count: {len(result.errors)}")
        print(f"  - Warning count: {len(result.warnings)}")
        
        if result.execution_paths:
            print("\n🛣️  Execution paths:")
            for i, path in enumerate(result.execution_paths[:3], 1):
                print(f"  Path {i}: {len(path.nodes)} nodes, {len(path.log_entries)} entries")


def demo_crewai_tool():
    """Demonstrate CrewAI tool usage"""
    print("\n\n=== CrewAI Tool Demo ===")
    
    # Create tool instance
    tool = LogAnalysisTool()
    
    # Use tool to analyze logs
    txt_log = "../../autogen_magneticone/logs/log_2025-05-17_17-47-03.txt"
    if Path(txt_log).exists():
        print(f"\n🔧 Using CrewAI tool to analyze: {txt_log}")
        result = tool._run(
            log_file_path=txt_log,
            log_format="auto",
            output_file="crewai_analysis_result.json"
        )
        
        print("📋 Tool analysis results:")
        print(result)


def demo_batch_analysis():
    """Batch analysis demo"""
    print("\n\n=== Batch Analysis Demo ===")
    
    analyzer = ExecutionLogAnalyzer()
    
    # Find all log files
    log_dir = Path("../../autogen_magneticone/logs")
    if log_dir.exists():
        log_files = list(log_dir.glob("*.txt"))
        print(f"📁 Found {len(log_files)} log files")
        
        total_errors = 0
        total_warnings = 0
        total_paths = 0
        
        for log_file in log_files[:3]:  # Analyze first 3 files
            try:
                print(f"\n📊 Analyzing: {log_file.name}")
                result = analyzer.analyze_log_file(str(log_file))
                
                total_errors += len(result.errors)
                total_warnings += len(result.warnings)
                total_paths += len(result.execution_paths)
                
                print(f"  - Paths: {len(result.execution_paths)}, Errors: {len(result.errors)}, Warnings: {len(result.warnings)}")
                
            except Exception as e:
                print(f"  ❌ Analysis failed: {e}")
        
        print(f"\n📈 Total:")
        print(f"  - Execution paths: {total_paths}")
        print(f"  - Error count: {total_errors}")
        print(f"  - Warning count: {total_warnings}")


if __name__ == "__main__":
    print("🔍 Log Analysis Tool Demo")
    print("=" * 50)
    
    try:
        demo_direct_analysis()
        demo_crewai_tool()
        demo_batch_analysis()
        
        print("\n✅ Demo complete!")
        print("\n💡 Tips:")
        print("  - Generated report files can be viewed with a Markdown editor")
        print("  - JSON analysis results can be further processed and visualized")
        print("  - Can be integrated into CI/CD pipelines for automated analysis")
        
    except Exception as e:
        print(f"❌ Error occurred during demo: {e}")
        import traceback
        traceback.print_exc()
