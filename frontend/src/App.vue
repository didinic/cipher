<script setup>
import { ref, computed } from 'vue'

const message = ref('')
const key = ref('')
const cipherType = ref('vigenere')
const output = ref('')
const error = ref('')

const keyPlaceholder = computed(() =>
  cipherType.value === 'caesar' ? 'Shift number e.g. 3' : 'Keyword e.g. RIVERCAT'
)

async function encrypt() {
  if (cipherType.value === 'vigenere') {
    const res = await fetch(`http://127.0.0.1:8000/txt2vigenere/${message.value}/${key.value}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    const data = await res.json()
    output.value = data.result
  }
}

async function decrypt() {
  if (cipherType.value === 'vigenere') {
    const res = await fetch(`http://127.0.0.1:8000/vigenere2txt/${message.value}/${key.value}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    const data = await res.json()
    output.value = data.result
  }
}

async function run(mode) {
  output.value = ''
  error.value = ''
  try {
    const res = await fetch(`/api/${mode}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: message.value,
        key: key.value,
        cipher: cipherType.value
      })
    })
    const data = await res.json()
    if (data.error) error.value = data.error
    else output.value = data.result
  } catch (e) {
    error.value = 'Could not reach server'
  }
}
</script>

<template>
  <div class="container">
    <h1>CIPHERBOARD</h1>

    <div class="toggle">
      <button :class="{ active: cipherType === 'vigenere' }" @click="cipherType = 'vigenere'">
        Vigenère
      </button>
      <button :class="{ active: cipherType === 'caesar' }" @click="cipherType = 'caesar'">
        Caesar
      </button>
    </div>

    <textarea v-model="message" placeholder="Enter your message..." />

    
    <input v-model="key" :placeholder="keyPlaceholder" />

  
    <div class="actions">
      <button @click="encrypt">ENCRYPT</button>
      <button @click="decrypt">DECRYPT</button>
    </div>

    <textarea v-if="output" readonly :value="output" />
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<style scoped>
.container {
  max-width: 600px;
  margin: 4rem auto;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  font-family: monospace;
}
h1 { text-align: center; letter-spacing: 0.2em; }
textarea { width: 100%; min-height: 120px; padding: 0.75rem; font-family: monospace; resize: vertical; }
input { width: 100%; padding: 0.75rem; font-family: monospace; }
.toggle { display: flex; gap: 0.5rem; }
.toggle button, .actions button {
  padding: 0.5rem 1.25rem;
  cursor: pointer;
  border: 1px solid #555;
  background: transparent;
  font-family: monospace;
}
.toggle button.active { border-color: #c8a96e; color: #c8a96e; }
.actions { display: flex; gap: 0.5rem; }
.actions button { flex: 1; }
.error { color: red; font-size: 0.85rem; }
</style>
