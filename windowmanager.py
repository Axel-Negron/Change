import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
import Change
import flask_app
import os
import shutil
import sys
import random
import subprocess
import threading
import time
import socket
import qrcode
from PIL import Image, ImageTk

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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # Check if the script is bundled with PyInstaller
        if getattr(sys, 'frozen', False):
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        else:
            # Not bundled, use the current working directory
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
    except Exception as e:
        print(f"Error in resource_path: {e}")
        return None

directory_path = "Enter directory of folder or file"


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.geometry('1280x750')
        self.resizable(False, False)
        self.title('Change')
        self.colors = ["#778080", "#424769", "#2F3337"]
        self.txtcolor = ["#f7f0f5","#f7f0f5"]
        self.directory = tk.StringVar()
        self.command = tk.StringVar()
        icon_path = resource_path("icon/Change.ico")
        self.iconbitmap(icon_path)
        self.sharelink = tk.StringVar()
        self.cwd = os.getcwd()
        self.copied = ""

        
        style = ttk.Style(self)
        style.configure("Primary.TFrame", background=self.colors[0])
        style.configure("Secondary.TFrame", background=self.colors[1])
        style.configure("Console.TFrame", background='#0C120C', foreground=self.txtcolor[1])
        style.configure("TCombobox", selectbackground=self.colors[0], fieldbackground='black', background=self.colors[0], foreground=self.txtcolor)
        self.configure(background=self.colors[0])

        self.lowerframe = ttk.Frame(self,height=500, width=1000,style="Primary.TFrame")
        self.lowerframe.pack(side="top", anchor='nw', padx=5, pady=5)
        
        self.consoleframe = ttk.Frame(self.lowerframe,style="Primary.TFrame")
        self.consoleframe.pack(side="left", anchor='nw', padx=10, pady=10,ipady=200)

        self.consolelbl = ttk.Label(
            self.consoleframe,
            text="Console",
            font=('Arial', 15, 'bold'),
            foreground=self.txtcolor[0],  # Set the text color
            background=self.colors[0]
        )
        self.consolelbl.pack(side='top', anchor='nw', pady=(0, 10))

        self.console_text = tk.Text(
            self.consoleframe,
            foreground=self.txtcolor[1],  # Set the text color
            background='black',
            height=35,
            width=75
        )
        self.console_text.configure(state='disabled')
        self.console_text.pack(side='top', anchor='nw', padx=5, pady=5)

        self.userinput = ttk.Entry(
            self.consoleframe,
            textvariable=self.command,
            style="Console.TFrame",
            foreground=self.txtcolor[1]  # Set the text color
        )
        self.userinput.pack(side='top', anchor='nw', padx=5, pady=5, ipadx=300, ipady=10)

        self.userinput.bind('<Return>', lambda event: self.user_input())
        


        self.lineframe = ttk.Frame(self.lowerframe, height=1000, width=1, style="Primary.TFrame")
        self.lineframe.pack(side="left", anchor='nw',padx=(90,0))

        # Create a canvas widget
        
        self.listfileslbl = ttk.Label(self.lowerframe, text="Queue:",font=('Arial', 15, 'bold'), foreground=self.txtcolor[0], background=self.colors[0])
        self.listfileslbl.pack(side='top',anchor='nw',pady=(20,5))
        self.selectionframe2 = ttk.Frame(self.lowerframe, width=20, height=50, style="Primary.TFrame")
        self.selectionframe2.pack(padx=5, pady=5, side="top", anchor='nw')
        
        self.fileselector = ttk.Entry(self.selectionframe2, textvariable=self.directory,style="Console.TFrame")
        self.fileselector.pack(side='left', anchor='nw', padx=(0,5), pady=5,ipadx=200,ipady=10)
        self.fileselector.bind('<FocusIn>', lambda event: on_entry_click(event, self.fileselector))
        self.fileselector.bind('<FocusOut>', lambda event: focus_out(event, self.fileselector))
        
        self.directorybutton = tk.Button(self.selectionframe2, text="Browse",bg=self.colors[2],
            fg=self.txtcolor[0],command=lambda: self.getdirectory(self.listfiles))
        self.directorybutton.pack(side='left')

        
        self.listfiles = tk.Listbox(self.lowerframe, width=70, height=5,background='black',foreground=self.txtcolor[0])
        self.listfiles.pack(anchor='nw')
        self.listfiles.bind("<Double-Button-1>",lambda event:remove_file(self.listfiles))
        self.fileselector.bind("<Return>",lambda event:self.listfiles.insert(tk.END, self.directory.get()))
        
        self.fileconverterframe = ttk.Frame(self.lowerframe,style="Primary.TFrame")
        self.fileconverterframe.pack(side="top", anchor='nw', padx=5)
        self.conversionlabel = tk.Label(self.fileconverterframe,justify='left',anchor='w',text='Choose file or files to convert',background='black',foreground=self.txtcolor[0],width=30)
        self.conversionlabel.pack(side="left",anchor='nw',pady=10,)
        
        self.convertto = ttk.Combobox(
            self.fileconverterframe,
            style="TCombobox"
        )
        self.convertto.pack(side="left", anchor='nw', padx=5, pady=10)

        self.startbutton = tk.Button(
            self.fileconverterframe,
            text="Begin",
            state=tk.DISABLED,
            command=lambda: self.beginconvert(),
            bg=self.colors[2],
            fg=self.txtcolor[0]
            

        )
        self.startbutton.pack(side="top", pady=10)
        
        self.send_to_terminal("Welcome To Change, A File Converter", self.console_text)
        
        
        self.sharediv = ttk.Frame(self.lowerframe,style="Primary.TFrame")
        self.sharediv.pack(side="top", anchor='nw', padx=5, pady=5)
        
        self.sharetxt = ttk.Label(self.sharediv, text="Share locally:",font=('Arial', 15, 'bold'), foreground=self.txtcolor[0], background=self.colors[0])
        self.sharetxt.pack(side='top',anchor='nw',pady=15)
        
        self.shareselectorframe = ttk.Frame(self.sharediv,style="Primary.TFrame")
        self.shareselectorframe.pack(side="top", anchor='nw', padx=5)
        self.shareentry = ttk.Entry(self.shareselectorframe, textvariable=self.sharelink,style="Console.TFrame")
        self.shareentry.pack(side='left', anchor='nw', pady=5,ipadx=200,ipady=10)
        self.sharebrowse = tk.Button(self.shareselectorframe, bg=self.colors[2],
            fg=self.txtcolor[0],text="Browse",command=lambda: self.getdirectory(self.listsharefiles))
        self.sharebrowse.pack(side="left",padx=(5,0))
        self.listsharefiles = tk.Listbox(self.sharediv, width=70, height=5,background='black',foreground=self.txtcolor[1])
        self.listsharefiles.pack(anchor='nw')
        self.listsharefiles.bind("<Double-Button-1>",lambda event:remove_file(self.listsharefiles))
        self.shareentry.bind("<Return>",lambda event:self.listsharefiles.insert(tk.END, self.sharelink.get()))
        self.sharebutton = tk.Button(
            self.sharediv,
            text="Share",
            command=lambda: self.share(),
            width=50,
            bg=self.colors[2],
            fg=self.txtcolor[0]
        )
        self.sharebutton.pack(side="top", pady=10)

        self.terminate_serverbtn = tk.Button(
            self.sharediv,
            text="Terminate Server",
            state=tk.DISABLED,
            command=lambda: self.terminate_server(),
            width=50,
            bg=self.colors[2],
            fg=self.txtcolor[0]
        )
        self.terminate_serverbtn.pack(side="top")
    
    def user_input(self,):
        self.console_text.configure(state='normal')
        cmd = self.command.get().split(' ', 1)[0]
        parsed_input = self.command.get().split(' ')
        match cmd:
            case "help":
                self.send_to_terminal("Available commands: help,clear,ls,cd,cwd,exit,copy,copy2,paste,copied?,rm,mkdir,convert", self.console_text)
                
            case "clear":
                self.console_text.delete('1.0', tk.END)
                
            case "ls":
                for item in os.listdir(self.cwd):
                    self.send_to_terminal(item, self.console_text)
            
            case "cd":
                if len(parsed_input) == 1:
                    self.send_to_terminal("Please provide a directory.", self.console_text)
                    
                elif parsed_input[1] == "..":
                    self.cwd = os.path.abspath(os.path.join(self.cwd, os.path.pardir))
                    self.send_to_terminal(f"CWD: {self.cwd}.", self.console_text)
                else:
                    try:
                        if os.path.exists(os.path.join(self.cwd, parsed_input[1])):
                            self.cwd = os.path.abspath(os.path.join(self.cwd, parsed_input[1]))
                            self.send_to_terminal(f"CWD: {self.cwd}.", self.console_text)
                        else:
                            self.send_to_terminal(f"Directory: {os.path.join(self.cwd, parsed_input[1])} not found.", self.console_text)
                    except:
                        self.send_to_terminal("Directory not found.", self.console_text)
            
            case "cwd":
                self.send_to_terminal(f"Directory: {self.cwd}", self.console_text)
            
            case "exit":
                self.send_to_terminal("Exiting...", self.console_text)
                exit()
                
            case "copy":
                temp = ""
                if len(parsed_input)==1:
                    self.send_to_terminal("Please provide a directory to copy.", self.console_text)
                else:
                    try:
                        for file in parsed_input[1:]:
                            temp+=f"{file},"
                            
                        temp = temp[:-1]
                        self.copied=temp
                        self.send_to_terminal("Files copied.", self.console_text)
                    except:
                        self.send_to_terminal("Error copying file/s.", self.console_text)
                        
            case "copy2":
                if len(parsed_input)!=3:
                    self.send_to_terminal("Please provide a directory from and to in which to copy.", self.console_text)
                else:
                    try:
                        shutil.copy(parsed_input[1], parsed_input[2])
                        self.send_to_terminal("Files copied to path.", self.console_text)
                    except:
                        self.send_to_terminal("Error copying file/s to location.", self.console_text)
                    
            case "paste":
                if self.copied == "":
                    self.send_to_terminal("No files to paste.", self.console_text) 
                    pass
                
                elif len(parsed_input) == 2:
                    for file in self.copied.split(","):
                        shutil.copy(file, parsed_input[1])
                    self.send_to_terminal("Files pasted to directory.", self.console_text)
                
                elif len(parsed_input) == 1:
                    for file in self.copied.split(","):
                        shutil.copy(file, self.cwd)
                    self.send_to_terminal("Files pasted to directory.", self.console_text)
                                 
                
            case "copied?":
                self.send_to_terminal(self.copied, self.console_text)   
            
            case "rm":
                if len(parsed_input) < 2:
                    self.send_to_terminal("Please provide a directory to remove.", self.console_text)
                else:
                    try:
                        for file in parsed_input[1:]:
                            if os.path.isdir(f"{self.cwd}/{file}"):
                                shutil.rmtree(f"{self.cwd}/{file}")
                                self.send_to_terminal("Folder/s removed.", self.console_text)
                            else:
                                os.remove(f"{self.cwd}/{file}")
                                self.send_to_terminal("File/s removed.", self.console_text)
                    except:
                        self.send_to_terminal("Error removing file/s.", self.console_text)
            
            case "mkdir":
                if len(parsed_input) == 1:
                    self.send_to_terminal("Please provide a directory to create.", self.console_text)
                else:
                    try:
                        for file in parsed_input[1:]:
                            os.mkdir(f"{self.cwd}/{file}")
                            self.send_to_terminal("Folder/s created.", self.console_text)
                    except:
                        self.send_to_terminal("Error creating folder/s.", self.console_text)
            
            case "mkfile":
                if len(parsed_input) == 1:
                    self.send_to_terminal("Please provide a file to create.", self.console_text)
                else:
                    try:
                        for file in parsed_input[1:]:
                            open(f"{self.cwd}/{file}", "w").close()
                            self.send_to_terminal("File/s created.", self.console_text)
                    except:
                        self.send_to_terminal("Error creating file/s.", self.console_text)
            
            case "hello":
                self.send_to_terminal("Hi!", self.console_text)
            
            case "hi":
                self.send_to_terminal("Hello!", self.console_text)
                
            case "convert":
                if len(parsed_input) == 1:
                    self.send_to_terminal("Please provide a file to convert.", self.console_text)
                else:
                    try:
                        for file in parsed_input[1:]:
                            self.fileselector.insert(tk.END, file)
                            if os.path.exists(file):
                                self.listfiles.insert(tk.END,file)
                                self.send_to_terminal(f"File: {file} added to queue.", self.console_text)
                        self.listfiles.configure(state='normal')
            
                        self.convertto.set('')
                        match self.listfiles.get(0,1)[0][-3:]:
                            
                            case"txt":
                                self.conversionlabel.configure(text="Convert from TXT to: ")
                                self.convertto['values'] = ('pdf','docx')
                                pass
                            
                            case "ocx":
                                self.conversionlabel.configure(text="Convert from DOCX to: ")
                                self.convertto['values'] = ('txt','pdf')
                                pass
                            
                            case"pdf":
                                self.conversionlabel.configure(text="Convert from PDF to: ")
                                self.convertto['values'] = ('txt','docx')
                                pass
                            
                            case"mp3":
                                self.conversionlabel.configure(text="Convert from MP3 to: ")
                                self.convertto['values'] = ('wav','flac')
                                pass
                            
                            case"lac":
                                self.convertto.set('')
                                self.conversionlabel.configure(text="Convert from FLAC to: ")
                                self.convertto['values'] = ('mp3','wav')
                                self.startbutton.configure(state=tk.NORMAL)
                                pass
                            
                            case"wav":
                                self.conversionlabel.configure(text="Convert from WAV to: ")
                                self.convertto['values'] = ('mp3','flac')
                                pass
                            
                            case"png":
                                self.conversionlabel.configure(text="Convert from PNG to: ")
                                self.convertto['values'] = ('JPG')
                                
                        self.startbutton.configure(state=tk.NORMAL)          
                    except:
                        self.send_to_terminal("Error adding to queue", self.console_text)
            
            case "open":
                if len(parsed_input) == 1:
                    self.send_to_terminal("Please provide a file to open.", self.console_text)
                else:
                    try:
                        self.send_to_terminal("Opening file.", self.console_text)
                        os.startfile(parsed_input[1])
                    except:
                        self.send_to_terminal("Error opening file.", self.console_text)
            case _:
                self.send_to_terminal(self.command.get(), self.console_text)
  
        self.userinput.delete(0, tk.END)
        self.command.set("")
        self.console_text.configure(state='disabled')
        
        return
  
    def send_to_terminal(self, text, terminal_text, max_lines=35):
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
        
        listbox.configure(state='normal')
            
        self.convertto.set('')
        match listbox.get(0,1)[0][-3:]:
            
            case"txt":
                self.conversionlabel.configure(text="Convert from TXT to: ")
                self.convertto['values'] = ('pdf','docx')
                pass
            
            case "ocx":
                self.conversionlabel.configure(text="Convert from DOCX to: ")
                self.convertto['values'] = ('txt','pdf')
                pass
            
            case"pdf":
                self.conversionlabel.configure(text="Convert from PDF to: ")
                self.convertto['values'] = ('txt','docx')
                pass
            
            case"mp3":
                self.conversionlabel.configure(text="Convert from MP3 to: ")
                self.convertto['values'] = ('wav','flac')
                pass
            
            case"lac":
                self.convertto.set('')
                self.conversionlabel.configure(text="Convert from FLAC to: ")
                self.convertto['values'] = ('mp3','wav')
                self.startbutton.configure(state=tk.NORMAL)
                pass
            
            case"wav":
                self.conversionlabel.configure(text="Convert from WAV to: ")
                self.convertto['values'] = ('mp3','flac')
                pass
            
            case"png":
                self.conversionlabel.configure(text="Convert from PNG to: ")
                self.convertto['values'] = ('JPG')
                
        self.startbutton.configure(state=tk.NORMAL)  
                  
    def beginconvert(self):
        
        self.send_to_terminal("Beginning conversion...", self.console_text)
        if self.listfiles.size() == 0:
            self.send_to_terminal("No files selected, aborting...", self.console_text)
            self.fileselector.configure(state='disabled')
            return
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
        self.startbutton.configure(state=tk.DISABLED)
        self.fileselector.delete(0,'end')
        directory_path = "Enter directory of folder or file"
        self.fileselector.insert(0, directory_path)
        pass    
    
    def share(self):
        try:
            self.image_label.destroy()
        except:
            pass
        if not os.path.exists('share'):
            os.mkdir('share')

        if not self.listsharefiles.get(0, 'end'):
            self.send_to_terminal("No files to share, returning...", self.console_text)
            return
        else:
            for i in range(50): 
                try:
                    path = f'share-{random.randint(1, 100)}'
                    os.mkdir(f'share/{path}')
                    os.mkdir(f'share/{path}/temp')
                    for file in self.listsharefiles.get(0, 'end'):
                        shutil.copy(file, f'share/{path}/temp')

                    shutil.make_archive(f"share/{path}/{path}", 'zip', f'share/{path}/temp')
                    break
                
                except:
                    continue
                
            self.send_to_terminal("Archive made, launching Flask app...", self.console_text)
            self.send_to_terminal("Using your IPV4 address to access with port 5000...", self.console_text)
            self.send_to_terminal(f"Your link: http://{self.getip()}:5000/download", self.console_text)


            if not os.path.exists("share.txt"):
                with open(f"share.txt", 'x') as f:
                    f.write(f"share/{path}/{path}.zip")
                    f.close()
            else:
                with open(f"share.txt", 'w') as f:
                    f.write(f"share/{path}/{path}.zip")
                    f.close()
                    
            
            flask_thread = threading.Thread(target=self.run_flask_app)
            flask_thread.start()
            time.sleep(1)
            self.terminate_serverbtn.configure(state=tk.NORMAL)
            qr = qrcode.QRCode(version=3, box_size=5, border=3, error_correction=qrcode.constants.ERROR_CORRECT_H)
            data = f'http://{self.getip()}:5000/download'
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f"share/{path}/qr_code.png")
            pil_image = Image.open(f"share/{path}/qr_code.png")
            tk_image = ImageTk.PhotoImage(pil_image)
            self.image_label = tk.Label(self.sharediv, image=tk_image)
            self.image_label.pack(pady=10)
            self.image_label.image = tk_image

            
            return
        
        
    def getip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        user_ip = s.getsockname()[0]
        s.close() 
        return user_ip
    
     
    def run_flask_app(self):
        try:
            # Start Flask app in the background
            flask_process = subprocess.Popen(['python', 'flask_app.py'])
            print("Flask App is running.")

            flask_process.wait()
        except KeyboardInterrupt:
            # Handle keyboard interrupt (e.g., Ctrl+C to terminate)
            print("KeyboardInterrupt: Stopping Flask App.\n")
            flask_process.terminate()
            flask_process.wait()
        except Exception as e:
            print(f"Error: {e}\n")
        finally:
            print("Flask App stopped.\n")

    def terminate_server(self):
        abs_path = os.path.abspath("terminate_server.bat")
        print(abs_path)
        result = subprocess.run(['powershell', '-Command', 'Start-Process', abs_path, '-Verb', 'RunAs'], check=True)
        print(f"Server terminated: Result {result}")
        self.terminate_serverbtn.configure(state=tk.DISABLED)
        self.image_label.destroy()

if __name__ == "__main__":
    flask_app = MainWindow()
    flask_app.mainloop()