"""
Template Management

Handles loading and processing of export templates.
"""

def get_template_path(template_name: str, file_type: str) -> str:
    """
    Resolve the path to a specific template.
    
    Args:
        template_name: Name of the template profile (e.g., 'default', 'rabdan')
        file_type: 'pptx' or 'docx'
    """
    # TODO: Implement template lookup logic
    return f"templates/{template_name}.{file_type}"

