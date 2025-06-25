"""Test template rendering functionality for CI."""

import json
import pathlib
import pytest
from src.csv_report.report.render import render_html_from_data


def test_template_rendering_with_dummy_data():
    """Test that template renders successfully with dummy data."""

    # Load test data
    data_file = pathlib.Path("data/dummy.json")

    if not data_file.exists():
        pytest.skip("Test data file not found")

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail("Invalid JSON in test data file")

    # Add report date
    data['report_date'] = "24. Juni 2025"

    # Test HTML rendering
    try:
        html_content = render_html_from_data(data)

        # Verify HTML was generated
        assert html_content is not None
        assert len(html_content) > 0

        # Verify it contains expected content
        assert "Zahnarztpraxis Report" in html_content
        assert "24. Juni 2025" in html_content
        assert "Kennzahlen" in html_content

        # Verify CSS was inlined (premailer worked)
        assert 'style=' in html_content

        # Verify it's valid HTML structure
        assert '<html' in html_content
        assert '</html>' in html_content
        assert '<head>' in html_content
        assert '<body' in html_content

    except Exception as e:
        pytest.fail(f"Template rendering failed: {e}")


def test_template_rendering_with_minimal_data():
    """Test template rendering with minimal required data."""

    minimal_data = {
        'report_date': '24. Juni 2025',
        'kpis': [
            {'name': 'Test KPI', 'value': '100', 'trend': '↗️'}
        ]
    }

    try:
        html_content = render_html_from_data(minimal_data)

        # Verify HTML was generated
        assert html_content is not None
        assert len(html_content) > 0

        # Verify it contains the test data
        assert "Test KPI" in html_content
        assert "100" in html_content
        assert "↗️" in html_content

    except Exception as e:
        pytest.fail(f"Template rendering with minimal data failed: {e}")


def test_template_rendering_error_handling():
    """Test that template rendering handles missing data gracefully."""

    # Test with missing required data
    incomplete_data = {
        'report_date': '24. Juni 2025'
        # Missing 'kpis' key
    }

    try:
        html_content = render_html_from_data(incomplete_data)

        # Should still render (kpis will be empty)
        assert html_content is not None
        assert "Zahnarztpraxis Report" in html_content

    except Exception as e:
        pytest.fail(f"Template should handle missing data gracefully: {e}")


if __name__ == "__main__":
    # Run tests directly
    print("🧪 Running template rendering tests...")

    test_template_rendering_with_dummy_data()
    test_template_rendering_with_minimal_data()
    test_template_rendering_error_handling()

    print("✅ All template rendering tests passed!")
