import tkinter as tk
from tkinter import scrolledtext
import subprocess

def run_mbt():
    input_text = input_box.get("1.0", tk.END).strip()
    if not input_text:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "Please enter some text.")
        return

    mbt_input = input_text + "\nEL\n"

    try:
        process = subprocess.Popen(
            ['mbt', '-s', 'kikuyu.data.settings', '-eEL'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=mbt_input)

        output_box.delete("1.0", tk.END)

        if stderr.strip():
            output_box.insert(tk.END, f"Error:\n{stderr}")
            return

        # Get all lines that contain tagged output
        lines = stdout.strip().split('\n')
        tag_lines = [line for line in lines if '/' in line and not line.startswith("mbt")]

        if not tag_lines:
            output_box.insert(tk.END, "No tagged output found.")
            return

        # Assume the last tagged line is the real result
        final_tag_line = tag_lines[-1]
        formatted_output = []

        for token in final_tag_line.strip().split():
            if '/' in token:
                parts = token.rsplit('/', 1)
                if len(parts) == 2:
                    word, tag = parts
                    formatted_output.append(f"{word} --> {tag}")

        output_box.insert(tk.END, "\n".join(formatted_output))

    except FileNotFoundError:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "Error: MBT command not found. Is it installed and in your PATH?")

# GUI Setup
window = tk.Tk()
window.title("Kikuyu Named Entity Recognition (MBT GUI)")

tk.Label(window, text="Enter Kikuyu Text:").pack()
input_box = scrolledtext.ScrolledText(window, height=5, width=70)
input_box.pack(padx=10, pady=5)

tk.Button(window, text="Tag Named Entities", command=run_mbt).pack(pady=10)

tk.Label(window, text="Tagged Output:").pack()
output_box = scrolledtext.ScrolledText(window, height=15, width=70)
output_box.pack(padx=10, pady=5)

window.mainloop()
