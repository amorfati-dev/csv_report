#!/usr/bin/env python3
"""Test script for HTML email functionality with premailer CSS inlining."""

import json
import pathlib
from src.csv_report.report.render import render_html_from_data

def test_html_rendering():
    """Test HTML rendering with premailer CSS inlining."""
    
    # Load test data
    data_file = pathlib.Path("data/dummy.json")
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Test data file not found: {data_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return False
    
    # Add report date
    data['report_date'] = "24. Juni 2025"
    
    try:
        # Render HTML with inlined CSS
        html_content = render_html_from_data(data)
        
        # Save to file for inspection
        output_file = pathlib.Path("reports/test_email_output.html")
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(html_content, encoding="utf-8")
        
        print(f"✓ HTML email content generated successfully")
        print(f"✓ Output saved to: {output_file}")
        
        # Check if CSS was inlined (should contain style attributes)
        if 'style=' in html_content:
            print("✓ CSS inlining appears to be working (style attributes found)")
        else:
            print("⚠️  CSS inlining may not be working (no style attributes found)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error rendering HTML: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing HTML email rendering with premailer...")
    success = test_html_rendering()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("📧 You can now test sending HTML emails")
    else:
        print("\n❌ Test failed!") 