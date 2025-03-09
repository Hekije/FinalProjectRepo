import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json

# File to store the game data
game_file = "games.json"

# Function to load game data
def load_games():
    if os.path.exists(game_file):
        with open(game_file, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Function to save game data
def save_games(games):
    with open(game_file, "w", encoding="utf-8") as file:
        json.dump(games, file, indent=4)

# Function to open the Add Game window
def add_game_window():
    add_window = tk.Toplevel(root)
    add_window.title("Add Game")
    add_window.geometry("400x500")
    add_window.config(bg="#121212")

    # Load and display image at the top
    img_path = "assets/vault.png"
    img = Image.open(img_path)
    img = img.resize((100, 100))
    img = ImageTk.PhotoImage(img)

    # Create a label to display the image
    img_label = tk.Label(add_window, image=img, bg="#121212")
    img_label.image = img  # Keep reference to avoid garbage collection
    img_label.pack(pady=10)

    # Game Title Input
    title_label = tk.Label(add_window, text="Game Title", fg="white", bg="#121212")
    title_label.pack(pady=5)
    title_entry = tk.Entry(add_window)
    title_entry.pack(pady=5)

    # Platform Input
    platform_label = tk.Label(add_window, text="Platform", fg="white", bg="#121212")
    platform_label.pack(pady=5)
    platform_entry = tk.Entry(add_window)
    platform_entry.pack(pady=5)

    # Genre Input
    genre_label = tk.Label(add_window, text="Genre", fg="white", bg="#121212")
    genre_label.pack(pady=5)
    genre_entry = tk.Entry(add_window)
    genre_entry.pack(pady=5)

    # Status Dropdown using ttk
    status_label = tk.Label(add_window, text="Status", fg="white", bg="#121212")
    status_label.pack(pady=5)
    status_var = tk.StringVar(add_window)
    status_var.set("Want to Play")
    status_menu = ttk.Combobox(add_window, textvariable=status_var, values=["Want to Play", "In Progress", "Completed"])
    status_menu.pack(pady=5)

    # Image Upload Button
    image_path = tk.StringVar()  # Store file path

    def upload_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            image_path.set(file_path)  # Store image path
            preview_image(file_path)  # Call preview function

    upload_button = tk.Button(add_window, text="Upload Image", bg="#2b2b2b", fg="white", command=upload_image)
    upload_button.pack(pady=5)

    # Image Preview function to display the selected image
    def preview_image(file_path):
        # Open and resize the selected image
        img = Image.open(file_path)
        img = img.resize((100, 100))  # Resize to fit the preview area
        img = ImageTk.PhotoImage(img)

        # Create a label to show the image preview
        preview_label = tk.Label(add_window, image=img, bg="#121212")
        preview_label.image = img  # Keep reference to avoid garbage collection
        preview_label.pack(pady=5)

    # Function to add game to list
    def add_game_to_list():
        title = title_entry.get()
        platform = platform_entry.get()
        genre = genre_entry.get()
        status = status_var.get()
        image = image_path.get()  # Get the image path

        # Error handling for empty fields and special characters
        if not title or not platform or not genre:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
        elif any(char in title for char in "!@#$%^&*()[]{};:,./<>?\\|~") or any(
                char in platform for char in "!@#$%^&*()[]{};:,./<>?\\|~"):
            messagebox.showwarning("Input Error", "Special characters are not allowed in title or platform.")
        elif image and not os.path.exists(image):  # Check if the image exists
            messagebox.showwarning("Image Error", "The selected image file does not exist.")
        else:
            # Create a new game entry and append it to the list
            new_game = {"title": title, "platform": platform, "genre": genre, "status": status, "image": image}
            games.append(new_game)
            save_games(games)  # Save the updated game list
            create_game_card(new_game)  # Add the game card to the UI
            add_window.destroy()  # Close the add window

    # Add Game Button
    add_game_btn = tk.Button(add_window, text="Add Game", bg="#2b2b2b", fg="white", command=add_game_to_list)
    add_game_btn.pack(pady=20)


# Function to create a game card
default_image = "images/default_image.jpg"


def create_game_card(game):
    game_card = tk.Frame(game_frame, bg="#2b2b2b", relief="raised", bd=2)
    game_card.pack(side="left", padx=10, pady=10)

    # Game Image
    image_path = game["image"] if game["image"] else default_image  # Use default image if none exists
    img = Image.open(image_path)
    img = img.resize((100, 100))  # Resize the image to fit the card
    img = ImageTk.PhotoImage(img)

    img_label = tk.Label(game_card, image=img, bg="#2b2b2b")
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.pack()

    # Game Title and Info
    title_label = tk.Label(game_card, text=game["title"], font=("Arial", 12, "bold"), bg="#2b2b2b", fg="white")
    title_label.pack()
    platform_label = tk.Label(game_card, text=f"Platform: {game['platform']}", bg="#2b2b2b", fg="white")
    platform_label.pack()

    status_label = tk.Label(game_card, text=f"Status: {game['status']}", bg="#2b2b2b", fg="white")
    status_label.pack()

    # Delete Button with confirmation dialog
    def confirm_delete():
        result = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this game?")
        if result:
            delete_game(game, game_card)

    delete_button = tk.Button(game_card, text="Delete", bg="#ff4c4c", fg="white", command=confirm_delete)
    delete_button.pack(pady=5)

    # Edit Button
    edit_button = tk.Button(game_card, text="Edit", bg="#4c8cff", fg="white", command=lambda: edit_game_window(game))
    edit_button.pack(pady=5)


# Function to update the displayed game cards
def update_game_cards():
    for widget in game_frame.winfo_children():
        widget.destroy()  # Remove all existing cards
    for game in games:
        create_game_card(game)  # Re-create cards with updated data


# Function to delete a game
def delete_game(game, game_card):
    games.remove(game)  # Remove game from the list
    save_games(games)  # Save the updated list
    game_card.destroy()  # Remove the game card from the UI


# Function to edit a game
def edit_game_window(game):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Game")
    edit_window.geometry("400x400")
    edit_window.config(bg="#121212")

    # Game Title Input
    title_label = tk.Label(edit_window, text="Game Title", fg="white", bg="#121212")
    title_label.pack(pady=5)
    title_entry = tk.Entry(edit_window)
    title_entry.insert(0, game['title'])
    title_entry.pack(pady=5)

    # Platform Input
    platform_label = tk.Label(edit_window, text="Platform", fg="white", bg="#121212")
    platform_label.pack(pady=5)
    platform_entry = tk.Entry(edit_window)
    platform_entry.insert(0, game['platform'])
    platform_entry.pack(pady=5)

    # Genre Input
    genre_label = tk.Label(edit_window, text="Genre", fg="white", bg="#121212")
    genre_label.pack(pady=5)
    genre_entry = tk.Entry(edit_window)
    genre_entry.insert(0, game['genre'])
    genre_entry.pack(pady=5)

    # Status Dropdown
    status_label = tk.Label(edit_window, text="Status", fg="white", bg="#121212")
    status_label.pack(pady=5)
    status_var = tk.StringVar(edit_window)
    status_var.set(game['status'])
    status_menu = ttk.Combobox(edit_window, textvariable=status_var,
                               values=["Want to Play", "In Progress", "Completed"])
    status_menu.pack(pady=5)

    # Function to save edited game
    def save_edited_game():
        game['title'] = title_entry.get()
        game['platform'] = platform_entry.get()
        game['genre'] = genre_entry.get()
        game['status'] = status_var.get()
        save_games(games)
        edit_window.destroy()
        update_game_cards()  # Refresh all games after editing

    # Save Button
    save_button = tk.Button(edit_window, text="Save Changes", bg="#2b2b2b", fg="white", command=save_edited_game)
    save_button.pack(pady=20)


# Load existing games
games = load_games()

# Create main window
root = tk.Tk()
root.title("GameVault")
root.geometry("800x600")
root.config(bg="#121212")

# Header
logo_path = "assets/GameVault.png"
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((300, 300))
logo_img = ImageTk.PhotoImage(logo_img)

# Create a label to display the logo
logo_label = tk.Label(root, image=logo_img, bg="#121212")
logo_label.image = logo_img  # Keep a reference to the image
logo_label.pack(pady=10)


# Search Bar
search_label = tk.Label(root, text="Search Games", fg="white", bg="#121212")
search_label.pack(pady=5)
search_entry = tk.Entry(root)
search_entry.pack(pady=5)


# Function for searching games
def search_games(event=None):
    search_term = search_entry.get().lower()
    filtered_games = [game for game in games if
                      search_term in game['title'].lower() or search_term in game['platform'].lower()]

    # Update displayed games based on search results
    for widget in game_frame.winfo_children():
        widget.destroy()  # Remove all current game cards

    for game in filtered_games:
        create_game_card(game)  # Add cards of filtered games to the frame


# Bind search function to search entry
search_entry.bind("<KeyRelease>", search_games)

# Game Cards Frame
game_frame = tk.Frame(root, bg="#121212")
game_frame.pack(fill="both", expand=True)

# Add Game Button
add_game_button = tk.Button(root, text="Add Game", bg="#4caf50", fg="white", command=add_game_window)
add_game_button.pack(pady=10)

# Load existing game cards
update_game_cards()

root.mainloop()