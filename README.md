# Vulnerable API Lab

## About

NotesKeeper is web application where users can read and write their notes from anytime and anywhere, but still there are some bugs related to API which needs to be pointed out before the bad guyz do their work. You can find the walkthrough on my [blog](http://divyanshudiwakar.com)

## Vulnerabilities

Reference : [OWASP TOP 10](https://owasp.org/www-project-api-security/)

-  Excessive Data Exposure
-  Security Misconfiguration
-  Broken User Authentication
-  Cross Site Request Forgery
-  Broken Access Controls

## Goals

- Finding sensitive API Endpoints leaking some Data
- Account Takeovers using Reset Password
- Rate Limiting on User Account Creation and Login Page
- Reading other's notes
- Updating other's notes
- JSON based CSRF
- Privilege Escalation from user to admin

## Installation

- Install the requirements from requiremet.txt
- Clone the repository
- python3 .\app.py

## Future Work

- Adding more functionalities in the Admin Panel
- Providing Defence mechanism (code change) for every vulnerability

## Creator

- Twitter : [Divyanshu Diwakar](https://twitter.com/ddiwakr)

## References

- [OWASP Kontra API Lab](https://application.security/free/owasp-top-10-API) 
- [InsiderPhd Generic University lab](https://github.com/InsiderPhD/Generic-University).
