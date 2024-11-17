<script lang="ts">
    import { page } from '$app/stores';
    import { user } from '$lib/stores/auth';
    let isMenuOpen = false;
    
    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
    }
</script>

<nav>
    <div class="nav-brand">
        <a href="/">Book Exchange</a>
    </div>
    
    <button class="menu-toggle" on:click={toggleMenu} aria-label="Toggle menu">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
    </button>

    <div class="nav-links {isMenuOpen ? 'open' : ''}">
        <a href="/" class:active={$page.url.pathname === '/'}>
            <button class="nav-button">Home</button>
        </a>
        {#if $user}
            <a href="/books/add" class:active={$page.url.pathname === '/books/add'}>
                <button class="nav-button">Add Book</button>
            </a>
            <a href="/profile/books" class:active={$page.url.pathname === '/profile/books'}>
                <button class="nav-button">My Books</button>
            </a>
            <a href="/profile" class:active={$page.url.pathname === '/profile'}>
                <button class="nav-button">Profile</button>
            </a>
        {:else}
            <a href="/login">
                <button class="nav-button">Login</button>
            </a>
        {/if}
    </div>
</nav>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Edu+AU+VIC+WA+NT+Pre:wght@400..700&display=swap');
    
    nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: linear-gradient(to right, #ca9b8f, #8B47B5);
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .nav-brand {
        font-family: 'Edu AU VIC WA NT Pre', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
    }
    
    .nav-brand a {
        color: white;
        text-decoration: none;
    }
    
    .menu-toggle .bar {
        width: 25px;
        height: 3px;
        background-color: white;
        margin: 4px 0;
        transition: 0.4s;
    }
    
    .nav-button {
        background: none;
        border: none;
        padding: 0.5rem 1rem;
        cursor: pointer;
        font-size: 1rem;
        color: white;
        transition: background 0.3s, color 0.3s;
    }
    
    .nav-button:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .active .nav-button {
        color: white;
        font-weight: bold;
        background: rgba(255, 255, 255, 0.1);
    }
    
    @media (max-width: 768px) {
        .nav-links {
            background: linear-gradient(to right, #FED0C5, #8B47B5);
        }
    }
</style>
