def generate_html_report(ports):
    html_template = ""

    # خواندن قالب HTML
    with open("templates/report_template.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    rows = ""
    for p in ports:
        rows += f"<tr><td>{p['port']}</td><td>{p['type']}</td></tr>"

    final_html = html_template.replace("{{ROWS}}", rows)

    with open("results/report.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("✔ HTML report generated!")
