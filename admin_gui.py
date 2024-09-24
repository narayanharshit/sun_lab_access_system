import tkinter as tk
from tkinter import messagebox
import sqlite3


# Function to view access logs
def view_access_logs():
    conn = sqlite3.connect('sun_lab_access.db')
    c = conn.cursor()
    c.execute("SELECT * FROM access_logs")
    rows = c.fetchall()
    conn.close()

    log_window = tk.Toplevel()
    log_window.title("Access Logs")

    if not rows:
        tk.Label(log_window, text="No access logs found").pack()
    else:
        headers = ("ID", "Student ID", "Timestamp")
        tk.Label(log_window, text="{:<10} {:<15} {:<20}".format(*headers)).pack()

        for row in rows:
            log_text = "{:<10} {:<15} {:<20}".format(row[0], row[1], row[2])
            tk.Label(log_window, text=log_text).pack()


# Function to manage user status (Activate, Suspend, Reactivate)
def manage_user_status(status):
    def update_status():
        student_id = student_id_entry.get()
        user_type = user_type_entry.get() if status == 'active' else None  # Only for new users

        conn = sqlite3.connect('sun_lab_access.db')
        c = conn.cursor()

        # Check if the user exists
        c.execute("SELECT status FROM users WHERE student_id = ?", (student_id,))
        result = c.fetchone()

        if result:  # User exists
            current_status = result[0]

            if status == 'active':  # Activate existing user
                if current_status == 'suspended':
                    c.execute("UPDATE users SET status = ? WHERE student_id = ?", ('active', student_id))
                    messagebox.showinfo("Success", f"User {student_id} has been activated.")
                else:
                    messagebox.showinfo("Info", f"User {student_id} is already {current_status}.")
            elif status == 'reactivated':  # Reactivate existing user
                if current_status == 'suspended':
                    c.execute("UPDATE users SET status = ? WHERE student_id = ?", ('reactivated', student_id))
                    messagebox.showinfo("Success", f"User {student_id} has been reactivated.")
                else:
                    messagebox.showinfo("Info", f"User {student_id} is already {current_status}.")
            elif status == 'suspended':  # Suspend existing user
                if current_status == 'active' or current_status == 'reactivated':
                    c.execute("UPDATE users SET status = ? WHERE student_id = ?", ('suspended', student_id))
                    messagebox.showinfo("Success", f"User {student_id} has been suspended.")
                else:
                    messagebox.showinfo("Info", f"User {student_id} is already suspended.")
        else:  # User doesn't exist, create a new user (for Activate only)
            if status == 'active':
                if user_type:
                    c.execute("INSERT INTO users (student_id, user_type, status) VALUES (?, ?, ?)",
                              (student_id, user_type, 'active'))
                    messagebox.showinfo("Success", f"New user {student_id} has been added and activated.")
                else:
                    messagebox.showwarning("Error", "User Type must be provided for new users.")
            else:
                messagebox.showinfo("Error", f"User {student_id} does not exist. You can only reactivate or suspend existing users.")

        conn.commit()
        conn.close()

    # Create a new window for updating status
    status_window = tk.Toplevel()
    status_window.title(f"{status.capitalize()} User")

    tk.Label(status_window, text="Enter Student ID:").pack()
    student_id_entry = tk.Entry(status_window)
    student_id_entry.pack()

    if status == 'active':  # Only prompt for user type if we are activating a new user
        tk.Label(status_window, text="Enter User Type (student, faculty, staff, etc.):").pack()
        user_type_entry = tk.Entry(status_window)
        user_type_entry.pack()
    else:
        user_type_entry = None  # Not needed for reactivation or suspension

    tk.Button(status_window, text=f"{status.capitalize()} User", command=update_status).pack()

# Function to search logs by filters (already implemented)
def search_logs_by_filter():
    filter_window = tk.Toplevel()
    filter_window.title("Search Logs")

    tk.Label(filter_window, text="Enter Student ID (optional):").pack()
    student_id_entry = tk.Entry(filter_window)
    student_id_entry.pack()

    tk.Label(filter_window, text="Enter Start Date (YYYY-MM-DD, optional):").pack()
    start_date_entry = tk.Entry(filter_window)
    start_date_entry.pack()

    tk.Label(filter_window, text="Enter End Date (YYYY-MM-DD, optional):").pack()
    end_date_entry = tk.Entry(filter_window)
    end_date_entry.pack()

    def search():
        student_id = student_id_entry.get().strip()
        start_date = start_date_entry.get().strip()
        end_date = end_date_entry.get().strip()

        conn = sqlite3.connect('sun_lab_access.db')
        c = conn.cursor()

        # Base query
        query = "SELECT * FROM access_logs WHERE 1=1"
        params = []

        # Add student ID filter if provided
        if student_id:
            query += " AND student_id=?"
            params.append(student_id)

        # Add start date filter if provided
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)

        # Add end date filter if provided
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        c.execute(query, params)
        rows = c.fetchall()
        conn.close()

        # Display the search results
        result_window = tk.Toplevel()
        result_window.title("Search Results")

        if not rows:
            tk.Label(result_window, text="No logs found").pack()
        else:
            # Display column headers
            headers = ("ID", "Student ID", "Timestamp")
            tk.Label(result_window, text="{:<10} {:<15} {:<20}".format(*headers)).pack()

            for row in rows:
                log_text = "{:<10} {:<15} {:<20}".format(row[0], row[1], row[2])
                tk.Label(result_window, text=log_text).pack()

    # Add button to trigger the search
    tk.Button(filter_window, text="Search", command=search).pack()

def view_user_details():
    # Create a new window for input
    user_details_window = tk.Toplevel()
    user_details_window.title("View User Details")

    tk.Label(user_details_window, text="Enter Student ID:").pack()
    student_id_entry = tk.Entry(user_details_window)
    student_id_entry.pack()

    def show_details():
        student_id = student_id_entry.get()

        conn = sqlite3.connect('sun_lab_access.db')
        c = conn.cursor()

        # Retrieve user details
        c.execute("SELECT * FROM users WHERE student_id = ?", (student_id,))
        user = c.fetchone()

        # Retrieve last access log for the user
        c.execute("SELECT timestamp FROM access_logs WHERE student_id = ? ORDER BY timestamp DESC LIMIT 1", (student_id,))
        last_access = c.fetchone()
        conn.close()

        if user:
            user_info = f"Student ID: {user[1]}\nUser Type: {user[2]}\nStatus: {user[3]}"
            if last_access:
                user_info += f"\nLast Access: {last_access[0]}"
            else:
                user_info += "\nLast Access: No access records found"
            messagebox.showinfo("User Details", user_info)
        else:
            messagebox.showinfo("Error", "User not found.")

    # Add a button to trigger the retrieval of user details
    tk.Button(user_details_window, text="Show Details", command=show_details).pack()


def show_dashboard():
    conn = sqlite3.connect('sun_lab_access.db')
    c = conn.cursor()

    # Count total users by status
    c.execute("SELECT COUNT(*) FROM users WHERE status = 'active'")
    active_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE status = 'suspended'")
    suspended_users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE status = 'reactivated'")
    reactivated_users = c.fetchone()[0]

    # Count total access logs
    c.execute("SELECT COUNT(*) FROM access_logs")
    total_logs = c.fetchone()[0]

    conn.close()

    summary = (f"Total Active Users: {active_users}\n"
               f"Total Suspended Users: {suspended_users}\n"
               f"Total Reactivated Users: {reactivated_users}\n"
               f"Total Access Logs: {total_logs}")

    messagebox.showinfo("System Dashboard", summary)


# Main admin GUI setup
def create_admin_gui():
    root = tk.Tk()
    root.title("SUN Lab Access System - Admin Panel")

    tk.Label(root, text="SUN Lab Access System").pack()

    # Buttons to view access logs and search logs by filters
    tk.Button(root, text="View All Access Logs", command=view_access_logs).pack()
    tk.Button(root, text="Search Logs by Filters", command=search_logs_by_filter).pack()

    # User management buttons
    tk.Button(root, text="Activate User", command=lambda: manage_user_status('active')).pack()
    tk.Button(root, text="Suspend User", command=lambda: manage_user_status('suspended')).pack()
    tk.Button(root, text="Reactivate User", command=lambda: manage_user_status('reactivated')).pack()

    # Buttons for additional features (User Details and Dashboard)
    tk.Button(root, text="View User Details", command=view_user_details).pack()
    tk.Button(root, text="View Dashboard", command=show_dashboard).pack()

    root.mainloop()



if __name__ == "__main__":
    create_admin_gui()
