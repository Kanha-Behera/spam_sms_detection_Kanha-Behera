#!/usr/bin/env python
"""
Spam SMS Detection - API Test Script
Tests all endpoints and validates backend functionality
"""

import requests
import json
import sys
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 5

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

def test_health_check() -> bool:
    """Test health check endpoint"""
    print_header("TEST 1: Health Check")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print_success("Health check passed")
            return True
        else:
            print_error(f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def test_root_endpoint() -> bool:
    """Test root endpoint"""
    print_header("TEST 2: Root Endpoint")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print_success("Root endpoint accessible")
            return True
        else:
            print_error(f"Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Root endpoint failed: {str(e)}")
        return False

def test_prediction(text: str, expected: str = None) -> bool:
    """Test single prediction"""
    print_header(f"TEST: Prediction")
    print(f"Input: {Colors.YELLOW}\"{text}\"{Colors.RESET}")
    
    try:
        payload = {"text": text}
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=payload,
            timeout=TIMEOUT
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            result = data.get("result")
            confidence = data.get("confidence", 0)
            
            print(f"Result: {Colors.BOLD}{result}{Colors.RESET}")
            print(f"Confidence: {confidence:.2%}")
            
            if expected and result != expected:
                print_error(f"Expected {expected}, got {result}")
                return False
            
            print_success(f"Prediction: {result}")
            return True
        else:
            print_error(f"Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Prediction failed: {str(e)}")
        return False

def test_batch_prediction() -> bool:
    """Test batch prediction endpoint"""
    print_header("TEST 3: Batch Prediction")
    
    messages = [
        {"text": "Free money! Click here to claim!"},
        {"text": "Hi, how are you doing today?"},
        {"text": "URGENT: Claim your prize now!"},
        {"text": "Let's meet for coffee"}
    ]
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/batch-predict",
            json=messages,
            timeout=TIMEOUT
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            predictions = data.get("predictions", [])
            
            print(f"Processed {len(predictions)} messages:\n")
            
            for i, pred in enumerate(predictions, 1):
                print(f"  {i}. {pred['text']}")
                print(f"     Result: {Colors.BOLD}{pred['result']}{Colors.RESET}")
                print(f"     Confidence: {pred['confidence']:.2%}\n")
            
            print_success(f"Batch prediction processed {len(predictions)} messages")
            return True
        else:
            print_error(f"Request failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Batch prediction failed: {str(e)}")
        return False

def test_invalid_input() -> bool:
    """Test error handling with invalid input"""
    print_header("TEST 4: Error Handling (Empty Input)")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json={"text": ""},
            timeout=TIMEOUT
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print_success(f"Correctly rejected empty input with status {response.status_code}")
            return True
        else:
            print_error("Should have rejected empty input")
            return False
    except Exception as e:
        print_error(f"Error handling test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                 SPAM SMS DETECTION - API TEST SUITE              ║
║                                                                   ║
║              Testing Backend Endpoints and Functionality          ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    print(f"{Colors.RESET}")
    
    print_info(f"API Base URL: {API_BASE_URL}")
    print_info(f"Timeout: {TIMEOUT}s\n")
    
    results = {}
    
    # Run tests
    results["Health Check"] = test_health_check()
    results["Root Endpoint"] = test_root_endpoint()
    results["Spam Message"] = test_prediction(
        "Congratulations! You've won a free iPhone. Click here to claim!",
        "Spam"
    )
    results["Ham Message"] = test_prediction(
        "Hi, how are you doing today?",
        "Ham"
    )
    results["Batch Prediction"] = test_batch_prediction()
    results["Error Handling"] = test_invalid_input()
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = f"{Colors.GREEN}PASSED{Colors.RESET}" if passed_flag else f"{Colors.RED}FAILED{Colors.RESET}"
        print(f"  {test_name:.<50} {status}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.RESET}")
        sys.exit(1)
