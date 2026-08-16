#!/bin/sh

import requests

response = requests.post(
    "https://api.paystack.co/transaction/initialize",
    headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
    json={"email": user.email, "amount": amount_in_kobo}
)