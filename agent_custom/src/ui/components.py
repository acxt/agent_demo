"""FastHTML + DaisyUI 组件"""

from fasthtml.common import *


def page_layout(title: str, *content):
    """页面布局
    
    Args:
        title: 页面标题
        *content: 页面内容
        
    Returns:
        完整页面HTML
    """
    return Html(
        Head(
            Title(title),
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            # Tailwind CSS + DaisyUI
            Link(href="https://cdn.jsdelivr.net/npm/daisyui@4.12.14/dist/full.min.css", rel="stylesheet"),
            Script(src="https://cdn.tailwindcss.com"),
            # HTMX
            Script(src="https://unpkg.com/htmx.org@1.9.10"),
            Style("""
                @config "./tailwind.config.js";
                @plugin "daisyui";
            """)
        ),
        Body(
            Div(
                *content,
                cls="min-h-screen bg-base-200"
            )
        )
    )


def navbar(title: str = "VideoAgent"):
    """导航栏组件"""
    return Div(
        Div(
            # Logo
            Div(
                A(title, href="/", cls="btn btn-ghost text-xl"),
                cls="flex-1"
            ),
            # 主题切换
            Div(
                Label(
                    Input(
                        type="checkbox",
                        value="dark",
                        cls="toggle theme-controller"
                    ),
                    Svg(
                        cls="w-6 h-6",
                        viewBox="0 0 24 24",
                        fill="currentColor"
                    ),
                    cls="swap swap-rotate"
                ),
                cls="flex-none"
            ),
            cls="navbar bg-base-100 shadow-lg"
        )
    )


def hero_section():
    """首页Hero区域"""
    return Div(
        Div(
            H1("AI视频创作助手", cls="text-5xl font-bold"),
            P("基于热点分析的智能视频生成系统", cls="py-6 text-lg"),
            Button(
                "开始创作",
                cls="btn btn-primary btn-lg",
                onclick="document.getElementById('create_modal').showModal()"
            ),
            cls="max-w-md"
        ),
        cls="hero min-h-[60vh] bg-base-200"
    )


def task_card(task: dict):
    """任务卡片组件
    
    Args:
        task: 任务数据
    """
    status_badge = {
        "pending": "badge-warning",
        "running": "badge-info",
        "completed": "badge-success",
        "failed": "badge-error"
    }
    
    return Div(
        Div(
            # 卡片标题
            H2(task.get("title", "未命名任务"), cls="card-title"),
            # 状态徽章
            Div(
                Span(task.get("status", "pending"), cls=f"badge {status_badge.get(task.get('status'), '')}"),
                cls="card-actions justify-end"
            ),
            # 任务信息
            P(task.get("description", ""), cls="text-sm text-base-content/70"),
            Div(
                Span(f"创建时间: {task.get('created_at', '')}", cls="text-xs"),
                cls="mt-2"
            ),
            # 操作按钮
            Div(
                Button("查看详情", cls="btn btn-sm btn-primary"),
                Button("重试", cls="btn btn-sm btn-ghost") if task.get("status") == "failed" else None,
                cls="card-actions justify-end mt-4"
            ),
            cls="card-body"
        ),
        cls="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow"
    )


def create_modal():
    """创建任务模态框"""
    return Dialog(
        Div(
            Form(
                H3("创建新任务", cls="font-bold text-lg mb-4"),
                
                # 任务类型选择
                Div(
                    Label("任务类型", cls="label"),
                    Select(
                        Option("完整流程", value="complete"),
                        Option("仅查找热点", value="hotspot"),
                        Option("分析视频", value="analyze"),
                        Option("生成提示词", value="generate"),
                        name="task_type",
                        cls="select select-bordered w-full"
                    ),
                    cls="form-control mb-4"
                ),
                
                # 关键词输入
                Div(
                    Label("搜索关键词（用逗号分隔）", cls="label"),
                    Input(
                        type="text",
                        name="keywords",
                        placeholder="例如: AI, 科技, 教程",
                        cls="input input-bordered w-full"
                    ),
                    cls="form-control mb-4"
                ),
                
                # 用户需求
                Div(
                    Label("创作需求", cls="label"),
                    Textarea(
                        name="user_input",
                        placeholder="描述你想要创作的视频内容...",
                        cls="textarea textarea-bordered w-full h-24"
                    ),
                    cls="form-control mb-4"
                ),
                
                # 按钮组
                Div(
                    Button("取消", type="button", cls="btn", onclick="this.closest('dialog').close()"),
                    Button(
                        "创建",
                        type="submit",
                        cls="btn btn-primary",
                        hx_post="/api/tasks",
                        hx_target="#task_list",
                        hx_swap="afterbegin"
                    ),
                    cls="modal-action"
                ),
                
                method="dialog"
            ),
            cls="modal-box"
        ),
        Form(method="dialog", cls="modal-backdrop"),
        id="create_modal",
        cls="modal"
    )


def stats_section(stats: dict):
    """统计数据展示"""
    return Div(
        # 统计卡片
        Div(
            Div(
                Div("总任务数", cls="stat-title"),
                Div(str(stats.get("total", 0)), cls="stat-value text-primary"),
                cls="stat"
            ),
            cls="stats shadow"
        ),
        Div(
            Div(
                Div("运行中", cls="stat-title"),
                Div(str(stats.get("running", 0)), cls="stat-value text-info"),
                cls="stat"
            ),
            cls="stats shadow"
        ),
        Div(
            Div(
                Div("已完成", cls="stat-title"),
                Div(str(stats.get("completed", 0)), cls="stat-value text-success"),
                cls="stat"
            ),
            cls="stats shadow"
        ),
        Div(
            Div(
                Div("失败", cls="stat-title"),
                Div(str(stats.get("failed", 0)), cls="stat-value text-error"),
                cls="stat"
            ),
            cls="stats shadow"
        ),
        cls="grid grid-cols-1 md:grid-cols-4 gap-4 p-4"
    )


def loading_spinner():
    """加载动画"""
    return Div(
        Span(cls="loading loading-spinner loading-lg text-primary"),
        cls="flex justify-center items-center h-64"
    )


def alert(message: str, type: str = "info"):
    """提示框
    
    Args:
        message: 提示信息
        type: 类型 (info/success/warning/error)
    """
    icons = {
        "info": "ℹ️",
        "success": "✓",
        "warning": "⚠",
        "error": "✕"
    }
    
    return Div(
        Svg(cls="stroke-current shrink-0 h-6 w-6"),
        Span(message),
        cls=f"alert alert-{type}"
    )

