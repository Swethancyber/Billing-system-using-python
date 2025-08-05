import tkinter as tk
from tkinter import messagebox, filedialog
import random
import os
import platform
import subprocess
from datetime import datetime  # Import for date/time handling

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AMBADI ENTERPRISES")
        self.root.geometry("1350x700+0+0")
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.bill_number = tk.StringVar(value=str(random.randint(1000, 9999)))
        self.search_bill = tk.StringVar()
        self.current_date_time = tk.StringVar()  # For displaying date/time

        # Product items with prices
        self.grocery_items = {
            "Rice": [tk.IntVar(), 50],
            "Wheat": [tk.IntVar(), 30],
            "Oil": [tk.IntVar(), 120],
            "Sugar": [tk.IntVar(), 40],
        }
        
        self.medical_items = {
            "Sanitizer": [tk.IntVar(), 60],
            "Mask (Pack)": [tk.IntVar(), 100],
            "Dettol": [tk.IntVar(), 80],
            "Paracetamol": [tk.IntVar(), 20],
        }
        
        self.electronics = {
            "USB Cable": [tk.IntVar(), 150],
            "Mouse": [tk.IntVar(), 300],
            "Keyboard": [tk.IntVar(), 500],
            "Headphones": [tk.IntVar(), 800],
        }

        # Total and tax variables
        self.total_vars = {
            "grocery": tk.StringVar(),
            "medical": tk.StringVar(),
            "electronics": tk.StringVar(),
        }

        self.tax_vars = {
            "grocery": tk.StringVar(),
            "medical": tk.StringVar(),
            "electronics": tk.StringVar(),
        }

        self.setup_ui()
        self.welcome_message()

    def setup_ui(self):
        # Header Frame
        header = tk.Frame(self.root, bd=10, relief=tk.GROOVE, bg="#4CAF50")
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="swethan billing system",
            font=("Helvetica", 24, "bold"),
            bg="#4CAF50",
            fg="white"
        ).pack()

        # Customer Details Frame
        customer_frame = tk.LabelFrame(
            self.root,
            text="Customer Details",
            font=("Arial", 12, "bold"),
            bd=10,
            bg="#f0f0f0"
        )
        customer_frame.pack(fill=tk.X, padx=10, pady=5)

        # Customer name
        tk.Label(customer_frame, text="Name", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5)
        tk.Entry(customer_frame, textvariable=self.customer_name, font=("Arial", 12), bd=5, relief=tk.GROOVE).grid(row=0, column=1, padx=5)

        # Phone number
        tk.Label(customer_frame, text="Phone", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=2, padx=5)
        tk.Entry(customer_frame, textvariable=self.customer_phone, font=("Arial", 12), bd=5, relief=tk.GROOVE).grid(row=0, column=3, padx=5)

        # Bill number (readonly)
        tk.Label(customer_frame, text="Bill No.", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=4, padx=5)
        tk.Entry(customer_frame, textvariable=self.bill_number, font=("Arial", 12), bd=5, relief=tk.GROOVE, state="readonly").grid(row=0, column=5, padx=5)

        # Date and Time (readonly)
        tk.Label(customer_frame, text="Date/Time", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=6, padx=5)
        tk.Entry(customer_frame, textvariable=self.current_date_time, font=("Arial", 12), bd=5, relief=tk.GROOVE, state="readonly").grid(row=0, column=7, padx=5)

        # Product Frames
        product_frames = tk.Frame(self.root)
        product_frames.pack(fill=tk.X, padx=10)

        # Function to create product sections
        def create_product_section(frame, title, items_dict):
            frame_inner = tk.LabelFrame(frame, text=title, font=("Arial", 12, "bold"), bd=5, bg="#f0f0f0")
            frame_inner.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

            row_num = 0
            for item, data in items_dict.items():
                tk.Label(frame_inner, text=item, font=("Arial", 11), bg="#f0f0f0").grid(row=row_num, column=0, padx=5, pady=5, sticky="w")
                tk.Entry(frame_inner, textvariable=data[0], font=("Arial", 11), width=8, bd=3, relief=tk.GROOVE).grid(row=row_num, column=1, padx=5, pady=5)
                tk.Label(frame_inner, text=f"₹{data[1]}", font=("Arial", 11), bg="#f0f0f0").grid(row=row_num, column=2, padx=5, pady=5)
                row_num += 1

        create_product_section(product_frames, "Grocery", self.grocery_items)
        create_product_section(product_frames, "Medical", self.medical_items)
        create_product_section(product_frames, "Electronics", self.electronics)

        # Bill Area Frame
        bill_frame = tk.Frame(self.root, bd=10, relief=tk.GROOVE)
        bill_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(bill_frame, text="Bill Area", font=("Arial", 14, "bold"), bd=7, relief=tk.GROOVE).pack(fill=tk.X)
        
        self.bill_text = tk.Text(bill_frame, height=15, font=("Courier", 12), bd=5, relief=tk.GROOVE)
        scroll_y = tk.Scrollbar(bill_frame, orient=tk.VERTICAL, command=self.bill_text.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.bill_text.pack(fill=tk.BOTH, expand=True)
        self.bill_text.configure(yscrollcommand=scroll_y.set)

        # Total & Tax Frame
        total_frame = tk.LabelFrame(self.root, text="Totals & Tax", font=("Arial", 12, "bold"), bd=10, bg="#f0f0f0")
        total_frame.pack(fill=tk.X, padx=10, pady=5)

        # Total Labels
        for i, (category, var) in enumerate(self.total_vars.items()):
            tk.Label(total_frame, text=f"Total {category.capitalize()}", font=("Arial", 11, "bold"), bg="#f0f0f0").grid(row=0, column=i*2, padx=5, pady=5)
            tk.Entry(total_frame, textvariable=var, font=("Arial", 11), width=10, state="readonly", bd=3, relief=tk.GROOVE).grid(row=0, column=i*2+1, padx=5, pady=5)

        # Tax Labels
        for i, (category, var) in enumerate(self.tax_vars.items()):
            tk.Label(total_frame, text=f"Tax {category.capitalize()} (5%)", font=("Arial", 11, "bold"), bg="#f0f0f0").grid(row=1, column=i*2, padx=5, pady=5)
            tk.Entry(total_frame, textvariable=var, font=("Arial", 11), width=10, state="readonly", bd=3, relief=tk.GROOVE).grid(row=1, column=i*2+1, padx=5, pady=5)

        # Action Buttons Frame
        button_frame = tk.Frame(self.root, bd=10, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Button Definitions
        buttons = [
            ("Generate Bill", "#4CAF50", self.generate_bill),
            ("Save Bill", "#2196F3", self.save_bill),
            ("Clear All", "#FF9800", self.clear_data),
            ("Exit", "#F44336", self.exit_app)
        ]

        for i, (text, color, command) in enumerate(buttons):
            tk.Button(
                button_frame, 
                text=text, 
                font=("Arial", 12, "bold"), 
                bg=color, 
                fg="white",
                bd=5, 
                width=12, 
                command=command
            ).grid(row=0, column=i, padx=5)

        # Update date/time display
        self.update_datetime()

    def update_datetime(self):
        """Update the current date and time display"""
        now = datetime.now()
        self.current_date_time.set(now.strftime("%Y-%m-%d %H:%M:%S"))
        # Update every second
        self.root.after(1000, self.update_datetime)

    def calculate_totals(self):
        totals = {"grocery": 0, "medical": 0, "electronics": 0}
        
        # Calculate Grocery Total
        for item, (qty, price) in self.grocery_items.items():
            totals["grocery"] += qty.get() * price
        
        # Calculate Medical Total
        for item, (qty, price) in self.medical_items.items():
            totals["medical"] += qty.get() * price

        # Calculate Electronics Total
        for item, (qty, price) in self.electronics.items():
            totals["electronics"] += qty.get() * price

        return totals

    def generate_bill(self):
        if not self.customer_name.get() or not self.customer_phone.get():
            messagebox.showerror("Error", "Customer Name & Phone are required!")
            return

        totals = self.calculate_totals()
        self.bill_text.delete(1.0, tk.END)
        
        # Format totals and taxes
        self.total_vars["grocery"].set(f"₹{totals['grocery']}")
        self.tax_vars["grocery"].set(f"₹{totals['grocery'] * 0.05:.2f}")
        self.total_vars["medical"].set(f"₹{totals['medical']}")
        self.tax_vars["medical"].set(f"₹{totals['medical'] * 0.05:.2f}")
        self.total_vars["electronics"].set(f"₹{totals['electronics']}")
        self.tax_vars["electronics"].set(f"₹{totals['electronics'] * 0.05:.2f}")

        # Get current date and time
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

        # Generate bill text with date/time
        bill_text = [
            "\t\tSuperMart Billing System\n",
            "\n=====================================",
            f"\nBill No: {self.bill_number.get()}",
            f"Date/Time: {date_time_str}",
            f"\nCustomer Name: {self.customer_name.get()}",
            f"\nPhone: {self.customer_phone.get()}",
            "\n=====================================",
            "\nProduct\t\tQty\tPrice\tTotal",
            "\n====================================="
        ]

        # Add grocery items
        for item, (qty, price) in self.grocery_items.items():
            if qty.get() > 0:
                bill_text.append(f"\n{item[:15]}\t\t{qty.get()}\t₹{price}\t₹{qty.get() * price}")

        # Add medical items
        for item, (qty, price) in self.medical_items.items():
            if qty.get() > 0:
                bill_text.append(f"\n{item[:15]}\t\t{qty.get()}\t₹{price}\t₹{qty.get() * price}")

        # Add electronics
        for item, (qty, price) in self.electronics.items():
            if qty.get() > 0:
                bill_text.append(f"\n{item[:15]}\t\t{qty.get()}\t₹{price}\t₹{qty.get() * price}")

        bill_text.extend([
            "\n=====================================",
            f"\nSubtotal Grocery: ₹{totals['grocery']} (Tax: ₹{totals['grocery'] * 0.05:.2f})",
            f"\nSubtotal Medical: ₹{totals['medical']} (Tax: ₹{totals['medical'] * 0.05:.2f})",
            f"\nSubtotal Electronics: ₹{totals['electronics']} (Tax: ₹{totals['electronics'] * 0.05:.2f})",
            "\n=====================================",
            f"\nGrand Total: ₹{(totals['grocery'] + totals['medical'] + totals['electronics'] + (totals['grocery'] * 0.05) + (totals['medical'] * 0.05) + (totals['electronics'] * 0.05)):.2f}",
            "\n=====================================",
            "\nThank you for shopping with us!"
        ])

        self.bill_text.insert(tk.END, "\n".join(bill_text))

        # Highlight important sections
        self.bill_text.tag_add("title", "1.0", "1.end")
        self.bill_text.tag_config("title", font=("Courier", 12, "bold"))
        
        self.bill_text.tag_add("total", f"{self.bill_text.get('1.0', tk.END).count('\n')-3}.0", "end")
        self.bill_text.tag_config("total", foreground="blue")

    def save_bill(self):
        if not self.customer_name.get() or not self.customer_phone.get():
            messagebox.showerror("Error", "Customer name and phone are required!")
            return
            
        bill_data = self.bill_text.get(1.0, tk.END)
        if not bill_data.strip():
            messagebox.showerror("Error", "No bill to save!")
            return

        # Prompt user for file path with initial filename suggestion
        initial_file = f"bill_{self.bill_number.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile=initial_file,
            title="Save Bill As"
        )

        if file_path:  # If user didn't cancel the dialog
            try:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Save the file with UTF-8 encoding
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(bill_data)
                
                # Show success message with saved path
                messagebox.showinfo("Success", f"Bill saved successfully at:\n{file_path}")
                
                # Option to open the saved file
                if messagebox.askyesno("Open File", "Would you like to open the saved bill?"):
                    self.open_file(file_path)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save bill:\n{str(e)}")

    def open_file(self, path):
        """Platform-independent file opener"""
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", path])
            else:
                subprocess.call(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't open file: {str(e)}")

    def clear_data(self):
        # Clear customer details
        self.customer_name.set("")
        self.customer_phone.set("")
        
        # Clear product quantities
        for items_dict in [self.grocery_items, self.medical_items, self.electronics]:
            for item, (qty, price) in items_dict.items():
                qty.set(0)
        
        # Clear totals and taxes
        for var in self.total_vars.values():
            var.set("")
        
        for var in self.tax_vars.values():
            var.set("")
        
        # Generate new bill number
        self.bill_number.set(str(random.randint(1000, 9999)))
        
        # Show welcome message
        self.welcome_message()

    def welcome_message(self):
        self.bill_text.delete(1.0, tk.END)
        welcome_text = [
            "\tWelcome to SuperMart Billing System\n",
            "\n1. Enter customer details",
            "2. Select product quantities",
            "3. Click 'Generate Bill'",
            "\nButtons Guide:",
            "- Generate Bill: Create your bill",
            "- Save Bill: Save to any location",
            "- Clear All: Reset entire form",
            "- Exit: Close application",
            "\nCurrent Date/Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        self.bill_text.insert(tk.END, "\n".join(welcome_text))

        # Format the welcome text
        self.bill_text.tag_add("welcome", "1.0", "1.end")
        self.bill_text.tag_config("welcome", font=("Courier", 12, "bold"))
        
        self.bill_text.tag_add("datetime", tk.END + "-2l", tk.END)
        self.bill_text.tag_config("datetime", foreground="blue")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()

    root.iconbitmap("D:\ANIME\logo for software.jpg")
    
    # Improve window scaling on Windows
    if platform.system() == "Windows":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    
    app = BillingApp(root)
    root.mainloop()
