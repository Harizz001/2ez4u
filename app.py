import os
import sys

# Memastikan direktori root masuk ke sys.path agar modul backend & frontend terbaca dengan aman
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
  print("Menjalankan aplikasi 2EZ4U Food Delivery...")

  # Mengimpor dan menjalankan antarmuka Tkinter dari frontend/ui.py
  from frontend.ui import root

  root.mainloop()