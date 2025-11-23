from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import razorpay

from .models import Order, Payment


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class VerifyPaymentView(APIView):
    def post(self, request):
        data = request.data

        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        signature = data.get("razorpay_signature")

        if not razorpay_order_id or not razorpay_payment_id or not signature:
            return Response(
                {"error": "Missing payment details"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify signature authenticity
            client.utility.verify_payment_signature(data)

            # Update Order Status
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.status = "PAID"
            order.save()

            # Save Payment record
            Payment.objects.create(
                order=order,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=signature,
                status="SUCCESS"
            )

            return Response({"message": "Payment verified"}, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("Payment verification failed: ", str(e))
            return Response(
                {"error": "Payment verification failed"},
                status=status.HTTP_400_BAD_REQUEST
            )
