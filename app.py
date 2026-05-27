import base64
import re
from pathlib import Path

import requests
import streamlit as st


st.set_page_config(
    page_title="Agent 商业研究中心",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

ASSET_DIR = Path(__file__).parent / "assets"
HERO_IMAGE = ASSET_DIR / "research-dashboard-bg.png"


def image_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


HERO_BG = image_data_uri(HERO_IMAGE)

st.markdown(
    f"""
    <style>
    :root {{
        --paper: #fff8ef;
        --paper-2: #fbf1e4;
        --ink: #33281f;
        --muted: #8f806f;
        --hairline: #e4d5bb;
        --gold: #c5a35f;
        --gold-soft: rgba(197, 163, 95, .16);
        --jade: #55775f;
    }}
    .stApp {{
        background:
            linear-gradient(180deg, rgba(255,248,239,.92), rgba(246,239,228,.98)),
            #f6efe4;
        color: var(--ink);
    }}
    [data-testid="stHeader"] {{
        background: rgba(255, 248, 239, .72);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid rgba(228, 213, 187, .8);
    }}
    [data-testid="stSidebar"] {{
        background: #f1e7d7;
        border-right: 1px solid var(--hairline);
    }}
    [data-testid="stSidebar"] * {{
        letter-spacing: 0;
    }}
    .block-container {{
        max-width: 1320px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }}
    .od-hero {{
        min-height: 300px;
        padding: 30px 32px;
        border: 1px solid var(--hairline);
        border-radius: 8px;
        background-image:
            linear-gradient(90deg, rgba(255,248,239,.96) 0%, rgba(255,248,239,.88) 42%, rgba(255,248,239,.38) 100%),
            url("{HERO_BG}");
        background-size: cover;
        background-position: center;
        box-shadow: 0 18px 48px rgba(61, 47, 34, .10);
        margin-bottom: 22px;
    }}
    .od-kicker {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: var(--jade);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 18px;
    }}
    .od-kicker::before {{
        content: "";
        width: 7px;
        height: 18px;
        border-radius: 2px;
        background: var(--gold);
    }}
    .od-hero h1 {{
        max-width: 680px;
        color: var(--ink);
        font-size: 46px;
        line-height: 1.05;
        letter-spacing: 0;
        margin: 0 0 14px;
    }}
    .od-hero p {{
        max-width: 660px;
        color: var(--muted);
        font-size: 16px;
        line-height: 1.7;
        margin: 0;
    }}
    .od-hero-strip {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 24px;
    }}
    .od-chip {{
        border: 1px solid rgba(197,163,95,.34);
        background: rgba(255,250,243,.72);
        color: #6f5d49;
        border-radius: 999px;
        padding: 7px 11px;
        font-size: 12px;
    }}
    .od-panel {{
        border: 1px solid var(--hairline);
        background: rgba(255,250,243,.84);
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 10px 28px rgba(61, 47, 34, .07);
    }}
    .od-section-title {{
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--ink);
        font-weight: 760;
        margin: 2px 0 14px;
    }}
    .od-section-title::before {{
        content: "";
        width: 4px;
        height: 18px;
        border-radius: 2px;
        background: var(--gold);
    }}
    div[data-testid="stForm"] {{
        border: 1px solid var(--hairline);
        background: rgba(255,250,243,.92);
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 10px 28px rgba(61,47,34,.07);
    }}
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {{
        border-radius: 8px !important;
    }}
    .stButton button, .stDownloadButton button, .stFormSubmitButton button {{
        border-radius: 8px !important;
        border: 1px solid rgba(197,163,95,.35) !important;
        background: #c5a35f !important;
        color: white !important;
        font-weight: 700 !important;
    }}
    .stButton button:hover, .stDownloadButton button:hover, .stFormSubmitButton button:hover {{
        border-color: #a9853d !important;
        background: #ad8b46 !important;
    }}
    div[data-testid="stExpander"] {{
        border: 1px solid var(--hairline);
        border-radius: 8px;
        background: rgba(255,250,243,.72);
    }}
    h1, h2, h3, h4 {{
        letter-spacing: 0 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="od-hero">
        <div class="od-kicker">Agent Research Workbench</div>
        <h1>智能商业分析报告系统</h1>
        <p>先搭建指标骨架，再生成市场份额、竞争格局、抗脆弱性和投资建议。左侧做投研仪表盘，右侧保留 AI 深度解读，让长报告变得可审计、可追踪、可快速阅读。</p>
        <div class="od-hero-strip">
            <span class="od-chip">Market Share</span>
            <span class="od-chip">Competitive Forces</span>
            <span class="od-chip">Antifragility</span>
            <span class="od-chip">Evidence-first Report</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

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

st.markdown('<div class="od-section-title">研究参数</div>', unsafe_allow_html=True)
with st.form("report_form"):
    target_input = st.text_input(
        "分析目标（公司或行业）",
        placeholder="例如: 瑞幸咖啡 / Tesla 2026 / 北美储能电池市场",
    )
    col_years, col_lens = st.columns([1, 2])
    with col_years:
        analysis_years = st.slider("分析回看年限", min_value=1, max_value=10, value=5)
    with col_lens:
        analysis_lens = st.selectbox(
            "优先分析视角",
            ["综合", "估值与财务质量", "市场份额与竞争格局", "现金流与资产质量", "抗脆弱性与风险", "增长与商业模式"],
        )
    generate_btn = st.form_submit_button("启动 Agent 深度调研", type="primary")

with st.expander("输出结构", expanded=False):
    st.markdown(
        """
        - 核心指标仪表盘：先列关键数据、置信度和待核验项
        - 证据清单：来源、日期、链接、支撑结论
        - 阅读路线：先看机会、风险和关键判断
        - 四大正文：市场格局、竞争分析、抗脆弱性、投资建议
        """
    )

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


def default_metrics(target: str, years: int, lens: str):
    return [
        {"label": "分析标的", "value": target, "sub": f"近 {years} 年 | {lens}"},
        {"label": "市场份额", "value": "待核验", "sub": "需引用权威来源"},
        {"label": "增长质量", "value": "待核验", "sub": "收入/利润/用户"},
        {"label": "竞争强度", "value": "待核验", "sub": "直接竞品与替代品"},
        {"label": "现金流/资产", "value": "待核验", "sub": "经营现金流与负债"},
        {"label": "抗脆弱性", "value": "待判断", "sub": "冲击中是否受益"},
    ]


def extract_metric_cards(markdown: str, fallback_cards: list[dict]):
    cards = [card.copy() for card in fallback_cards]
    patterns = {
        "市场份额": r"(市场份额|份额)[^|\n]*\|[^|\n]*?([0-9]+(?:\.[0-9]+)?%)",
        "增长质量": r"(收入|利润|营收|增长)[^|\n]*\|[^|\n]*?([+-]?[0-9]+(?:\.[0-9]+)?%)",
        "竞争强度": r"(竞争强度|竞争格局|竞争)[^|\n]*\|[^|\n]*?([^|\n]{2,20})",
        "现金流/资产": r"(现金流|资产质量|负债)[^|\n]*\|[^|\n]*?([^|\n]{2,20})",
        "抗脆弱性": r"(抗脆弱性|抗脆弱)[^|\n]*\|[^|\n]*?([^|\n]{2,20})",
    }
    for card in cards:
        pattern = patterns.get(card["label"])
        if not pattern:
            continue
        match = re.search(pattern, markdown)
        if match:
            card["value"] = match.group(2).strip()
            card["sub"] = "来自报告自动抽取"
    return cards


def render_metric_card(card: dict):
    st.markdown(
        f"""
        <div style="
            border:1px solid #e4d5bb;
            border-radius:8px;
            padding:15px 14px 13px;
            background:linear-gradient(180deg, #fffaf3 0%, #fff6ea 100%);
            box-shadow:0 8px 22px rgba(61,47,34,.06);
            min-height:104px;
        ">
            <div style="font-size:12px;color:#8d7b68;margin-bottom:8px;">{card["label"]}</div>
            <div style="font-size:24px;font-weight:700;color:#3d2f22;line-height:1.1;">{card["value"]}</div>
            <div style="font-size:11px;color:#a89880;margin-top:8px;">{card["sub"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard(cards: list[dict], search_status: str = "等待生成"):
    st.markdown('<div class="od-panel">', unsafe_allow_html=True)
    st.markdown('<div class="od-section-title">指标仪表盘</div>', unsafe_allow_html=True)
    first, second = st.columns(2)
    for index, card in enumerate(cards):
        with first if index % 2 == 0 else second:
            render_metric_card(card)
            st.write("")
    st.caption(f"资料状态：{search_status}")
    st.markdown("</div>", unsafe_allow_html=True)


def render_workflow(years: int, lens: str):
    st.markdown('<div class="od-panel">', unsafe_allow_html=True)
    st.markdown('<div class="od-section-title">阅读路线</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        1. 先看近 `{years}` 年关键指标是否有真实来源。
        2. 再看 `{lens}` 是否支持投资结论。
        3. 最后检查黑天鹅/灰犀牛风险是否改变仓位建议。
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)


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
                    "analysis_years": analysis_years,
                    "analysis_lens": analysis_lens,
                    "report_mode": report_mode,
                    "api_key": api_key_input.strip() or None,
                    "base_url": base_url_input.strip() or None,
                    "model": model_input.strip() or None,
                    "jina_api_key": jina_api_key_input.strip() or None,
                }
                chunks = []
                dashboard_col, report_col = st.columns([0.9, 1.7], gap="large")
                base_cards = default_metrics(target, analysis_years, analysis_lens)

                def capture_stream():
                    for chunk in stream_report(payload):
                        chunks.append(chunk)
                        yield chunk

                with dashboard_col:
                    render_dashboard(base_cards)
                    render_workflow(analysis_years, analysis_lens)
                    with st.expander("证据与来源", expanded=True):
                        st.caption("报告生成后，请优先查看右侧“证据清单”。仪表盘中的数值会尽量从报告表格自动抽取。")

                with report_col:
                    st.markdown('<div class="od-section-title">AI 解读</div>', unsafe_allow_html=True)
                    st.write_stream(capture_stream)

                report_markdown = "".join(chunks)
                updated_cards = extract_metric_cards(report_markdown, base_cards)
                if updated_cards != base_cards:
                    with dashboard_col:
                        st.markdown("---")
                        render_dashboard(updated_cards, "已从报告中抽取部分指标")

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
