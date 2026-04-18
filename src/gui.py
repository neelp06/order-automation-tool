import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from ingest import load_orders
from database import save_to_db
from job_cards import generate_job_card
from report import generate_report

# --- Core Logic ---
def process_orders(filepath, log):
    try:
        log("📂 Loading orders...")
        df = load_orders(filepath)
        log(f"✅ {len(df)} orders loaded.")

        log("💾 Saving to database...")
        save_to_db(df)

        log("🖨️  Generating job cards...")
        valid_orders = df[~df['is_duplicate'] & ~df['missing_data']]
        for _, order in valid_orders.iterrows():
            generate_job_card(order)
        log(f"✅ {len(valid_orders)} job cards created.")

        log("📊 Generating Excel report...")
        generate_report(df)

        log("=" * 40)
        log("✅ All done! Check your job_cards/ and output/ folders.")

    except Exception as e:
        log(f"❌ Error: {str(e)}")

# --- GUI ---
def build_gui():
    root = tk.Tk()
    root.title("Order Automation Tool")
    root.geometry("550x500")
    root.resizable(False, False)
    root.configure(bg="#2C3E50")

    # --- Title ---
    title = tk.Label(
        root,
        text="📦 Order Automation Tool",
        font=("Helvetica", 18, "bold"),
        bg="#2C3E50",
        fg="white"
    )
    title.pack(pady=20)

    # --- File Selection ---
    file_frame = tk.Frame(root, bg="#2C3E50")
    file_frame.pack(pady=10)

    file_label = tk.Label(
        file_frame,
        text="No file selected",
        font=("Helvetica", 10),
        bg="#2C3E50",
        fg="#BDC3C7",
        width=40,
        anchor='w'
    )
    file_label.pack(side='left', padx=10)

    selected_file = {'path': None}

    def select_file():
        filepath = filedialog.askopenfilename(
            title="Select Order CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if filepath:
            selected_file['path'] = filepath
            short_name = filepath.split("/")[-1]
            file_label.config(text=f"📄 {short_name}", fg="#2ECC71")
            run_btn.config(state='normal')

    browse_btn = tk.Button(
        file_frame,
        text="Browse",
        font=("Helvetica", 10, "bold"),
        bg="#3498DB",
        fg="white",
        relief="flat",
        padx=10,
        command=select_file
    )
    browse_btn.pack(side='left')

    # --- Log Box ---
    log_frame = tk.Frame(root, bg="#2C3E50")
    log_frame.pack(pady=10, padx=20, fill='both', expand=True)

    log_box = tk.Text(
        log_frame,
        height=15,
        font=("Courier", 10),
        bg="#1A252F",
        fg="#2ECC71",
        relief="flat",
        state='disabled'
    )
    log_box.pack(fill='both', expand=True)

    def log(message):
        log_box.config(state='normal')
        log_box.insert('end', message + "\n")
        log_box.see('end')
        log_box.config(state='disabled')

    # --- Run Button (created before run() so it exists) ---
    run_btn = tk.Button(
        root,
        text="▶ Run",
        font=("Helvetica", 13, "bold"),
        bg="#27AE60",
        fg="white",
        relief="flat",
        padx=20,
        pady=10,
        state='disabled',
    )
    run_btn.pack(pady=15)

    # --- Run Function (defined after run_btn exists) ---
    def run():
        if not selected_file['path']:
            messagebox.showwarning("No File", "Please select a CSV file first.")
            return

        log("=" * 40)
        log("🚀 Starting automation...")
        log("=" * 40)
        run_btn.config(state='disabled', text="Processing...")

        def task():
            process_orders(selected_file['path'], log)
            run_btn.config(state='normal', text="▶ Run")

        threading.Thread(target=task).start()

    # --- Attach command now that both exist ---
    run_btn.config(command=run)

    root.mainloop()

build_gui()