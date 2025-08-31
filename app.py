"""
Flask App Runner - Financial Scoring API
Chạy server API hệ thống chấm điểm tài chính
"""

import sys
import os
from datetime import datetime

# Add src to path để import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.api.scoring_api import FinancialScoringAPI


def print_startup_banner():
    """In banner khởi động server"""
    print("🚀 FINANCIAL SCORING API SERVER v2.0")
    print("=" * 50)
    print("📡 Starting server...")
    print("Available endpoints:")
    print("  POST /process-groups - Calculate weighted group scores for multiple companies")
    print("  GET  /health - Health check")
    print()
    print("🌐 Server running at: http://localhost:5000")
    print("📖 API Documentation: ./API_DOCUMENTATION.md")
    print()
    print("ℹ️  API now accepts numeric values and calculates weighted scores.")
    print("✅ Supports batch processing for multiple companies.")
    print("✅ Accepts 'weights' for individual indicators.")
    print()
    print("Press CTRL+C to quit")
    print("=" * 50)


def main():
    """Main function để chạy Flask server"""
    try:
        # Print startup information
        print_startup_banner()
        
        # Tạo và chạy API server
        api = FinancialScoringAPI()
        api.run(host='0.0.0.0', port=5000, debug=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
