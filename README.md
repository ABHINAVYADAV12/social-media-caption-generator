# Social Media Caption Generator

A powerful AI-powered tool that generates creative and engaging captions for your social media posts.

## Features

- Generate creative captions for various social media platforms
- Multiple caption styles and tones
- Customizable hashtag suggestions
- Easy-to-use web interface
- Save and manage your favorite captions

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## Libraries and Dependencies

The application uses the following key libraries:

- `gradio`: For creating the web interface
- `transformers`: For natural language processing tasks
- `torch`: Deep learning framework
- `nltk`: Natural Language Toolkit for text processing
- `pandas`: For data manipulation
- `numpy`: For numerical operations
- `python-dotenv`: For managing environment variables
- `requests`: For making HTTP requests

## Installation

### Method 1: Using pip (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/social-media-caption-generator.git
   cd social-media-caption-generator
   ```

2. Create and activate a virtual environment:

   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Method 2: Manual Installation

If you prefer to install packages manually:

```bash
pip install gradio>=3.39.0 numpy>=1.21.0 pandas>=1.3.0 transformers>=4.30.0 torch>=2.0.0 python-dotenv>=1.0.0 requests>=2.28.0 nltk>=3.8.1
```

### Additional Setup

After installation, you need to download the required NLTK data:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Usage

1. Run the application:

   ```bash
   python social.py
   ```

2. Open your web browser and navigate to `http://localhost:7860`

3. Enter your post details and let the AI generate captions for you!

## Configuration

You can customize the application by modifying the `.gradio` configuration file. This file stores:

- Interface layout settings
- Theme configurations
- Default parameters
- Example inputs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository.
