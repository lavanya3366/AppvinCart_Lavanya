from django.shortcuts import render
from django.http import JsonResponse
import stripe

# Assuming you've already configured your Stripe API keys
stripe.api_key = 'pk_test_51OjzIASJ953jewJiOuQ6eIBMX0bYJjK24T0la6mSqgeexEOxPxe18E2H0hOhi3aq28I7S2lx2xrqQPlpXn46ttBw00rkfoE65a'

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

            # Render payment.html template with success message
            return render(request, 'payment.html', {'success': True})
        except stripe.error.InvalidRequestError as e:
            # Return error response if the payment method ID is invalid
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            # Return error response for other exceptions
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Render the payment_form.html template for GET requests
        return render(request, 'payment.html')