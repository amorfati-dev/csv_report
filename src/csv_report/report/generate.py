"""Module for generating reports."""
from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader


def generate_report(data: pd.DataFrame) -> str:
    """Generate a report from the DataFrame.

    Args:
        data: DataFrame containing the analysis data

    Returns:
        Generated report as a string
    """
    # Initialize Jinja2 environment
    template_dir = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Load and render template
    template = env.get_template("template.j2")
    return template.render(data=data)


def save_report(report: str, output_path: Path) -> Path:
    """Save the generated report to a file.

    Args:
        report: The report content as a string
        output_path: The path where to save the report

    Returns:
        Path to the saved report file
    """
    # Create parent directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the report
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return output_path