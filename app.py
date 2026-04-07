import gradio as gr
import time
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random
import io
from PIL import Image
from matplotlib.patches import Patch

# -------------------------------
# PIPELINE SIMULATION
# -------------------------------

def run_easy():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    errors = {"C": "KeyError: column 'c' not found"}
    return errors, "B"

def run_medium():
    df = pd.DataFrame({"name": ["A"], "age": [25]})
    errors = {"D": "TypeError: unsupported operand"}
    return errors, "C"

def run_hard():
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    errors = {"D": "ValueError: shape mismatch"}
    return errors, "B"

# -------------------------------
# GRAPH VISUALIZATION
# -------------------------------

def draw_graph(current=None, visited=None, root=None):
    G = nx.DiGraph()
    edges = [("A","B"),("B","C"),("C","D")]
    G.add_edges_from(edges)

    color_map = []
    for node in G.nodes():
        if node == root:
            color_map.append("green")
        elif node == current:
            color_map.append("red")
        elif visited and node in visited:
            color_map.append("yellow")
        else:
            color_map.append("skyblue")

    plt.figure(figsize=(13, 7))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=2000, font_size=16, font_weight="bold")

    # Create legend positioned outside the plot area on the right
    legend_elements = [
        Patch(facecolor="green", label="Root Cause Node"),
        Patch(facecolor="red", label="Current Node"),
        Patch(facecolor="yellow", label="Visited Nodes"),
        Patch(facecolor="skyblue", label="Unvisited Nodes")
    ]
    plt.legend(handles=legend_elements, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=12, framealpha=0.9)
    plt.title("Pipeline Dependency Graph", fontsize=14, fontweight="bold")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)

    img = Image.open(buf)
    return img

# -------------------------------
# AGENT SIMULATION
# -------------------------------

def agent_reasoning(error_node, root):
    return f"""
Agent Analysis:
- Error detected at node {error_node}
- Traversing upstream dependencies
- Checking transformations
- Root cause identified at node {root}
- Suggested fix: Resolve schema mismatch
"""

# -------------------------------
# MAIN GENERATOR FUNCTION
# -------------------------------

def run_debugger(task):
    progress = 0
    logs = ""
    visited = []
    step_rewards = []
    total_reward = 0

    if task == "Easy":
        errors, root = run_easy()
    elif task == "Medium":
        errors, root = run_medium()
    else:
        errors, root = run_hard()

    error_node = list(errors.keys())[0]
    affected_nodes = ", ".join([n for n in ["A", "B", "C", "D"] if n not in [root, error_node]])
    summary_text = (
        f"🔴 Root Cause: Node {root}\n"
        f"🟠 Affected Nodes: {affected_nodes or 'None'}\n"
        f"⚠️ Total Errors: {len(errors)}"
    )
    suggestion_text = (
        f"Suggestion: Resolve the issue at node {error_node} and verify schema consistency "
        "across upstream transformations. Fix column name mismatch if present."
    )

    steps = [
        ("Step 1: Inspect output node", error_node),
        ("Step 2: Move upstream", "C"),
        ("Step 3: Analyze transformation", "B"),
        ("Step 4: Identify root cause", root),
    ]

    for i, (text, node) in enumerate(steps):
        logs += text + "\n"
        visited.append(node)
        progress = int((i+1)/len(steps)*100)

        # Calculate reward for this step
        step_reward = round(random.uniform(0.3, 0.6), 2)
        step_rewards.append((text, step_reward))
        total_reward += step_reward

        # Format rewards display
        rewards_text = "**Step Rewards Breakdown:**\n\n"
        for idx, (step_name, reward) in enumerate(step_rewards, 1):
            rewards_text += f"{step_name}: +{reward}\n"
        rewards_text += f"\n**Total Reward: {round(total_reward, 2)}**"

        graph_img = draw_graph(current=node, visited=visited, root=root)

        yield (
            "\n".join([f"{k}: {v}" for k,v in errors.items()]),
            progress,
            logs,
            graph_img,
            agent_reasoning(error_node, root),
            suggestion_text,
            rewards_text,
            summary_text,
            f"Root Cause: {root}\nSteps Taken: {len(steps)}"
        )

        time.sleep(1.2)

# -------------------------------
# UI
# -------------------------------

with gr.Blocks(title="MeshClean Debugger") as demo:
    css_styles = """
        body { background-color: #f8fbff; color: #0f172a; }
        .gradio-container { background-color: #f8fbff; color: #0f172a; }
        .gradio-markdown { color: #0f172a; }
        textarea, input, select { background-color: #ffffff !important; color: #0f172a !important; border-color: #2563eb !important; }
        .gr-button { background-color: #2563eb !important; color: #ffffff !important; }
        .gradio-image img { border: 1px solid #2563eb; }
        .gr-block { background-color: #ffffff; }
    """

    with gr.Row():
        
        # LEFT PANEL
        with gr.Column(scale=3):
            gr.Markdown("# MeshClean Debugger")
            gr.Markdown("### Technical Pipeline Error Investigator")

            summary = gr.Markdown(
                "🔴 Root Cause: -\n🟠 Affected Nodes: -\n⚠️ Total Errors: -"
            )

            task = gr.Dropdown(
                ["Easy", "Medium", "Hard"],
                label="Select Task"
            )

            error_box = gr.Textbox(label="Error Log", interactive=False)

            run_btn = gr.Button("Run Debugger")

            progress = gr.Slider(0, 100, value=0, label="Progress")

        # RIGHT PANEL
        with gr.Column(scale=7):

            gr.Markdown("### Debugging Process")
            logs = gr.Textbox(lines=10, interactive=False)

            gr.Markdown("### Pipeline Visualization")
            graph = gr.Image()

            gr.Markdown("### Agent Analysis")
            analysis = gr.Textbox(lines=6, interactive=False)

            gr.Markdown("### Suggestion")
            suggestion = gr.Textbox(lines=2, interactive=False)

            gr.Markdown("### Rewards Breakdown")
            rewards = gr.Markdown("No steps executed yet")

            gr.Markdown("### Final Result")
            result = gr.Textbox(lines=3, interactive=False)

    run_btn.click(
        fn=run_debugger,
        inputs=task,
        outputs=[
            error_box,
            progress,
            logs,
            graph,
            analysis,
            suggestion,
            rewards,
            summary,
            result,
        ]
    )

    demo.launch(css=css_styles)
