import customtkinter as ctk
from tkinter import messagebox
from tkinter import font
from Query import send_query

# Color palette from the mockup
COLOR_BLACK = "#1B1C22"
COLOR_DARK_GREY = "#2D3036"
COLOR_LIGHT_GREY = "#3A3E49"
COLOR_DARK_WHITE = "#A5ADB6"
COLOR_OFF_WHITE = "#F4F5F6"
COLOR_RED = "#D24235"

# Set message limit
input_limit = 500

# Initialize main application window
app = ctk.CTk()
app.geometry("700x700")
app.minsize(700, 700)
app.title("FlashForge")
app.configure(fg_color=COLOR_BLACK)

# Load custom font
font_reg = ctk.CTkFont(
    family="Space Grotesk", 
    weight="normal", 
    size=16
)
font_bold = ctk.CTkFont(
    family="Space Grotesk", 
    weight="bold", 
    size=16
)

# Chatbox window (output display)
chatbox = ctk.CTkTextbox(
    app, 
    width=700, 
    corner_radius=25, 
    wrap="word", 
    font=font_bold, 
    text_color=COLOR_OFF_WHITE, 
    fg_color="transparent"
)
chatbox.pack(
    fill="y", 
    expand=True
)
chatbox.configure(state="disabled")

# Divider between chatbox and user input
divider = ctk.CTkFrame(
    app, 
    width=600, 
    height=2, 
    fg_color=COLOR_DARK_GREY
)
divider.pack()

# Character limit indicator
char_limit_label = ctk.CTkLabel(
    app, 
    text=f"0 / {input_limit}", 
    font=font_reg, 
    text_color=COLOR_BLACK, 
    bg_color="transparent", 
    anchor="center"
)
char_limit_label.pack(
    fill="x", 
    padx=25, 
    pady=5
)

# User input textbox (for entering messages)
user_input_frame = ctk.CTkFrame(
    app, 
    width=650, 
    corner_radius=25, 
    fg_color=COLOR_DARK_GREY
)
user_input_frame.pack(
    pady=(0, 25)
)
user_input = ctk.CTkTextbox(
    user_input_frame, 
    width=530, 
    height=150, 
    corner_radius=25, 
    fg_color="transparent", 
    wrap="word", 
    font=font_reg, 
    text_color=COLOR_OFF_WHITE
)
user_input.grid(
    row=0, 
    column=0, 
    padx=25, 
    pady=0, 
    sticky="nwse" 
)
user_input_frame.columnconfigure(
    0, 
    weight=1
)

# Send button (arrow icon)
send_button = ctk.CTkButton(
    user_input_frame, 
    width=40, 
    height=40, 
    corner_radius=10, 
    fg_color=COLOR_OFF_WHITE, 
    text="⮝", 
    font=font_bold, 
    text_color=COLOR_BLACK
)
send_button.grid(
    row=0, 
    column=1, 
    padx=(15, 15), 
    pady=(15, 0), 
    sticky="ne"
)
send_button.columnconfigure(
    1, 
    weight=0
)

# Function to handle gradual color transition
def gradual_color_transition(widget, start_color, end_color, steps=50, interval=1):
    start_rgb = widget.winfo_rgb(start_color)
    end_rgb = widget.winfo_rgb(end_color)
    delta_rgb = [(end - start) / steps for start, end in zip(start_rgb, end_rgb)]

    def update_color(step=0):
        if step <= steps:
            new_color = "#%04x%04x%04x" % tuple(int(start + delta * step) for start, delta in zip(start_rgb, delta_rgb))

            widget.configure(
                fg_color=new_color
            )
            widget.after(
                interval, 
                update_color, 
                step + 1
            )

    update_color()

# Function to get the current color of the widget
def get_current_color(widget):
    return widget.cget("fg_color")

# Bind the gradual color transition to the hover event
send_button.bind(
    "<Enter>", 
    lambda e: gradual_color_transition(send_button, get_current_color(send_button), 
    COLOR_DARK_WHITE)
)
send_button.bind(
    "<Leave>", 
    lambda e: gradual_color_transition(send_button, get_current_color(send_button), 
    COLOR_OFF_WHITE)
)

# Function to update character limit indicator
def update_char_limit(event):
    current_length = len(user_input.get("1.0", "end").strip())
    percentage = current_length / input_limit

    # Calculate the new color based on the percentage
    start_rgb = app.winfo_rgb(COLOR_BLACK)
    end_rgb = app.winfo_rgb(COLOR_OFF_WHITE)
    new_rgb = tuple(int(start + (end - start) * percentage) for start, end in zip(start_rgb, end_rgb))
    new_color = "#%04x%04x%04x" % new_rgb

    if current_length > input_limit:
        char_limit_label.configure(
            text=f"{current_length} / {input_limit}", 
            text_color=COLOR_RED
        )

    else:
        char_limit_label.configure(
            text=f"{current_length} / {input_limit}", 
            text_color=new_color
        )

# Bind the update_char_limit function to the user input textbox
user_input.bind(
    "<KeyRelease>", 
    update_char_limit
)

# Function to handle sending a message
def send_message():
    message = user_input.get("1.0", "end").strip()
    
    if len(message) > 0:
        if len(message) <= input_limit:
            # Display the user message in the chatbox
            chatbox.configure(
                state="normal"
            )
            chatbox.insert(
                "end", 
                f"User:\n{message}\n\n"
            )
            chatbox.configure(
                state="disabled"
            )
            user_input.delete(
                "1.0", 
                "end"
            )
            char_limit_label.configure(
                text=f"0 / {input_limit}", 
                text_color=COLOR_BLACK
            )

            # Query the AI model and display the response
            response = send_query(message)
            chatbox.configure(
                state="normal"
            )
            chatbox.insert(
                "end", 
                f"FlashForge AI:\n{response}\n\n"
            )
            chatbox.configure(
                state="disabled"
            )
        else:
            messagebox.showwarning(
                "Warning", 
                f"Message exceeds {input_limit} character limit."
            )
    else:
        messagebox.showwarning(
            "Warning", 
            "Message cannot be empty."
        )

send_button.configure(
    command=send_message
)

app.mainloop()