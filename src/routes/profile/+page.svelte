<script lang="ts">
  import { user } from '$lib/stores/auth';
  import { changePassword, logOut } from '$lib/auth';
  import { goto } from '$app/navigation';

  let newPassword = '';
  let confirmNewPassword = '';
  let error = '';
  let message = '';

  async function handlePasswordChange() {
    if (newPassword !== confirmNewPassword) {
      error = 'Passwords do not match';
      return;
    }

    const result = await changePassword(newPassword);
    if (result.success) {
      message = 'Password updated successfully';
      error = '';
      newPassword = '';
      confirmNewPassword = '';
    } else {
      error = result.error;
      message = '';
    }
  }

  async function handleLogout() {
    const result = await logOut();
    if (result.success) {
      goto('/login');
    }
  }
</script>

<div class="min-h-screen  py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-3xl mx-auto">
    <div class="glass-card shadow-xl rounded-lg overflow-hidden">
      <div class="px-4 py-5 sm:p-6">
        <h1 class="text-4xl font-extrabold text-white text-center mb-8">Profile</h1>

        {#if $user}
          <p class="text-lg text-white mb-6">Email: {$user.email}</p>

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

          <form on:submit|preventDefault={handlePasswordChange} class="mb-8">
            <h2 class="text-2xl font-semibold text-white mb-4">Change Password</h2>

            <div class="mb-4">
              <label for="new-password" class="block text-sm font-medium text-white mb-2">
                New Password
              </label>
              <input
                type="password"
                id="new-password"
                bind:value={newPassword}
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div class="mb-6">
              <label for="confirm-new-password" class="block text-sm font-medium text-white mb-2">
                Confirm New Password
              </label>
              <input
                type="password"
                id="confirm-new-password"
                bind:value={confirmNewPassword}
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button type="submit" class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-300">
              Update Password
            </button>
            
          </form>

          <button 
            class="w-full mb-8 bg-gray-200 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-300 transition duration-300"
            on:click={handleLogout}
          >
            Logout
          </button>
        {:else}
          <p class="text-lg text-white">Please log in to view your profile.</p>
        {/if}
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
