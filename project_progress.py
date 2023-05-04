from string import Template
import yaml


def format_list_items(items):
    formatted_items = "\n".join([f"\\item {item}" for item in items])
    return f"\\begin{{itemize}}\n{formatted_items}\n\\end{{itemize}}"


def generate_title_slide_latex(title_slide_data):
    title = title_slide_data["title"]
    author = title_slide_data["author"]
    date = title_slide_data["date"]
    logo = title_slide_data["logo"]

    preamble_latex = r"""
    \logo{\includegraphics[height=1cm]{%s}}
    \title{%s}
    \author{%s}
    \date{%s}
    """ % (logo, title, author, date)

    return preamble_latex


def generate_project_timeline_latex(timeline_data):
    sprints = timeline_data

    sprint_lines = []
    for sprint in sprints:
        sprint_line = f"\\ganttbar[progress={sprint['progress']}, bar label font=\\tiny, bar/.append style={{fill={sprint['color']}}}]{{{sprint['label']}}}{{{sprint['start']}}}{{{sprint['end']}}}"
        sprint_lines.append(sprint_line)

    sprint_lines_str = " \\\\\n".join(sprint_lines)

    latex = f"""
\\begin{{frame}}
\\frametitle{{Project Timeline}}
\\begin{{center}}
\\begin{{ganttchart}}[
  x unit=0.1cm,
  y unit chart=0.5cm,
  time slot format=isodate,
  title/.style={{fill=none, draw=none, yshift=0.375cm}}
]{{2023-03-06}}{{2023-06-11}}
  \\gantttitlecalendar{{month}} \\\\
  {sprint_lines_str}
\\end{{ganttchart}}
\\end{{center}}
\\end{{frame}}
    """
    return latex.strip()


def generate_accomplishments_latex(accomplishments_data):
    accomplishments_latex_lines = [
        r"\begin{frame}{What We Have Accomplished So Far}\begin{itemize}"]

    for accomplishment in accomplishments_data:
        accomplishments_latex_lines.append(r"\item " + accomplishment)

    accomplishments_latex_lines.append(r"\end{itemize}\end{frame}")

    return "\n".join(accomplishments_latex_lines)


def generate_demo_latex(demo_data):
    demo_latex_lines = [
        r"\begin{frame}{Demo or Video of the Demo}",
        demo_data["description"] + r" \href{" + demo_data["url"] +
        r"}{\textcolor{blue}{" + demo_data["link_text"] + r"}} or video.",
        r"\end{frame}"
    ]
    return "\n".join(demo_latex_lines)


def generate_concerns_and_risks_latex(concerns_and_risks_data):
    concerns_and_risks_latex_lines = [
        r"\begin{frame}{Concerns and Risks}\begin{itemize}"]

    for concern_or_risk in concerns_and_risks_data:
        concerns_and_risks_latex_lines.append(r"\item " + concern_or_risk)

    concerns_and_risks_latex_lines.append(r"\end{itemize}\end{frame}")

    return "\n".join(concerns_and_risks_latex_lines)


def generate_next_sprint_latex(next_sprint_data):
    next_sprint_latex_lines = [
        r"\begin{frame}{On Deck for the Next Sprint}\begin{itemize}"]

    for next_sprint_item in next_sprint_data:
        next_sprint_latex_lines.append(r"\item " + next_sprint_item)

    next_sprint_latex_lines.append(r"\end{itemize}\end{frame}")

    return "\n".join(next_sprint_latex_lines)


def generate_q_and_a_latex(q_and_a_data):
    q_and_a_latex_lines = [
        r"\begin{frame}{Q&A}",
        q_and_a_data["description"],
        r"\end{frame}"
    ]
    return "\n".join(q_and_a_latex_lines)


def generate_project_summary_latex(project_summary_data):
    project_summary_latex = r"\begin{frame}{Project Summary}\begin{itemize}"
    for item in project_summary_data:
        project_summary_latex += r"\item " + item + "\n"
    project_summary_latex += r"\end{itemize}\end{frame}"
    return project_summary_latex


# Read YAML content from file
with open('outline.yaml', 'r') as file:
    outline = yaml.safe_load(file)

latex_sections = []

for section in outline:
    if "title_slide" in section:
        title_slide_data = section["title_slide"]
        title_slide_preamble = generate_title_slide_latex(title_slide_data)

    if "project_timeline" in section:
        project_timeline_data = section["project_timeline"]
        timeline_latex = generate_project_timeline_latex(project_timeline_data)
        latex_sections.append(timeline_latex)

    if "accomplishments" in section:
        accomplishments_data = section["accomplishments"]
        accomplishments_latex = generate_accomplishments_latex(
            accomplishments_data)
        latex_sections.append(accomplishments_latex)

    if "demo" in section:
        demo_data = section["demo"]
        demo_latex = generate_demo_latex(demo_data)
        latex_sections.append(demo_latex)

    if "next_sprint" in section:
        next_sprint_data = section["next_sprint"]
        next_sprint_latex = generate_next_sprint_latex(next_sprint_data)
        latex_sections.append(next_sprint_latex)

    if "concerns_or_risks" in section:
        concerns_and_risks_data = section["concerns_or_risks"]
        concerns_and_risks_latex = generate_concerns_and_risks_latex(
            concerns_and_risks_data)
        latex_sections.append(concerns_and_risks_latex)

    if "q_and_a" in section:
        q_and_a_data = section["q_and_a"]
        q_and_a_latex = generate_q_and_a_latex(q_and_a_data)
        latex_sections.append(q_and_a_latex)

    if "project_summary" in section:
        data = section["project_summary"]
        data = generate_project_summary_latex(data)
        latex_sections.append(data)

# Join all the generated LaTeX sections with newline separators
content = "\n".join(latex_sections)


def generate_latex_document(title_slide_preamble, content):
    latex_document = r"""
\documentclass{beamer}
\usepackage{pgfgantt}
\usepackage{hyperref}
\usepackage{xcolor}

\usetheme{metropolis}           % Use metropolis theme
\definecolor{header}{RGB}{197,32,49}
\definecolor{font}{RGB}{255,255,255}

% Set colors for header bar
\setbeamercolor{palette primary}{bg=header,fg=font}
\setbeamercolor{palette secondary}{bg=header,fg=font}
\setbeamercolor{palette tertiary}{bg=header,fg=font}
\setbeamercolor{palette quaternary}{bg=header,fg=font}
""" + title_slide_preamble + r"""

\begin{document}

\begin{frame}
\titlepage
\end{frame}
""" + content + r"""

\end{document}
"""
    return latex_document


latex_document = generate_latex_document(title_slide_preamble, content)


print(latex_document)
