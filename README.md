#Bot detection system
This is a machine learning system that detects malicious bots on websites by analyzing behavioral signals using mouse tracking, keystroke dynamics, and session analysis.

#Phase 1 - Signal Collection
Currently building the data collection pipeline. Current status be viewed from [PROGRESS.md](PROGRESS.md)

#What does this project do?

1) Collects Behavioral signals from web users such as mouse, keyboard, clicking, scrolling.
2) Analyzes Patterns to distinguish humanlike activity and bot activity 
3) Trains ML models to detect bot-like behavior
4) Provides API for real-time bot detection 

#Why Bot Detection is important
There are various ways for bots to attack websites:
1) Credential Stuffing: bruteforce of millions of password combinations
2) Account takeover: Automating Login attempts
3) Scraping: Stealing data at scale
4) Fraud: Fake account creation and abuse
5) DDoS: Overwhelming servers with too many requests


This project will demonstrate how to defend against bots by understanding their behavior.

## Tech stack
- **Backend**: Flask (Python)- simple to use and quick prototyping
- **Frontend**: Vanilla JavaScript + HTML/CSS - good to learn
- **ML**: Scikit-learn, NumPy, Pandas - good to learn for industry standard
- **Testing**: Pytest - used to verify that features work
- **Data**: JSON (Phase 1-3), PostgreSQL (Phase 5+) - simple and easy to scale
- **Deployment**: AWS Lambda - serverless and scalable

#Project Phases

- **Phase 1**: Signal Collection (Current)
- **Phase 2**: Feature Engineering
- **Phase 3**: Data Collection & Labeling
- **Phase 4**: ML Model Training
- **Phase 5**: Deployment & Monitoring
- **Phase 6**: Advanced Features


#Understanding Bot detection

Mouse movement:
    Humans - curved, random 
    Bots - Linear, Direct

Typing Speed:
    Humans - ranges from 30 - 100 wpm
    Bots - Uniform / instant

Click Timing:
    Humans - Delays, hesitation 
    Bots - Immediate

Idle Time:
    Humans - frequent breaks
    Bots - Constant action

Tab Focus: 
    Humans - Leaves/returns
    Bots - Always focused

Scroll Pattern: 
    Humans - Natural flow
    Bots - Jump to targets
    