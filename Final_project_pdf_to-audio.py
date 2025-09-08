import pdfplumber  # pip install pdfplumber
import pyttsx3     # pip install pyttsx3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import re

class SimpleAudiobookConverter:
    def __init__(self):
        # Initialize TTS engine
        self.engine = pyttsx3.init()
        self.current_text = ""
        self.is_playing = False
        
        # Create GUI
        self.root = tk.Tk()
        self.root.title("Simple PDF to Audiobook Converter")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f4ff")  # Soft background
        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10), background="#f0f4ff")
        style.configure("TFrame", background="#f0f4ff")

        
        self.setup_ui()
    
    def setup_ui(self):
        # File selection
        ttk.Button(self.root, text="Select PDF File", command=self.select_pdf).pack(pady=10)
        
        self.file_label = ttk.Label(self.root, text="No file selected")
        self.file_label.pack(pady=5)
        
        # Speed control
        speed_frame = ttk.Frame(self.root)
        speed_frame.pack(pady=10)
        
        ttk.Label(speed_frame, text="Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.IntVar(value=200)
        ttk.Scale(speed_frame, from_=100, to=300, variable=self.speed_var, 
                 orient=tk.HORIZONTAL, length=200).pack(side=tk.LEFT, padx=10)
        self.speed_label = ttk.Label(speed_frame, text="200 WPM")
        self.speed_label.pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Play Audio", command=self.play_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stop Audio", command=self.stop_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save as WAV", command=self.save_audio).pack(side=tk.LEFT, padx=5)
        
        # Text preview
        ttk.Label(self.root, text="📖 Text Preview:").pack(anchor=tk.W, padx=20, pady=(20,5))
        self.text_area = tk.Text(self.root, height=15, width=70, wrap=tk.WORD)
        self.text_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Status
        self.status = ttk.Label(self.root, text="Ready")
        self.status.pack(pady=5)


        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=5)

        
        # Update speed label
        self.speed_var.trace('w', self.update_speed_label)
    
    def update_speed_label(self, *args):
        self.speed_label.config(text=f"{self.speed_var.get()} WPM")
    
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            self.file_label.config(text=f"Selected: {file_path.split('/')[-1]}")
            self.extract_text(file_path)
    
    def extract_text(self, pdf_path):
        try:
            self.status.config(text="Extracting text...")
            self.root.update()
            
            # Open PDF and extract text using pdfplumber
            text = ""
            
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text += f"Page {page_num}:\n{page_text}\n\n"
            
            if not text.strip():
                raise Exception("No text found in PDF")
            
            # Clean text
            text = self.clean_text(text)
            self.current_text = text
            
            # Display in text area
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, text)
            
            word_count = len(text.split())
            self.status.config(text=f"Ready - {word_count} words extracted")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text: {str(e)}")
            self.status.config(text="Error extracting text")
    
    def clean_text(self, text):
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that cause TTS issues
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        return text.strip()
    
    def play_audio(self):
        if not self.current_text:
            messagebox.showwarning("Warning", "No text to play. Please select a PDF first.")
            return
        
        if self.is_playing:
            messagebox.showinfo("Info", "Audio is already playing")
            return
        
        # Set TTS properties
        self.engine.setProperty('rate', self.speed_var.get())
        
        def play_thread():
            try:
                self.is_playing = True
                self.status.config(text="Playing audio...")
                self.engine.say(self.current_text)
                self.engine.runAndWait()
                self.is_playing = False
                self.status.config(text="Playback finished")
            except Exception as e:
                self.is_playing = False
                messagebox.showerror("Error", f"Playback error: {str(e)}")
                self.status.config(text="Playback error")
        
        threading.Thread(target=play_thread, daemon=True).start()
    
    def stop_audio(self):
        if self.is_playing:
            self.engine.stop()
            self.is_playing = False
            self.status.config(text="Playback stopped")
        else:
            messagebox.showinfo("Info", "No audio is playing")
    
    def save_audio(self):
        if not self.current_text:
            messagebox.showwarning("Warning", "No text to save. Please select a PDF first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Audio As",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")]
        )
        
        if file_path:
            try:
                self.status.config(text="Saving audio...")
                self.root.update()
                
                # Set TTS properties
                self.engine.setProperty('rate', self.speed_var.get())
                
                # Save to file
                self.engine.save_to_file(self.current_text, file_path)
                self.engine.runAndWait()
                
                messagebox.showinfo("Success", f"Audio saved to {file_path}")
                self.status.config(text="Audio saved successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save audio: {str(e)}")
                self.status.config(text="Error saving audio")
    
    def run(self):
        self.root.mainloop()

# Main execution
if __name__ == "__main__":
    app = SimpleAudiobookConverter()
    app.run()
