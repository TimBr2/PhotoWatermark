### This is a photo watermark maker

# $ pip install pillow
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox
import os

filename = ""  # Initialize filename variable

# Function to upload the image file
def upload_file():
    global filename
    filename = filedialog.askopenfilename(title="Select Your Image")
    if filename:
        file_upload_btn.config(fg='green')
        f = filename.split('/')[-1]
        uploaded_file_name.config(text=f"File Name: {f}")
        
    else:
        messagebox.showerror("Error", "No file selected!")
        file_upload_btn.config(fg='black')

# Function to add watermark
def water_mark():
    global filename
    f = filename.split('/')[-1]
    if not filename:
        messagebox.showerror("Error", "Please upload an image first!")
        return

    try:
        text = water_text.get()
        main_image = Image.open(filename).convert("RGBA")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image: {e}")
        return

    # Create watermark
    watermark = Image.new("RGBA", main_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark)

    # Calculate font size
    w, h = main_image.size
    font_size = int(min(w, h) / 6)
    try:
        font_path = os.path.join("/mnt/c/Windows/Fonts/arialbd.ttf")  # Adjust path if on a different OS
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        messagebox.showerror("Error", "Font not found. Make sure font is available.")
        return

    # Calculate position for watermark
    text_bbox = draw.textbbox((0, 0), text, font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    pos = (w - text_w - 10, h - text_h - 10)

    # Draw the watermark
    draw.text(pos, text, font=font, fill=(255, 255, 255, 128))

    # Merge the watermark with the original image
    final_image = Image.alpha_composite(main_image, watermark)

    # Save the final image
    new_filename = f'watermarked_image_{f}.png'
    final_image.save(new_filename)
    final_image.show()

    # Clear the input fields
    water_text.delete(0, tk.END)
    uploaded_file_name.config(text="")
    file_upload_btn.config(fg='black')

# UI Setup
main = tk.Tk()
main.title('Watermark Your Image')

# Text Entry for Watermark
water_text = tk.Entry(fg="black", font=('Arial', 12, 'bold'))
file_upload_btn = tk.Button(text="Upload Image", font=('Arial', 12, 'bold'), command=upload_file)
submit_btn = tk.Button(text='Apply Watermark', font=('Arial', 12, 'bold'), command=water_mark)

# Label to display uploaded file name
uploaded_file_name = tk.Label(text="No file selected", fg='black', font=('Arial', 12, 'bold'))

# Layout
water_text.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
file_upload_btn.grid(row=1, column=1, pady=10, padx=10)
submit_btn.grid(row=1, column=2, pady=10, padx=10)
uploaded_file_name.grid(row=2, column=1, columnspan=2, pady=10)

# Run the application
main.mainloop()

