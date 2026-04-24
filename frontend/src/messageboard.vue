<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const comments = ref([])
const error = ref('')
const postError = ref('')
const postSuccess = ref('')
const friends = ref(JSON.parse(localStorage.getItem('friends') || '{}'))

// New comment form
const newComment = ref('')
const loggedInUser = localStorage.getItem('username') || 'anonymous'
const userKey = localStorage.getItem('user_key') || ''

// Per-comment decrypt state: { [id]: { key, result, error, loading } }
const decryptState = ref({})

function logout() {
    localStorage.removeItem('isAuth')
    localStorage.removeItem('username')
    localStorage.removeItem('user_key')
    router.push('/login')
}

async function fetchComments() {
    error.value = ''
    try {
        const res = await fetch('http://127.0.0.1:8000/comments')
        const data = await res.json()
        // data is an object like { comment1: {...}, comment2: {...} }
        comments.value = Object.values(data).reverse()
    } catch (e) {
        error.value = 'Could not load comments.'
    }
}

async function postComment() {
    postError.value = ''
    postSuccess.value = ''

    if (!newComment.value.trim()) {
        postError.value = 'Message cannot be empty.'
        return
    }

    try {
        const res = await fetch('http://127.0.0.1:8000/comment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                comment: newComment.value,
                author: loggedInUser,
                key: userKey
            })
        })

        if (!res.ok) {
            postError.value = 'Failed to post comment.'
            return
        }

        postSuccess.value = 'Message posted and encrypted.'
        newComment.value = ''
        await fetchComments()
    } catch (e) {
        postError.value = 'Network error.'
    }
}

async function decryptComment(comment) {
    const id = comment.id
    const state = decryptState.value[id]

    if (!state?.key?.trim()) {
        decryptState.value[id] = { ...state, error: 'Enter a key to decrypt.', result: '' }
        return
    }

    decryptState.value[id] = { ...state, loading: true, error: '', result: '' }

    try {
        const res = await fetch('http://127.0.0.1:8000/decrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                comment_id: id,
                key: state.key
            })
        })

        const data = await res.json()

        // API returns the decrypted string directly, or { message: "not found" }
        if (typeof data === 'string') {
            decryptState.value[id] = { ...decryptState.value[id], loading: false, result: data, error: '' }
        } else if (data.message === 'not found') {
            decryptState.value[id] = { ...decryptState.value[id], loading: false, error: 'Comment not found.', result: '' }
        } else {
            decryptState.value[id] = { ...decryptState.value[id], loading: false, result: JSON.stringify(data), error: '' }
        }
    } catch (e) {
        decryptState.value[id] = { ...decryptState.value[id], loading: false, error: 'Network error.', result: '' }
    }
}

function initDecryptState(id) {
    if (!decryptState.value[id]) {
        decryptState.value[id] = { key: '', result: '', error: '', loading: false }
    }
}

onMounted(() => {
    if (!localStorage.getItem('isAuth')) {
        router.push('/login')
        return
    }
    fetchComments()
})
</script>

<template>
    <div class="container">

        <div class="topbar">
            <span class="brand">CIPHERBOARD / MESSAGES</span>
            <button @click="logout">LOGOUT</button>
        </div>

<section v-if="Object.keys(friends).length > 0" class="friends-section">
    <h2>// FRIENDS</h2>
    <div class="friends-list">
        <div v-for="(info, name) in friends" :key="name" class="friend-card">
            <span class="author">{{ name }}</span>
            <span class="friend-key">key: {{ info.personal_key }}</span>
        </div>
    </div>
</section>

        <h1>MESSAGE BOARD</h1>
        <p class="subtitle">All messages are Vigenère-encrypted. Supply the correct key to read them.</p>

        <!-- Post new comment -->
        <section class="post-section">
            <h2>// POST ENCRYPTED MESSAGE</h2>
            <p class="posting-as">Posting as <span class="author">{{ loggedInUser }}</span></p>

            <label>Message</label>
            <textarea v-model="newComment" placeholder="Write your plaintext message..." />

            <div class="actions">
                <button @click="postComment">ENCRYPT &amp; POST</button>
            </div>

            <p v-if="postError" class="msg-error">{{ postError }}</p>
            <p v-if="postSuccess" class="msg-ok">{{ postSuccess }}</p>
        </section>

        <div class="divider"></div>

        <!-- Comments feed -->
        <section class="feed-section">
            <h2>// ENCRYPTED FEED</h2>

            <p v-if="error" class="msg-error">{{ error }}</p>
            <p v-if="!error && comments.length === 0" class="empty">No messages yet.</p>

            <div
                v-for="comment in comments"
                :key="comment.id"
                class="comment-card"
                @vue:mounted="initDecryptState(comment.id)"
            >
                <div class="comment-meta">
                    <span class="author">{{ comment.author }}</span>
                    <span class="comment-id">#{{ comment.id }}</span>
                </div>

                <div class="ciphertext">{{ comment.encrypt_text }}</div>

                <div
                    v-if="decryptState[comment.id]?.result"
                    class="plaintext"
                >
                    <span class="label">DECRYPTED →</span> {{ decryptState[comment.id].result }}
                </div>

                <div class="decrypt-row">
                    <input
                        :value="decryptState[comment.id]?.key || ''"
                        @input="decryptState[comment.id] = { ...decryptState[comment.id], key: $event.target.value }"
                        placeholder="Key to decrypt..."
                        @keyup.enter="decryptComment(comment)"
                        @vue:mounted="initDecryptState(comment.id)"
                    />
                    <button
                        @click="decryptComment(comment)"
                        :disabled="decryptState[comment.id]?.loading"
                    >
                        {{ decryptState[comment.id]?.loading ? '...' : 'DECRYPT' }}
                    </button>
                </div>

                <p v-if="decryptState[comment.id]?.error" class="msg-error small">
                    {{ decryptState[comment.id].error }}
                </p>
            </div>
        </section>

    </div>
</template>

<style scoped>
.container {
    max-width: 680px;
    margin: 3rem auto;
    padding: 0 1rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    font-family: monospace;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand {
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    color: #888;
}

.topbar button {
    padding: 0.4rem 1rem;
    cursor: pointer;
    border: 1px solid #555;
    background: transparent;
    font-family: monospace;
    font-size: 0.8rem;
}

.topbar button:hover {
    border-color: #c8a96e;
    color: #c8a96e;
}

h1 {
    text-align: center;
    letter-spacing: 0.2em;
    margin: 0;
}

.subtitle {
    text-align: center;
    color: #888;
    font-size: 0.82rem;
    margin: 0;
}

h2 {
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    color: #c8a96e;
    margin: 0 0 0.75rem 0;
}

.post-section,
.feed-section {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
}

label {
    font-size: 0.8rem;
    color: #aaa;
    letter-spacing: 0.05em;
}

input {
    width: 100%;
    padding: 0.65rem 0.75rem;
    font-family: monospace;
    background: transparent;
    border: 1px solid #444;
    color: inherit;
    box-sizing: border-box;
}

input:focus {
    outline: none;
    border-color: #c8a96e;
}

textarea {
    width: 100%;
    min-height: 90px;
    padding: 0.65rem 0.75rem;
    font-family: monospace;
    background: transparent;
    border: 1px solid #444;
    color: inherit;
    resize: vertical;
    box-sizing: border-box;
}

textarea:focus {
    outline: none;
    border-color: #c8a96e;
}

.actions button {
    padding: 0.5rem 1.5rem;
    cursor: pointer;
    border: 1px solid #555;
    background: transparent;
    font-family: monospace;
    letter-spacing: 0.05em;
}

.actions button:hover {
    border-color: #c8a96e;
    color: #c8a96e;
}

.divider {
    border-top: 1px solid #333;
    margin: 0.5rem 0;
}

.posting-as {
    font-size: 0.82rem;
    color: #888;
    margin: 0;
}

.posting-as .author {
    color: #c8a96e;
}

.empty {
    color: #666;
    font-size: 0.85rem;
}

/* Comment cards */
.comment-card {
    border: 1px solid #333;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}

.comment-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #888;
}

.author {
    color: #c8a96e;
    letter-spacing: 0.05em;
}

.comment-id {
    color: #555;
}

.ciphertext {
    font-size: 0.9rem;
    word-break: break-all;
    color: #ccc;
    letter-spacing: 0.05em;
    padding: 0.5rem;
    background: #111;
    border-left: 2px solid #333;
}

.plaintext {
    font-size: 0.88rem;
    padding: 0.5rem;
    background: #0d1f0d;
    border-left: 2px solid #4caf50;
    color: #8bc98b;
    word-break: break-word;
}

.label {
    color: #4caf50;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
}

.decrypt-row {
    display: flex;
    gap: 0.5rem;
}

.decrypt-row input {
    flex: 1;
    padding: 0.45rem 0.65rem;
    font-size: 0.85rem;
}

.decrypt-row button {
    padding: 0.45rem 1rem;
    cursor: pointer;
    border: 1px solid #555;
    background: transparent;
    font-family: monospace;
    font-size: 0.8rem;
    white-space: nowrap;
}

.decrypt-row button:hover:not(:disabled) {
    border-color: #c8a96e;
    color: #c8a96e;
}

.decrypt-row button:disabled {
    opacity: 0.4;
    cursor: default;
}

.msg-error {
    color: #e05555;
    font-size: 0.82rem;
    margin: 0;
}

.msg-ok {
    color: #4caf50;
    font-size: 0.82rem;
    margin: 0;
}

.small {
    font-size: 0.78rem;
}

.friends-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.friends-list {
    display: flex;
    flex-direction: row;
    gap: 0.75rem;
    flex-wrap: wrap;
}

.friend-card {
    border: 1px solid #333;
    padding: 0.5rem 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    min-width: 120px;
}

.friend-key {
    font-size: 0.75rem;
    color: #888;
    letter-spacing: 0.05em;
}
</style>