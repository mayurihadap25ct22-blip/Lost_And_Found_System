import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector


# =========================
# DATABASE CONNECTION
# =========================

def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mayuri2007",
        database="lost_found_db"
    )


# =========================
# REGISTER
# =========================

def register():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter username and password"
        )
        return

    db = connect_database()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )

    result = cursor.fetchone()

    if result:
        messagebox.showwarning(
            "Warning",
            "Username already exists"
        )
    else:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )

        db.commit()

        messagebox.showinfo(
            "Success",
            "Registration successful!"
        )

    cursor.close()
    db.close()


# =========================
# LOGIN
# =========================

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter username and password"
        )
        return

    db = connect_database()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    result = cursor.fetchone()

    cursor.close()
    db.close()

    if result:
        messagebox.showinfo(
            "Success",
            "Login successful!"
        )

        root.withdraw()
        dashboard()

    else:
        messagebox.showerror(
            "Error",
            "Invalid username or password"
        )


# =========================
# ADD ITEM
# =========================

def add_item():

    item_type = type_entry.get().strip()
    item_name = name_entry.get().strip()
    category = category_entry.get().strip()
    location = location_entry.get().strip()
    date = date_entry.get().strip()
    description = description_entry.get().strip()
    contact = contact_entry.get().strip()
    status = status_entry.get().strip()

    if item_type == "" or item_name == "" or category == "" or location == "":
        messagebox.showwarning(
            "Warning",
            "Please fill all important fields"
        )
        return

    db = connect_database()
    cursor = db.cursor()

    query = """
    INSERT INTO items
    (item_type, item_name, category, location,
    date_found_lost, description, contact, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        item_type,
        item_name,
        category,
        location,
        date,
        description,
        contact,
        status
    )

    cursor.execute(query, values)

    db.commit()

    cursor.close()
    db.close()

    messagebox.showinfo(
        "Success",
        "Item added successfully!"
    )

    clear_fields()


# =========================
# CLEAR FIELDS
# =========================

def clear_fields():

    type_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)


# =========================
# VIEW ALL ITEMS
# =========================

def view_items():

    view_window = tk.Toplevel()
    view_window.title("All Lost & Found Items")
    view_window.geometry("1200x500")

    tk.Label(
        view_window,
        text="All Lost & Found Items",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    columns = (
        "ID",
        "Type",
        "Name",
        "Category",
        "Location",
        "Date",
        "Description",
        "Contact",
        "Status"
    )

    table = ttk.Treeview(
        view_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=120)

    table.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    db = connect_database()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM items")

    records = cursor.fetchall()

    for record in records:
        table.insert(
            "",
            tk.END,
            values=record
        )

    cursor.close()
    db.close()


# =========================
# SEARCH ITEM
# =========================

def search_item():

    search_window = tk.Toplevel()
    search_window.title("Search Item")
    search_window.geometry("1200x550")

    tk.Label(
        search_window,
        text="Search Lost & Found Item",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    tk.Label(
        search_window,
        text="Enter Item Name"
    ).pack()

    search_entry = tk.Entry(
        search_window,
        width=40
    )

    search_entry.pack(pady=5)

    columns = (
        "ID",
        "Type",
        "Name",
        "Category",
        "Location",
        "Date",
        "Description",
        "Contact",
        "Status"
    )

    table = ttk.Treeview(
        search_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=120)

    table.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    def search():

        for row in table.get_children():
            table.delete(row)

        db = connect_database()
        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM items WHERE item_name LIKE %s",
            ("%" + search_entry.get() + "%",)
        )

        records = cursor.fetchall()

        for record in records:
            table.insert(
                "",
                tk.END,
                values=record
            )

        cursor.close()
        db.close()

    tk.Button(
        search_window,
        text="Search",
        width=15,
        command=search
    ).pack(pady=10)


# =========================
# UPDATE ITEM
# =========================

def update_item():

    update_window = tk.Toplevel()
    update_window.title("Update Item")
    update_window.geometry("600x650")

    tk.Label(
        update_window,
        text="Update Item",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(
        update_window,
        text="Enter Item ID"
    ).pack()

    id_entry = tk.Entry(
        update_window,
        width=40
    )

    id_entry.pack(pady=5)

    tk.Label(update_window, text="Item Name").pack()

    update_name = tk.Entry(
        update_window,
        width=40
    )

    update_name.pack(pady=5)

    tk.Label(update_window, text="Category").pack()

    update_category = tk.Entry(
        update_window,
        width=40
    )

    update_category.pack(pady=5)

    tk.Label(update_window, text="Location").pack()

    update_location = tk.Entry(
        update_window,
        width=40
    )

    update_location.pack(pady=5)

    tk.Label(update_window, text="Description").pack()

    update_description = tk.Entry(
        update_window,
        width=40
    )

    update_description.pack(pady=5)

    tk.Label(update_window, text="Contact").pack()

    update_contact = tk.Entry(
        update_window,
        width=40
    )

    update_contact.pack(pady=5)

    tk.Label(update_window, text="Status").pack()

    update_status = tk.Entry(
        update_window,
        width=40
    )

    update_status.pack(pady=5)

    def update():

        item_id = id_entry.get().strip()

        if item_id == "":
            messagebox.showwarning(
                "Warning",
                "Please enter Item ID"
            )
            return

        db = connect_database()
        cursor = db.cursor()

        query = """
        UPDATE items
        SET item_name=%s,
            category=%s,
            location=%s,
            description=%s,
            contact=%s,
            status=%s
        WHERE id=%s
        """

        values = (
            update_name.get(),
            update_category.get(),
            update_location.get(),
            update_description.get(),
            update_contact.get(),
            update_status.get(),
            item_id
        )

        cursor.execute(query, values)

        db.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo(
                "Success",
                "Item updated successfully!"
            )
        else:
            messagebox.showerror(
                "Error",
                "Item ID not found"
            )

        cursor.close()
        db.close()

    tk.Button(
        update_window,
        text="Update Item",
        width=20,
        command=update
    ).pack(pady=20)


# =========================
# DELETE ITEM
# =========================

def delete_item():

    delete_window = tk.Toplevel()
    delete_window.title("Delete Item")
    delete_window.geometry("400x250")

    tk.Label(
        delete_window,
        text="Delete Item",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        delete_window,
        text="Enter Item ID"
    ).pack()

    id_entry = tk.Entry(
        delete_window,
        width=30
    )

    id_entry.pack(pady=10)

    def delete():

        item_id = id_entry.get().strip()

        if item_id == "":
            messagebox.showwarning(
                "Warning",
                "Please enter Item ID"
            )
            return

        answer = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to delete this item?"
        )

        if answer:

            db = connect_database()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM items WHERE id=%s",
                (item_id,)
            )

            db.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo(
                    "Success",
                    "Item deleted successfully!"
                )
                delete_window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Item ID not found"
                )

            cursor.close()
            db.close()

    tk.Button(
        delete_window,
        text="Delete Item",
        width=20,
        command=delete
    ).pack(pady=15)


# =========================
# DASHBOARD
# =========================

def dashboard():

    global type_entry
    global name_entry
    global category_entry
    global location_entry
    global date_entry
    global description_entry
    global contact_entry
    global status_entry

    window = tk.Toplevel()
    window.title("Lost & Found Dashboard")
    window.geometry("600x750")

    tk.Label(
        window,
        text="Lost & Found Item Reporting System",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(
        window,
        text="Item Type"
    ).pack()

    type_entry = tk.Entry(
        window,
        width=40
    )

    type_entry.pack(pady=5)

    tk.Label(
        window,
        text="Item Name"
    ).pack()

    name_entry = tk.Entry(
        window,
        width=40
    )

    name_entry.pack(pady=5)

    tk.Label(
        window,
        text="Category"
    ).pack()

    category_entry = tk.Entry(
        window,
        width=40
    )

    category_entry.pack(pady=5)

    tk.Label(
        window,
        text="Location"
    ).pack()

    location_entry = tk.Entry(
        window,
        width=40
    )

    location_entry.pack(pady=5)

    tk.Label(
        window,
        text="Date (YYYY-MM-DD)"
    ).pack()

    date_entry = tk.Entry(
        window,
        width=40
    )

    date_entry.pack(pady=5)

    tk.Label(
        window,
        text="Description"
    ).pack()

    description_entry = tk.Entry(
        window,
        width=40
    )

    description_entry.pack(pady=5)

    tk.Label(
        window,
        text="Contact"
    ).pack()

    contact_entry = tk.Entry(
        window,
        width=40
    )

    contact_entry.pack(pady=5)

    tk.Label(
        window,
        text="Status"
    ).pack()

    status_entry = tk.Entry(
        window,
        width=40
    )

    status_entry.pack(pady=5)

    # ADD
    tk.Button(
        window,
        text="Add Item",
        width=20,
        command=add_item
    ).pack(pady=8)

    # VIEW
    tk.Button(
        window,
        text="View All Items",
        width=20,
        command=view_items
    ).pack(pady=8)

    # SEARCH
    tk.Button(
        window,
        text="Search Item",
        width=20,
        command=search_item
    ).pack(pady=8)

    # UPDATE
    tk.Button(
        window,
        text="Update Item",
        width=20,
        command=update_item
    ).pack(pady=8)

    # DELETE
    tk.Button(
        window,
        text="Delete Item",
        width=20,
        command=delete_item
    ).pack(pady=8)


# =========================
# LOGIN WINDOW
# =========================

root = tk.Tk()

root.title("Lost & Found Item Reporting System")

root.geometry("450x350")

tk.Label(
    root,
    text="Lost & Found Item Reporting System",
    font=("Arial", 18, "bold")
).pack(pady=25)

tk.Label(
    root,
    text="Username"
).pack()

username_entry = tk.Entry(
    root,
    width=30
)

username_entry.pack(pady=5)

tk.Label(
    root,
    text="Password"
).pack()

password_entry = tk.Entry(
    root,
    width=30,
    show="*"
)

password_entry.pack(pady=5)

tk.Button(
    root,
    text="Login",
    width=15,
    command=login
).pack(pady=10)

tk.Button(
    root,
    text="Register",
    width=15,
    command=register
).pack()

root.mainloop()
