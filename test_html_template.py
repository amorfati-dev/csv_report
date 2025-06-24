#!/usr/bin/env python3
"""
Test script to render the HTML template with data from dummy.json.
This ensures the template works locally before integration.
"""

import json
import os
from jinja2 import Environment, FileSystemLoader

def test_html_template():
    """Test the HTML template with data from dummy.json."""
    
    # Setup Jinja2 environment
    template_dir = os.path.join('src', 'csv_report', 'report')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('report_template.html')
    # Load data from dummy.json
    dummy_file = os.path.join('data', 'dummy.json')
    
    try:
        with open(dummy_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Dummy data file not found: {dummy_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        return None
    
    # Render the template
    html_output = template.render(**data)
    
    # Save the rendered HTML
    output_file = os.path.join('reports', 'test_report.html')
    os.makedirs('reports', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"✅ Template rendered successfully!")
    print(f"📄 Output saved to: {output_file}")
    print(f"🌐 Open the file in your browser to view the report")
    print(f"📊 Data loaded from: {dummy_file}")
    
    return output_file

if __name__ == '__main__':
    test_html_template() 