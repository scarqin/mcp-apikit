# MCP-APIKit

## 项目简介

MCP-APIKit 是一个微服务控制平面（Microservice Control Plane）服务，专门用于从 Eolink OpenAPI 获取 API 信息，并将其提供给 IDE 的 MCP Server，以实现 API 场景的集成和管理。

## 功能特点

- 从 Eolink OpenAPI 获取完整的 API 列表和详细信息
- 提供标准化的 API 数据格式，便于 IDE 集成
- 支持 API 信息的缓存和更新
- 提供简单的配置界面，方便设置 Eolink OpenAPI 的访问凭证

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
   - 在配置文件中设置 API Key 和其他必要参数

4. 启动服务
   ```bash
   source venv/bin/activate && python run.py
   ```

## 使用方法

1. 启动服务后，访问管理界面配置 Eolink OpenAPI 的访问凭证
2. MCP Server 可通过预定义的 API 端点获取 API 信息

## API 文档

### 获取 API 列表

```
GET /api/list
```

返回所有可用的 API 列表。

### 获取 API 详情

```
GET /api/detail/{api_id}
```

返回指定 API 的详细信息。

## 配置说明

配置文件位于 `config/config.json`，主要包含以下配置项：

- `eolink_api_key`: Eolink OpenAPI 的 API Key
- `eolink_base_url`: Eolink OpenAPI 的基础 URL
- `cache_ttl`: API 信息缓存的有效期（秒）

## 开发与贡献

欢迎贡献代码或提出问题。请遵循以下步骤：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件
