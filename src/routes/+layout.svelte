<script>
	import '../app.css';
	import { user } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import { auth } from '$lib/firebase';
	import { goto } from '$app/navigation';
	import Navbar from '$lib/components/Navbar.svelte'; 
	import { page } from '$app/stores';

	onMount(() => {
		return auth.onAuthStateChanged((firebaseUser) => {
			user.set(firebaseUser);
		});
	});
</script>

<Navbar></Navbar>

<main>
	{#if $page.status === 404}
		<div class="not-found-card">
			<div class="not-found">404 - Page Not Found</div>
		</div>
	{:else}
		<slot></slot>
	{/if}
</main>

<style>
	nav {
		padding: 1rem;
		background-color: #f0f0f0;
	}

	nav a {
		margin-right: 1rem;
	}

	main {
		padding: 2rem;
	}

	.not-found-card {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}

	.not-found {
		text-align: center;
		font-size: 2rem;
		color: white;
		padding: 4rem;
		background-color: rgba(139, 71, 181, 0.3);
		margin: 2rem;
		border-radius: 8px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}
</style>
