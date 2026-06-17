# Security Policy

Thank you for helping keep VietQuill secure.

## Reporting a Vulnerability

If you believe you have discovered a security vulnerability in VietQuill, please report it privately.

Please do **not** open a public GitHub issue for security-related vulnerabilities.

Instead, contact the maintainer at:

* Email: [nguyenquangsang0709@gmail.com](mailto:nguyenquangsang0709@gmail.com)
* GitHub: https://github.com/ngwgsang

When reporting a vulnerability, please include:

* A clear description of the issue
* Steps to reproduce the vulnerability
* A proof-of-concept (if available)
* The affected version(s)
* Any suggested mitigations or fixes

We will make reasonable efforts to:

1. Acknowledge receipt of the report.
2. Investigate the issue.
3. Provide updates regarding remediation.
4. Release a fix if the vulnerability is confirmed.

## Supported Versions

As VietQuill is currently under active research and development, security fixes are generally provided only for the latest release.

| Version        | Supported |
| -------------- | --------- |
| Latest release | ✅         |
| Older releases | ❌         |

## Security Considerations

VietQuill may interact with:

* Hugging Face Hub repositories
* Third-party datasets
* Third-party pretrained models
* User-provided text inputs

Users should exercise caution when:

* Loading models from untrusted sources
* Executing third-party code
* Using experimental features
* Processing sensitive or confidential data

We recommend:

* Keeping dependencies up to date
* Using trusted model repositories
* Reviewing downloaded artifacts before execution
* Running experiments in isolated environments when appropriate

## Scope

This security policy applies to:

* VietQuill source code
* Official VietQuill releases
* Official VietQuill demo applications

This policy does not cover:

* Third-party models
* Third-party datasets
* External services integrated by users
* User-customized deployments

## Responsible Disclosure

We ask security researchers to provide a reasonable amount of time for investigation and remediation before publicly disclosing a vulnerability.

We appreciate responsible disclosure and welcome contributions that help improve the security of the VietQuill ecosystem.
