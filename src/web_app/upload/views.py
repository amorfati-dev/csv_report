"""
Views for CSV upload functionality.
"""

import os
import tempfile
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

# Add the csv_report module to the path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from csv_report.load import load_csv
from csv_report.report.generate import generate_report, save_report
from csv_report.database import DatabaseService
from csv_report.logging_config import setup_cli_logging


def upload_view(request):
    """Main upload view."""
    return render(request, 'upload/upload.html')


@csrf_exempt
@require_http_methods(["POST"])
def process_csv(request):
    """Process uploaded CSV file."""
    logger = setup_cli_logging()
    
    try:
        if 'csv_file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        uploaded_file = request.FILES['csv_file']
        
        # Validate file type
        if not uploaded_file.name.endswith('.csv'):
            return JsonResponse({'error': 'Please upload a CSV file'}, status=400)
        
        logger.info(f"Processing uploaded CSV file: {uploaded_file.name}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        try:
            # Load CSV using existing logic
            logger.info("Loading CSV data")
            df = load_csv(csv_file=temp_file_path)
            logger.info(f"CSV loaded successfully: {len(df)} rows, {len(df.columns)} columns")
            
            # Use Django ORM to create run record
            from .models import Run as DjangoRun
            
            # Create run record using Django ORM
            run = DjangoRun.objects.create(
                csv_file=uploaded_file.name,
                output_format='html',
                rows_processed=len(df),
                status='processing'
            )
            logger.info(f"Run record created with ID: {run.id}")
            
            # Generate report
            logger.info("Generating report")
            report = generate_report(df)
            
            # Save report to the main reports directory
            reports_dir = Path(__file__).parent.parent.parent.parent.parent.parent / "reports"
            reports_dir.mkdir(parents=True, exist_ok=True)
            output_path = reports_dir / f"{uploaded_file.name.replace('.csv', '_analysis.html')}"
            final_path = save_report(report, output_path)
            logger.info(f"Report saved: {final_path}")
            
            # Update run status using Django ORM
            run.status = 'completed'
            run.save()
            
            logger.info("CSV processing completed successfully")
            
            return JsonResponse({
                'success': True,
                'message': 'CSV processed successfully',
                'run_id': run.id,
                'rows_processed': len(df),
                'report_path': str(final_path)
            })
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        logger.error(f"Error processing CSV: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': f'Error processing CSV: {str(e)}'
        }, status=500)


def reports_view(request):
    """View to display all reports."""
    try:
        from .models import Run as DjangoRun
        
        # Get runs using Django ORM
        runs = DjangoRun.objects.all().order_by('-timestamp')[:20]
        
        # Add report file paths to runs
        for run in runs:
            if run.status == 'completed':
                report_filename = f"{run.csv_file.replace('.csv', '_analysis.html')}"
                run.report_url = f"/reports/{report_filename}"
        
        return render(request, 'upload/reports.html', {'runs': runs})
    except Exception as e:
        messages.error(request, f'Error loading reports: {str(e)}')
        return render(request, 'upload/reports.html', {'runs': []})
