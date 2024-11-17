
export interface Book {
    id: string;
    userId: string;
    title: string;
    author: string;
    genre: string;
    condition: 'New' | 'Like New' | 'Very Good' | 'Good' | 'Fair' | 'Poor';
    available: boolean;
    description?: string;
    image?: string;
    createdAt: Date;
    updatedAt: Date;
}

export type BookFormData = Omit<Book, 'id' | 'userId' | 'createdAt' | 'updatedAt'>;