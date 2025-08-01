import gradio as gr
from transformers import pipeline
import random

# Initialize the models
caption_generator = pipeline("text-generation", model="gpt2")
sentiment_pipeline = pipeline("sentiment-analysis")

# Emoji dictionary
emoji_dict = {
    "positive": ["😊", "🌟", "🔥", "💪", "🚀", "✨"],
    "negative": ["😢", "😞", "💔", "😠", "😓"],
    "neutral": ["🙂", "😐", "🧐", "🤔", "😶"]
}

def get_emojis(text):
    try:
        label = sentiment_pipeline(text)[0]['label'].lower()
        return ''.join(random.sample(emoji_dict.get(label, ["😐"]), 3))
    except:
        return "😊😊😊"

def get_hashtags(prompt, platform):
    words = prompt.lower().split()
    tags = ["#" + word.replace(" ", "") for word in words if len(word) > 3]

    platform_tags = {
        "Instagram": ["#instadaily", "#igers", "#picoftheday", "#instagood", "#photooftheday"],
        "LinkedIn": ["#career", "#leadership", "#networking", "#business", "#success"],
        "Twitter": ["#tweet", "#trending", "#news", "#viral", "#twitter"]
    }
    return " ".join(tags[:5] + random.sample(platform_tags[platform], 2))

def generate_post(prompt, platform):
    if not prompt.strip():
        return "Please enter a keyword or theme", "", ""
        
    # Generate caption
    caption = caption_generator(
        prompt,
        max_length=100,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.9,
        top_p=0.9
    )[0]['generated_text']

    # Generate emojis
    emojis = get_emojis(caption)

    # Generate hashtags
    hashtags = get_hashtags(prompt, platform)

    return caption.strip(), emojis, hashtags

# Custom CSS for better styling
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

# Create the interface
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

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)