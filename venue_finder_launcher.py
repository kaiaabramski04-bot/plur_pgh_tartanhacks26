import tkinter as tk
from tkinter import messagebox
import sys
import os

def start_quiz(root):
    """Starts the Pittsburgh Venue Finder quiz."""
    # Close the launcher window
    root.destroy()
    # Import and run the quiz
    try:
        import plur_pgh
        plur_pgh.main()
    except ImportError:
        messagebox.showerror("Error", "Could not import the quiz module. Make sure 'plur_pgh.py' is in the same directory.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def main():
    # Create the main window
    root = tk.Tk()
    root.title("PLUR PGH - Pittsburgh Venue Finder")
    root.geometry("700x500")
    root.resizable(True, True)

    # Title label
    title_label = tk.Label(root, text="PLUR PGH",
                          font=("Arial", 24, "bold"), fg="darkblue")
    title_label.pack(pady=20)

    # Description text
    description = """
Welcome to the Pittsburgh Venue Finder!

This interactive quiz helps you discover the perfect venues in Pittsburgh based on your preferences.

How it works:
• Enter your location, budget, and preferences
• The site will then calculate scores for each venue in our database
• The top 3 venues with the highest scores will be presented to you

Ready to find your next favorite spot in Pittsburgh?
    """

    desc_label = tk.Label(root, text=description, font=("Arial", 12), justify=tk.LEFT, wraplength=550)
    desc_label.pack(pady=10, padx=20)

    # Start Quiz button
    start_button = tk.Button(root, text="Start Quiz", font=("Arial", 16, "bold"),
                            bg="green", fg="white", command=lambda: start_quiz(root),
                            width=20, height=2)
    start_button.pack(pady=30)

    # Footer
    footer_label = tk.Label(root, text="Built with Python & Tkinter",
                           font=("Arial", 10), fg="gray")
    footer_label.pack(side=tk.BOTTOM, pady=10)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()