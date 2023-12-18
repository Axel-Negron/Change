import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
import Change
import qrcode
import os
import random
import shutil
import http.server
import socketserver
import threading
from PIL import Image, ImageTk
import sys

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

        self.geometry('1280x800')
        self.resizable(False, False)
        self.title('Change')
        self.colors = ["#E5E9EC", "#D0D7DD", "#7C616C"]
        self.directory = tk.StringVar()
        self.command = tk.StringVar()
        icon_path = resource_path("icon/Change.ico")
        self.iconbitmap(icon_path)
        self.ip = tk.StringVar()
        self.share_progress_var = tk.DoubleVar()
        self.share_progress_var.set(0.0)
        

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

        self.consolelbl = ttk.Label(self.consoleframe, text="Console",font=('Arial', 15, 'bold'), foreground='black', background=self.colors[0])
        self.consolelbl.pack(side='top',anchor='nw')
        self.console_text = tk.Text(self.consoleframe, foreground='white', background='black', height=32, width=70)
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
        
        
        self.listfileslbl = ttk.Label(self.lowerframe, text="Queue:",font=('Arial', 15, 'bold'), foreground='black', background=self.colors[0])
        self.listfileslbl.pack(side='top',anchor='nw',pady=15)
        self.listfiles = tk.Listbox(self.lowerframe, width=70, height=5,background='black',foreground='white')
        self.listfiles.pack(anchor='nw')
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
        
        
        self.sharelbl = ttk.Label(self.lowerframe, text="Share Files locally:",font=('Arial', 20, 'bold'), foreground='black', background=self.colors[0])
        self.sharelbl.pack(side='top',anchor='nw')
        
        
        self.useriplbl = ttk.Label(self.lowerframe, text="IP w/ port (example: 127.0.0.1:8000):",font=('Arial', 15, 'bold'), foreground='black', background=self.colors[0])
        self.useriplbl.pack(side='top',anchor='nw')
        self.userip = ttk.Entry(self.lowerframe, textvariable=self.ip,style="Console.TFrame")
        self.userip.pack(side='top', anchor='nw', padx=5, pady=5,ipadx=240,ipady=10)
        self.sharefileslbl = ttk.Label(self.lowerframe, text="Queued files to share:",font=('Arial', 15, 'bold'), foreground='black', background=self.colors[0])
        self.sharefileslbl.pack(side='top',anchor='nw')
        self.sharefiles = tk.Listbox(self.lowerframe, width=70, height=2,background='black',foreground='white')
        self.sharefiles.pack(pady=10,anchor='nw')
        self.sharefiles.bind("<Double-Button-1>",lambda event:remove_file(self.sharefiles))
        
        self.picksharedir = ttk.Button(self.lowerframe, text="Browse", command=lambda: self.getdirectory(self.sharefiles))
        self.picksharedir.pack(ipadx=200)
        self.sharefilesbtn = ttk.Button(self.lowerframe, text="Share", command=lambda: self.share())
        self.sharefilesbtn.pack(ipadx=200)
        
        
    def share(self):
        try:
            self.shareframe.destroy()
            self.shareqr_label.destroy()
        except:
            pass

        self.send_to_terminal("Beginning share, creating zip file", self.console_text)
        if self.sharefiles.get(0, tk.END) == ():
            self.send_to_terminal("No files selected", self.console_text)
            return

        sharedir = f"share-{random.randint(0, 100)}"

        os.makedirs(sharedir, exist_ok=True)
        os.makedirs(resource_path(f'{sharedir}/share-rawfile'), exist_ok=True)

        self.send_to_terminal("Copying files", self.console_text)
        for file in self.sharefiles.get(0, tk.END):
            shutil.copy(file, resource_path(f"{sharedir}/share-rawfile"))

        fileaddress = resource_path(f"{sharedir}/{sharedir}")
        self.send_to_terminal("Done", self.console_text)
        self.send_to_terminal("Zipping files", self.console_text)
        shutil.make_archive(fileaddress, 'zip', resource_path(f"{sharedir}/share-rawfile"))


        self.send_to_terminal("Creating QR code", self.console_text)



        address_parts = self.ip.get().split(':')
        if len(address_parts) < 2:
            self.send_to_terminal("No port specified, defaulting to 8000", self.console_text)
            address_parts.append(8000)
            pass
        host = address_parts[0]
        port = int(address_parts[1])

        http_thread = threading.Thread(target=self.start_http_server, args=(host, int(port),sharedir))
        http_thread.start()

        self.send_to_terminal("QR code created. Scan to download", self.console_text)
        

    def start_http_server(self, host, port, sharedir):
        self.send_to_terminal(sharedir, self.console_text)
        self.send_to_terminal(f'File will be in /{sharedir}/{sharedir}.zip', self.console_text)
        # Define the HTTP server handler
        class MyHandler(http.server.SimpleHTTPRequestHandler):
            file_downloaded = False

            def do_GET(self):
                super().do_GET()
                if self.path == f'/{sharedir}/{sharedir}.zip':
                    # File is downloaded, set the flag
                    self.file_downloaded = True
                    # Respond to the client to ensure the file is fully downloaded
                    self.send_response(200)
                    self.end_headers()
                    shutil.rmtree(sharedir)
                    try:
                        self.server.server_close()
                    except:
                        return
                    return

        # Attempt to bind to different ports until an available one is found
        for i in range(10):
            try:
                current_port = port + i
                with socketserver.TCPServer((host, current_port), MyHandler) as httpd:
                    print(f"HTTP server listening on {host}:{current_port}")

                    # Create QR code and display it
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    
                    full_url = f"http://{host}:{current_port}/{f'/{sharedir}/{sharedir}.zip'}"
                    qr.add_data(full_url)
                    qr.make(fit=True)
                    # Create an image from the QR code
                    img = qr.make_image(fill_color="black", back_color="white")
                    static_folder = f"{sharedir}/static_folder"
                    os.makedirs(static_folder, exist_ok=True)
                    img.save(os.path.join(static_folder, f'qrcode-{sharedir}.png'))
                    resized = img.resize((200, 200))

                    # Display QR code
                    self.shareframe = ttk.Frame(self.lowerframe, style="Secondary.TFrame")
                    self.shareframe.pack(padx=5, pady=5, side="top")
                    self.shareqr = ImageTk.PhotoImage(resized)
                    self.shareqr_label = ttk.Label(self.shareframe, image=self.shareqr)
                    self.shareqr_label.pack(side='top')

                    # Start serving
                    self.send_to_terminal(f"Server attempt on address {host}:{current_port}", self.console_text)
                    try: 
                        httpd.serve_forever()
                    except:
                        self.send_to_terminal(f"Sent file at address {host}:{current_port}", self.console_text)
                        return
            except:
                continue
                    
        
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
        
        listbox.configure(state='normal')
            
        
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
            
            case"mp3":
                self.convertto.set('')
                self.conversionlabel.configure(text="Convert from MP3 to: ")
                self.convertto['values'] = ('wav','flac')
                self.startbutton.configure(state='normal')
                pass
            
            case"lac":
                self.convertto.set('')
                self.conversionlabel.configure(text="Convert from FLAC to: ")
                self.convertto['values'] = ('mp3','wav')
                self.startbutton.configure(state='normal')
                pass
            
            case"wav":
                self.convertto.set('')
                self.conversionlabel.configure(text="Convert from WAV to: ")
                self.convertto['values'] = ('mp3','flac')
                self.startbutton.configure(state='normal')
                pass
                
    
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
        self.startbutton.configure(state='disabled')
        
        pass         

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()