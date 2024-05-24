from openai import OpenAI

client = OpenAI(api_key='OPENAI_API_KEY')

import ctypes

import customtkinter as ctk
import tkinter
import requests
from PIL import Image, ImageTk
from io import BytesIO
# Set the OpenAI API key


def generate_image(prompt):

  try:
    response = client.images.generate(prompt=prompt,     
    n=1,    
    size="512x512")
    image_url = response.data[0].url
    return image_url
  
  except Exception as e:
    print(f"Error generating image: {e}")
    return None

def generate_caption(image_description):

  messages = [
      {"role": "system", "content": "You are a creative assistant."},
      {"role": "user", "content": f"Generate a creative caption for an image described as follows: {image_description}"}
  ]


  try:

    response = client.chat.completions.create(model="gpt-4",  # Use GPT-4 model identifier
      
    messages=messages,
      
    max_tokens=50,
      
       temperature=1.0)


    caption = response.choices[0].message.content.strip()
    
    tkinter.messagebox.showinfo(title='Your caption', message=caption,)
    
    return caption


  except Exception as e:


    print(f"Error generating caption: {e}")


    return None

def generate():
  
  image_prompt = prompt_entry.get("0.0", tkinter.END)
  image_prompt += "in style: " + style_dropdown.get()
  image_url = generate_image(image_prompt)
  
  

  if image_url:

    print(f"Generated Image URL: {image_url}")

    image_description = image_prompt

    caption = generate_caption(image_description)

    if caption:

      print(f"Generated Caption: {caption}")
      response = requests.get(image_url) 
      img = Image.open(BytesIO(response.content))
      img = ImageTk.PhotoImage(img)
      canvas.image = img
      canvas.create_image(0,0, anchor ="nw", image=img)
      
      # img.show()

    else:
      print("Failed to generate image.")
      


root = ctk.CTk()
root.title("AI Image Generator")

ctk.set_appearance_mode("dark")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)


prompt_label = ctk.CTkLabel(input_frame, text="Prompt")
prompt_label.grid(row=0,column=0, padx=10, pady=10)
prompt_entry = ctk.CTkTextbox(input_frame, height=10)
prompt_entry.grid(row=0,column=1, padx=10, pady=10)

style_label = ctk.CTkLabel(input_frame, text="Style")
style_label.grid(row=1,column=0, padx=10, pady=10)
style_dropdown = ctk.CTkComboBox(input_frame, values=["Realistic", "Cartoon", "3D Illustration", "Flat Art"])
style_dropdown.grid(row=1, column=1, padx=10, pady=10)


generate_button = ctk.CTkButton(input_frame, text="Generate", command=generate)
generate_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=10)

canvas = tkinter.Canvas(root, width=512, height=512)
canvas.pack(side="left")

root.mainloop()
  

      
  

