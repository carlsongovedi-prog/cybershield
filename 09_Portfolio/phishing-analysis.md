# Phishing case study: fake "MoMo account suspended" email

**Source:** invented training sample (no real organisation or live link).

## 1. Sender
- Display name: "MTN MoMo Support". Real address: support@mtn-momo-secure.example.
- The domain is not the company's real domain. It is a look-alike built from the brand name plus words like "secure".
- Reply-To is a different address on a free email service, so replies would go to the attacker.

## 2. Red flags found
1. **Urgency and threat:** "suspended in 24 hours" pushes me to act without thinking.
2. **Generic greeting:** "Dear Customer". A real provider usually uses my name.
3. **Mismatched sender:** display name says the company; the address does not.
4. **Suspicious link:** the visible text and the real destination are not the company's official site.
5. **Asks for secrets:** a PIN and ID number. A real provider never asks for a PIN by email or SMS.
6. **Reply-To differs from From:** a common trick to redirect replies.

## 3. Link destinations
- Shown: "Click here". Real destination (defanged): hxxp://momo-verify-login[.]example/login
- Not the official site. Plain http (no HTTPS) and a made-up verification domain.
- I did not click it. To check safely, hover to read the real address or paste it into a URL checker.

## 4. SPF / DKIM / DMARC (from "Show original" in the mail client)
| Check | Result in this sample | Meaning |
|---|---|---|
| SPF | fail | The sending server is not allowed to send for the From domain |
| DKIM | none | The message is not signed by the claimed domain |
| DMARC | fail | The domain's own policy says this message is not legitimate |

(In the invented sample these are assumed results. In a real email, copy them from the headers.)

## 5. Recommended action
- Do not click, reply or enter any PIN or ID.
- Report it using the mail client's "Report phishing" option, or forward to the IT or security contact.
- Delete it afterwards.
- If anyone already entered details: change the password and PIN at once using the official app, contact the provider through its official number, and tell IT.
- IT: block the sender domain and link domain, search other mailboxes for the same email.

## 6. Lessons for staff
- Real providers do not threaten to close an account by email.
- Never give a PIN, password or code to anyone who asks, by any channel.
- Check the real sender address and the link destination before acting.
- When unsure, use the official app or phone number, not the email's link.
