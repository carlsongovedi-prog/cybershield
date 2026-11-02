# CyberShield AI Security Assessment — Safety Checklist

## Project Information

- Project ID: AISEC-001
- Assessment Type: AI Security Assessment
- Status: Educational and Planning
- Prepared by: CyberShield Security Team

## 1. Before Testing

- [ ] Identify the system owner.
- [ ] Obtain written authorization.
- [ ] Confirm the exact target application and environment.
- [ ] Define permitted IP addresses, domains, APIs and accounts.
- [ ] Document testing dates and time windows.
- [ ] Identify prohibited activities.
- [ ] Confirm whether test data is synthetic.
- [ ] Establish an emergency contact.
- [ ] Confirm backup and recovery arrangements where applicable.
- [ ] Review the assessment scope document.

## 2. During Testing

- [ ] Stay strictly within the approved scope.
- [ ] Use test accounts and synthetic data.
- [ ] Avoid accessing real users' private information.
- [ ] Do not attempt destructive actions.
- [ ] Do not perform denial-of-service testing.
- [ ] Do not extract or expose confidential data.
- [ ] Record test dates, methods and observations.
- [ ] Store evidence securely.
- [ ] Redact secrets, tokens and personal information.
- [ ] Stop immediately if unexpected impact occurs.

## 3. AI-Specific Safety Checks

- [ ] Use harmless prompt-injection test examples.
- [ ] Do not attempt to extract real system prompts containing confidential information.
- [ ] Do not expose real API keys or credentials.
- [ ] Use synthetic examples when testing information disclosure.
- [ ] Do not connect the AI system to unauthorized external tools.
- [ ] Check that sensitive actions require appropriate human approval.
- [ ] Verify that test results do not affect real users.

## 4. After Testing

- [ ] Stop all testing activities.
- [ ] Securely store assessment evidence.
- [ ] Remove temporary test data where authorized.
- [ ] Document findings accurately.
- [ ] Assign risk ratings based on evidence.
- [ ] Provide remediation recommendations.
- [ ] Notify the system owner of significant findings.
- [ ] Confirm that no unauthorized changes remain.
- [ ] Prepare the final assessment report.

## 5. Stop-Testing Conditions

Immediately stop testing if:

- The system behaves unexpectedly or becomes unstable.
- Real customer or personal data is exposed.
- Testing affects users or business operations.
- You discover access outside the approved scope.
- You encounter credentials or confidential information not intended for the test.
- The system owner withdraws authorization.

## 6. Final Safety Confirmation

Assessment conducted within approved scope: __________________

Unexpected impact identified: __________________

Evidence securely stored: __________________

Assessor: __________________

Date: __________________

Note: A completed checklist does not replace written authorization.
