# KYY (Know Your YouTuber)

KYY or Know Your YouTuber is an AI-powered chat application that allows users to interact with their favorite YouTubers through intelligent conversations based on video transcripts. By using the YouTuber's username and your OpenAI API key, the system pulls recent video data and creates a personalized chat experience, leveraging OpenAI's GPT models to simulate conversations based on the YouTuber's recent content.

## Features
- **Efficient Transcript Analysis**: Automatically fetches YouTube video transcripts, processes them, and dynamically selects the right amount of video content that fits within OpenAI's GPT-4o-mini context window.
- **Cost-Effective**: The project is based on GPT-4o-mini, keeping the API usage cost relatively low.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/M0ckenv1r0n/KYY
   cd KYY
   ```

2. Install the dependencies:
   Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

   The dependencies include:
   - customtkinter==5.2.2: For creating a GUI.
   - scrapetube==2.5.1: To scrape YouTube videos.
   - openai==1.48.0: For interacting with the OpenAI API.
   - pillow==10.4.0: To manage any image processing tasks.
   - youtube_transcript_api==0.6.2: To fetch video transcripts.
   - tiktoken==0.8.0: For managing tokenization of transcripts for GPT context handling.

## Usage

1. Configure API keys:
   You’ll need to set your OpenAI API key in the environment or within the application. You can get the API key from OpenAI's website (https://platform.openai.com/account/api-keys).

2. Start the Application:
   Run the Python script:

   ```bash
   python main.py
   ```

3. Enter YouTube Channel Name:
   Provide the YouTuber's username whose videos you'd like to chat with.

   __In this format: PewDiePie__ ~~@PewDiePie~~


## How it Works

1. Scrape YouTube Data: The app uses scrapetube to fetch a list of videos from the specified YouTuber.
2. Retrieve Transcripts: youtube_transcript_api fetches the transcripts of each video.
3. Process and Tokenize: Using tiktoken, the system determines how many videos can fit into GPT-4's context window for effective conversation flow.
4. Chat Simulation: OpenAI's GPT-4o-mini model is used to generate conversation responses based on the YouTuber's video content.

## Future Improvements

- Enhanced GUI: Improve the user interface for a more intuitive experience.
- Support for Multiple APIs: Add support for other LLM APIs like Gemini which basically makes sensebecause of 1m context window.
- Advanced AI Features: Implement an improvede system instructions that'll lead to better YouTuber's style imitation and more accurate responses to personal queries.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
