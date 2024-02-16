from django.core.mail import EmailMessage
import os

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=os.environ.get('EMAIL_FROM'),
      to=[data['to_email']]
    )
    email.send()
# class UserPasswordResetView(APIView):
#   renderer_classes = [UserRenderer]
#   def post(self, request, uid, token, format=None):
#     serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
#     serializer.is_valid(raise_exception=True)
#     return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)