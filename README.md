# CallCenterQualityEvaluator

A desktop application for evaluating call center agent quality based on audio transcriptions.

## Key Features

- Audio transcription
- AI-powered text processing
- Quality evaluation based on customizable criteria
- Export results in HTML format

## Prerequisites

- Windows 10 or higher
- Python 3.6 or higher
- PyCharm (recommended)
- API key for generative AI service

## Quick Installation (Windows + PyCharm)

1. **Clone the repository:**
   - Open PyCharm
   - Select "Get from VCS" on the welcome screen
   - URL: `https://github.com/AdamXacur/CallCenterQualityEvaluator.py`
   - Choose project location and click "Clone"

2. **Set up virtual environment:**
   - PyCharm should detect the `requirements.txt` file and offer to create a virtual environment
   - If not, go to File > Settings > Project > Python Interpreter
   - Click the gear icon > Add > Virtualenv Environment > New environment

3. **Install dependencies:**
   - Open a terminal in PyCharm (View > Tool Windows > Terminal)
   - Ensure the virtual environment is activated
   - Run: `pip install -r requirements.txt`

## Usage

1. Open `main.py` in PyCharm and run the script
2. Enter your Google Cloud API key
3. Use the interface buttons to transcribe audio, process text, and generate evaluations
4. Export results as HTML when ready

## Important Files

- `main.py`: Main application script
- `requirements.txt`: List of dependencies
- `content.json`, `content2.json`, `proff.json`: Structured prompts for the AI model

## License

This project is licensed under the GNU General Public License v3 (GPLv3). See the `LICENSE` file for more details.

## Contact

For questions or issues, please open an issue on GitHub or contact the maintainer at [xacurlopez@gmail.com].

## Installation without PyCharm

If you prefer not to use PyCharm, you can set up the project using these steps:

1. **Clone the repository:**
   git clone https://github.com/AdamXacur/CallCenterQualityEvaluator.py
cd CallCenterQualityEvaluator.py
2. **Create a virtual environment:**
   python -m venv venv
3. **Activate the virtual environment:**
   venv\Scripts\activate
4. **Install dependencies:**
   pip install -r requirements.txt
5. **Run the application:**
   python main.py
Follow the same usage instructions as above once the application is running.

Tutorial
For a step-by-step video tutorial on setting up and using the application, watch: [CallCenterQualityEvaluator Tutorial]([https://www.youtube.com/watch?v=mVsjMZU6hf8])
