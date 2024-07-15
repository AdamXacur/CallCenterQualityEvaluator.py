# CallCenterQualityEvaluator.py
# Call Center Agent Quality Evaluator

This project is a desktop application designed to evaluate the quality of call center agents based on audio transcriptions. The application allows you to transcribe audio files, process and polish transcriptions, and generate evaluations based on predefined quality criteria.

## Features

- **Audio Transcription**: Transcribe audio files using Google Speech Recognition or Whisper models.
- **Text Dialysis**: Process transcriptions using a custom AI model to improve clarity and consistency.
- **Quality Evaluation**: Generate quality evaluations based on user-defined criteria.
- **Export Results**: Export the results of the evaluation in HTML format.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- An API key for the generative AI service

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/AdamXacur/CallCenterQualityEvaluator.py
    cd yourrepository
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application**:
    ```sh
    python main.py
    ```

2. **API Key**:
   - Enter your API key in the provided field in the application.

3. **Transcribe Audio**:
   - Click the "Transcribe Audio" button and select a WAV file to transcribe.

4. **Process Transcription**:
   - Click the "Dialize" button to process the transcribed text.

5. **Generate Evaluation**:
   - Enter the quality criteria in the "Quality Criteria" section.
   - Click the "Generate Evaluation" button to generate the evaluation based on the transcribed text and quality criteria.

6. **Export Results**:
   - Click the "Export Results" button to save the evaluation results as an HTML file.

## Files

- main.py: The main script to run the application.
- requirements.txt`: Lists all the dependencies needed for the project.
- content.json: Contains a structured prompt for dialing transcripts.
- content2.json: Contains a structured prompt for the behavior of the model against the 2 inputs, the conversation and the quality items to evaluate.
- proff.json: Contains a structured prompt to tell the model to correct the inconsistencies in the call caused by the lack of accuracy of the transcription systems. 

## Dependencies

- `tkinter`
- `ttkbootstrap`
- `google-generativeai`
- `whisper`
- `pygame`
- `speech_recognition`

These dependencies are listed in the `requirements.txt` file and can be installed using `pip install -r requirements.txt`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Contact

If you have any questions or issues, please open an issue on GitHub or contact the project maintainer at [xacurlopez@gmail.com].



