# Mock Interview Simulator (Local • Privacy-First)

A lightweight, fully local mock interview simulator built with **Python + Tkinter**.
Practice answering questions under time pressure with a **two-phase timer** and an optional
**live webcam preview** for self-observation (posture, eye contact, facial expressions).

> **Not affiliated with any school, program, or organization.**
> This repository provides a *generic* interview practice framework only.

---

## Key Features

- **Two-phase timer workflow**
  - Preparation phase (default: 10s)
  - Answer phase (default: 90s)
- **Local webcam preview (optional)**
  - Real-time preview from your webcam
  - No uploads, no cloud calls, no tracking
- **Easy to customize**
  - Timers, UI colors, and question list are defined in one place

---

## How to use

- Click **Next Question** to start a new round
- The app runs:
  1) Preparation countdown
  2) Answer countdown
- Use **Pause/Resume** to control the timer

---

## Privacy & Responsible Use

- Runs **entirely on your machine**
- Does **not** transmit video/audio/questions
- Ships with **generic placeholder questions** only

### What you should NOT do

- Do not include or publish proprietary, confidential, or NDA-protected interview content.
- Do not claim endorsement or partnership with any institution.

---

## Requirements

- Python 3.8+ recommended
- A working webcam (optional but recommended)

Dependencies are listed in `requirements.txt`:

- `opencv-python`
- `Pillow`

---

## Installation

```bash
git clone https://github.com/heropig114514/mock-interview-simulator.git
cd mock-interview-simulator
pip install -r requirements.txt
```

---

## Run

```bash
python interview.py
```

---

## Customize Questions

Edit `QUESTION_BANK` in `interview.py`.

If you plan to open-source the repository, keep questions **generic**.

Example (generic):

```python
QUESTION_BANK = [
    "Why are you interested in this role or program?",
    "Tell me about a recent project you worked on and what you learned.",
    "Describe a challenge you faced and how you handled it.",
]
```

---

## Configuration

In `interview.py`, you can adjust:

- `PREP_TIME_LIMIT` (seconds)
- `INTERVIEW_TIME_LIMIT` (seconds)
- `VIDEO_REFRESH_RATE` (ms)
- UI theme colors

---

## Contributing

Issues and PRs are welcome.

- Keep PRs focused and small
- Avoid adding institution-specific or confidential interview content

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This tool is provided "as is" for educational and practice purposes.
You are responsible for ensuring your usage complies with any agreements (e.g., NDAs)
and applicable laws/policies.
