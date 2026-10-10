import tkinter as tk

def tombol():
    root = tk.Tk()
    root.title("Tombol Example")

    def on_button_click():
        print("Tombol clicked!")

    tombol_button = tk.Button(root, text="Click Me", command=on_button_click)
    tombol_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    tombol()