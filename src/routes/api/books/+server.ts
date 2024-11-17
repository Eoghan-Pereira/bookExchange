import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
    try {
        const search = url.searchParams.get('search') || '';
        const genre = url.searchParams.get('genre') || '';
        
        const queryParams = new URLSearchParams();
        if (search) queryParams.append('search', search);
        if (genre) queryParams.append('genre', genre);
        
        const apiUrl = `http://localhost:8000/api/books?${queryParams}`;
        const response = await fetch(apiUrl);
        const books = await response.json();
        return json(books);
    } catch (error) {
        return json({ error: 'Failed to fetch books' }, { status: 500 });
    }
};

export const POST: RequestHandler = async ({ request }) => {
    try {
        const formData = await request.formData();

        // Get the Authorization header from the request
        const authorization = request.headers.get('Authorization');

        const response = await fetch('http://localhost:8000/api/books', {
            method: 'POST',
            headers: {
                // Forward the Authorization header if needed
                'Authorization': authorization || ''
                // Do not set 'Content-Type' when sending FormData
            },
            body: formData
        });
        
        const result = await response.json();
        return json(result);
    } catch (error) {
        return json({ error: 'Failed to create book' }, { status: 500 });
    }
};