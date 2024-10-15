#!/bin/python3
### This is a photo watermark maker

# $ pip install pillow
from PIL import Image, ImageDraw, ImageFont     # Pillow to handle immages
import tkinter as tk                            # tkinter for creating GUI (Graphical User Interface)
from tkinter import filedialog, messagebox
import os                                       # Managing file paths
from os import listdir
import glob                                     # getting images from folder

foldername = ""  # Initialize filename variable

# Select the folder you want
def select_folder():
    global foldername
    foldername = filedialog.askdirectory(title="Select the folder with the images")
    print(foldername)
    # check if the folder is selected
    if foldername:
        folder_select_btn.config(fg='green')
        folder_label.config(text=f"Folder: {foldername}")
    else:
        messagebox.showerror("Error","No folder selected!")
        folder_select_btn.config(fg='black')

# Function to add watermark
def water_mark():
    global foldername
    f = foldername.split('/')[-1]   # f is foldername without path
    print(f)

    # get all images (.jpeg, .jpg, .png) from the folder with glob and if no images error or listdir from os
    for images in os.listdir(foldername):
        if (images.endswith(".jpg") or images.endswith(".png")
            or images.endswith(".jpeg")):
            print(images)
            # check if image is found
            if not images:
                messagebox.showerror("Error", "Please upload an image")
                return
            try:
                text = water_text.get()
                main_image = Image.open(foldername+"/"+images).convert("RGBA")
            # give error if images can not be opened
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
                return
            
            # create watermark
            watermark = Image.new("RGBA", main_image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(watermark)

            # Calculate font size
            w, h = main_image.size
            font_size = int(min(w,h) / 8)
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
            folder_label.config(text="")
            submit_btn.config(fg='black')           

    # loop throug each image with image.open function and convert("RGBA")

    # create watermark
    
    #calculate font size

    # calculate position of watermark

    # Merge with original image

    # save the final watermarked images

    # clear input fields and reset labels and button colors

# UI Setup
main = tk.Tk()  # initialize main tkinter window
main.title('Watermark Your Image')

# Text Entry for Watermark
water_text = tk.Entry(fg="black", font=('Arial', 12, 'bold'))
folder_select_btn = tk.Button(text="Upload Image-Folder", font=('Arial', 12, 'bold'), command=select_folder)
submit_btn = tk.Button(text='Apply Watermark', font=('Arial', 12, 'bold'), command=water_mark)

# Label to display uploaded file name
folder_label = tk.Label(text="No file selected", fg='black', font=('Arial', 12, 'bold'))

# Layout
water_text.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
folder_select_btn.grid(row=1, column=1, pady=10, padx=10)
submit_btn.grid(row=1, column=2, pady=10, padx=10)
folder_label.grid(row=2, column=1, columnspan=2, pady=10)

# Run the application
main.mainloop()

