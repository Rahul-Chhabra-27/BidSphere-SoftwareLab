from rest_framework.views import APIView
from rest_framework.response import Response
from .order_view import Order, OrderItem



class CreateOrderView(APIView):
    def post(self, request):
        user = request.user
        amount = request.data.get("amount")
        cart_items = request.data.get("cart_items", [])

        if not amount or not user.is_authenticated:
            return Response({"error": "Invalid request"}, status=400)

        order = Order.objects.create(
            user=user,
            total_amount=amount,
            status="PENDING"
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_id=item["id"],
                quantity=1
            )

        razorpay_order = client.order.create({
            "amount": int(amount) * 100,
            "currency": "INR",
            "payment_capture": 1
        })

        order.razorpay_order_id = razorpay_order["id"]
        order.save()

        return Response({"order": razorpay_order, "db_order_id": order.id})
