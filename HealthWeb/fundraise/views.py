
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .models import DonationPost, Donation
from django.shortcuts import render
from .utils import client

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)
        amount = int(data.get("amount"))
        post_id = data.get("post_id")

        if amount <= 0:
            return JsonResponse({"error": "Invalid amount"}, status=400)

        amount_paise = amount * 100  # Razorpay works in paise

        order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        return JsonResponse({
            "order_id": order["id"],
            "key": settings.RAZORPAY_KEY_ID,
            "amount": amount_paise
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.db.models import F

@csrf_exempt
def verify_payment(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        data = json.loads(request.body)

        razorpay_order_id = data["razorpay_order_id"]
        razorpay_payment_id = data["razorpay_payment_id"]
        razorpay_signature = data["razorpay_signature"]
        amount = int(data["amount"])
        post_id = data["post_id"]

        # Verify signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        # Payment verified — update donation post
        post = get_object_or_404(DonationPost, id=post_id)
        post.raised_amount = F("raised_amount") + amount
        post.save(update_fields=["raised_amount"])

        # 🔥 Create Donation record
        Donation.objects.create(
            post=post,
            user=request.user if request.user.is_authenticated else None,
            amount=amount,
            razorpay_payment_id=razorpay_payment_id
        )

        return JsonResponse({"status": "success"})

    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({"error": "Payment verification failed"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def donation_list(request):
    posts = DonationPost.objects.filter(
        is_active=True,
        end_date__gte=timezone.now()
    )
    print(posts)
    return render(request, "fundraise/donationpage.html", {"posts": posts})

@login_required
def donation_detail(request, pk):
    post = get_object_or_404(DonationPost, pk=pk, is_active=True)
    return render(request, "fundraise/paymentpage.html", {"post": post})
