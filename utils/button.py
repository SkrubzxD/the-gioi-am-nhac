from flask import Blueprint, render_template

# This file is intended to provide reusable UI components or 
# logic for generic styled elements across the application.

ui_components_bp = Blueprint('ui_components', __name__)

@ui_components_bp.app_template_filter('generic_button')
def generic_button_style(text, href="#", class_name=""):
    """
    Returns a string representing a generic styled button.
    Usage in Jinja: {{ 'Click Me' | generic_button(href='/path', class_name='extra-class') | safe }}
    """
    style = (
        "display: inline-block; "
        "padding: 10px 20px; "
        "background-color: #800000; "
        "color: #fff; "
        "text-decoration: none; "
        "border-radius: 5px; "
        "font-weight: bold; "
        "transition: background-color 0.3s ease;"
    )
    return f'<a href="{href}" class="btn-generic {class_name}" style="{style}">{text}</a>'
