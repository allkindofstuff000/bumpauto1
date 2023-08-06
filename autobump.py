import tkinter as tk
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import winsound

# Create the root window
root = tk.Tk()
root.title("Post Bump Automation")
root.geometry("400x400")
root.configure(bg="orange")

# Function to start the bump automation
def start_bump():
    # Get the Chrome profile directories from the input field
    profile_directories = profile_directories_entry.get().split(",")

    # Set the executable path to the Chromium browser
    executable_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    # Create Chrome options and set the profile directories
    chrome_options = Options()
    for profile_directory in profile_directories:
        chrome_options.add_argument(f'--user-data-dir={profile_directory}')

    # Set up the Chrome driver with custom options and executable path
    driver = uc.Chrome(options=chrome_options, executable_path=executable_path)

    # Maximize the window
    driver.maximize_window()

    # Set the browser window size to a specific width and height (adjust as needed)
    driver.set_window_size(500, 800)

    # URL for Post 1 and Post 2
    post1_url = post1_url_entry.get()
    post2_url = post2_url_entry.get()

    # Function to bump the post
    bump_count = 0
    def bump_post(post_url):
        nonlocal bump_count
        driver.get(post_url)
        try:
            bump_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "managePublishAd"))
            )
            bump_button.click()
            winsound.Beep(1000, 3000)  # Play beep sound after clicking the button
            bump_count += 1
            total_bump_label.config(text=f"Total Bumps Counted: {bump_count}")
            log_text.insert(tk.END, f"Bumped to Top for Post {post_url}.\n")
        except Exception as e:
            log_text.insert(tk.END, f"Error clicking the 'Bump to Top' button for Post {post_url}: {e}\n")

    # Countdown function
    def countdown_timer(seconds):
        while seconds > 0:
            countdown_label.config(text=f"Time Left: {seconds} seconds")
            time.sleep(1)
            seconds -= 1
        countdown_label.config(text="")

    # Start the bumping process in a separate thread
    def bump_thread():
        profile_directories_label.pack_forget()
        profile_directories_entry.pack_forget()
        post1_url_label.pack_forget()
        post1_url_entry.pack_forget()
        post2_url_label.pack_forget()
        post2_url_entry.pack_forget()
        start_bump_button.pack_forget()

        all_kind_of_stuff_label = tk.Label(root, text="AllKindofStuff", font=("Helvetica", 18, "bold"), bg="orange")
        all_kind_of_stuff_label.pack()

        while True:
            bump_post(post1_url)
            countdown_timer(5)  # Wait for 910 seconds (approx. 15 minutes)
            bump_post(post2_url)
            countdown_timer(5)  # Wait for 910 seconds (approx. 15 minutes)

    bumping_thread = Thread(target=bump_thread)
    bumping_thread.start()

# Create the entry fields and buttons
profile_directories_label = tk.Label(root, text="Paste Chrome Profile Directories (comma-separated):", bg="orange")
profile_directories_label.pack()
profile_directories_entry = tk.Entry(root, width=50)
profile_directories_entry.pack()

post1_url_label = tk.Label(root, text="Paste Post 1 URL Here:", bg="orange")
post1_url_label.pack()
post1_url_entry = tk.Entry(root, width=50)
post1_url_entry.pack()

post2_url_label = tk.Label(root, text="Paste Post 2 URL Here:", bg="orange")
post2_url_label.pack()
post2_url_entry = tk.Entry(root, width=50)
post2_url_entry.pack()

start_bump_button = tk.Button(root, text="Start Bump", command=start_bump)
start_bump_button.pack()

# Countdown label
countdown_label = tk.Label(root, text="", font=("Helvetica", 16), bg="orange")
countdown_label.pack()

# Total bump count label
total_bump_label = tk.Label(root, text="Total Bumps Counted: 0", font=("Helvetica", 16), bg="orange")
total_bump_label.pack()

# Log text field
log_text = tk.Text(root, width=50, height=10)
log_text.pack()

# Function to quit the application
def quit_app():
    root.destroy()

quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.pack()

# Run the GUI
root.mainloop()
