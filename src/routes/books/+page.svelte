<script lang="ts">
    import { onMount } from 'svelte';
    import { getAllBooks } from '$lib/api';
    import { user } from '$lib/stores/auth';
    import { goto } from '$app/navigation';
    import BookCard from '$lib/components/BookCard.svelte';

    let books = [];
    let loading = false;
    let error = '';

    async function loadBooks() {
        loading = true;
        try {
            books = await getAllBooks();
        } catch (err) {
            error = err.message;
        }
        loading = false;
    }

    function initiateExchange(bookId: string) {
        if (!$user) {
            goto('/login');
            return;
        }
        goto(`/exchanges/initiate?bookId=${bookId}`);
    }

    onMount(loadBooks);
</script>

<div class="books-grid">
    <h1>Available Books</h1>
    
    {#if loading}
        <p>Loading books...</p>
    {:else if error}
        <p class="error">{error}</p>
    {:else}
        <div class="grid">
            {#each books as book}
                <BookCard {book} />
            {/each}
        </div>
    {/if}
</div>

<style>
    .books-grid {
        padding: 1rem;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 1rem;
    }
</style>