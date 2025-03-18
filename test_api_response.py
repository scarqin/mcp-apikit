import json
import requests
import sys

# Test the API response format
def test_api_response():
    """Test the API response format to ensure it matches the required structure."""
    # Sample API response data
    sample_response = {
        "paginator": {
            "page": 1,
            "size": 10,
            "total": 11
        },
        "items": [
            {
                "api_id": 47405190,
                "api_name": "获取阅读信息",
                "api_uri": "/readdetail",
                "api_status": 0,
                "api_request_type": 1,
                "create_time": "2022-03-20 22:54:10",
                "group_id": 1632813,
                "api_update_time": "2022-03-20 22:54:10",
                "starred": 0,
                "order_num": 0,
                "remove_time": "2022-11-03 21:07:00",
                "api_protocol": 0,
                "api_type": "http",
                "api_manager_id": 108,
                "update_user_id": 108,
                "create_user_id": 108,
                "group_path": "1632813",
                "group_name": "书籍",
                "customize_list": [],
                "version_name": "",
                "mock_enable": True,
                "case_cover": False,
                "message_encoding": "utf-8",
                "api_tag": "",
                "manager": "Scar",
                "creator": "Scar",
                "updater": "Scar"
            }
        ]
    }
    
    # Expected response format
    expected_response = {
        "type": "array",
        "data": sample_response,
        "status": "success"
    }
    
    print("Sample API Response:")
    print(json.dumps(expected_response, indent=2, ensure_ascii=False))
    
    # Try to connect to the local server if it's running
    try:
        base_url = "http://localhost:8000"
        response = requests.get(f"{base_url}/api/list")
        if response.status_code == 200:
            print("\nActual API Response from server:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            
            # Verify response structure
            actual_response = response.json()
            if "type" in actual_response and "data" in actual_response and "status" in actual_response:
                if "paginator" in actual_response["data"] and "items" in actual_response["data"]:
                    print("\n✅ API response format is correct!")
                else:
                    print("\n❌ API response format is incorrect. Missing 'paginator' or 'items' in data.")
            else:
                print("\n❌ API response format is incorrect. Missing 'type', 'data', or 'status'.")
        else:
            print(f"\nFailed to connect to server: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("\nCould not connect to the local server. Is it running?")
        print("You can start the server with: python run.py")

if __name__ == "__main__":
    test_api_response()
