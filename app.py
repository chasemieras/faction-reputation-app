"""Brings in customtkinter for the program"""
import json
import customtkinter

customtkinter.set_appearance_mode("dark")


class GroupFrame(customtkinter.CTkFrame):
    """Creates a group to display on the screen"""

    def __init__(self, master, group_name, start_rep, rep_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.group_name = group_name
        self.rep_callback = rep_callback
        self.rep = start_rep

        # Row 0 - Label and value side-by-side, left-aligned
        self.label = customtkinter.CTkLabel(
            self, text=f"{self.group_name} Reputation:")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.rep_var = customtkinter.StringVar(value=str(self.rep))
        self.rep_display = customtkinter.CTkLabel(
            self, textvariable=self.rep_var)
        self.rep_display.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Row 1 - Entry on left, Submit on right
        self.entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter new rep (-1000 to 1000)", width=240)
        self.entry.bind("<Return>", self.submit_rep)
        self.entry.grid(row=1, column=0, columnspan=2,
                        padx=5, pady=5, sticky="w")

        self.submit_btn = customtkinter.CTkButton(
            self, text="Submit", width=80, command=self.submit_rep)
        self.submit_btn.grid(row=1, column=2, padx=5, pady=5, sticky="e")

        # Row 2 - Centered frame holding the 6 buttons
        self.button_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, columnspan=3, pady=5)

        # Place buttons inside the frame, tightly packed
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

    def submit_rep(self, event=None):
        """Adds the submitted reputation to the group"""
        try:
            value = int(self.entry.get())
            new_rep = self.rep + value
            # Clamp the value between -1000 and 1000
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
        self.groups = {}  # Store group reputations

        self.save_btn = customtkinter.CTkButton(
            self, text="Save", command=self.save_groups)
        self.save_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.load_bn = customtkinter.CTkButton(
            self, text="Load", command=self.load_groups)
        self.load_bn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.add_group_btn = customtkinter.CTkButton(
            self, text="Add Group", command=self.open_add_group_dialog)
        self.add_group_btn.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.groups_frame = customtkinter.CTkScrollableFrame(self)
        self.groups_frame.grid(row=2, column=0, columnspan=2,
                               padx=10, pady=10, sticky="nsew")

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def save_groups(self):
        data = {}
        counter = 0

        for group, reputation in self.groups.items():
            counter += 1
            group_key = f"group{counter}"
            data[group_key] = {
                "name": group,
                "rep": reputation
            }
            print(f"  {group}: {reputation}")

        file_path = "data.json"
        with open(file_path, 'w', encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        print("Outputted data to data.json")

    def load_groups(self):
        file_path = "data.json"
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
                for group_key, group_info in data.items():
                    name = group_info["name"]
                    rep = group_info["rep"]
                    print(f"{group_key} ({name}): {rep}")
                    self.add_group(name, rep)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            print(
                f"Error: Could not decode JSON from '{file_path}'. Check for valid JSON format.")

    def open_add_group_dialog(self):
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
        def rep_callback(group_name, new_rep):
            self.groups[group_name] = new_rep

        group_frame = GroupFrame(self.groups_frame, name, rep, rep_callback)
        group_frame.pack(padx=5, pady=5, fill="x")
        self.groups[name] = rep
        print("Current groups and reputations:")
        for group, reputation in self.groups.items():  # TODO use this to make the save function
            print(f"  {group}: {reputation}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
