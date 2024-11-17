import { get } from 'svelte/store';
import { user } from '$lib/stores/auth';

const API_BASE_URL = 'http://localhost:8000/api';

export const fetchBooks = async () => {
    const response = await fetch(`${API_BASE_URL}/books`);
    if (!response.ok) {
        throw new Error('Failed to fetch books');
    }
    return response.json();
};

export const addBook = async (bookData: any) => {
    const response = await fetch(`${API_BASE_URL}/books`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookData),
    });
    if (!response.ok) {
        throw new Error('Failed to add book');
    }
    return response.json();
};

export const getUserBooks = async (userId: string) => {
    const response = await fetch(`${API_BASE_URL}/books/${userId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch user books');
    }
    return response.json();
};

export const updateBook = async (bookId: string, bookData: any) => {
    const authToken = get(user)?.authToken;
    const response = await fetch(`${API_BASE_URL}/books/${bookId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(bookData),
    });
    if (!response.ok) {
        console.error('Update failed:', await response.text());
        throw new Error('Failed to update book');
    }
    return response.json();
};

export const deleteBook = async (bookId: string) => {
    const authToken = get(user)?.authToken;
    const response = await fetch(`${API_BASE_URL}/books/${bookId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${authToken}`
        }
    });
    if (!response.ok) {
        console.error('Delete failed:', await response.text());
        throw new Error('Failed to delete book');
    }
    return response.json();
};

export const initiateExchange = async (exchangeData: any) => {
    const response = await fetch(`${API_BASE_URL}/exchanges`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${exchangeData.authToken}`,
        },
        body: JSON.stringify(exchangeData),
    });
    if (!response.ok) {
        throw new Error('Failed to initiate exchange');
    }
    return response.json();
};

export const getUserExchanges = async (userId: string) => {
    const response = await fetch(`${API_BASE_URL}/exchanges/user/${userId}`, {
        headers: {
            'Authorization': `Bearer ${user.authToken}`,
        },
    });
    if (!response.ok) {
        throw new Error('Failed to fetch exchanges');
    }
    return response.json();
};

export const getExchangeDetails = async (exchangeId: string) => {
    const response = await fetch(`${API_BASE_URL}/exchanges/${exchangeId}`, {
        headers: {
            'Authorization': `Bearer ${user.authToken}`,
        },
    });
    if (!response.ok) {
        throw new Error('Failed to fetch exchange details');
    }
    return response.json();
};

export const respondToExchange = async (exchangeId: string, action: string, updates?: any) => {
    const response = await fetch(`${API_BASE_URL}/exchanges/${exchangeId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${user.authToken}`,
        },
        body: JSON.stringify({ action, updates }),
    });
    if (!response.ok) {
        throw new Error('Failed to respond to exchange');
    }
    return response.json();
};

export const updateExchange = async (exchangeId: string, updates: any) => {
    const response = await fetch(`${API_BASE_URL}/exchanges/${exchangeId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${user.authToken}`,
        },
        body: JSON.stringify(updates)
    });
    if (!response.ok) throw new Error('Failed to update exchange');
    return response.json();
};

export const cancelExchange = async (exchangeId: string) => {
    const response = await fetch(`${API_BASE_URL}/exchanges/${exchangeId}/cancel`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${user.authToken}`,
        }
    });
    if (!response.ok) throw new Error('Failed to cancel exchange');
    return response.json();
};

export const markExchangeComplete = async (exchangeId: string) => {
    const response = await fetch(`${API_BASE_URL}/exchanges/${exchangeId}/complete`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${user.authToken}`,
        }
    });
    if (!response.ok) throw new Error('Failed to complete exchange');
    return response.json();
};

export async function getAllBooks() {
    const response = await fetch('/api/books');
    if (!response.ok) throw new Error('Failed to fetch books');
    return response.json();
}

export async function getExchange(exchangeId: string, authToken: string) {
    const response = await fetch(`/api/exchanges/${exchangeId}`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
    });
    if (!response.ok) throw new Error('Failed to fetch exchange details');
    return response.json();
}

export const updateExchangeStatus = async (exchangeId: string, status: string, authToken: string) => {
    const response = await fetch(`${API_BASE_URL}/exchanges/${exchangeId}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({ status })
    });
    
    if (!response.ok) {
        throw new Error('Failed to update exchange status');
    }
    
    return response.json();
};

export async function getUserTransactions(userId: string, authToken: string, query: string = '') {
    const response = await fetch(`/api/transactions/${userId}${query}`, {
        headers: {
            'Authorization': `Bearer ${authToken}`
        }
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch transactions');
    }
    
    return response.json();
}

export async function createTransaction(transactionData: any, authToken: string) {
    const response = await fetch('/api/transactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(transactionData)
    });
    
    if (!response.ok) {
        throw new Error('Failed to create transaction');
    }
    
    return response.json();
}

export async function getAvailableBooks(authToken: string) {
    const response = await fetch(`${API_BASE_URL}/exchanges/available-books`, {  // Changed URL
        headers: {
            'Authorization': `Bearer ${authToken}`
        }
    });

    if (!response.ok) {
        console.error('Failed to fetch available books:', response.status);
        throw new Error('Failed to fetch available books');
    }

    const data = await response.json();
    console.log('Available books response:', data);  // Debug log
    return data;
}