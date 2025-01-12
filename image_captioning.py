import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer

class ImageCaptioningAI:
    """
    A user-friendly application for generating captions from images.

    This application utilizes a pre-trained Vision Encoder-Decoder model 
    (specifically, ViT-GPT2) to analyze images and produce human-readable descriptions.
    """

    def __init__(self, master):
        """
        Initializes the graphical user interface (GUI) and loads the necessary models.

        Args:
            master: The root tkinter window for the application.
        """
        self.master = master
        self.master.title("Image Captioning AI")
        self.master.geometry("800x600")
        self.master.configure(bg="#f0f0f0")  # Soft gray background

        # Load pre-trained models for image understanding and caption generation
        self.feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

        # Construct the user interface
        self._create_gui()

    def _create_gui(self):
        """
        Builds the graphical user interface with intuitive layout and visual elements.
        """
        # Main container for better organization
        main_frame = tk.Frame(self.master, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Area for displaying the selected image
        self.image_frame = tk.Frame(main_frame, width=400, height=400, bg="#e0e0e0")
        self.image_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Label to hold the displayed image
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # Section for user controls and caption output
        self.control_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.control_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Button to allow users to select an image
        self.load_button = tk.Button(
            self.control_frame, 
            text="Choose Image", 
            command=self._load_image, 
            bg="#4CAF50", 
            fg="white",
            width=20 
        )
        self.load_button.pack(pady=5)

        # Button to trigger the caption generation process
        self.caption_button = tk.Button(
            self.control_frame, 
            text="Generate Caption", 
            command=self._generate_caption, 
            bg="#2196F3", 
            fg="white",
            width=20
        )
        self.caption_button.pack(pady=5)

        # Area to display the generated caption
        self.caption_label = tk.Label(
            self.control_frame, 
            text="Caption will appear here", 
            wraplength=300, 
            bg="#f0f0f0",
            font=("Arial", 12)
        )
        self.caption_label.pack(pady=10)

        # Visual feedback during caption generation
        self.loading_label = tk.Label(
            self.control_frame, 
            text="Generating caption...", 
            font=("Arial", 12), 
            fg="gray"
        )
        self.loading_label.pack(pady=10)
        self.loading_label.grid_remove()  # Initially hidden

    def _load_image(self):
        """
        Allows the user to select an image file and displays it within the application.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((400, 400))  # Resizes the image for display
            photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def _generate_caption(self):
        """
        Uses the pre-trained model to generate a textual description of the loaded image.
        """
        if hasattr(self, 'image'):
            self.loading_label.grid()  # Display the loading message
            self.caption_label.config(text="")  # Clear previous caption
            self.master.update()  # Refresh the GUI to show the loading message

            # Process the image for model input
            inputs = self.feature_extractor(images=self.image, return_tensors="pt")

            # Generate the caption using the pre-trained model
            output = self.model.generate(**inputs, max_length=20)
            caption = self.tokenizer.decode(output[0], skip_special_tokens=True)

            # Hide the loading message and display the generated caption
            self.loading_label.grid_remove()
            self.caption_label.config(text=caption)
        else:
            self.caption_label.config(text="Please load an image first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCaptioningAI(root)
    root.mainloop()

print("Image Captioning AI has been implemented. Run this script to use the application!")