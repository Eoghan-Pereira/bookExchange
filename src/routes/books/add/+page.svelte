<script lang="ts">
    import { goto } from '$app/navigation';
    import { user } from '$lib/stores/auth';
    import { get } from 'svelte/store';
    import { Input, Label, Select, Textarea, Fileupload, Alert } from 'flowbite-svelte';

    let book = {
        title: '',
        author: '',
        genre: '',
        condition: 'new',
        isAvailable: true,
        description: '',
        userId: get(user)?.uid
    };

    let image: File | null = null;
    const conditions = ['new', 'like-new', 'good', 'fair', 'poor'].map(c => ({ value: c, name: c }));
    const genres = ['Fiction', 'Non-Fiction', 'Science', 'History', 'Biography', 'Other'].map(g => ({ value: g, name: g }));

    let errorMessage = '';
    let loading = false;

    $: book.userId = get(user)?.uid;
    $: authToken = get(user)?.authToken;

    let textareaProps = {
        id: 'description',
        name: 'description',
        label: 'Description',
        rows: 4,
        placeholder: 'Enter book description...'
    };

    let fileuploadProps = {
        id: 'book_image'
    };

    async function handleSubmit() {
        if (!image) {
            errorMessage = 'Please select a book image';
            return;
        }

        loading = true;
        errorMessage = '';

        if (!book.title || !book.author || !book.genre) {
            errorMessage = 'Please fill in all required fields';
            loading = false;
            return;
        }

        try {
            const formData = new FormData();
            formData.append('title', book.title);
            formData.append('author', book.author);
            formData.append('genre', book.genre);
            formData.append('condition', book.condition);
            formData.append('isAvailable', book.isAvailable.toString());
            formData.append('description', book.description);
            formData.append('userId', book.userId);
            formData.append('image', image);

            const response = await fetch('/api/books', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${authToken}`
                },
                body: formData
            });

            if (response.ok) {
                await response.json();
                goto('/profile/books');
            } else {
                errorMessage = 'Failed to add book';
            }
        } catch (error) {
            errorMessage = 'Failed to connect to server';
        } finally {
            loading = false;
        }
    }
</script>

<div class="max-w-2xl mx-auto p-8">
    <h1 class="text-3xl font-bold mb-6">Add New Book</h1>

    {#if errorMessage}
        <Alert color="red" class="mb-4">{errorMessage}</Alert>
    {/if}

    <div class="bg-white bg-opacity-50 backdrop-filter backdrop-blur-lg p-6 rounded-lg shadow-lg">
        <form on:submit|preventDefault={handleSubmit} class="space-y-6">
            <div>
                <Label for="book_image" class="mb-2">Book Image (Required)</Label>
                <Fileupload
                    {...fileuploadProps}
                    accept="image/*"
                    on:change={(e) => (image = (e.target as HTMLInputElement)?.files?.[0] || null)}
                />
                {#if image}
                    <img src={URL.createObjectURL(image)} alt="Book preview" class="mt-2 max-w-[200px] max-h-[200px]" />
                {/if}
            </div>

            <div>
                <Label for="title" class="mb-2">Title*</Label>
                <Input id="title" required bind:value={book.title} placeholder="Enter book title" />
            </div>

            <div>
                <Label for="author" class="mb-2">Author*</Label>
                <Input id="author" required bind:value={book.author} placeholder="Enter author name" />
            </div>

            <div>
                <Label for="genre" class="mb-2">Genre*</Label>
                <Select 
                    id="genre" 
                    required 
                    bind:value={book.genre} 
                    items={genres} 
                    class="text-gray-900 bg-white"
                />
            </div>

            <div>
                <Label for="condition" class="mb-2">Condition*</Label>
                <Select 
                    id="condition" 
                    required 
                    bind:value={book.condition} 
                    items={conditions} 
                    class="text-gray-900 bg-white"
                />
            </div>

            <div>
                <Label for="description" class="mb-2">Description</Label>
                <Textarea {...textareaProps} bind:value={book.description} />
            </div>
            <button
                type="submit"
                disabled={loading}
                class="w-full px-4 py-2 text-white bg-black hover:bg-gray-800 rounded-lg disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
                {loading ? 'Adding Book...' : 'Add Book'}
            </button>
        </form>
    </div>
</div>

<style>
    
</style>