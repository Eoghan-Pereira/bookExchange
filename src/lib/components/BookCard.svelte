<script lang="ts">
    import { user } from '$lib/stores/auth';
    import { goto } from '$app/navigation';
    
    export let book;
    let isFlipped = false;
    
    function handleFlip() {
        isFlipped = !isFlipped;
    }
</script>

<div class="card {isFlipped ? 'flipped' : ''}" style="height: 400px;">
    <div class="card-inner">
        <div class="card-front">
            <img src={`data:image/jpeg;base64,${book.image_base64}`} alt={book.title} />
            <div class="card-content">
                <h1><strong>{book.title}</strong></h1>
                <p>By: {book.author}</p>
            </div>
            <div class="button-container">
                <button on:click={handleFlip} class="exchange-btn">
                    Read More
                </button>
            </div>
        </div>
        <div class="card-back">
            <h3>Book Description</h3>
            <p><strong>{book.title}</strong></p>
            <p>{book.description}</p>
            <div class="button-container">
                <button on:click={handleFlip} class="cancel-btn">
                    Close
                </button>
            </div>
        </div>
    </div>
</div>

<style>
    .card {
        perspective: 1000px;
        position: relative;
        margin: 1rem;
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
    text-align: left;
    color: white; 
}

    .card-back {
        transform: rotateY(180deg);
        text-align: left;
        overflow-y: auto; 
    }

    .card-front img {
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
        line-height: 1.1;
        padding: 0.5rem 0;
        width: 100%;
    }

    .card-content h3 {
        margin: 0.5rem 0;
    }

    .card-content p {
        margin: 0.25rem 0;
    }

    .button-container {
        margin-top: auto;
        width: 100%;
    }

    .exchange-btn, .cancel-btn {
        width: 100%;
        padding: 0.5rem;  /* Reduced from 0.75rem */
        min-height: 32px;
        max-height: 40px;
        height: auto;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .exchange-btn {
        background-color: rgba(76, 175, 80, 0.9);
        color: white;
    }

    .cancel-btn {
        background-color: rgba(244, 67, 54, 0.9);
        color: white;
    }

    .exchange-btn:hover, .cancel-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    @media (max-width: 768px) {
        .card {
            min-height: 300px;
        }

        .card-front img {
            min-height: 150px;
            max-height: 200px;
        }

        .exchange-btn, .cancel-btn {
            padding: 0.3rem;
            min-height: 28px;
            max-height: 36px;
        }
    }

    @media (max-width: 480px) {
        .card {
            min-height: 250px;
        }

        .card-front img {
            min-height: 120px;
            max-height: 150px;
        }

        .exchange-btn, .cancel-btn {
            padding: 0.25rem;
            min-height: 24px;
            max-height: 32px;
        }
    }
</style>
