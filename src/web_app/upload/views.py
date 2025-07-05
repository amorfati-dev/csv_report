"""Views for CSV upload functionality."""

# Add the csv_report module to the path
import sys
import tempfile
from pathlib import Path

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

sys.path.append(str(Path(__file__).parent.parent.parent))

from csv_report.load import load_csv
from csv_report.logging_config import setup_cli_logging
from csv_report.report.generate import generate_report, save_report

from .models import Run

# Setup logging
logger = setup_cli_logging()


def upload_view(request):
    """Display the upload form."""
    return render(request, "upload/upload.html")


@csrf_exempt
@require_http_methods(["POST"])
def process_csv(request):
    """Process uploaded CSV file and generate report."""
    if "csv_file" not in request.FILES:
        return JsonResponse({"error": "Please upload a CSV file"}, status=400)

    uploaded_file = request.FILES["csv_file"]
    logger.info(f"Processing uploaded CSV file: {uploaded_file.name}")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        temp_file_path = temp_file.name

    try:
        # Load CSV
        df = load_csv(csv_file=temp_file_path)
        logger.info(
            f"CSV loaded successfully: {len(df)} rows, {len(df.columns)} columns",
        )

        # Create run record
        run = Run.objects.create(
            csv_file=uploaded_file.name,
            output_format="html",
            status="processing",
        )
        logger.info(f"Run record created with ID: {run.id}")

        # Generate report
        logger.info("Generating report")
        report = generate_report(df, output_format="html")

        # Save report
        output_path = Path("reports") / f"report_{run.id}.html"
        output_path.parent.mkdir(exist_ok=True)
        final_path = save_report(report, output_path)
        logger.info(f"Report saved: {final_path}")

        # Update run status using Django ORM
        run.status = "completed"
        run.rows_processed = len(df)
        run.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Report generated successfully",
                "rows_processed": len(df),
                "report_path": str(final_path),
            },
        )

    except Exception as e:
        logger.exception(f"Error processing CSV: {e!s}")
        return JsonResponse({"error": f"Error processing CSV: {e!s}"}, status=500)

    finally:
        # Clean up temporary file
        Path(temp_file_path).unlink()


def reports_view(request):
    """Display list of generated reports."""
    try:
        runs = Run.objects.all().order_by("-timestamp")
        return render(request, "upload/reports.html", {"runs": runs})
    except Exception as e:
        messages.error(request, f"Error loading reports: {e!s}")
        return render(request, "upload/reports.html", {"runs": []})
