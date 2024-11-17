<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    export let onSearch: (filters: any) => void;
    
    const dispatch = createEventDispatcher();
    
    let filters = {
        keyword: '',
        genre: '',
        condition: '',
        availability: ''
    };

    let searchTerm = '';
    let selectedGenre = 'all';

    const genres = ['all', 'Fiction', 'Non-Fiction', 'Science', 'History', 'Biography', 'Other'];

    function handleSearch() {
        dispatch('search', filters);
    }

    function resetFilters() {
        filters = {
            keyword: '',
            genre: '',
            condition: '',
            availability: ''
        };
        handleSearch();
    }

    function handleSubmit() {
        const filters = {
            search: searchTerm,
            genre: selectedGenre === 'all' ? '' : selectedGenre
        };
        onSearch(filters);
    }
</script>

<div class="search-filters">
    <input
        type="text"
        placeholder="Search books by name or author ..."
        bind:value={searchTerm}
        on:input={() => handleSubmit()}
    />
    
    <select bind:value={selectedGenre} on:change={() => handleSubmit()}>
        {#each genres as genre}
            <option value={genre}>{genre}</option>
        {/each}
    </select>
</div>


<style>
    .search-filters {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        padding: 1rem;
    }
    
    input, select {
        padding: 0.5rem;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    input {
        flex: 1;
    }

    .search-filter {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }

    .search-bar input {
        width: 100%;
        padding: 0.8rem;
        border: 1px solid #ddd;
        border-radius: 4px;
        margin-bottom: 1rem;
    }

    .filters {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }

    select {
        padding: 0.5rem;
        border: 1px solid #ddd;
        border-radius: 4px;
        min-width: 150px;
    }

    .reset-btn {
        padding: 0.5rem 1rem;
        background: #f44336;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
</style>