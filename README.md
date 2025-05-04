# LeanPrompt - Prompt Optimization Tool

LeanPrompt helps optimize AI prompts by reducing unnecessary tokens while preserving meaning, leading to cost and energy savings.

## Features

- Prompt optimization with configurable aggressiveness levels
- Token counting and cost savings tracking
- Politeness preservation option
- Web UI (Streamlit) and CLI interfaces
- Real-time optimization statistics
- Cost savings visualization

## Installation

1. Clone this repository
2. Install dependencies:
```sh
pip install streamlit pandas matplotlib
```

## Usage

### Web Interface
Run the Streamlit app:
```sh
streamlit run app.py
```

### CLI Mode
If Streamlit is not installed, the app will run in CLI mode:
```sh
python app.py
```

## Configuration

Key settings in [app.py](app.py):
- `COST_PER_TOKEN`: Cost per token (default: $0.00002)
- `STATS_FILE`: Path to save statistics (default: stats.json)
- `LOGO_PATH`: Path to logo file

## Features

### Optimization Options
- **Aggressiveness Levels**: gentle, medium, aggressive
- **Politeness Preservation**: Optional preservation of polite phrases
- **Token Tracking**: Real-time token and cost savings calculations

### Statistics
- Total tokens saved
- Total cost saved
- Historical data visualization
- Daily savings breakdown

## Note

This demo simulates IBM Granite's behavior. For production use, replace the `simulate_granite` function with actual API calls.