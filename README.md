# MCP-APIKit

## 项目简介

MCP-APIKit 是一个微服务控制平面（Microservice Control Plane）服务，专门用于从 Eolink OpenAPI 获取 API 信息，并将其提供给 IDE 的 MCP Server，以实现 API 场景的集成和管理。

## 功能特点

- 从 Eolink OpenAPI 获取完整的 API 列表和详细信息
- 提供标准化的 API 数据格式，便于 IDE 集成
- 支持 API 信息的缓存和更新
- 提供简单的配置界面，方便设置 Eolink OpenAPI 的访问凭证
- 自动创建默认配置文件，简化初始化过程

## 安装与配置

### 依赖项

- Python 3.8+
- 相关依赖包（见 requirements.txt）

### 安装步骤

1. 克隆仓库
   ```bash
   git clone https://github.com/yourusername/mcp-apikit.git
   cd mcp-apikit
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置 Eolink OpenAPI 凭证
   - 系统会自动创建默认配置文件 `config/config.json`
   - 通过配置界面或直接编辑配置文件设置 API Key 和其他必要参数

4. 启动服务
   ```bash
   python run.py
   ```

## 使用方法

1. 启动服务后，访问管理界面配置 Eolink OpenAPI 的访问凭证
2. MCP Server 可通过预定义的 API 端点获取 API 信息

## API 文档

### 获取 API 列表

```
GET /api/list
```

返回所有可用的 API 列表，格式如下：

```json
{
  "type": "array",
  "data": {
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
        "mock_enable": true,
        "case_cover": false,
        "message_encoding": "utf-8",
        "api_tag": "",
        "manager": "Scar",
        "creator": "Scar",
        "updater": "Scar"
      }
    ]
  },
  "status": "success"
}
```

### 获取 API 详情

```
GET /api/detail/{api_id}
```

返回指定 API 的详细信息，使用相同的标准响应格式。

## 配置说明

配置文件位于 `config/config.json`，主要包含以下配置项：

- `eolink_api_key`: Eolink OpenAPI 的 API Key
- `eolink_base_url`: Eolink OpenAPI 的基础 URL
- `cache_ttl`: API 信息缓存的有效期（秒）
- `space_id`: Eolink 空间 ID
- `project_id`: Eolink 项目 ID

**注意**: 配置文件已添加到 `.gitignore`，不会被提交到版本控制系统中，确保 API 密钥安全。

## 测试

运行测试脚本验证 API 响应格式：

```bash
python test_api_response.py
```

## 开发与贡献

欢迎贡献代码或提出问题。请遵循以下步骤：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件
