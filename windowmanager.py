import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
import Change

def on_entry_click(event, entry: tk.Entry):
    if entry.get() == directory_path:
        entry.delete(0, tk.END)  # Delete the current content
        

def focus_out(event, entry):
    if not entry.get():
        entry.insert(0, directory_path)  # Insert the default text
        
def remove_file(listbox: tk.Listbox):
    selected_index = listbox.curselection()
    if selected_index:
        item = listbox.get(selected_index)
        listbox.delete(selected_index)
        pass
    
    if listbox.size()==0:
        return 1
    
    return 0


directory_path = "Enter directory of folder or file"

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.geometry('1280x720')
        self.title('Change')
        self.colors = ["#E5E9EC", "#D0D7DD", "#7C616C"]
        self.directory = tk.StringVar()
        self.command = tk.StringVar()
        self.iconbitmap("icon/Change.ico")

        style = ttk.Style(self)
        style.configure("Primary.TFrame", background=self.colors[0])
        style.configure("Secondary.TFrame", background=self.colors[1])
        style.configure("Console.TFrame", background='black', foreground="white")
        self.configure(background=self.colors[0])

        self.selectionframe = ttk.Frame(self, width=1280, height=50, style="Primary.TFrame")
        self.selectionframe.pack(padx=5, pady=5, side="top", anchor='nw')

        self.fileselector = ttk.Entry(self.selectionframe, width=150, textvariable=self.directory)
        self.fileselector.pack(side="left", padx=5, pady=5, ipady=5)
        self.fileselector.insert(0, directory_path)  # Set initial text

        # Bind events to functions
        self.fileselector.bind('<FocusIn>', lambda event: on_entry_click(event, self.fileselector))
        self.fileselector.bind('<FocusOut>', lambda event: focus_out(event, self.fileselector))

        self.directorybutton = ttk.Button(self.selectionframe, width=100, text="Browse", command=lambda: self.getdirectory(self.listfiles))
        self.directorybutton.pack(side="left", padx=5, pady=5, ipady=5)

        self.lowerframe = ttk.Frame(self,height=500, width=1000,style="Primary.TFrame")
        self.lowerframe.pack(side="top", anchor='nw', padx=5, pady=5)
        
        self.consoleframe = ttk.Frame(self.lowerframe,style="Primary.TFrame")
        self.consoleframe.pack(side="left", anchor='nw', padx=10, pady=10,ipady=200)

        self.console_text = tk.Text(self.consoleframe, foreground='white', background='black', height=35, width=70)
        self.console_text.configure(state='disabled')
        self.console_text.pack(side='top', anchor='nw', padx=5, pady=5)

        self.userinput = ttk.Entry(self.consoleframe, textvariable=self.command,style="Console.TFrame")
        self.userinput.pack(side='top', anchor='nw', padx=5, pady=5,ipadx=280,ipady=10)
        self.userinput.bind('<Return>', lambda event: self.send_to_terminal(self.userinput.get(), self.console_text))
        


        self.lineframe = ttk.Frame(self.lowerframe, height=1000, width=1, style="Primary.TFrame")
        self.lineframe.pack(side="left", anchor='nw')

        # Create a canvas widget
        canvas = tk.Canvas(self.lineframe, width=8, height=600, background=self.colors[0])
        canvas.pack(padx=50,pady=10)

        # Add a line in canvas widget
        canvas.create_line(0, 0, 0, 1000, fill='black', width=20)
        
        self.listfiles = tk.Listbox(self.lowerframe, width=70, height=5,background='black',foreground='white')
        self.listfiles.pack(pady=15)
        self.listfiles.bind("<Double-Button-1>",lambda event:remove_file(self.listfiles))
        
        self.fileconverterframe = ttk.Frame(self.lowerframe,style="Primary.TFrame")
        self.fileconverterframe.pack(side="top", anchor='nw', padx=5, pady=5)
        self.conversionlabel = tk.Label(self.fileconverterframe,justify='left',anchor='w',text='Choose file or files to convert',background='black',foreground='white',width=30)
        self.conversionlabel.pack(side="left",anchor='nw',pady=10,)
        
        self.convertto = ttk.Combobox(self.fileconverterframe,background='black',foreground='white')
        self.convertto.pack(side="left",anchor='nw',padx=5,pady=10)
        
        self.startbutton = ttk.Button(self.fileconverterframe,text="Begin",state='disabled',command= lambda: self.beginconvert())
        self.startbutton.pack(side="top",pady=10)
        
        self.send_to_terminal("Welcome To Change, A File Converter", self.console_text)
        
    def send_to_terminal(self, text, terminal_text, max_lines=36):
        if text == "":
            return

        terminal_text.configure(state='normal')

        # Insert the new text at the end of the Text widget
        terminal_text.insert(tk.END, text + '\n')

        # Get the current number of lines
        lines = terminal_text.get("1.0", tk.END).split('\n')

        # Keep only the last 'max_lines' lines
        if len(lines) > max_lines:
            terminal_text.delete("1.0", f"{int(len(lines) - max_lines)}.0")

        # Clear the entry widget
        self.userinput.delete(0, tk.END)
        terminal_text.configure(state='disabled')
        
    def getdirectory(self,listbox:tk.Listbox):
        selected_directory = filedialog.askopenfilenames()
        if(selected_directory == ""):
            return
        if selected_directory:
            self.directory.set(selected_directory)
            self.fileselector.delete(0, tk.END)  # Clear the current content
            self.fileselector.insert(0, selected_directory)
        
        for file in selected_directory:
            listbox.insert(tk.END, file)
            
        
        match listbox.get(0,1)[0][-3:]:
            case"txt":
                self.convertto.set('')
                self.conversionlabel.configure(text="Convert from TXT to: ")
                self.convertto['values'] = ('pdf','docx')
                self.startbutton.configure(state='normal')
  
                pass
            
            case "ocx":
                self.convertto.set('')
                self.conversionlabel.configure(text="Convert from DOCX to: ")
                self.convertto['values'] = ('txt','pdf')
                self.startbutton.configure(state='normal')
                pass
            
            case"pdf":
                self.convertto.set('')
                self.conversionlabel.configure(text="Convert from PDF to: ")
                self.convertto['values'] = ('txt','docx')
                self.startbutton.configure(state='normal')
                pass
    
    def beginconvert(self):
        self.send_to_terminal("Beginning conversion...", self.console_text)
        command = []
        filetype = self.listfiles.get(0,1)[0][-3:]
        files = []
        for item in self.listfiles.get(0,tk.END):
            if item[-3:] != filetype:
                log = f"{item} is not of type {filetype}"
                self.send_to_terminal(log, self.console_text)
                showerror("Error", "All files must be the same type\n Aborting...") 
                return
            else:
                log = f"{item} of type {filetype} has been added to queue"
                self.send_to_terminal(log, self.console_text)
                files.append(item)
        self.send_to_terminal("Converting this may take a while =]", self.console_text)
        Change.convert(files,self.convertto.get())
        self.send_to_terminal("Done, check output folder to see results =]", self.console_text)
        self.convertto.set('')
        self.listfiles.delete(0,tk.END)
        self.conversionlabel.configure(text="Choose file or files to convert")
        self.startbutton.configure(state='disabled')
        
        pass         

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()