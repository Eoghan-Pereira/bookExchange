
import { writable } from 'svelte/store';

export const notifications = writable([]);

export function addNotification(notification) {
    notifications.update(n => [...n, {
        id: Date.now(),
        timestamp: new Date(),
        read: false,
        ...notification
    }]);
}

export function markAsRead(notificationId) {
    notifications.update(n => 
        n.map(notification => 
            notification.id === notificationId 
                ? { ...notification, read: true }
                : notification
        )
    );
}