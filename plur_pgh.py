import csv
import sys
import tkinter as tk
from tkinter import messagebox, ttk

def load_data(filepath='plurpgh.csv'):
    """
    Loads data using the standard csv library.
    Returns a list of dictionaries.
    """
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        return []

def get_user_input_gui(unique_types):
    """Handles the user interface using Tkinter GUI."""
    root = tk.Tk()
    root.title("PITTSBURGH VENUE FINDER QUIZ")
    root.geometry("500x600")

    # Zip Code
    tk.Label(root, text="1. Enter your preferred Zip Code (e.g., 15201):").pack(pady=5)
    zip_entry = tk.Entry(root)
    zip_entry.pack(pady=5)

    # Budget
    tk.Label(root, text="2. What is your max budget?").pack(pady=5)
    budget_var = tk.StringVar(value="$")
    budget_frame = tk.Frame(root)
    budget_frame.pack(pady=5)
    tk.Radiobutton(budget_frame, text="$ (Budget-friendly)", variable=budget_var, value="$").pack(anchor=tk.W)
    tk.Radiobutton(budget_frame, text="$$ (Moderate)", variable=budget_var, value="$$").pack(anchor=tk.W)
    tk.Radiobutton(budget_frame, text="$$$ (High-end)", variable=budget_var, value="$$$").pack(anchor=tk.W)

    # Venue Type
    tk.Label(root, text="3. What type of venue matches your vibe? (Select multiple)").pack(pady=5)
    type_vars = []
    type_frame = tk.Frame(root)
    type_frame.pack(pady=5)
    for dtype in unique_types:
        var = tk.BooleanVar()
        tk.Checkbutton(type_frame, text=dtype, variable=var).pack(anchor=tk.W)
        type_vars.append((dtype, var))

    # Preferences
    tk.Label(root, text="4. Any specific preferences? (Select multiple)").pack(pady=5)
    pref_options = ['LGBT +', 'Adult Club', 'Activity']
    pref_vars = []
    pref_frame = tk.Frame(root)
    pref_frame.pack(pady=5)
    for pref in pref_options:
        var = tk.BooleanVar()
        tk.Checkbutton(pref_frame, text=pref, variable=var).pack(anchor=tk.W)
        pref_vars.append((pref, var))

    # Result variables
    result = {}

    def submit():
        user_zip = zip_entry.get().strip()
        user_budget = budget_var.get()
        selected_types = [dtype for dtype, var in type_vars if var.get()]
        selected_prefs = [pref for pref, var in pref_vars if var.get()]
        result.update({
            'zip': user_zip,
            'budget': user_budget,
            'types': selected_types,
            'prefs': selected_prefs
        })
        root.quit()

    tk.Button(root, text="Find Venues", command=submit).pack(pady=20)
    root.mainloop()
    root.destroy()
    return result['zip'], result['budget'], result['types'], result['prefs']

def calculate_scores(data, user_zip, user_budget, user_types, user_prefs):
    """
    Scores venues based on user input using standard Python lists/dicts.
    """
    
    # Budget Mapping
    price_rank = {'$': 1, '$$': 2, '$$$': 3}
    user_rank = price_rank.get(user_budget, 1)
    
    scored_results = []
    
    for row in data:
        score = 0
        
        # 1. Zip Code Match (+50 points)
        if row.get('Zip Code', '').strip() == user_zip:
            score += 50
            
        # 2. Type Match (+30 points)
        # We strip whitespace to be safe
        if row.get('type', '').strip() in user_types:
            score += 30
            
        # 3. Budget Weighting
        v_price = row.get('price', '').strip()
        
        if v_price in price_rank:
            v_rank = price_rank[v_price]
            diff = user_rank - v_rank
            
            if diff < 0:
                # Venue is more expensive than budget -> Huge Penalty
                score -= 1000
            else:
                # 30 pts for exact match, -10 for every step cheaper
                # Example: User $$$ (3). Venue $ (1). Diff = 2. Score = 30 - 20 = 10 pts.
                weight_score = 30 - (diff * 10)
                score += max(0, weight_score)
        
        # 4. Preferences (+20 points each)
        for pref in user_prefs:
            # Check if column has a value (is not empty and not '0')
            val = row.get(pref, '').strip()
            if val and val != '0':
                score += 20
        
        # Store result if it's not totally excluded
        if score > -100:
            # Add score to the row dictionary for sorting
            row['match_score'] = score
            scored_results.append(row)
            
    # Sort by score descending (highest first)
    scored_results.sort(key=lambda x: x['match_score'], reverse=True)
    
    return scored_results[:3]

def display_results_gui(top_venues):
    """Displays the top recommendations in a GUI window."""
    result_window = tk.Tk()
    result_window.title("TOP 3 RECOMMENDATIONS")
    result_window.geometry("700x500")

    tk.Label(result_window, text="TOP 3 RECOMMENDATIONS", font=("Arial", 16, "bold")).pack(pady=10)

    if not top_venues:
        tk.Label(result_window, text="No matching venues found based on your criteria.").pack(pady=20)
    else:
        # Create a frame for the text area with scrollbar
        frame = tk.Frame(result_window)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Arial", 10))
        text_area.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_area.yview)

        for rank, row in enumerate(top_venues, 1):
            text_area.insert(tk.END, f"#{rank}: {row.get('title', 'Unknown Name')}\n")
            text_area.insert(tk.END, f"Zip Code: {row.get('Zip Code', 'N/A')}\n")
            text_area.insert(tk.END, f"Type: {row.get('type', 'N/A')} ({row.get('price', 'N/A')})\n")
            
            url = row.get('website', '')
            if not url: url = "No URL provided"
            text_area.insert(tk.END, f"URL: {url}\n")
            
            desc = row.get('description', '')
            if not desc: desc = "No description available."
            if len(desc) > 150:
                desc = desc[:147] + "..."
            text_area.insert(tk.END, f"Description: {desc}\n\n")
            text_area.insert(tk.END, "-" * 50 + "\n\n")

        text_area.config(state=tk.DISABLED)  # Make it read-only

    tk.Button(result_window, text="Close", command=result_window.quit).pack(pady=10)
    result_window.mainloop()
    result_window.destroy()

def main():
    # Load Data
    data = load_data()
    if not data:
        messagebox.showerror("Error", "CSV file not found. Please ensure 'plurpgh.csv' is in the same folder.")
        return

    # Extract unique types dynamically
    unique_types = sorted(list(set(row.get('type', '').strip() for row in data if row.get('type'))))
    
    # Run GUI Interface
    u_zip, u_budget, u_types, u_prefs = get_user_input_gui(unique_types)
    
    # Calculate Results
    top_venues = calculate_scores(data, u_zip, u_budget, u_types, u_prefs)
    
    # Display Results in GUI
    display_results_gui(top_venues)

if __name__ == "__main__":
    main()

