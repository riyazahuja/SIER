# SIER

## Introduction
Welcome to SIER, a cutting-edge platform designed to revolutionize the way individuals and small institutions engage with the financial markets. Utilizing advanced AI and machine learning techniques, SIER aims to provide personalized, accurate, and intuitive financial forecasting and portfolio management.

## Project Goals
SIER aims to:

- **Democratize Financial Forecasting**: Make advanced financial analysis tools accessible to a broader audience, beyond big institutions.
- **Personalize Investment Strategies**: Offer customizable strategies that match the user's risk profile, investment goals, and preferences.
- **Incorporate Alternative Data**: Leverage non-traditional data sources for more comprehensive and unique market insights.
- **Promote Ethical Investing**: Provide options for users interested in ESG and sustainable investing.
- **Ensure Transparency**: Make AI decisions understandable and transparent, building trust and knowledge among users.
- **Foster a Collaborative Community**: Create a space where users can learn from and collaborate with each other.
- **Adapt and Innovate**: Continuously improve and innovate the platform based on user feedback and market changes.

## File/Repository Structure

- `/data`: Contains raw data, processed data, and data retrieval scripts, ensuring a robust foundation for analysis and model training.
    - `/raw`: Raw data files from various sources.
    - `/processed`: Cleaned and preprocessed data ready for analysis.
    - `/scripts`: Scripts for data retrieval and preprocessing.

- `/docs`: Documentation files, including detailed project proposals, technical references, and user manuals.

- `/models`: AI and machine learning models, including both the initial models and subsequent iterations.
    - `/domains`: Interfaces and model domains for data handling.  
    - `/training`: Scripts and notebooks used for model training.
    - `/evaluation`: Tools and scripts for model evaluation and validation.

- `/src`: Source code for the SIER platform, including data processing, model inference, and front-end interface.
    - `/api`: Code for the backend, including data APIs and model serving.
    - `/services`: External API accesses and price servicing.
    - `/ui`: Front-end code for the web application or user interface.
    - `/utils`: Caching and other utilities

- `/tests`: Automated tests for software components to ensure reliability and performance.

- `/deploy`: Scripts and configuration files for deploying the application in various environments.


## UI Setup and Local Development

### Setting Up the Local HTTP Server

SIER's UI is built with web technologies and can be run locally using `http-server`, a simple, zero-configuration command-line HTTP server. To set up and run the UI on your local machine, follow these steps:

1. **Install `http-server` globally**: This allows you to use `http-server` from any directory in your command line.
    ```bash
    npm install -g http-server
    ```
   - If you do not have Node.js and npm installed, download and install them from [nodejs.org](https://nodejs.org/).

2. **Navigate to the Project Root**: Change into the root directory of the SIER project where the `index.html` file is located within the `src/ui` directory.

3. **Start the Server**: Run the following command to start `http-server`, disabling caching with `-c-1`:
    ```bash
    http-server -c-1
    ```
    - The `-c-1` flag is used to prevent the server from caching files.

4. **Access the UI**: Open your web browser and navigate to the following address to view the UI:
    ```
    http://127.0.0.1:8080/src/ui/
    ```

### Development and Testing

- **Live Reloading**: For a better development experience with live reloading, consider using `http-server` with a watch tool like `nodemon` or integrating a more advanced build tool like `webpack` that provides a development server with live reloading out of the box.
- **Testing**: Test the UI in multiple browsers and screen sizes to ensure compatibility and responsiveness.
- **Contributions**: If you make changes to the UI, please ensure they are well-documented and tested before submitting a pull request.

## How to Contribute

- **Fork the Repository**: Start by forking the repository and cloning it to your local machine.
- **Understand the Goals**: Familiarize yourself with the project goals and current structure.
- **Pick a Task**: Look at the current issues or proposed enhancements and pick something that aligns with your skills and interests.
- **Coding Standards**: Ensure your code adheres to the established standards and is well-documented.
- **Submit a Pull Request**: Once you're satisfied with your work, submit a pull request for review.


