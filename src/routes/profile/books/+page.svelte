<script lang="ts">
    import { onMount } from 'svelte';
    import { getUserBooks, updateBook, deleteBook } from '$lib/api';
    import { user } from '$lib/stores/auth';
    import { goto } from '$app/navigation';
    import { Modal, Alert } from 'flowbite-svelte';
    import { conditions, genres } from '$lib/constants';
  
    let books = [];
    let error = '';
    let showModal = false;
    let selectedBook = null;
    let mode = ''; // 'edit' or 'delete'
    let isFlipped = {};
    let modalError = '';

    onMount(async () => {
      try {
        if ($user?.uid) {
          books = await getUserBooks($user.uid);
        }
      } catch (err) {
        error = 'Failed to load books';
      }
    });

    function openModal(book, event) {
      event.stopPropagation(); // Prevent card flip
      selectedBook = { ...book }; // Clone the book object
      showModal = true;
      mode = ''; // Reset mode
      modalError = '';
    }
  
    async function handleDelete() {
      try {
        modalError = '';
        await deleteBook(selectedBook._id);
        books = books.filter(b => b._id !== selectedBook._id);
        showModal = false;
      } catch (err) {
        modalError = 'Failed to delete book';
        console.error(err);
      }
    }
  
    async function handleUpdate() {
      try {
        modalError = '';
        // Create a copy of selectedBook without _id
        const { _id, ...updateData } = selectedBook;
        await updateBook(_id, updateData);
        const index = books.findIndex(b => b._id === _id);
        if (index !== -1) {
          books[index] = { ...selectedBook };
        }
        showModal = false;
      } catch (err) {
        modalError = 'Failed to update book';
        console.error(err);
      }
    }

    function handleFlip(bookId) {
        isFlipped[bookId] = !isFlipped[bookId];
    }

    function navigateToAddBooks() {
        goto('/books/add');
    }
</script>


<div class="page-wrapper">
    <div class="profile-books">
</div>
  {#if error}
    <p class="error">{error}</p>
  {:else}
    <div class="books-grid">
      {#if books.length === 0}
        <div class="glass-card-container">
          <div class="glass-card" on:click={navigateToAddBooks}>
            <p>Add books to see books in My Books</p>
          </div>
        </div>
      {/if}
      {#each books as book}
        <div class="card {isFlipped[book._id] ? 'flipped' : ''}" style="height: 400px;">
          <div class="card-inner">
            <div class="card-front">
              <img src={`data:image/jpeg;base64,${book.image_base64}`} alt="{book.title}" class="book-image" />
              <div class="card-content">
                <h3>{book.title}</h3>
                <p><strong>Author:</strong> {book.author}</p>
                <p><strong>Genre:</strong> {book.genre}</p>
              </div>
              <div class="button-container">
                <button on:click={() => handleFlip(book._id)} class="info-btn">Read More</button>
                <button on:click={(e) => openModal(book, e)} class="edit-btn">Edit</button>
              </div>
            </div>
            <div class="card-back">
              <h1><strong>Book Details</strong></h1>
              <p><strong>{book.title}</strong></p>
              <p>{book.description}</p>
              <div class="button-container">
                <button on:click={() => handleFlip(book._id)} class="cancel-btn">Close</button>
              </div>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<!-- Modal -->
{#if showModal}
  <Modal bind:open={showModal} size="lg">
    {#if modalError}
      <Alert color="red" class="mb-4">{modalError}</Alert>
    {/if}
    {#if mode === ''}
      <h3 class="mb-4 text-xl font-medium">What would you like to do?</h3>
      <div class="flex justify-end gap-4">
        <button 
          class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          on:click={() => mode = 'edit'}
        >
          Edit Book
        </button>
        <button 
          class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          on:click={handleDelete}
        >
          Delete Book
        </button>
      </div>
    {:else if mode === 'edit'}
      <h3 class="mb-4 text-xl font-medium">Edit Book</h3>
      <form on:submit|preventDefault={handleUpdate} class="space-y-4">
        <div>
          <label for="title" class="block mb-2">Title*</label>
          <input 
            id="title"
            type="text"
            class="w-full p-2 border rounded"
            bind:value={selectedBook.title}
            required
          />
        </div>
        <div>
          <label for="author" class="block mb-2">Author*</label>
          <input 
            id="author"
            type="text"
            class="w-full p-2 border rounded"
            bind:value={selectedBook.author}
            required
          />
        </div>
        <div>
          <label for="genre" class="block mb-2">Genre*</label>
          <select 
            id="genre"
            class="w-full p-2 border rounded"
            bind:value={selectedBook.genre}
            required
          >
            {#each genres as genre}
              <option value={genre.value}>{genre.name}</option>
            {/each}
          </select>
        </div>
        <div>
          <label for="condition" class="block mb-2">Condition*</label>
          <select 
            id="condition"
            class="w-full p-2 border rounded"
            bind:value={selectedBook.condition}
            required
          >
            {#each conditions as condition}
              <option value={condition.value}>{condition.name}</option>
            {/each}
          </select>
        </div>
        <div>
          <label for="description" class="block mb-2">Description</label>
          <textarea 
            id="description"
            class="w-full p-2 border rounded"
            bind:value={selectedBook.description}
            rows="3"
          ></textarea>
        </div>
        <div class="flex justify-end gap-4">
          <button 
            type="submit"
            class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Save Changes
          </button>
          <button 
            type="button"
            class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
            on:click={() => showModal = false}
          >
            Cancel
          </button>
        </div>
      </form>
    {/if}
  </Modal>
{/if}

<style>
    .page-wrapper {
        width: 100vw;
        max-width: 100%;
        overflow-x: hidden;
        padding-top: 1rem;
        min-height: 100vh; /* Make it full height */
        color: white; /* Make text readable on dark background */
    }

    .profile-books {
        width: 100%;
    }


  .books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    padding: 1.5rem;
  }

  .card {
    perspective: 1000px;
    position: relative;
    margin: 0;
    min-height: 400px;
  }

  .card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.8s;
    transform-style: preserve-3d;
  }

  .card.flipped .card-inner {
    transform: rotateY(180deg);
  }

  .card-front, .card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    padding: 1rem;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
  }

  .card-back {
    transform: rotateY(180deg);
    text-align: left;
  }

  .book-image {
    width: 100%;
    height: auto;
    min-height: 200px;
    max-height: 300px;
    object-fit: cover;
    border-radius: 8px;
  }

  .card-content {
    flex-grow: 1;
    text-align: left;
    line-height: 1.2;
    padding: 0.5rem 0;
  }

  .button-container {
    margin-top: auto;
    display: flex;
    gap: 0.5rem;
    width: 100%;
  }

  .info-btn, .edit-btn, .cancel-btn {
    flex: 1;
    padding: 0.5rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s ease;
  }

  .info-btn {
    background-color: rgba(33, 150, 243, 0.9);
    color: white;
  }

  .edit-btn {
    background-color: rgba(76, 175, 80, 0.9);
    color: white;
  }

  .cancel-btn {
    background-color: rgba(244, 67, 54, 0.9);
    color: white;
  }

  .info-btn:hover, .edit-btn:hover, .cancel-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  @media (max-width: 768px) {
    .card {
      min-height: 350px;
    }

    .book-image {
      min-height: 150px;
      max-height: 200px;
    }
  }

  .glass-card-container {
    display: flex;
    align-items: center;
    justify-content: center;
    grid-column: 1 / -1;
  }

  .glass-card {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 300px; /* Increased height */
    width: 100%; /* Full width */
    max-width: 600px; /* Max width */
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    padding: 1rem; /* Added padding */
  }

  .glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .glass-card p {
    font-size: 1.2rem;
    color: white;
    text-align: center;
    margin: 0;
  }
</style>