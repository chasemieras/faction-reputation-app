"""Brings in customtkinter for the program"""
import json
from tkinter import filedialog
import customtkinter

customtkinter.set_appearance_mode("dark")


class GroupFrame(customtkinter.CTkFrame):
    """Creates a group to display on the screen"""

    def __init__(self, master, group_name, start_rep, rep_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.group_name = group_name
        self.rep_callback = rep_callback
        self.rep = start_rep

        self.label = customtkinter.CTkLabel(
            self, text=f"{self.group_name} Reputation:")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.rep_var = customtkinter.StringVar(value=str(self.rep))
        self.rep_display = customtkinter.CTkLabel(
            self, textvariable=self.rep_var)
        self.rep_display.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter new rep (-1000 to 1000)", width=240)
        self.entry.bind("<Return>", self.submit_rep)
        self.entry.grid(row=1, column=0, columnspan=2,
                        padx=5, pady=5, sticky="w")

        self.submit_btn = customtkinter.CTkButton(
            self, text="Submit", width=80, command=self.submit_rep)
        self.submit_btn.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.delete_btn = customtkinter.CTkButton(
            self, text="Remove", width=80, command=self.delete_group)
        self.delete_btn.grid(row=1, column=3, padx=5, pady=5, sticky="e")

        self.button_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=5)

        buttons = [
            ("-10", -10),
            ("-5", -5),
            ("-1", -1),
            ("+1", 1),
            ("+5", 5),
            ("+10", 10),
        ]

        for i, (text, val) in enumerate(buttons):
            btn = customtkinter.CTkButton(
                self.button_frame, text=text, width=30, command=lambda v=val: self.add_to_rep(v)
            )
            btn.grid(row=0, column=i, padx=2)

    def delete_group(self):
        """Removes the group"""
        self.destroy()

    def submit_rep(self, event=None):
        """Adds the submitted reputation to the group"""
        try:
            value = int(self.entry.get())
            new_rep = self.rep + value
            if new_rep > 1000:
                new_rep = 1000
            elif new_rep < -1000:
                new_rep = -1000
            self.rep = new_rep
            self.rep_var.set(str(self.rep))
            self.rep_callback(self.group_name, self.rep)
        except ValueError:
            self.entry.configure(placeholder_text="Enter a valid integer")

    def add_to_rep(self, to_add):
        """Adds a basic number to the rep"""
        self.rep = self.rep + to_add
        self.rep_var.set(str(self.rep))
        self.rep_callback(self.group_name, self.rep)


class App(customtkinter.CTk):
    """Main program"""

    def __init__(self):
        super().__init__()
        self.title("Faction Reputation App")
        self.geometry("500x400")
        self.groups = {}
        self.file_name = "data"

        self.file_name_entry = customtkinter.CTkEntry(
            self, placeholder_text="Change default file name (data)", width=240)
        self.file_name_entry.bind("<Return>", self.submit_file_name)
        self.file_name_entry.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.file_name_entry_btn = customtkinter.CTkButton(
            self, text="Save File Name", command=self.submit_file_name)
        self.file_name_entry_btn.grid(
            row=0, column=1, padx=5, pady=5, sticky="ew")
        self.open_file_btn = customtkinter.CTkButton(
            self, text="Open File", command=self.open_file)
        self.open_file_btn.grid(
            row=0, column=2, padx=5, pady=5, sticky="ew")

        self.save_btn = customtkinter.CTkButton(
            self, text="Save", command=self.save_groups)
        self.save_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.load_bn = customtkinter.CTkButton(
            self, text="Load", command=self.load_groups_from_default)
        self.load_bn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.add_group_btn = customtkinter.CTkButton(
            self, text="Add Group", command=self.open_add_group_dialog)
        self.add_group_btn.grid(
            row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.groups_frame = customtkinter.CTkScrollableFrame(self)
        self.groups_frame.grid(row=3, column=0, columnspan=3,
                               padx=10, pady=10, sticky="nsew")

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.notification_label = customtkinter.CTkLabel(
            self, text="", fg_color="gray20")
        self.notification_label.grid(
            row=4, column=0, columnspan=3, sticky="ew", padx=0, pady=(0, 2))
        self.notification_label.configure(wraplength=400)
        self.notification_label.grid_remove()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

    def open_file(self):
        """Opens a specific file then loads the data"""
        filename = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("JSON files", "*.json")]
        )

        if filename:
            with open(filename, 'r', encoding="utf-8") as file:
                data = json.load(file)
                self.load_groups(data)
                msg = f"Loaded data from file: {filename}"
                print(msg)
                self.show_notification(msg)

    def submit_file_name(self):
        """Changes where the data will be saved to"""
        new_name = self.file_name_entry.get()
        if len(new_name) == 0:
            msg = "Please enter text to change the file name"
        else:
            self.file_name = new_name
            msg = f"File name changed to {self.file_name}"
        print(msg)
        self.show_notification(msg)

    def show_notification(self, message):
        """Show a notification at the bottom for 5 seconds"""
        self.notification_label.configure(text=message)
        self.notification_label.grid()
        self.after(5000, self.notification_label.grid_remove)

    def save_groups(self):
        """Saves the groups to a json file"""
        data = {}
        counter = 0

        if len(self.groups) == 0:
            msg = "There are no groups to output"
            print(msg)
            self.show_notification(msg)
        else:
            file_path = f"{self.file_name}.json"
            for group, reputation in self.groups.items():
                counter += 1
                group_key = f"group{counter}"
                data[group_key] = {
                    "name": group,
                    "rep": reputation
                }
                print(f"  {group}: {reputation}")

            with open(file_path, 'w', encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4)
            msg = f"Outputted data to {file_path}"
            print(msg)
            self.show_notification(msg)

    def load_groups_from_default(self):
        """Loads the groups from a json file"""
        file_path = f"{self.file_name}.json"
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            self.load_groups(data)

    def load_groups(self, data):
        """Loads the groups from a json file"""
        for group_key, group_info in data.items():
            name = group_info["name"]
            rep = group_info["rep"]
            print(f"{group_key} ({name}): {rep}")
            self.add_group(name, rep)

    def open_add_group_dialog(self):
        """Opens a popup to add a new group"""
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Add Group")
        dialog.geometry("300x240")
        dialog.wait_visibility()
        dialog.grab_set()

        def submit(event=None):
            name = name_entry.get().strip()
            try:
                rep = int(rep_entry.get())
            except ValueError:
                rep_entry.delete(0, "end")
                rep_entry.insert(0, "0")
                return
            if not name:
                name_entry.configure(placeholder_text="Enter a name")
                return
            if not -1000 <= rep <= 1000:
                rep_entry.delete(0, "end")
                rep_entry.insert(0, "0")
                return
            if name in self.groups:
                name_entry.delete(0, "end")
                name_entry.configure(placeholder_text="Name exists")
                return
            self.add_group(name, rep)
            dialog.destroy()

        name_label = customtkinter.CTkLabel(dialog, text="Group Name:")
        name_label.pack(pady=(10, 0))
        name_entry = customtkinter.CTkEntry(dialog)
        name_entry.pack(pady=5, fill="x", padx=10)
        name_entry.bind("<Return>", submit)

        rep_label = customtkinter.CTkLabel(
            dialog, text="Start Reputation (-1000 to 1000):")
        rep_label.pack(pady=(10, 0))
        rep_entry = customtkinter.CTkEntry(dialog)
        rep_entry.insert(0, "0")
        rep_entry.pack(pady=5, fill="x", padx=10)

        submit_btn = customtkinter.CTkButton(
            dialog, text="Add", command=submit)
        submit_btn.pack()

    def add_group(self, name, rep):
        """Adds the group to the group frame"""
        def rep_callback(group_name, new_rep):
            self.groups[group_name] = new_rep

        group_frame = GroupFrame(self.groups_frame, name, rep, rep_callback)
        group_frame.pack(padx=5, pady=5, fill="x")
        self.groups[name] = rep
        print("Current groups and reputations:")
        for group, reputation in self.groups.items():
            print(f"  {group}: {reputation}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
