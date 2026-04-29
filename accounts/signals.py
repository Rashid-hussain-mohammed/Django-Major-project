from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Order

@receiver(post_save, sender=Order)
def order_updated(sender, instance, created, **kwargs):
    print(f"⚡ [SIGNAL] Order {instance.id} was just saved!")
    channel_layer = get_channel_layer()
    
    try:
        # 🚨 TEMPORARY FIX: Hardcode to '1' to match your Angular dashboard!
        restaurant_id = '1' 
        print(f"⚡ [SIGNAL] Broadcasting to room: restaurant_{restaurant_id}")
        
        async_to_sync(channel_layer.group_send)(
            f'restaurant_{restaurant_id}',
            {
                'type': 'dashboard_update',
                'message': 'reload_orders'
            }
        )
    except Exception as e:
        print(f"❌ [SIGNAL ERROR] Could not send message: {e}")