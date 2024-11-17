<script lang="ts">
  import { loginWithEmail, loginWithGoogle } from '$lib/auth';
  import { goto } from '$app/navigation';
  
  let email = '';
  let password = '';
  let error = '';

  async function handleLogin() {
    const result = await loginWithEmail(email, password);
    if (result.success) {
      goto('/');
    } else {
      error = result.error;
    }
  }

  async function handleGoogleLogin() {
    const result = await loginWithGoogle();
    if (result.success) {
      goto('/');
    } else {
      error = result.error;
    }
  }
</script>

<div class="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-3xl mx-auto">
    <div class="glass-card shadow-xl rounded-lg overflow-hidden">
      <div class="px-4 py-5 sm:p-6">
        <h1 class="text-3xl font-bold text-gray-900 text-center mb-8">Login</h1>
        
        {#if error}
          <div class="p-4 mb-4 text-red-700 bg-red-100 rounded-lg">
          {error}
          </div>
        {/if}

        <form on:submit|preventDefault={handleLogin} class="mb-8">
          <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            bind:value={email}
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          </div>

          <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            Password
          </label>
          <input
            type="password"
            id="password"
            bind:value={password}
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          </div>

          <button type="submit" class="w-full bg-gray-800 text-white py-2 px-4 rounded-md hover:bg-grey-300 mb-4">
          Login
          </button>
        </form>

        <button 
          class="w-full mb-8 bg-gray-200 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-300"
          on:click={handleGoogleLogin}
        >
          Login with Google
        </button>

        <div class="flex justify-between text-sm text-gray-800">
          <a href="/signup" class="hover:text-blue-800">Create account</a>
          <a href="/forgot-password" class="hover:text-blue-800">Forgot password?</a>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .glass-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease-in-out;
  }

  .glass-card:hover {
    transform: scale(1.05);
  }
</style>
