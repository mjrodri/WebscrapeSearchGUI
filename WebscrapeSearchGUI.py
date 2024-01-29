import tkinter as tk
import beautifulsoup4
from tkinter import messagebox, ttk
from bs4 import BeautifulSoup
import requests

def search_keywords():
    url = url_entry.get()
    keywords = keywords_entry.get().split(',')
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all text content within the webpage
        text_content = soup.get_text()
        
        # Search for keywords
        found_keywords = [keyword.strip() for keyword in keywords if keyword.strip() in text_content]
        
        # Display search results
        if found_keywords:
            result_text.config(state="normal")
            result_text.delete("1.0", tk.END)
            for keyword in found_keywords:
                result_text.insert(tk.END, f"Keyword: {keyword}\n\n", "keyword")
            result_text.config(state="disabled")
        else:
            result_text.config(state="normal")
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "No keywords found.")
            result_text.config(state="disabled")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve URL: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("Web Scraping Keyword Search")

# URL input
url_frame = ttk.Frame(root)
url_frame.pack(fill="x", padx=10, pady=5)
tk.Label(url_frame, text="Enter URL:").pack(side="left")
url_entry = tk.Entry(url_frame, width=50)
url_entry.pack(side="left", expand=True, fill="x")

# Keywords input
keywords_frame = ttk.Frame(root)
keywords_frame.pack(fill="x", padx=10, pady=5)
tk.Label(keywords_frame, text="Enter Keywords (comma-separated):").pack(side="left")
keywords_entry = tk.Entry(keywords_frame, width=50)
keywords_entry.pack(side="left", expand=True, fill="x")

# Search button
search_button = ttk.Button(root, text="Search", command=search_keywords)
search_button.pack(pady=5)

# Search results
result_text_frame = ttk.Frame(root)
result_text_frame.pack(fill="both", expand=True, padx=10, pady=5)
result_text_scrollbar = ttk.Scrollbar(result_text_frame, orient="vertical")
result_text_scrollbar.pack(side="right", fill="y")
result_text = tk.Text(result_text_frame, wrap="word", yscrollcommand=result_text_scrollbar.set, state="disabled")
result_text.pack(fill="both", expand=True)
result_text_scrollbar.config(command=result_text.yview)
result_text.tag_configure("keyword", foreground="blue", font=("Arial", 10, "bold"))

root.mainloop()