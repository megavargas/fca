from domain.models import Domain

def check_domain(sender, user, request, **kwargs):
    _, created = Domain.objects.get_or_create(name=user.email.split('@')[1])
    if created: 
        user.is_owner = True
        user.save()

