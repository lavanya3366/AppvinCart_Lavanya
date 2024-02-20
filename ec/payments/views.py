from django.shortcuts import render
from django.http import JsonResponse
import stripe
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Sum
from app.models import Cart
from app.models import Product

# Assuming you've already configured your Stripe API keys
stripe.api_key = 'sk_test_51OjzIASJ953jewJiMdX1WxftSqeF0JQCBJpHEXjfV9TieKO53fGrIt74bc3a4Fizb3HbVFbqBwVcImJOwzmqFStC00OkVB7jP0'

def add_payment_method(request):
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')
        
        try:
            # Create a new customer in Stripe
            customer = stripe.Customer.create(
            payment_method=payment_method_id,
            email=request.user.email,  # Assuming you have a user object
            invoice_settings={
                    'default_payment_method': payment_method_id
                }
            )
            
            # Optionally, save the payment method ID to your user's profile
            # request.user.payment_method_id = payment_method_id
            # request.user.save()

            # Send email notification
            send_mail(
                'Payment Successful',
                'Your payment was successful.',
                'apshvp@gmail.com',  # Replace with sender email
                ['lavashri0303@gmail.com'],  # Replace with recipient email
                fail_silently=False,
            )


            # Render payment.html template with success message
            return render(request, 'productpayment.html', {'success': True})
        except stripe.error.InvalidRequestError as e:
            # Return error response if the payment method ID is invalid
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            # Return error response for other exceptions
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Render the payment_form.html template for GET requests
        return render(request, 'payment.html')

    


def process_payment(request):
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')

        try:
            # Retrieve the user's cart items from the database
            cart_items = Cart.objects.filter(user=request.user)

            # Calculate the total cost of items in the cart
            total_cost = cart_items.aggregate(total_cost=Sum('total_cost'))['total_cost'] or 0
            total_cost = int(total_cost * 100)  # Convert to cents

            # Confirm the payment with Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=total_cost,
                currency="usd",
                payment_method=payment_method_id,
                confirm=True,
            )

            # Save payment information to database (optional)
            # Example: Payment.objects.create(payment_method_id=payment_method_id, user=request.user)

            # Send email notification
            send_mail(
                'Payment Successful',
                'Your payment was successful.',
                'apshvp@gmail.com',  # Replace with sender email
                ['lavashri0303@gmail.com'],  # Replace with recipient email
                fail_silently=False,
            )

            # Render payment confirmation template
            return render(request, 'payment_success.html', {'payment_intent': payment_intent})
        except stripe.error.StripeError as e:
            # Handle payment failure
            return render(request, 'payment_failure.html', {'error': str(e), 'payment_intent': None})

    else:
        # Return error response if request method is not POST
        return render(request, 'payment_failure.html', {'error': 'Method not allowed.', 'payment_intent': None})
# from django.shortcuts import render
# from django.http import JsonResponse
# import stripe

# # Set your Stripe API key
# stripe.api_key = 'your_stripe_api_key'

# def checkout(request):
#     if request.method == 'POST':
#         # Retrieve payment method ID from the request (e.g., from Stripe Elements or Checkout)
#         payment_method_id = request.POST.get('payment_method_id')

#         # Create or retrieve a customer
#         customer = stripe.Customer.create(
#             payment_method=payment_method_id,
#             email='customer@example.com',
#         )

#         # Create a payment intent
#         intent = stripe.PaymentIntent.create(
#             amount=1000,  # Amount in cents
#             currency='usd',
#             customer=customer.id,
#             payment_method=customer.invoice_settings.default_payment_method,
#             confirm=True,
#         )

#         # Optionally, you can return the client secret to complete the payment on the client side
#         return JsonResponse({'client_secret': intent.client_secret})

#     # If the request method is not POST, render the checkout page
#     return render(request, 'checkout.html')
