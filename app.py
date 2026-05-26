import requests
import streamlit as st


st.set_page_config(
    page_title="Agent 商业研究中心",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

st.title("📊 智能 Agent 商业分析报告系统")
st.subheader("一键生成包含市场份额、抗脆弱性评估及投资建议的深度报告")

st.sidebar.header("模型配置")
mode_label = st.sidebar.selectbox(
    "生成模式",
    ["Jina 免费搜索 + 便宜 LLM", "Perplexity 深度研究"],
)
report_mode = "jina_llm" if mode_label.startswith("Jina") else "deep_research"

default_base_url = (
    "https://api.deepseek.com/v1"
    if report_mode == "jina_llm"
    else "https://api.perplexity.ai"
)
default_model = "deepseek-chat" if report_mode == "jina_llm" else "sonar-deep-research"

api_key_input = st.sidebar.text_input(
    "API Key（可选，留空则使用后端环境变量）",
    type="password",
    placeholder="sk-...",
)
jina_api_key_input = st.sidebar.text_input(
    "Jina API Key（可选）",
    type="password",
    help="Jina 搜索接口返回 401 时填写；留空则后端会降级继续生成报告。",
)
base_url_input = st.sidebar.text_input("API Base URL", value=default_base_url)
model_input = st.sidebar.text_input("模型名称", value=default_model)

with st.form("report_form"):
    target_input = st.text_input(
        "分析目标（公司或行业）",
        placeholder="例如: 瑞幸咖啡 / Tesla 2026 / 北美储能电池市场",
    )
    generate_btn = st.form_submit_button("启动 Agent 深度调研", type="primary")

STREAM_API_URL = "http://127.0.0.1:8000/api/generate_report_stream"


def parse_error(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text
    return f"后端服务异常：{detail}"


def stream_report(payload: dict):
    with requests.post(
        STREAM_API_URL,
        json=payload,
        timeout=300,
        stream=True,
    ) as response:
        if response.status_code != 200:
            raise RuntimeError(parse_error(response))

        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk


if generate_btn:
    if not target_input.strip():
        st.warning("⚠️ 请先在左侧输入分析目标！")
    else:
        spinner_text = (
            f"🕵️‍♂️ Agent 正在检索关于 '{target_input}' 的最新数据并进行抗脆弱性建模，"
            "这通常需要 1-2 分钟，请稍候..."
        )
        with st.spinner(spinner_text):
            try:
                st.markdown("---")
                target = target_input.strip()
                payload = {
                    "target": target,
                    "report_mode": report_mode,
                    "api_key": api_key_input.strip() or None,
                    "base_url": base_url_input.strip() or None,
                    "model": model_input.strip() or None,
                    "jina_api_key": jina_api_key_input.strip() or None,
                }
                chunks = []
                report_box = st.container()

                def capture_stream():
                    for chunk in stream_report(payload):
                        chunks.append(chunk)
                        yield chunk

                with report_box:
                    st.write_stream(capture_stream)

                report_markdown = "".join(chunks)
                st.success("✅ 报告生成成功！")
                st.download_button(
                    label="📥 下载 Markdown 报告",
                    data=report_markdown,
                    file_name=f"{target}_AI商业分析报告.md",
                    mime="text/markdown",
                )
            except RuntimeError as exc:
                st.error(f"❌ {exc}")
            except requests.exceptions.RequestException as exc:
                st.error(f"❌ 无法连接到后端服务器: {exc}")
else:
    st.info(
        "💡 请在左侧侧边栏输入你想研究的企业或细分行业名称"
        "（例如：'Tesla 2026' 或 '北美储能电池市场'），然后点击启动。"
    )
