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

<script lang="ts">
  import { resetPassword } from '$lib/auth';

  let email = '';
  let message = '';
  let error = '';

  async function handleResetPassword() {
    const result = await resetPassword(email);
    if (result.success) {
      message = 'Password reset email sent. Please check your inbox.';
      error = '';
    } else {
      error = result.error;
      message = '';
    }
  }
</script>

<div class="min-h-screen  py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-3xl mx-auto">
    <div class="glass-card shadow-xl rounded-lg overflow-hidden">
      <div class="px-4 py-5 sm:p-6">
        <h1 class="text-3xl font-bold text-gray-900 text-center mb-8">Reset Password</h1>

        {#if error}
          <div class="p-4 mb-4 text-red-700 bg-red-100 rounded-lg">
            {error}
          </div>
        {/if}

        {#if message}
          <div class="p-4 mb-4 text-green-700 bg-green-100 rounded-lg">
            {message}
          </div>
        {/if}

        <form on:submit|preventDefault={handleResetPassword} class="mb-8">
          <div class="mb-6">
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

            <button type="submit" class="w-full bg-gray-800 text-white py-2 px-4 rounded-md hover:bg-black">
            Send Reset Link
            </button>
          </form>

          <div class="text-center">
            <a href="/login" class="text-gray-600 hover:text-gray-800">Back to Login</a>
        </div>
      </div>
    </div>
  </div>
</div>