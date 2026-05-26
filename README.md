# AI Agent 商业分析报告系统

一个 FastAPI + Streamlit 的最小可运行 Demo，用联网深度研究模型生成商业分析报告。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置环境变量

### 模式一：深度研究模型

默认使用 Perplexity OpenAI-compatible API：

```bash
export REPORT_MODE="deep_research"
export PERPLEXITY_API_KEY="你的 Perplexity Key"
```

可选配置：

```bash
export AGENT_BASE_URL="https://api.perplexity.ai"
export AGENT_MODEL="sonar-deep-research"
```

### 模式二：Jina 免费搜索 + 便宜 LLM

这种模式会先调用 Jina AI 搜索接口抓取实时资料，再把搜索结果喂给 DeepSeek 或其他 OpenAI-compatible 模型。

```bash
export REPORT_MODE="jina_llm"
export LLM_API_KEY="你的 DeepSeek 或转发站 Key"
export LLM_BASE_URL="https://api.deepseek.com/v1"
export LLM_MODEL="deepseek-chat"
```

可选搜索配置：

```bash
export JINA_SEARCH_BASE_URL="https://s.jina.ai/"
export SEARCH_TIMEOUT_SECONDS="20"
export SEARCH_CONTEXT_CHARS="12000"
```

如果未来把前端换成 React、Vue 或纯 HTML/JS，可以按域名限制 CORS：

```bash
export CORS_ALLOW_ORIGINS="http://localhost:5173,https://your-domain.com"
```

如果改用其他 OpenAI-compatible 服务，也可以设置：

```bash
export OPENAI_API_KEY="你的 API Key"
export AGENT_BASE_URL="https://api.openai.com/v1"
export AGENT_MODEL="gpt-4.1"
```

## 启动后端

```bash
.venv/bin/python server.py
```

后端地址：http://127.0.0.1:8000

接口：

- `POST /api/generate_report`：普通非流式返回，适合服务端批处理。
- `POST /api/generate_report_stream`：流式返回 Markdown，适合网页端实时展示。

## 启动前端

另开一个终端：

```bash
.venv/bin/streamlit run app.py
```

前端默认地址：http://localhost:8501

前端请求超时已设置为 `timeout=300` 秒，适合 `sonar-deep-research` 这类耗时较长的深度研究模型。
