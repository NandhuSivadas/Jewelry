from .models import AuditLog

class AuditService:
    @staticmethod
    def log(action: str, category: str, request=None, actor=None, target=None, detail: dict = None, severity: str = "INFO") -> AuditLog:
        ip_address = None
        user_agent = ""
        actor_email = ""
        
        if request:
            ip_address = request.META.get('REMOTE_ADDR')
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:300]
            
            if not actor and hasattr(request, 'user') and request.user.is_authenticated:
                actor = request.user
                
        if actor:
            actor_email = getattr(actor, 'email', str(actor))
            
        target_type = ""
        target_id = ""
        target_repr = ""
        if target:
            target_type = target.__class__.__name__
            target_id = str(getattr(target, 'pk', ''))
            target_repr = str(target)[:200]
            
        return AuditLog.objects.create(
            actor=actor,
            actor_email=actor_email,
            action=action,
            category=category,
            target_type=target_type,
            target_id=target_id,
            target_repr=target_repr,
            ip_address=ip_address,
            user_agent=user_agent,
            detail=detail or {},
            severity=severity
        )
