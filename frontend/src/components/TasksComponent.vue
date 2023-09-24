<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const tasks = ref([])
const error = ref('')

async function getTasks() {
    try {
        const path = '/api/tasks'
        const res = await axios.get(path)
        tasks.value = res.data?.tasks
    } catch (err) {
        console.error(err)
    }
}

async function removeTask(event) {
    try {
        const taskId = event.target.value
        const path = `http://localhost:5000/tasks/${taskId}`
        const res = await axios.delete(path)
        console.log(res.data)
        if (res.data?.status === 'success') {
            tasks.value = tasks.value.filter(
                (task) => task.id !== Number(taskId)
            )
            // tasks.value.splice(taskIndex, 1)
        }
    } catch (err) {
        console.error(err)
    }
}

async function updateTask(event) {
    error.value = '';
    const title = document.getElementById('title').value
    const description = document.getElementById('description').value
    if (!title || !description) {
        error.value = 'One of title or description is missing!'
    } else {
        tasks.value.push({id: 40, title: title, description: description});
    }
}

onMounted(() => {
    getTasks()
})
</script>

<template>
    <div class="task_manager_container">
        <h1>Task Manager</h1>

        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <input
                            id="title"
                            type="text"
                            placeholder="Task title"
                        />
                    </td>
                    <td>
                        <textarea
                            id="description"
                            placeholder="Task description"
                        />
                    </td>
                    <td>
                        <input
                            class="btn"
                            type="submit"
                            value="Submit"
                            @click.prevent="updateTask"
                        />
                    </td>
                </tr>
            </tbody>
            <tbody v-if='error'>
                <tr>
                    <td></td>
                    <td style='color: red; padding: 16px;'>
                        {{ error }}
                    </td>
                    <td></td>
                </tr>
            </tbody>
            <tbody v-for="(task, index) in tasks" :key="index">
                <tr>
                    <td>{{ task.title }}</td>
                    <td>{{ task.description }}</td>
                    <td class="task-btn">
                        <button
                            :value="task.id"
                            class="btn"
                            @click.prevent="updateTask"
                        >
                            Update
                        </button>
                        <button
                            :value="task.id"
                            class="btn btn-danger"
                            @click.prevent="removeTask"
                        >
                            Delete
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style>
.task_manager_container {
    display: flex;
    flex-direction: column;
    text-align: center;
    gap: 16px;
    margin: 16px;
}

table {
    border-spacing: 0;
}

tbody:nth-child(even) {
    background-color: lightgrey;
}

tr,
td {
    padding: 8px 12px;
}

.btn {
    padding: 12px 16px;
    margin: 4px 8px;
    border: 1px solid transparent;
    border-radius: 8px;
    cursor: pointer;

    &:hover {
        border: 1px solid #e0e0e0;
    }
}

.btn-danger {
    background-color: #ee0000;
    color: white;
}

form {
    display: flex;
    flex-direction: column;
    text-align: left;
}

textarea,
input {
    padding: 8px;
    resize: none;
    border-radius: 8px;
    border: none;
}

textarea {
    flex-shrink: 1;
    width: 400px;
    /*height: 80px;*/
}
</style>
