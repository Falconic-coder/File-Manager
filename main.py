import tkinter as tk
from tkinter import  ttk, messagebox
import os
import shutil
from send2trash import send2trash
import re


class Main:
    
    current_directory = f"C:\\\\Users"
    path = ""
    copied_from = None
    copy_to = None

    def __init__(self, master):
        self.master = master
        self.ribbon()
        self.entries()
        self.main()

    def ribbon(self):
        self.frame = tk.Frame(self.master, bg="lightgrey")

        copy_img = tk.PhotoImage(file="resized_images/copy.png")
        paste_img = tk.PhotoImage(file="resized_images/paste.png")
        new_folder_img = tk.PhotoImage(file="resized_images/add-folder.png")
        delete_img = tk.PhotoImage(file="resized_images/trash.png")
        lvlUp_Img = tk.PhotoImage(file="resized_images/lvl-up.png")

        self.copy_btn = tk.Button(self.frame, image=copy_img, text="Copy", compound="top", borderwidth=0, bg="lightgrey", command=self.on_click_copy_btn, state=tk.DISABLED)
        self.paste_btn = tk.Button(self.frame, image=paste_img, text="Paste", compound="top", borderwidth=0, bg="lightgrey", command=self.on_click_paste_btn, state=tk.DISABLED)
        self.new_folder_btn = tk.Button(self.frame, image=new_folder_img, text="New Folder", compound="top", borderwidth=0, bg="lightgrey", command=self.on_click_new_folder_btn)
        self.delete_btn = tk.Button(self.frame, image=delete_img, text="Delete", compound="top", borderwidth=0, bg="lightgrey", command=self.on_click_delete_btn, state=tk.DISABLED)
        self.one_up_btn = tk.Button(self.frame, image=lvlUp_Img, text="Up", compound="top", borderwidth=0, bg="lightgrey", command=self.one_lvl_up)

        self.copy_btn.image = copy_img
        self.paste_btn.image = paste_img
        self.new_folder_btn.image = new_folder_img
        self.delete_btn.image = delete_img
        self.one_up_btn.image = lvlUp_Img
        

        self.copy_btn.grid(row=0, column=1, padx=10, pady=5)
        self.paste_btn.grid(row=0, column=2, padx=10, pady=5)
        self.new_folder_btn.grid(row=0, column=3, padx=10, pady=5)
        self.delete_btn.grid(row=0, column=4, padx=10, pady=5)
        self.one_up_btn.grid(row=0, column=0, padx=10, pady=5)

        self.frame.pack(fill=tk.BOTH)

    def entries(self):
        self.frame_entries = tk.Frame(self.master)

        self.current_dir_ent = ttk.Combobox(self.frame_entries, width=108, values=["C:\\Users"])
        self.current_dir_ent.current(0)
        self.current_dir_ent.grid(row=0, column=0, padx=15)

        self.current_dir_ent.bind("<Return>", self.current_dir)

        self.frame_entries.pack(fill=tk.BOTH, pady=5)


    def current_dir(self, event):
        self.current_directory = self.current_dir_ent.get()
        self.path = self.current_directory
        self.main_frame.destroy()
        self.main()

    def main(self):
        self.main_frame = tk.Frame(self.master, bg="white")

        self.canvas = tk.Canvas(self.main_frame, height=800, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.second_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        self.main_frame.pack(fill=tk.BOTH, pady=10)
        
        self.check_path_and_create_directory()

    def check_path_and_create_directory(self):
        try:
            dir = os.listdir(self.current_directory)

        except PermissionError:
            self.new_folder_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
            self.copy_btn.config(state=tk.DISABLED)
            self.paste_btn.config(state=tk.DISABLED)
            messagebox.showerror("File Explorer", f"Access is denied.\nCannot open {self.current_directory}.")

        except FileNotFoundError:
            self.new_folder_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
            self.copy_btn.config(state=tk.DISABLED)
            self.paste_btn.config(state=tk.DISABLED)
            messagebox.showerror("File Explorer", f"Cannot find {self.current_directory}.\nCheck the spelling and try again.")

        else:
            if self.copy_to != None:
                self.copy_btn.config(state=tk.NORMAL)
                self.paste_btn.config(state=tk.NORMAL)
                
            if len(dir) == 0:
                self.empty_folder_lbl = tk.Label(self.second_frame, text="Empty Folder", font=("Helvatica", 10), bg="white", fg="grey")
                self.empty_folder_lbl.grid(row=0, column=0, padx=20, pady=10)
            else:
                folder_img = tk.PhotoImage(file="resized_images/folder.png")
                file_img = tk.PhotoImage(file="resized_images/file.png")

                self.buttons = []

                for i, dir in enumerate(dir):
                    self.btn = tk.Button(self.second_frame, text=f"  {dir}", compound="left", bg="white", width=650, borderwidth=0, anchor="w", command=lambda i=i: self.On_Click_Folder(i), activebackground="lightblue")
                    
                    if os.path.isfile(self.current_directory+"\\"+dir):
                        self.btn.config(image=file_img)
                        self.btn.image = file_img
                    else:
                        self.btn.config(image=folder_img)
                        self.btn.image = folder_img

                    self.btn.grid(row=i, column=0, padx=10)   
                    self.buttons.append(self.btn)

                self.new_folder_btn.config(state=tk.NORMAL)
                self.delete_btn.config(state=tk.NORMAL)

    def On_Click_Folder(self, i):

        path = self.current_directory+"\\"+self.buttons[i]["text"][2:]

        self.copy_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.NORMAL)
        if os.path.isfile(path):
            path = os.path.realpath(path)
            os.startfile(path)
            
        else:
            self.current_directory = path
            self.current_dir_ent.delete(0, tk.END)
            self.current_dir_ent.insert(0, self.current_directory)

            self.main_frame.destroy()
            self.main()
        self.path = path

    def on_click_copy_btn(self):
        self.copied_from = self.path
        self.paste_btn.config(state=tk.NORMAL)

    def on_click_paste_btn(self):
        self.copy_to = self.path

        if os.path.isfile(self.copied_from):
            shutil.copy2(self.copied_from, self.copy_to)

        else:
            shutil.copytree(self.copied_from, self.copy_to+"\\"+self.copied_from.split("\\")[-1]) 

        self.main_frame.destroy()
        self.main()

    def on_click_new_folder_btn(self):
        self.new_win = tk.Toplevel()
        self.new_win.title("New Folder")
        self.new_win.geometry("350x150")
        self.new_win.resizable(width=False, height=False)

        folder_img = tk.PhotoImage(file="resized_images/folder64.png")
        self.folder_img_lbl = tk.Label(self.new_win, image=folder_img)
        self.folder_img_lbl.image = folder_img
        self.folder_img_lbl.grid(row=0, column=0, pady=10, padx=10)

        self.folder_name_ent = ttk.Entry(self.new_win, width=38)
        self.folder_name_ent.insert(0, "New Folder")
        self.folder_name_ent.grid(row=0, column=1, pady=10, padx=10)

        self.create_btn = ttk.Button(self.new_win, text="Create", command=self.create_btn_clicked)
        self.cancel_btn = ttk.Button(self.new_win, text="Cancel", command=self.new_win.destroy)
        self.cancel_btn.grid(row=1, column=1, pady=10, padx=10, sticky="e")
        self.create_btn.grid(row=1, column=1, pady=10, padx=10, sticky="w")

    def create_btn_clicked(self):
        try:
            os.mkdir(self.current_directory+"\\"+self.folder_name_ent.get())

        except FileExistsError:
            messagebox.showerror("Error!", "Cannot create folder with that name.\nFolder already exists in the directory\nwith that name.")
        
        else:
            self.new_win.destroy()
            self.main_frame.destroy()
            self.main()

    def on_click_delete_btn(self):
        self.new_win = tk.Toplevel()
        self.new_win.title("Delete Directory")
        self.new_win.geometry("320x130")
        self.new_win.resizable(width=False, height=False)

        self.folder_name = self.path.split("\\")[-1]
        self.folder_name_lbl = ttk.Label(self.new_win, text=f"Are you sure to delete the selected folder? ", font=("Hevatica", 11), foreground="red")
        self.folder_name_lbl.grid(row=0, column=0, pady=10, padx=25)

        self.delete_permanently = ttk.Button(self.new_win, text="Delete Permanently", width=40, command=self.on_click_delete_permanently)
        self.move_to_trash = ttk.Button(self.new_win, text="Move to Recycle Bin", width=40, command=self.on_click_move_to_trash_btn)
        self.cancel_btn = ttk.Button(self.new_win, text="Cancel", width=40, command=self.new_win.destroy)

        self.cancel_btn.grid(row=3, column=0, padx=25)
        self.move_to_trash.grid(row=1, column=0, padx=25)
        self.delete_permanently.grid(row=2, column=0, padx=25)

    def on_click_move_to_trash_btn(self):
        send2trash(self.path)
        self.new_win.destroy()
        self.current_directory = self.current_directory.replace(f"\\{self.folder_name}", "")
        self.path = self.current_directory
        self.current_dir_ent.delete(0, tk.END)
        self.current_dir_ent.insert(0, self.path)
        self.main_frame.destroy()
        self.main()
    
    def on_click_delete_permanently(self):
        if os.path.isfile(self.path):
            os.remove(self.path)
        else:
            shutil.rmtree(self.path)
        
        self.new_win.destroy()
        self.current_directory = self.current_directory.replace(f"\\{self.folder_name}", "")
        self.path = self.current_directory
        self.main_frame.destroy()
        self.main()
        self.current_dir_ent.delete(0, tk.END)
        self.current_dir_ent.insert(0, self.path)


    def one_lvl_up(self):
        currPath = self.current_directory
        if(currPath == "C:\\"):
            return
        sliced = currPath.split("\\")
        removedElm = sliced.pop()
        if removedElm in currPath:
            newPath = currPath.replace(removedElm, "")[:-1]
            self.current_directory = newPath
            self.current_dir_ent.delete(0, tk.END)
            self.current_dir_ent.insert(0, newPath)
            self.main_frame.destroy()
            self.main()
            self.path = newPath


if __name__ == "__main__":
    win = tk.Tk()
    win.title("File Manager")
    win.geometry("700x600")
    win.resizable(width=False, height=False)
    Main(win)
    win.mainloop()
