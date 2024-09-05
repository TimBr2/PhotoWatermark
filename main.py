### This is a photo watermark maker

# $ pip install pillow
from PIL import Image, ImageDraw, ImageFont     # Pillow to handle immages
import tkinter as tk                            # tkinter for creating GUI (Graphical User Interface)
from tkinter import filedialog, messagebox
import os                                       # Managing file paths

filename = ""  # Initialize filename variable

# Function to upload the image file, triggered when user clicks "Upload Image"
def upload_file():
    global filename
    filename = filedialog.askopenfilename(title="Select Your Image")    # opens file dialog to select image file
    # Check if file is selected and change text in green, otherwise show error message
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
    f = filename.split('/')[-1]     # f is the filename without the entire path
    
    # check if file is uploaded, exits with return
    if not filename:
        messagebox.showerror("Error", "Please upload an image first!")
        return
    
    try:
        text = water_text.get()     # get the entered text by user from the water_text entry field
        main_image = Image.open(filename).convert("RGBA")   # Open image file and convert to RGBA (allows handling transparency)
    # give error message when image cannot be opened
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image: {e}")
        return

    # Create watermark
    watermark = Image.new("RGBA", main_image.size, (255, 255, 255, 0))  # Creates transparant image, same size as original, RGBA collor with ending 0 means full transparency
    draw = ImageDraw.Draw(watermark)    # Creates object to draw on the watermark image

    # Calculate font size
    w, h = main_image.size  # width and height of original image
    font_size = int(min(w, h) / 8)  # The watermark is 1/6 proportion to the image size
    try:
        font_path = os.path.join("/mnt/c/Windows/Fonts/arialbd.ttf")  # Path to image font, Adjust path if on a different OS
        font = ImageFont.truetype(font_path, font_size)     # loads the font
    # give error when font file is not found
    except IOError:
        messagebox.showerror("Error", "Font not found. Make sure font is available.")
        return

    # Calculate position for watermark
    text_bbox = draw.textbbox((0, 0), text, font)   #box of the watermark with text and font
    text_w = text_bbox[2] - text_bbox[0]    # width of watermark text
    text_h = text_bbox[3] - text_bbox[1]    # height of watermark text
    pos = (w - text_w - 10, h - text_h - 10)    # position where the watermark is drawn: bottom right, 10-pixel

    # Draw the watermark
    draw.text(pos, text, font=font, fill=(255, 255, 255, 128))  # 128 is semi-transparant watermark

    # Merge the watermark with the original image
    final_image = Image.alpha_composite(main_image, watermark)

    # Save the final image
    new_filename = f'watermarked_image_{f}.png'
    final_image.save(new_filename)
    final_image.show()

    # Clear the input fields + resets labels and button color
    water_text.delete(0, tk.END)
    uploaded_file_name.config(text="")
    file_upload_btn.config(fg='black')

# UI Setup
main = tk.Tk()  # initialize main tkinter window
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

