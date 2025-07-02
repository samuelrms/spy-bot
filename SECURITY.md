# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please send an email to [samuelaoliveiraramos@gmail.com.com](mailto:samuelaoliveiraramos@gmail.com.com). All security vulnerabilities will be promptly addressed.

Please include the following information in your report:

- **Type of issue** (buffer overflow, SQL injection, cross-site scripting, etc.)
- **Full paths of source file(s) related to the vulnerability**
- **The location of the affected source code (tag/branch/commit or direct URL)**
- **Any special configuration required to reproduce the issue**
- **Step-by-step instructions to reproduce the issue**
- **Proof-of-concept or exploit code (if possible)**
- **Impact of the issue, including how an attacker might exploit it**

This information will help us quickly assess and address the vulnerability.

## Security Best Practices

When using this bot, please follow these security best practices:

1. **Never share your bot token** - Keep it in your `.env` file and never commit it to version control
2. **Use environment variables** - Store sensitive configuration in environment variables
3. **Regular updates** - Keep your dependencies updated to the latest secure versions
4. **Monitor logs** - Regularly check bot logs for any suspicious activity
5. **Limit permissions** - Only grant the bot the permissions it actually needs

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine the affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all supported versions
4. Release new versions with the fixes
5. Publicly announce the vulnerability and the fix

## Credits

We would like to thank all security researchers who responsibly disclose vulnerabilities to us.
