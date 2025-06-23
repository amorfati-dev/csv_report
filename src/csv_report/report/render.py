import json
import pathlib
from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = pathlib.Path(__file__).parent
env = Environment(
    loader=FileSystemLoader(BASE_DIR),
    autoescape=select_autoescape()
)

def render(report_date: str):
    """Render the HTML report with data from dummy.json."""
    # Load data from dummy.json (located in project root data/ directory)
    data_file = pathlib.Path("/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/03_side_hussel/04_dev/projekte/csv_report/data/dummy.json")
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {data_file}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"📄 File content:")
        with open(data_file, 'r', encoding='utf-8') as f:
            print(f.read())
        return
    
    # Update the report_date in the data
    data['report_date'] = report_date
    
    # Render template
    tmpl = env.get_template("report_template.html")
    html = tmpl.render(**data)
    
    # Save output to reports directory
    output_dir = BASE_DIR.parent.parent.parent / "reports"
    output_dir.mkdir(exist_ok=True)
    out = output_dir / "report_output.html"
    out.write_text(html, encoding="utf-8")
    
    print(f"✓ Report gerendert → {out.relative_to(BASE_DIR.parent.parent.parent)}")

if __name__ == "__main__":
    render("23. Juni 2025") 