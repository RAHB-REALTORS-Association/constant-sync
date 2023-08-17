[![Continuous Integration](https://github.com/RAHB-REALTORS-Association/constant-sync/actions/workflows/python-3.11.yml/badge.svg)](https://github.com/RAHB-REALTORS-Association/constant-sync/actions/workflows/python-3.11.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Constant Sync** is an automated synchronization tool designed to keep your data in sync with Constant Contact. It offers a seamless OAuth2 authentication mechanism, scheduled data synchronization, and comprehensive error handling to ensure your contacts are always up-to-date.

## 📖 Table of Contents
- [🛠️ Setup](#%EF%B8%8F-setup)
- [🧑‍💻 Usage](#-usage)
- [🛡️ Privacy](#%EF%B8%8F-privacy)
- [🌐 Community](#-community)
  - [Contributing 👥🤝](#contributing-)
  - [Reporting Bugs 🐛📝](#reporting-bugs-)
- [📄 License](#-license)

## 🛠️ Setup

**1. Clone the Repository 📁**

```bash
git clone https://github.com/RAHB-REALTORS-Association/constant-sync.git
```

**2. Install Dependencies 📦**

Navigate to the project directory and run:

```bash
pip install -r requirements.txt
```

**3. Configuration 🔧**

Ensure you have your `config.py` file set up with the necessary credentials for your JSON API endpoint and Constant Contact.

**4. Running the Application 🚀**

Execute:

```bash
python app.py
```

This will start the Flask server, and you can navigate to the displayed URL to initiate the OAuth2 flow with Constant Contact.

## 🧑‍💻 Usage

Visit the provided URL and click on "Authorize with Constant Contact". Once authorized, the tool will automatically sync your member database with Constant Contact at the specified intervals.

## 🛡️ Privacy

This tool respects your data. No data is stored beyond what is necessary for synchronization purposes. All communication with Constant Contact is secure and compliant with their API requirements.

## 🌐 Community

### Contributing 👥🤝

Contributions, feedback, and bug reports are welcome! For more details, please refer to the [Contributing Guide](CONTRIBUTING.md).

[![Submit a PR](https://img.shields.io/badge/Submit_a_PR-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/constant-sync/compare)

### Reporting Bugs 🐛📝

If you encounter any issues or have suggestions, please [open a new issue](https://github.com/RAHB-REALTORS-Association/constant-sync/issues/new).

[![Raise an Issue](https://img.shields.io/badge/Raise_an_Issue-GitHub-%23060606?style=for-the-badge&logo=github&logoColor=fff)](https://github.com/RAHB-REALTORS-Association/constant-sync/issues/new/choose)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
