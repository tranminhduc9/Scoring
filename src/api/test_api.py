"""
Test file và examples cho Financial Scoring API
"""

import requests
import json
import pandas as pd
import numpy as np


class APITester:
    """Class để test các API endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            print("=== Health Check Test ===")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            print()
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    def test_group_correlation_api(self):
        """Test group correlation scoring API"""
        print("=== Group Correlation API Test ===")
        
        # Sample data - group_scores now as lists to preserve order
        test_data = {
            "epsilon": 0.1,
            "company_id": "COMPANY_001",
            "group_correlation_matrices": {
                "Liquidity": [
                    [1.0, 0.85, 0.7],
                    [0.85, 1.0, 0.8],
                    [0.7, 0.8, 1.0]
                ],
                "Profitability": [
                    [1.0, 0.92, 0.88],
                    [0.92, 1.0, 0.85],
                    [0.88, 0.85, 1.0]
                ],
                "Efficiency": [
                    [1.0, 0.6, 0.5],
                    [0.6, 1.0, 0.4],
                    [0.5, 0.4, 1.0]
                ]
            },
            "group_scores": {
                "Liquidity": ["T5", "T7", "T6"],          # List format - preserves order
                "Profitability": ["T8", "T6", "T7"],      # List format - preserves order
                "Efficiency": ["T4", "T5", "T3"]          # List format - preserves order
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/score/group-correlation",
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            print()
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Group correlation API test failed: {e}")
            return False
    
    def test_calculate_group_max_api(self):
        """Test calculate group max API"""
        print("=== Calculate Group Max API Test ===")
        
        test_data = {
            "group_scores": ["T5", "T7", "T3", "T8", "T4"]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/score/calculate-group-max",
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            print()
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Calculate group max API test failed: {e}")
            return False
    
    def test_check_correlation_api(self):
        """Test check correlation API"""
        print("=== Check Correlation API Test ===")
        
        test_data = {
            "epsilon": 0.05,  # Ngưỡng nghiêm ngặt hơn
            "matrix_1": [
                [1.0, 0.95, 0.9],
                [0.95, 1.0, 0.87],
                [0.9, 0.87, 1.0]
            ],
            "matrix_2": [
                [1.0, 0.92, 0.88],
                [0.92, 1.0, 0.85],
                [0.88, 0.85, 1.0]
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/score/check-correlation",
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            print()
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Check correlation API test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Chạy tất cả tests"""
        print("=" * 50)
        print("FINANCIAL SCORING API TESTS")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Group Correlation", self.test_group_correlation_api),
            ("Calculate Group Max", self.test_calculate_group_max_api),
            ("Check Correlation", self.test_check_correlation_api)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"Test {test_name} encountered error: {e}")
                results[test_name] = False
        
        print("=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        for test_name, passed in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        return results


def example_direct_usage():
    """Example sử dụng trực tiếp không qua API"""
    print("=" * 50)
    print("DIRECT USAGE EXAMPLES")
    print("=" * 50)
    
    from src.api.scoring_api import process_company_scoring, calculate_max_score_for_group
    
    # Example 1: Tính điểm max cho một nhóm
    print("Example 1: Calculate max score for group")
    scores = ["T3", "T7", "T5", "T8", "T4"]
    max_score = calculate_max_score_for_group(scores)
    print(f"Input scores: {scores}")
    print(f"Max score: {max_score}")
    print()
    
    # Example 2: Xử lý scoring với correlation
    print("Example 2: Process company scoring with correlation")
    
    # Tạo correlation matrices
    liquidity_corr = pd.DataFrame([
        [1.0, 0.85, 0.7],
        [0.85, 1.0, 0.8],
        [0.7, 0.8, 1.0]
    ])
    
    profitability_corr = pd.DataFrame([
        [1.0, 0.92, 0.88],
        [0.92, 1.0, 0.85],
        [0.88, 0.85, 1.0]
    ])
    
    group_correlation_matrices = {
        "Liquidity": liquidity_corr,
        "Profitability": profitability_corr
    }
    
    group_scores = {
        "Liquidity": ["T5", "T7", "T6"],        # List format
        "Profitability": ["T8", "T6", "T7"]     # List format
    }
    
    final_scores = process_company_scoring(
        group_correlation_matrices, 
        group_scores, 
        epsilon=0.1
    )
    
    print("Group scores input:")
    for group, scores in group_scores.items():
        print(f"  {group}: {scores}")   # scores is now a list
    
    print(f"\nFinal scores after correlation processing:")
    for group, score in final_scores.items():
        print(f"  {group}: {score}")
    print()


if __name__ == "__main__":
    # Test direct usage first
    example_direct_usage()
    
    # Test API endpoints
    tester = APITester()
    
    print("Note: Make sure to start the API server first by running:")
    print("python src/api/scoring_api.py")
    print()
    
    input("Press Enter when API server is running...")
    
    # Run API tests
    tester.run_all_tests()
