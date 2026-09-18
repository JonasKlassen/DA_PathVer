import tkinter as tk
from DA_PathVer.execution.gui import RepeatArrVerifierGUI

def main():
    root = tk.Tk()
    app = RepeatArrVerifierGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
