# 🎯 IntelliPath - AI Career Path Recommender

An intelligent, AI-powered web application that analyzes your resume and generates personalized career development plans based on your skills, experience, interests, and career goals.

## Features

- 📄 **Multi-Format Resume Parsing**: Extract text from PDF, DOCX, and TXT files
- 🧠 **AI-Powered Analysis**: 
  - Named Entity Recognition (NER) to identify skills, experience, and education
  - Extract job titles, companies, projects, certifications, and achievements
- 🎯 **Personalized Career Paths**: 
  - 3-stage career development plans (Entry, Mid, Senior level)
  - Considers your area of interest and future goals
  - Customized recommendations based on your timeline preferences
- 📊 **Comprehensive Resume Analysis**: 
  - Skills identification
  - Job title extraction
  - Company history
  - Education background
  - Projects and achievements
- 💾 **Download Results**: Save your career plan in Markdown or Text format
- 🎨 **User-Friendly Interface**: Modern, responsive Streamlit UI with intuitive navigation

## Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/) - Web app framework
- **NLP**: [Transformers](https://huggingface.co/transformers/) - Named Entity Recognition
- **ML**: [PyTorch](https://pytorch.org/) - Deep learning framework
- **Document Processing**: 
  - [python-docx](https://python-docx.readthedocs.io/) - DOCX parsing
  - [PyPDF2](https://pypdf2.readthedocs.io/) - PDF parsing
  - [lxml](https://lxml.de/) - XML/HTML processing
- **Data Processing**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Utilities**: [python-dateutil](https://dateutil.readthedocs.io/), [pytz](https://pytz.sourceforge.io/)

## Project Structure

```
intellipath/
├── app.py                 # Main Streamlit application
├── resume_parser.py       # Resume text extraction (PDF, DOCX, TXT)
├── iextract.py           # Named Entity Recognition and entity extraction
├── generator.py          # Career path generation using LLMs
├── utils.py              # Utility functions (file handling, etc.)
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── models/              # Directory for cached models (if needed)
```

### File Descriptions

- **app.py**: Main Streamlit application with UI components, user input handling, and orchestration
- **resume_parser.py**: Extracts text content from various resume formats
- **iextract.py**: Uses transformer models for NER to identify and normalize entities from resume text
- **generator.py**: Generates personalized career path recommendations using LLMs
- **utils.py**: Helper functions for file uploads, temporary file management, etc.

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- ~2GB free disk space (for models)

### Setup

1. **Clone or download the project**
   ```bash
   cd intellipath
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv intellipath_env
   ```

3. **Activate the virtual environment**
   - **Windows**:
     ```bash
     .\intellipath_env\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     source intellipath_env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Activate the virtual environment** (if not already active)
   ```bash
   # Windows
   .\intellipath_env\Scripts\Activate.ps1
   
   # macOS/Linux
   source intellipath_env/bin/activate
   ```

2. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

3. **Access the application**
   - Open your browser and navigate to: `http://localhost:8501`
   - The app will also provide Network URL for access from other devices

## Usage Guide

1. **Upload Your Resume**
   - Click the upload button and select your resume (PDF, DOCX, or TXT format)
   - The file will be processed automatically

2. **Specify Your Preferences**
   - **Area of Interest**: Select your preferred technology field
   - **Future Goals**: Choose all applicable career goals
   - **Additional Goals**: Add any specific preferences or context
   - **Timeline**: Select your preferred pace of career advancement

3. **Generate Career Path**
   - Click "Generate Personalized Career Path" button
   - The app will analyze your resume and generate recommendations

4. **Review Results**
   - **Resume Analysis Tab**: See extracted skills, experience, and qualifications
   - **Career Path Tab**: View your personalized 3-stage development plan
   - **Raw Text Tab**: Review the extracted resume text
   - **Download Tab**: Save your career plan as Markdown or Text
   - **Your Preferences Tab**: Review the preferences you selected

## Technology Details

### NER Model
The application uses Hugging Face transformer models for Named Entity Recognition to identify:
- Skills and technologies
- Job titles and positions
- Company names
- Educational institutions
- Certifications
- Projects and achievements

### LLM Integration
Career path generation uses state-of-the-art language models from Hugging Face to create personalized, context-aware recommendations.

### Performance Optimization
- Models are cached after first download
- Parallel processing for faster analysis
- Streamlit caching for improved performance

## Troubleshooting

### ModuleNotFoundError or ImportError
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

### Out of Memory (OOM) Errors
- Close other applications
- For production, consider using:
  - Quantized models
  - Hugging Face Inference API
  - GPU acceleration (if available)

### Slow Performance
- First run downloads models (~2GB) - this is normal
- Subsequent runs will be faster
- Consider using GPU for faster inference

### Resume Not Parsing Correctly
- Ensure resume is in supported format (PDF, DOCX, TXT)
- Try exporting resume as TXT and uploading that
- Check that file is not corrupted

## Development

### Adding New Features
1. Modify relevant module (e.g., `generator.py` for career path logic)
2. Update UI in `app.py` if needed
3. Test thoroughly before deployment

### Model Updates
- Update transformer model version in `iextract.py` and `generator.py`
- Test with sample resumes
- Update `requirements.txt` if new dependencies are needed

## Deployment

### For Small-Scale Deployment
This Streamlit app can be deployed on:
- **Streamlit Cloud** (recommended for Streamlit apps)
- **Heroku**
- **AWS EC2**
- **DigitalOcean**
- **PythonAnywhere**

### For Production
- Use quantized or smaller models
- Implement Hugging Face Inference API for better scalability
- Add authentication and user management
- Implement database for storing results
- Set up monitoring and logging
- Consider GPU acceleration

### Environment Variables
If deploying, you may want to set:
- Model cache directory
- Temporary file directory
- API keys (if using external services)

## Contributing

To improve IntelliPath:
1. Test with various resume formats and content
2. Suggest improvements for entity recognition
3. Propose new career path analysis features
4. Report bugs and issues

## Future Enhancements

- [ ] Support for video resume analysis
- [ ] Multi-language resume support
- [ ] Integration with job boards for real-time opportunity matching
- [ ] Salary expectations based on career path
- [ ] Networking recommendations
- [ ] Skill gap analysis with learning resources
- [ ] Career milestone tracking
- [ ] Export to PDF with professional formatting
- [ ] API endpoint for integration with other services
- [ ] User accounts and result history

## License

This project is provided as-is for educational and commercial use.

## Disclaimer

IntelliPath provides AI-generated career recommendations based on resume analysis. These recommendations should be considered as guidance and not as professional career advice. Always consult with career professionals for important career decisions.

## Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section above
2. Review application logs
3. Test with sample resume files
4. Verify all dependencies are correctly installed

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- NLP powered by [Hugging Face Transformers](https://huggingface.co/transformers/)
- Deep learning with [PyTorch](https://pytorch.org/)

---

**Last Updated**: February 2026