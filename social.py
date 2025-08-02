"""
Social Media Post Generator
--------------------------
This script creates a web interface for generating social media posts with captions, emojis, and hashtags.
It uses the Hugging Face Transformers library for text generation and sentiment analysis.
"""

import gradio as gr
from transformers import pipeline
import random

# Initialize the machine learning models
# GPT-2 model for text generation
caption_generator = pipeline("text-generation", model="gpt2")
# Sentiment analysis model to determine emotion in text
sentiment_pipeline = pipeline("sentiment-analysis")

# Dictionary mapping sentiment categories to relevant emojis
# Used to add contextual emojis based on the sentiment of generated text
emoji_dict = {
    "positive": ["😊", "🌟", "🔥", "💪", "🚀", "✨"],
    "negative": ["😢", "😞", "💔", "😠", "😓"],
    "neutral": ["🙂", "😐", "🧐", "🤔", "😶"]
}

def get_emojis(text):
    """
    Generate relevant emojis based on the sentiment of the input text.
    
    Args:
        text (str): Input text to analyze for sentiment
        
    Returns:
        str: String of 3 emojis matching the detected sentiment
    """
    try:
        # Get sentiment label (positive/negative/neutral)
        label = sentiment_pipeline(text)[0]['label'].lower()
        # Return 3 random emojis matching the sentiment
        return ''.join(random.sample(emoji_dict.get(label, ["😐"]), 3))
    except Exception as e:
        # Default to happy emojis if there's an error in sentiment analysis
        print(f"Error in sentiment analysis: {e}")
        return "😊😊😊"

def get_hashtags(prompt, platform):
    """
    Generate relevant hashtags based on the input prompt and selected platform.
    
    Args:
        prompt (str): User's input text
        platform (str): Selected social media platform
        
    Returns:
        str: String of generated hashtags
    """
    # Extract words longer than 3 characters from the prompt
    words = prompt.lower().split()
    tags = ["#" + word.replace(" ", "") for word in words if len(word) > 3]

    # Platform-specific hashtag suggestions
    platform_tags = {
        "Instagram": ["#instadaily", "#igers", "#picoftheday", "#instagood", "#photooftheday"],
        "LinkedIn": ["#career", "#leadership", "#networking", "#business", "#success"],
        "Twitter": ["#tweet", "#trending", "#news", "#viral", "#twitter"]
    }
    
    # Combine 5 most relevant hashtags from prompt with 2 platform-specific ones
    return " ".join(tags[:5] + random.sample(platform_tags[platform], 2))

def generate_post(prompt, platform):
    """
    Generate a complete social media post including caption, emojis, and hashtags.
    
    Args:
        prompt (str): User's input text or theme
        platform (str): Selected social media platform
        
    Returns:
        tuple: (caption, emojis, hashtags) - The generated post components
    """
    # Validate input
    if not prompt.strip():
        return "Please enter a keyword or theme", "", ""
    
    try:
        # Generate caption using GPT-2 model
        caption = caption_generator(
            prompt,                    # Input prompt
            max_length=100,           # Maximum length of generated text
            num_return_sequences=1,    # Number of captions to generate
            do_sample=True,           # Enable random sampling for diverse outputs
            temperature=0.9,          # Controls randomness (higher = more random)
            top_p=0.9                 # Nucleus sampling parameter
        )[0]['generated_text']

        # Generate relevant emojis based on caption sentiment
        emojis = get_emojis(caption)

        # Generate platform-appropriate hashtags
        hashtags = get_hashtags(prompt, platform)

        return caption.strip(), emojis, hashtags
        
    except Exception as e:
        print(f"Error generating post: {e}")
        return "An error occurred while generating the post. Please try again.", "", ""

# Custom CSS for enhancing the web interface
# This CSS customizes the appearance of the Gradio UI components
custom_css = """
.gradio-container {
    max-width: 800px !important;
    margin: 0 auto !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1 {
    text-align: center;
    color: #4a6baf;
    margin-bottom: 10px;
}
.description {
    text-align: center;
    margin-bottom: 20px;
    color: #666;
}
.input-section {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}
.output-section {
    background: #f0f4f8;
    padding: 20px;
    border-radius: 10px;
}
.output-box {
    background: white;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 15px;
    border-left: 4px solid #4a6baf;
}
"""

# Create the main application interface using Gradio Blocks
# This sets up the web UI with custom styling and layout
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🚀 Social Media Post Generator
    *Generate catchy captions, relevant hashtags, and emojis for your social media posts!*
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            with gr.Group():
                input_text = gr.Textbox(
                    label="🎯 Enter your topic or theme",
                    placeholder="e.g., morning coffee, weekend vibes, work from home...",
                    lines=2
                )
                platform = gr.Radio(
                    ["Instagram", "LinkedIn", "Twitter"],
                    label="📱 Select Platform",
                    value="Instagram"
                )
                
                generate_btn = gr.Button("✨ Generate Post", variant="primary")
                
                # Sample inputs
                with gr.Row():
                    gr.Examples(
                        examples=[
                            ["Morning coffee and productivity", "Instagram"],
                            ["Exciting career opportunities", "LinkedIn"],
                            ["Breaking news in tech", "Twitter"]
                        ],
                        inputs=[input_text, platform],
                        label="💡 Try these examples:"
                    )
            
        with gr.Column(scale=4):
            with gr.Tabs():
                with gr.TabItem("Generated Post"):
                    output_caption = gr.Textbox(
                        label="📝 Caption",
                        interactive=False,
                        lines=4
                    )
                    output_emojis = gr.Textbox(
                        label="😊 Emojis",
                        interactive=False
                    )
                    output_hashtags = gr.Textbox(
                        label="#️⃣ Hashtags",
                        interactive=False
                    )
            
            with gr.Row():
                clear_btn = gr.Button("🔄 Clear")
                copy_btn = gr.Button("📋 Copy All")
    
    # Connect the button
    generate_btn.click(
        fn=generate_post,
        inputs=[input_text, platform],
        outputs=[output_caption, output_emojis, output_hashtags]
    )
    
    # Clear button functionality
    def clear_all():
        return "", "", ""
    
    clear_btn.click(
        fn=lambda: ("", "", ""),
        inputs=None,
        outputs=[output_caption, output_emojis, output_hashtags]
    )
    
    # Copy button functionality
    def copy_to_clipboard(caption, emojis, hashtags):
        import pyperclip
        full_text = f"{caption}\n\n{emojis}\n\n{hashtags}"
        pyperclip.copy(full_text)
        return "Copied to clipboard!"
    
    copy_output = gr.Textbox(visible=False)
    copy_btn.click(
        fn=copy_to_clipboard,
        inputs=[output_caption, output_emojis, output_hashtags],
        outputs=copy_output
    )

# Main entry point for the application
if __name__ == "__main__":
    # Start the web server and make the interface publicly accessible
    # Set share=True to create a public link (useful for sharing)
    # For production, you might want to set share=False and configure proper hosting
    demo.launch(share=True)