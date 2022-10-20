from pickle import TRUE
import tkinter as tk

print(tk.Tcl().eval('info patchlevel'))

app = tk.Tk()
pan = tk.PanedWindow(app)
f1 = tk.LabelFrame(pan, text="left", width=150, height=150)
f2 = tk.LabelFrame(pan, text="right", width=150)

f1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
f2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
pan.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

pan.add(f1)
pan.add(f2)

app.mainloop()