
import { writable } from 'svelte/store';

function createNotificationsStore() {
    const { subscribe, update } = writable([]);
    
    return {
        subscribe,
        add: (notification) => update(notifications => [
            ...notifications,
            { id: Date.now(), ...notification }
        ]),
        remove: (id) => update(notifications =>
            notifications.filter(n => n.id !== id)
        )
    };
}

export const notifications = createNotificationsStore();