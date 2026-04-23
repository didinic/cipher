<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
const username = ref('')
const password = ref('')
const output = ref('')
const error = ref('')
const router = useRouter()

async function login() {

    try {
        output.value = ''
        error.value = ''

         if (!username.value || !password.value) {
            error.value = 'All fields are required'
            return
        }

        const res = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value
            })
        })
        
        const data = await res.json()

        if (!res.ok) {
            error.value = data.message || 'Login failed'
            localStorage.removeItem('isAuth')
        } else {
            output.value = 'Login successful'
            localStorage.setItem('isAuth', 'true')

            router.push('/messageboard')
        }


        console.log(data)

    } catch (e) {

        error.value = 'Network error'
        console.error(e)

    }



}



</script >

<template>

    <div class="container">
        <h1>START TO ENCRYPT</h1>

        <label for="uname"><b>Username</b></label>
        <input type="text" v-model="username" required>

        <label for="psw"><b>Password</b></label>
        <input type="password" v-model="password" required>

        <div class="toggle">
            <button @click="login">
                LOGIN
            </button>

            <p v-if="error">{{ error }}</p>

        </div>

    </div>




</template>

<style>
.container {
    max-width: 600px;
    margin: 4rem auto;
    padding: 0 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    font-family: monospace;
}

h1 {
    text-align: center;
    letter-spacing: 0.2em;
}


.toggle {
    display: flex;
    gap: 0.5rem;
    align-self: center;

}

.toggle button {
    padding: 0.5rem 1.25rem;
    cursor: pointer;
    border: 1px solid #555;
    background: transparent;
    font-family: monospace;
}
</style>