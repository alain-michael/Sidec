from django import template

register = template.Library()

@register.filter
def to_percentage(marks_obtained, total_marks):
    """
    Custom template filter to convert marks obtained to a percentage.
    """
    try:
        # Convert the values to floats and calculate the percentage.
        percentage = (float(marks_obtained) / float(total_marks)) * 100
        # Return the percentage as a string with two decimal places.
        return float('{:.1f}'.format(percentage))
    except (ValueError, TypeError, ZeroDivisionError):
        # If conversion fails or division by zero occurs, return an empty string or handle the error as desired.
        return ''
