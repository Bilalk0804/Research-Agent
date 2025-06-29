# AI Research Assistant with Streamlit Interface

A powerful AI research assistant powered by Mixtral-8x7B and LangChain, featuring a beautiful Streamlit web interface.

## Features

- 🔍 **Web Search**: DuckDuckGo integration for real-time web searches
- 📚 **Wikipedia Integration**: Access to Wikipedia articles and information
- 💾 **File Saving**: Save research results to local files
- 🎨 **Beautiful UI**: Modern, responsive Streamlit interface
- 📊 **Export Functionality**: Download research results as JSON
- 🛠️ **Tool Management**: Visual display of available tools and their status

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirement.txt
```

### 2. Environment Variables

Create a `.env` file in the project root with your API keys:

```env
NVIDIA_API_KEY=your_nvidia_api_key_here
```

### 3. Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## How to Use the Streamlit Interface

### 1. **Main Interface**
- The app features a clean, modern interface with a sidebar for settings
- Enter your research query in the text area
- Click "🔍 Start Research" to begin the research process

### 2. **Sidebar Features**
- **Model Status**: Shows if the AI model is loaded successfully
- **Available Tools**: Lists all available research tools
- **Clear History**: Remove all previous research results
- **Export Results**: Download all research results as JSON

### 3. **Research Results**
- Results are displayed in expandable cards
- Each result shows:
  - 📝 **Summary**: AI-generated research summary
  - 📚 **Sources**: Links and references used
  - 🛠️ **Tools Used**: Which tools were utilized
- Action buttons for each result:
  - 💾 **Save to File**: Save individual results
  - 📋 **Copy Summary**: Copy summary to clipboard
  - 🗑️ **Delete**: Remove specific results

### 4. **Quick Stats**
- View statistics about your research session
- Track total queries and last research time

## File Structure

```
Langchain_Proj1/
├── main.py              # Original command-line version
├── streamlit_app.py     # Streamlit web interface
├── tools.py             # Custom tools implementation
├── requirement.txt      # Python dependencies
├── README.md           # This file
└── .env                # Environment variables (create this)
```

## Customization

### Adding New Tools
1. Define your tool function in `tools.py`
2. Add it to the tools list in `streamlit_app.py`
3. The interface will automatically display it in the sidebar

### Styling
The app uses custom CSS for styling. You can modify the CSS in the `st.markdown()` section of `streamlit_app.py` to customize the appearance.

### Model Configuration
To change the AI model, modify the `init_chat_model()` call in the `initialize_model()` function.

## Troubleshooting

### Common Issues

1. **Model Loading Error**
   - Check your NVIDIA API key in the `.env` file
   - Ensure you have sufficient API credits

2. **Tool Errors**
   - Verify internet connection for web search tools
   - Check Wikipedia API availability

3. **Streamlit Issues**
   - Make sure Streamlit is installed: `pip install streamlit`
   - Check if port 8501 is available

### Performance Tips

- The model is cached using `@st.cache_resource` for better performance
- Research results are stored in session state to persist during the session
- Use the "Clear History" button to free up memory if needed

## Advanced Usage

### Batch Research
You can perform multiple research queries in one session. All results are stored and can be exported together.

### Integration with Other Tools
The modular design allows easy integration with additional tools:
- Academic databases
- News APIs
- Custom data sources

## Contributing

Feel free to enhance the interface by:
- Adding new visualization components
- Implementing additional export formats
- Creating custom themes
- Adding user authentication

---

**Built with ❤️ using Streamlit, LangChain, and Mixtral-8x7B** 