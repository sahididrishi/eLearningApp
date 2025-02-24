def unread_notifications(request):
    if request.user.is_authenticated:
        # We assume your Notification model has an `is_read` BooleanField
        count = request.user.notifications.filter(is_read=False).count()
        return {'unread_count': count}
    else:
        return {'unread_count': 0}