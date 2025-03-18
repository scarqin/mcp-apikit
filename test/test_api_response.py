import json
from src.utils.config_manager import ConfigManager
from src.utils.eolink_client import EolinkClient

def main():
    # 初始化配置管理器和Eolink客户端
    config_manager = ConfigManager()
    eolink_client = EolinkClient(config_manager)
    
    # 获取配置文件中的space_id和project_id
    space_id = config_manager.space_id
    project_id = config_manager.project_id
    
    # 调用get_all_apis方法获取API列表
    apis = eolink_client.get_all_apis(
        space_id=space_id,
        project_id=project_id,
        page=1,
        size=10  # 限制返回的API数量，便于查看
    )
    
    # 打印API响应信息
    print("API响应信息:")
    print(json.dumps(apis, indent=2, ensure_ascii=False))
    
    # 如果想查看原始响应，可以直接调用_make_request方法
    print("\n原始响应信息:")
    endpoint = "/v3/api-management/apis"
    params = {
        "space_id": space_id,
        "project_id": project_id,
        "page": 1,
        "size": 10
    }
    raw_response = eolink_client._make_request(endpoint, params=params)
    print(json.dumps(raw_response, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
