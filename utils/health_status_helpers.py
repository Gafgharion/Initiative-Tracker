from get_status_string import get_random_status_string
import customtkinter


def write_current_health(
    participant, health_entry, current_health, status_label, initial_values
):
    """Update current health and refresh status string."""
    # Update the current health
    current_health[participant] = int(health_entry.get())

    # Get the maximum health for the participant (assuming it's stored in initial_values)
    maximum_health = initial_values[participant]["health"]

    # Update the button color based on the new health status
    status_color = get_health_status_color_indicator(
        current_health[participant], maximum_health
    )
    status_label.configure(fg_color=status_color)


def delayed_check_health_status(
    app, participant, health_entry, current_health, status_label, initial_values
):
    """Schedule health status update after a delay."""
    # Cancel the previous scheduled callback
    if (
        hasattr(app.main_frame, "delayed_health_callback_id")
        and app.main_frame.delayed_health_callback_id
    ):
        app.after_cancel(app.main_frame.delayed_health_callback_id)

    # Schedule a new callback after 200 milliseconds
    app.main_frame.delayed_health_callback_id = app.after(
        200,
        lambda: write_current_health(
            participant, health_entry, current_health, status_label, initial_values
        ),
    )


def get_status_string_and_color(
    current_health, maximum_health, status_lists, monster_type
):
    health_percentage = (int(current_health) / int(maximum_health)) * 100
    if health_percentage == 100:
        health_status = "Full HP"
        color = "green"
    else:
        health_status, color = get_random_status_string(
            health_percentage, monster_type, status_lists
        )
    return health_status, color


def get_health_status_color_indicator(current_health, maximum_health):
    health_percentage = (int(current_health) / int(maximum_health)) * 100
    if health_percentage >= 80:
        color = "chartreuse4"
    elif health_percentage >= 60 and health_percentage < 80:
        color = "chartreuse1"
    elif health_percentage >= 40 and health_percentage < 60:
        color = "orange"
    elif health_percentage >= 20 and health_percentage < 40:
        color = "firebrick1"
    elif health_percentage >= 0 and health_percentage < 20:
        color = "firebrick4"
    return color
