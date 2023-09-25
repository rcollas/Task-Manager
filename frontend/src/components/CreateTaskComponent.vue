<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

interface Task {
    title: string
    description: string
}

const data = ref<Task>({ title: '', description: '' })
const emit = defineEmits(['addTask']);

async function createTask() {
    const path = 'http://localhost:5000/tasks'
    const {title, description} = data.value;
    if (!title || !description) {
        window.alert(`You must specify a title and a description.`)
        return
    }
    try {
        const res = await axios.post(
            path,
            { title: title, description: description },
            {
                headers: { 'Content-Type': 'application/json' }
            }
        )
        if (res.status === 200) {
            emit('addTask', title, description);
            data.value.title = '';
            data.value.description = '';
        }
        console.log(res.data)
    } catch (err) {
        console.error(err)
    }
}
</script>

<template>
    <div class="task_container">
        <div class="title header">
            <h5>Title</h5>
            <input
                type="text"
                placeholder="Enter a title"
                v-model="data.title"
            />
        </div>
        <span class="vertical_divider"></span>
        <div class="description_container header">
            <h5>Description</h5>
            <textarea
                placeholder="Enter a description"
                rows="4"
                v-model="data.description"
            />
        </div>
        <span class="vertical_divider"></span>
        <div class="btn_container">
            <button
                type="submit"
                class="btn"
                @click.prevent="createTask"
            >
                Create
            </button>
        </div>
    </div>
</template>

<style>
input,
textarea {
    padding: 8px;
    box-sizing: border-box;
    width: 100%;
    resize: none;
    border-radius: 8px;
    border: none;
    font-size: inherit;
    font-family: inherit;
}

.header {
    align-self: flex-start;
}
</style>
