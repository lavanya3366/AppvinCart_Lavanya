from django.shortcuts import render
from django.http import JsonResponse
import stripe
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail

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

    
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
import stripe


def process_payment(request):
    if request.method == 'POST':
        payment_method_id = request.POST.get('payment_method_id')

        try:
            # Confirm the payment with Stripe
            payment_intent = stripe.PaymentIntent.create(
               # Adjust amount as needed (in cents)
                amount=2000,
                currency="usd",
                automatic_payment_methods={"enabled": True},
                payment_method_types=["card"],


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
      payment_intent = stripe.PaymentIntent.create(
               # Adjust amount as needed (in cents)
                amount=2000,
                currency="usd",
                automatic_payment_methods={"enabled": True},)
               
        # Return error response if request method is not POST
      return render(request, 'payment_success.html', {'payment_intent': payment_intent})

