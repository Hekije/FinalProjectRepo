from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

# Creates the main window
root = tk.Tk()
root.title("GameVault")
root.geometry("600x450")
root.configure(bg="#121212")  # Dark background color

# Logo
image_path = r"C:\Users\Henry\PycharmProjects\PythonProject\assets\GameVault.png"
try:
    # Open and resize the image
    original_image = Image.open(image_path)
    resized_image = original_image.resize((300, 300))

    # Converted to PhotoImage for Tkinter
    logo = ImageTk.PhotoImage(resized_image)

    # Added the logo to a label widget
    # noinspection PyTypeChecker
    logo_label = tk.Label(root, image=logo, bg="#121212")
    logo_label.image = logo
    logo_label.pack(pady=10)

except Exception as e:
    print(f"Error loading image: {e}")

# Custom button style
style = ttk.Style()
style.configure("Rounded.TButton",
                font=("Arial", 12),
                foreground="black",  # Make button text black
                background="white",
                borderwidth=2,
                relief="flat",
                padding=10)
style.map("Rounded.TButton",
          background=[("active", "#dddddd")])  # Slightly gray on hover

# Title Label
label = tk.Label(root, text="Your Game Collection", font=("Arial", 16, "bold"), bg="#121212", fg="white")
label.pack(pady=10)

# Listbox to display games
game_listbox = tk.Listbox(root, width=50, height=10, bg="#222222", fg="white", font=("Arial", 12))
game_listbox.pack(pady=10)

# Frame for buttons
button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=10)

# Function to add a game
def add_game():
    add_window = tk.Toplevel(root)
    add_window.title("Add Game")
    add_window.geometry("400x300")
    add_window.configure(bg="#1e1e1e")  # Dark background

    # Labels and Entry Fields
    tk.Label(add_window, text="Game Title:", bg="#1e1e1e", fg="white").pack(pady=5)
    title_entry = tk.Entry(add_window, width=40, bg="#333333", fg="white", insertbackground="white")
    title_entry.pack(pady=5)

    tk.Label(add_window, text="Platform:", bg="#1e1e1e", fg="white").pack(pady=5)
    platform_entry = tk.Entry(add_window, width=40, bg="#333333", fg="white", insertbackground="white")
    platform_entry.pack(pady=5)

    tk.Label(add_window, text="Genre:", bg="#1e1e1e", fg="white").pack(pady=5)
    genre_entry = tk.Entry(add_window, width=40, bg="#333333", fg="white", insertbackground="white")
    genre_entry.pack(pady=5)

    tk.Label(add_window, text="Status (Completed/Wishlist):", bg="#1e1e1e", fg="white").pack(pady=5)
    status_entry = tk.Entry(add_window, width=40, bg="#333333", fg="white", insertbackground="white")
    status_entry.pack(pady=5)

    # Save button
    def save_game():
        title = title_entry.get()
        platform = platform_entry.get()
        genre = genre_entry.get()
        status = status_entry.get()
        game_listbox.insert(tk.END, f"{title} - {platform} - {genre} - {status}")
        add_window.destroy()

    save_button = ttk.Button(add_window, text="Save", style="Rounded.TButton", command=save_game)
    save_button.pack(pady=20)

# Buttons
add_button = ttk.Button(button_frame, text="Add Game", style="Rounded.TButton", command=add_game)
edit_button = ttk.Button(button_frame, text="Edit Game", style="Rounded.TButton")
delete_button = ttk.Button(button_frame, text="Delete Game", style="Rounded.TButton")
exit_button = ttk.Button(button_frame, text="Exit", style="Rounded.TButton", command=root.quit)

# Arrange buttons
add_button.grid(row=0, column=0, padx=10, pady=5)
edit_button.grid(row=0, column=1, padx=10, pady=5)
delete_button.grid(row=0, column=2, padx=10, pady=5)
exit_button.grid(row=0, column=3, padx=10, pady=5)

# Run the application
root.mainloop()
