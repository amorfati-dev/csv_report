"""Main module for the CSV report generator using Typer CLI."""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from sqlalchemy import text

from .load import load_csv
from .report.generate import generate_report, save_report
from .database import DatabaseService

# Initialize Typer app and console
app = typer.Typer(help="Generate reports from CSV files with database tracking")
console = Console()


@app.command()
def generate(
    csv_file: Optional[str] = typer.Option(
        None, 
        "--csv-file", 
        "-f",
        help="Path to the CSV file to analyze"
    ),
    output_format: str = typer.Option(
        "markdown",
        "--output-format",
        "-o", 
        help="Format of the output report",
        case_sensitive=False
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "--output",
        help="Output file path (default: reports/sp500_analysis.{format})"
    )
):
    """Generate a report from a CSV file and store the run in the database."""
    
    # Validate output format
    if output_format.lower() not in ["markdown", "html"]:
        typer.echo(f"❌ Invalid output format: {output_format}. Use 'markdown' or 'html'")
        raise typer.Exit(1)
    
    # Initialize database service
    db_service = DatabaseService()
    
    try:
        with console.status("[bold green]Loading CSV data..."):
            df = load_csv(csv_file=csv_file)
        
        # Create run record in database
        run = db_service.create_run(
            csv_file=csv_file or "default",
            output_format=output_format.lower(),
            rows_processed=len(df),
            status="processing"
        )
        
        console.print(f"📊 Processing {len(df)} rows...")
        
        with console.status("[bold green]Generating report..."):
            # Generate report
            report = generate_report(df)
            
            # Determine output file path
            if output_file:
                output_path = Path(output_file)
            else:
                output_path = Path(f"reports/sp500_analysis.{output_format.lower()}")
            
            # Ensure reports directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save report
            final_path = save_report(report, output_path)
        
        # Update run status to completed
        run.status = "completed"
        with db_service.engine.begin() as conn:
            conn.execute(
                text("UPDATE run SET status = 'completed' WHERE id = :id"), 
                {"id": run.id}
            )
        
        console.print(f"✅ Report generated and saved to: {final_path}")
        console.print(f"📊 Run recorded in database with ID: {run.id}")
        
    except Exception as e:
        # Update run status to failed
        if 'run' in locals():
            run.status = "failed"
            run.error_message = str(e)
            with db_service.engine.begin() as conn:
                conn.execute(
                    text("UPDATE run SET status = 'failed', error_message = :error WHERE id = :id"), 
                    {"error": str(e), "id": run.id}
                )
        
        console.print(f"❌ Error: {e}")
        raise typer.Exit(1)


@app.command()
def show_runs(
    limit: int = typer.Option(
        10, 
        "--limit", 
        "-l",
        help="Number of recent runs to show"
    ),
    run_id: Optional[int] = typer.Option(
        None,
        "--run-id",
        "-r", 
        help="Show details for a specific run ID"
    )
):
    """Show recent report generation runs from the database."""
    
    db_service = DatabaseService()
    
    if run_id:
        # Show specific run details
        run = db_service.get_run_by_id(run_id)
        if not run:
            console.print(f"❌ Run with ID {run_id} not found")
            raise typer.Exit(1)
        
        # Create detailed panel
        details = f"""
📅 Timestamp: {run.timestamp}
📁 CSV File: {run.csv_file}
📄 Output Format: {run.output_format}
✅ Status: {run.status}
"""
        if run.rows_processed:
            details += f"📊 Rows Processed: {run.rows_processed}\n"
        if run.error_message:
            details += f"❌ Error: {run.error_message}\n"
        
        console.print(Panel(details, title=f"Run Details (ID: {run.id})"))
        
        # Show KPIs for this run
        kpis = db_service.get_kpis_for_run(run.id)
        if kpis:
            kpi_table = Table(title=f"KPIs ({len(kpis)})")
            kpi_table.add_column("Name", style="cyan")
            kpi_table.add_column("Value", style="green")
            kpi_table.add_column("Unit", style="yellow")
            kpi_table.add_column("Description", style="white")
            
            for kpi in kpis:
                kpi_table.add_row(
                    kpi.name,
                    str(kpi.value),
                    kpi.unit or "",
                    kpi.description or ""
                )
            console.print(kpi_table)
        else:
            console.print("📈 No KPIs recorded for this run")
    
    else:
        # Show recent runs summary
        runs = db_service.get_recent_runs(limit)
        if not runs:
            console.print("📭 No runs found in database")
            return
        
        # Create table
        table = Table(title=f"Recent Runs (showing {len(runs)} most recent)")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Date", style="green")
        table.add_column("File", style="yellow")
        table.add_column("Format", style="blue")
        table.add_column("Status", style="red")
        table.add_column("Rows", style="magenta")
        
        for run in runs:
            date_str = run.timestamp.strftime("%Y-%m-%d %H:%M")
            file_name = Path(run.csv_file).name[:18] + ".." if len(Path(run.csv_file).name) > 20 else Path(run.csv_file).name
            rows_str = str(run.rows_processed) if run.rows_processed else "N/A"
            
            # Color code status
            status_style = "green" if run.status == "completed" else "red" if run.status == "failed" else "yellow"
            
            table.add_row(
                str(run.id),
                date_str,
                file_name,
                run.output_format,
                run.status,
                rows_str
            )
        
        console.print(table)


@app.command()
def init_db():
    """Initialize the database and create tables."""
    from .db_init import main as init_db_main
    init_db_main()


def main():
    """Main entry point for the Typer application."""
    app()


if __name__ == "__main__":
    app()
