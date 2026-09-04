import tkinter as tk
from repeat_arr_verifier.execution.gui import RepeatArrVerifierGUI

def main():
    root = tk.Tk()
    app = RepeatArrVerifierGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
