# ValorantGPT

<p align="center">
  <a href="" rel="noopener">
 <img width=128px height=58px src="https://i.postimg.cc/MHHtzdmX/valgpt.png" alt="Project logo"></a>
</p>

ValorantGPT is a program that enhances the in-game chat experience in Valorant by providing automated responses as a supportive teammate. It utilizes the power of OpenAI's GPT-3 language model to generate appropriate replies based on incoming messages.

## How It Works

The program connects to the Valorant game client through a WebSocket connection and listens for incoming chat messages. When a message is received, it processes the message and generates a response using the ChatGPT model. The response is then sent back to the game chat.

## Prerequisites

- Python 3.7 or higher
- Valorant game client running

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nur-zaman/valorantGPT.git
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Configure the program:

   - Open the `config.json` file and provide the necessary values:
     - `chatgptToken`: Access token for OpenAI's ChatGPT API. [How?](https://github.com/acheong08/ChatGPT)
     - `discord_webhook_url`: URL of the Discord webhook to send notifications.
     - `in_game_name`: Your in-game name in Valorant.
     - `players_to_avoid`: List of player names to avoid responding to.

4. Customize the prompt:

    - Open the prompt.txt file.
    - Modify the existing content to match the desired persona and character you want to portray as a supportive teammate. You can include phrases, keywords, or responses that align with your desired in-game persona.


## Usage

- Start the Valorant game client first.
- Run the `start.bat` script to start the program.
- The program will listen to the in-game chat and respond accordingly as a supportive teammate.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request.
