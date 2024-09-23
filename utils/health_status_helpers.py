from get_status_string import get_random_status_string
import customtkinter

def write_current_health(app, participant, health_entry, row, current_health, main_frame, initial_values, status_lists):
    """Update current health and refresh status string."""
    # Update the current health
    current_health[participant] = int(health_entry.get())

    # Get new status string and color
    status_string, status_color = get_status_string_and_color(
        current_health[participant],
        initial_values[participant][1],
        status_lists,
        initial_values[participant][2]
    )

    # Update the status label in the app's main_frame
    if participant in app.status_labels:
        status_label = app.status_labels[participant]
        status_label.configure(text=status_string, fg_color=status_color)


def delayed_check_health_status(app, participant, health_entry, row, current_health, initial_values, status_lists):
    """Schedule health status update after a delay."""
    # Cancel the previous scheduled callback
    if hasattr(app.main_frame, 'delayed_health_callback_id') and app.main_frame.delayed_health_callback_id:
        app.after_cancel(app.main_frame.delayed_health_callback_id)

    # Schedule a new callback after 200 milliseconds
    app.main_frame.delayed_health_callback_id = app.after(
        200, lambda: write_current_health(app, participant, health_entry, row, current_health, app.main_frame, initial_values, status_lists)
    )


def get_status_string_and_color(current_health, maximum_health, status_lists, monster_type):
    health_percentage = (int(current_health) / int(maximum_health)) * 100
    if health_percentage == 100:
        health_status = "Full HP"
        color = "green"
    else:
        health_status, color = get_random_status_string(health_percentage, monster_type, status_lists)
    return health_status, color
