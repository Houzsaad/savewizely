## Savewizely

A backend-only digital savings platform built with Django REST Framework. Savewise helps users build disciplined saving habits by letting them lock money until a chosen date or savings goal, with early withdrawal available for a penalty fee.

Status: In active development. This README reflects the intended scope and will be updated as features land.

## What Savewise Is (and Isn't)
Savewizely is not a general payments app. Unlike OPay or PalmPay, it's not built for everyday transfers or bill payments. Its only job is helping people save consistently — money goes in, gets locked, and comes out either at maturity or early with a penalty.

## Core Features (MVP)

Authentication — Register, login, forgot password, JWT-based auth

Wallet — Balance tracking, funding via Paystack, withdrawal after unlock

Locked Savings — Lock funds for a fixed duration (daily/weekly/monthly/yearly/fixed date); funds are inaccessible until maturity

Goal-Based Savings — Set a target amount and duration; app tracks daily contribution progress and missed-day streaks

Early Unlock — Withdraw locked savings before maturity, minus a penalty percentage

Transaction History — Full ledger of every deposit, withdrawal, lock, and unlock, each with a unique reference

Receipts — Downloadable PDF receipts for any transaction

Deferred to a Later Phase

Dedicated/static deposit account numbers (requires a licensed banking-as-a-service partner)

Profile editing, settings pages, notifications

Automatic bank-linked recurring savings

Loans and money transfers

These are left out of the MVP deliberately — the goal is a focused, working core before adding surface-level features.

## Tech Stack
Backend: Python, Django, Django REST Framework
Database: PostgreSQL
Auth: JWT (djangorestframework-simplejwt)
Payments: Paystack (wallet funding)
Scheduled tasks: Celery + Redis (for lock maturity checks)
Deployment: Render

## Project Structure

Code
Setup
Bash
API Overview
Endpoint
Method
Description
/register/
POST
Create a new account
/login/
POST
Obtain JWT access/refresh tokens
/login/refresh/
POST
Refresh JWT access token
/forgot-password/
POST
Request a password reset link
/reset-password/
POST
Reset password with token


##Setup
# Clone and enter the project
git clone https://github.com/Houzsaad/savewizely.git
cd savewise

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver 
More endpoints (wallet, locked savings, goals) will be documented here as they're built.

## Roadmap
✅ Authentication
⬜ Wallet + Paystack funding
⬜ Locked Savings
⬜ Goal-Based Savings
⬜ Early Unlock + penalty logic
⬜ Transaction history + PDF receipts
⬜ API docs (Swagger), tests, deployment
Author
Built by Huzaifa Sa'ad as a portfolio/fintech backend project.